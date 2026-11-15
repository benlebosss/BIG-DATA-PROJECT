"""Q7: actors/actresses with a 20+ year movie career, 15+ movies, whose peak came early.

Career = the feature movies (with at least ``min_votes`` votes) where the person is
credited as ``actor``/``actress`` in ``title.principals``. Span = last year - first year.

The career is split at its middle year. A peak is "early" when:
  - the person's highest rated movie was released in the first half of the career, and
  - the average rating of first-half movies is higher than that of second-half movies.
``rating_drop`` (first-half average minus second-half average) measures how early the peak is.

Usage: python -m src.exploration.q7_early_peak_actors [--min-votes 100]
"""
import argparse

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from src.common.spark_session import get_spark
from src.exploration.common import feature_movies, load, rated, save


def acting_credits(basics: DataFrame, principals: DataFrame, ratings: DataFrame,
                   min_votes: int) -> DataFrame:
    movies = rated(feature_movies(basics), ratings, min_votes) \
        .select("tconst", "primaryTitle", "startYear", "averageRating")
    actors = principals.where(F.col("category").isin("actor", "actress")) \
        .select("tconst", "nconst").distinct()
    return actors.join(movies, "tconst")


def early_peak_actors(basics: DataFrame, principals: DataFrame, ratings: DataFrame,
                      names: DataFrame, min_votes: int = 100, min_years: int = 20,
                      min_movies: int = 15) -> DataFrame:
    credits = acting_credits(basics, principals, ratings, min_votes)
    careers = credits.groupBy("nconst").agg(
        F.count("*").alias("n_movies"),
        F.min("startYear").alias("first_year"),
        F.max("startYear").alias("last_year"),
        F.max_by(F.struct("primaryTitle", "startYear", "averageRating"),
                 F.col("averageRating")).alias("best"),
    ).withColumn("span_years", F.col("last_year") - F.col("first_year")) \
        .where((F.col("span_years") >= min_years) & (F.col("n_movies") >= min_movies)) \
        .withColumn("mid_year", F.col("first_year") + F.col("span_years") / 2)

    halves = credits.join(careers.select("nconst", "mid_year"), "nconst").groupBy("nconst").agg(
        F.avg(F.when(F.col("startYear") <= F.col("mid_year"), F.col("averageRating"))).alias("early_avg"),
        F.avg(F.when(F.col("startYear") > F.col("mid_year"), F.col("averageRating"))).alias("late_avg"),
    )
    return (
        careers.join(halves, "nconst")
        .where((F.col("best.startYear") <= F.col("mid_year")) & (F.col("early_avg") > F.col("late_avg")))
        .join(names.select("nconst", "primaryName"), "nconst", "left")
        .select("nconst", "primaryName", "n_movies", "first_year", "last_year", "span_years",
                F.col("best.primaryTitle").alias("best_movie"), F.col("best.startYear").alias("best_year"),
                F.col("best.averageRating").alias("best_rating"),
                F.round("early_avg", 2).alias("early_avg"), F.round("late_avg", 2).alias("late_avg"),
                F.round(F.col("early_avg") - F.col("late_avg"), 2).alias("rating_drop"))
        .orderBy(F.desc("rating_drop"))
    )


def main(min_votes: int = 100) -> None:
    spark = get_spark("q7-early-peak-actors")
    result = early_peak_actors(load(spark, "title.basics"), load(spark, "title.principals"),
                               load(spark, "title.ratings"), load(spark, "name.basics"), min_votes)
    save(result, "q7_early_peak_actors")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-votes", type=int, default=100)
    main(ap.parse_args().min_votes)
