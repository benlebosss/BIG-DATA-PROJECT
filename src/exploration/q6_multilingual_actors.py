"""Q6: actors/actresses successful in movies originally made in several languages.

IMDb has no "original language" column, and the ``isOriginalTitle`` rows of ``title.akas``
never carry a language. The original language of a movie is therefore inferred as the
language of its localized titles that are written exactly like ``originalTitle``
(e.g. "Le Fabuleux Destin d'Amélie Poulain" listed with language ``fr``). When several
languages match, the most frequent one wins. Movies without any match are left out and
the coverage is reported.

A movie is successful when ``averageRating >= min_rating`` and ``numVotes >= min_votes``.

Usage: python -m src.exploration.q6_multilingual_actors [--min-rating 7.0 --min-votes 10000]
"""
import argparse

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F

from src.common.spark_session import get_spark
from src.exploration.common import feature_movies, load, rated, save


def original_language(movies: DataFrame, akas: DataFrame) -> DataFrame:
    """(tconst, language) inferred from the akas matching the original title."""
    norm = lambda c: F.lower(F.trim(c))  # noqa: E731
    matches = (
        akas.where(F.col("language").isNotNull())
        .select(F.col("titleId").alias("tconst"), "language", norm(F.col("title")).alias("t"))
        .join(movies.select("tconst", norm(F.col("originalTitle")).alias("t")), ["tconst", "t"])
        .groupBy("tconst", "language").count()
    )
    best = Window.partitionBy("tconst").orderBy(F.desc("count"), "language")
    return matches.withColumn("r", F.row_number().over(best)).where("r = 1") \
        .select("tconst", F.col("language").alias("original_language"))


def multilingual_actors(basics: DataFrame, akas: DataFrame, principals: DataFrame,
                        ratings: DataFrame, names: DataFrame, min_rating: float = 7.0,
                        min_votes: int = 10000) -> DataFrame:
    hits = rated(feature_movies(basics), ratings, min_votes) \
        .where(F.col("averageRating") >= min_rating)
    hits = hits.join(original_language(hits, akas), "tconst") \
        .select("tconst", "primaryTitle", "original_language")
    actors = principals.where(F.col("category").isin("actor", "actress")) \
        .select("tconst", "nconst").distinct()
    return (
        actors.join(hits, "tconst")
        .groupBy("nconst").agg(
            F.countDistinct("original_language").alias("n_languages"),
            F.array_sort(F.collect_set("original_language")).alias("languages"),
            F.count("*").alias("n_successful_movies"),
            F.slice(F.collect_list(F.concat_ws(" [", "primaryTitle", F.concat("original_language", F.lit("]")))),
                    1, 10).alias("examples"))
        .where(F.col("n_languages") >= 2)
        .join(names.select("nconst", "primaryName"), "nconst", "left")
        .select("nconst", "primaryName", "n_languages", F.array_join("languages", ",").alias("languages"),
                "n_successful_movies", F.array_join("examples", " | ").alias("examples"))
        .orderBy(F.desc("n_languages"), F.desc("n_successful_movies"))
    )


def language_coverage(basics: DataFrame, akas: DataFrame, ratings: DataFrame,
                      min_rating: float, min_votes: int) -> DataFrame:
    hits = rated(feature_movies(basics), ratings, min_votes).where(F.col("averageRating") >= min_rating)
    langs = original_language(hits, akas)
    return hits.join(langs, "tconst", "left").agg(
        F.count("*").alias("successful_movies"),
        F.count("original_language").alias("with_inferred_language"),
        F.round(100 * F.count("original_language") / F.count("*"), 1).alias("coverage_pct"))


def main(min_rating: float = 7.0, min_votes: int = 10000) -> None:
    spark = get_spark("q6-multilingual-actors")
    basics, akas, ratings = load(spark, "title.basics"), load(spark, "title.akas"), load(spark, "title.ratings")
    save(language_coverage(basics, akas, ratings, min_rating, min_votes), "q6_language_coverage")
    result = multilingual_actors(basics, akas, load(spark, "title.principals"), ratings,
                                 load(spark, "name.basics"), min_rating, min_votes).cache()
    save(result, "q6_actors_2plus_languages")
    save(result.where("n_languages >= 3"), "q6_actors_3plus_languages")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-rating", type=float, default=7.0)
    ap.add_argument("--min-votes", type=int, default=10000)
    a = ap.parse_args()
    main(a.min_rating, a.min_votes)
