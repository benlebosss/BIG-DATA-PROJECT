"""Q4: directors with exactly one movie rated >= 8.0 whose other movies average <= 6.0.

Directors come from ``title.crew.directors``. Only feature movies with at least
``min_votes`` votes are considered, so that a rating given by a handful of people
cannot create a "hit". "Multiple other movies" means at least two other movies.

Usage: python -m src.exploration.q4_one_hit_directors [--min-votes 100]
"""
import argparse

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from src.common.spark_session import get_spark
from src.exploration.common import feature_movies, load, rated, save, split_list


def directed_movies(basics: DataFrame, crew: DataFrame, ratings: DataFrame,
                    min_votes: int) -> DataFrame:
    movies = rated(feature_movies(basics), ratings, min_votes) \
        .select("tconst", "primaryTitle", "startYear", "averageRating", "numVotes")
    directors = crew.select("tconst", F.explode(split_list("directors")).alias("nconst"))
    return movies.join(directors, "tconst")


def one_hit_directors(basics: DataFrame, crew: DataFrame, ratings: DataFrame, names: DataFrame,
                      min_votes: int = 100, hit: float = 8.0, low: float = 6.0,
                      min_others: int = 2) -> DataFrame:
    dm = directed_movies(basics, crew, ratings, min_votes)
    is_hit = F.col("averageRating") >= hit
    per_director = dm.groupBy("nconst").agg(
        F.sum(is_hit.cast("int")).alias("n_hits"),
        F.sum((~is_hit).cast("int")).alias("n_others"),
        F.avg(F.when(~is_hit, F.col("averageRating"))).alias("others_avg_rating"),
        F.max_by(F.struct("primaryTitle", "startYear", "averageRating", "numVotes"),
                 F.col("averageRating")).alias("hit"),
    )
    return (
        per_director.where((F.col("n_hits") == 1) & (F.col("n_others") >= min_others)
                           & (F.col("others_avg_rating") <= low))
        .join(names.select("nconst", "primaryName"), "nconst", "left")
        .select("nconst", "primaryName",
                F.col("hit.primaryTitle").alias("hit_title"), F.col("hit.startYear").alias("hit_year"),
                F.col("hit.averageRating").alias("hit_rating"), F.col("hit.numVotes").alias("hit_votes"),
                "n_others", F.round("others_avg_rating", 2).alias("others_avg_rating"))
        .orderBy(F.desc("hit_votes"))
    )


def main(min_votes: int = 100) -> None:
    spark = get_spark("q4-one-hit-directors")
    result = one_hit_directors(load(spark, "title.basics"), load(spark, "title.crew"),
                               load(spark, "title.ratings"), load(spark, "name.basics"), min_votes)
    save(result, "q4_one_hit_directors")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-votes", type=int, default=100)
    main(ap.parse_args().min_votes)
