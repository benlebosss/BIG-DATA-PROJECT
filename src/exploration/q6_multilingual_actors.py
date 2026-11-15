"""Q6: actors/actresses successful in movies originally made in several languages.

IMDb has no "original language" column, and the ``isOriginalTitle`` rows of ``title.akas``
never carry a language. The original language of a movie is resolved in this order:

1. Wikidata original language (P364), gathered by ``src.exploration.wikidata_language``
   (table ``data/external/wikidata_language``), when it gives a single language;
2. when Wikidata lists several languages the movie is a multilingual production and is
   excluded by default (``--multi-language imdb`` keeps the Wikidata language that the
   IMDb heuristic below also finds, at the risk of picking an export title's language);
3. without Wikidata answer, the IMDb heuristic alone: language of the localized titles
   written exactly like ``originalTitle`` (most frequent one).

Movies left without language are excluded, and the coverage per source is reported.

A movie is successful when ``averageRating >= min_rating`` and ``numVotes >= min_votes``.

Usage: python -m src.exploration.q6_multilingual_actors [--min-rating 7.0 --min-votes 10000]
"""
import argparse
from pathlib import Path

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F

from src.common.spark_session import get_spark
from src.exploration.common import feature_movies, load, rated, save
from src.exploration.wikidata_language import TABLE_DIR

# Wikidata sometimes gives both the macro-language and the language (Chinese / Mandarin).
SAME_LANGUAGE = {"zh": "cmn"}


def normalize(col: str) -> F.Column:
    mapping = F.create_map(*[F.lit(x) for kv in SAME_LANGUAGE.items() for x in kv])
    return F.coalesce(mapping[F.col(col)], F.col(col))


def imdb_language(movies: DataFrame, akas: DataFrame) -> DataFrame:
    """(tconst, imdb_language) inferred from the akas matching the original title."""
    norm = lambda c: F.lower(F.trim(c))  # noqa: E731
    matches = (
        akas.where(F.col("language").isNotNull())
        .select(F.col("titleId").alias("tconst"), "language", norm(F.col("title")).alias("t"))
        .join(movies.select("tconst", norm(F.col("originalTitle")).alias("t")), ["tconst", "t"])
        .groupBy("tconst", "language").count()
    )
    best = Window.partitionBy("tconst").orderBy(F.desc("count"), "language")
    return matches.withColumn("r", F.row_number().over(best)).where("r = 1") \
        .select("tconst", F.col("language").alias("imdb_language")) \
        .withColumn("imdb_language", normalize("imdb_language"))


def original_language(movies: DataFrame, akas: DataFrame, wikidata: DataFrame = None,
                      multi_language: str = "exclude") -> DataFrame:
    """(tconst, original_language, language_source) following the order of the docstring."""
    imdb = imdb_language(movies, akas)
    if wikidata is None:
        return imdb.select("tconst", F.col("imdb_language").alias("original_language"),
                           F.lit("imdb_akas").alias("language_source"))
    wd = (wikidata.where(F.col("language_code").isNotNull())
          .withColumn("language_code", normalize("language_code"))
          .groupBy("tconst").agg(F.array_sort(F.collect_set("language_code")).alias("wd_languages")))
    both = movies.select("tconst").join(wd, "tconst", "left").join(imdb, "tconst", "left")
    has_wd = F.col("wd_languages").isNotNull()
    single = has_wd & (F.size("wd_languages") == 1)
    agrees = has_wd & F.array_contains("wd_languages", F.col("imdb_language"))         & F.lit(multi_language == "imdb")
    return both.select(
        "tconst",
        F.when(single, F.col("wd_languages")[0])
        .when(agrees, F.col("imdb_language"))
        .when(~has_wd, F.col("imdb_language")).alias("original_language"),
        F.when(single, "wikidata")
        .when(agrees, "wikidata+imdb_akas")
        .when(has_wd, "multilingual")
        .when(F.col("imdb_language").isNotNull(), "imdb_akas")
        .otherwise("unknown").alias("language_source"),
    )


def load_wikidata(spark, table_dir: str = TABLE_DIR) -> DataFrame:
    return spark.read.parquet(table_dir) if Path(table_dir).exists() else None


def successful_movies(basics: DataFrame, ratings: DataFrame, min_rating: float,
                      min_votes: int) -> DataFrame:
    return rated(feature_movies(basics), ratings, min_votes).where(F.col("averageRating") >= min_rating)


def multilingual_actors(basics: DataFrame, akas: DataFrame, principals: DataFrame,
                        ratings: DataFrame, names: DataFrame, min_rating: float = 7.0,
                        min_votes: int = 10000, wikidata: DataFrame = None,
                        multi_language: str = "exclude") -> DataFrame:
    hits = successful_movies(basics, ratings, min_rating, min_votes)
    hits = hits.join(original_language(hits, akas, wikidata, multi_language), "tconst") \
        .where(F.col("original_language").isNotNull()) \
        .select("tconst", "primaryTitle", "original_language")
    actors = principals.where(F.col("category").isin("actor", "actress")) \
        .select("tconst", "nconst").distinct()
    example = F.concat("primaryTitle", F.lit(" ["), "original_language", F.lit("]"))
    return (
        actors.join(hits, "tconst")
        .groupBy("nconst").agg(
            F.countDistinct("original_language").alias("n_languages"),
            F.array_sort(F.collect_set("original_language")).alias("languages"),
            F.count("*").alias("n_successful_movies"),
            F.slice(F.array_sort(F.collect_list(example)), 1, 10).alias("examples"))
        .where(F.col("n_languages") >= 2)
        .join(names.select("nconst", "primaryName"), "nconst", "left")
        .select("nconst", "primaryName", "n_languages", F.array_join("languages", ",").alias("languages"),
                "n_successful_movies", F.array_join("examples", " | ").alias("examples"))
        .orderBy(F.desc("n_languages"), F.desc("n_successful_movies"))
    )


def language_coverage(basics: DataFrame, akas: DataFrame, ratings: DataFrame, min_rating: float,
                      min_votes: int, wikidata: DataFrame = None,
                      multi_language: str = "exclude") -> DataFrame:
    """Number and share of successful movies per language source."""
    hits = successful_movies(basics, ratings, min_rating, min_votes)
    langs = original_language(hits, akas, wikidata, multi_language)
    total = hits.count()
    return (hits.join(langs, "tconst", "left")
            .groupBy(F.coalesce("language_source", F.lit("unknown")).alias("language_source")).count()
            .withColumn("pct", F.round(100 * F.col("count") / total, 1))
            .orderBy(F.desc("count")))


def main(min_rating: float = 7.0, min_votes: int = 10000, multi_language: str = "exclude") -> None:
    spark = get_spark("q6-multilingual-actors")
    basics, akas, ratings = load(spark, "title.basics"), load(spark, "title.akas"), load(spark, "title.ratings")
    wikidata = load_wikidata(spark)
    if wikidata is None:
        print("[q6] no Wikidata table: run src.exploration.wikidata_language first for better languages")
    save(language_coverage(basics, akas, ratings, min_rating, min_votes, wikidata, multi_language),
         "q6_language_coverage")
    hits = successful_movies(basics, ratings, min_rating, min_votes)
    save(original_language(hits, akas, wikidata, multi_language).groupBy("original_language").count()
         .orderBy(F.desc("count")), "q6_successful_movies_per_language")
    result = multilingual_actors(basics, akas, load(spark, "title.principals"), ratings,
                                 load(spark, "name.basics"), min_rating, min_votes, wikidata,
                                 multi_language).cache()
    save(result, "q6_actors_2plus_languages")
    save(result.where("n_languages >= 3"), "q6_actors_3plus_languages")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-rating", type=float, default=7.0)
    ap.add_argument("--min-votes", type=int, default=10000)
    ap.add_argument("--multi-language", choices=["exclude", "imdb"], default="exclude")
    a = ap.parse_args()
    main(a.min_rating, a.min_votes, a.multi_language)
