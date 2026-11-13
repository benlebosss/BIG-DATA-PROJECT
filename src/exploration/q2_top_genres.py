"""Q2 + Q3: top three movie genres per year (1980-2025) and how they compare to the others.

Popularity of a genre in a year = total number of IMDb votes received by the feature
movies of that genre released that year (votes measure audience engagement, the rating
measures appreciation). A movie with several genres counts for each of them.

Q3 compares, for every year, the top three genres with all the remaining genres
(share of votes, number of movies, average rating, votes per movie).

Usage: python -m src.exploration.q2_top_genres [--start 1980 --end 2025]
"""
import argparse

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F

from src.common.spark_session import get_spark
from src.exploration.common import feature_movies, load, rated, save, with_genre


def genre_year_popularity(basics: DataFrame, ratings: DataFrame,
                          start: int = 1980, end: int = 2025) -> DataFrame:
    movies = with_genre(rated(feature_movies(basics), ratings)) \
        .where(F.col("startYear").between(start, end))
    return (
        movies.groupBy(F.col("startYear").alias("year"), "genre").agg(
            F.count("*").alias("n_movies"),
            F.sum("numVotes").alias("total_votes"),
            (F.sum(F.col("averageRating") * F.col("numVotes")) / F.sum("numVotes")).alias("avg_rating"),
        )
        .withColumn("rank", F.row_number().over(
            Window.partitionBy("year").orderBy(F.desc("total_votes"), "genre")))
        .withColumn("vote_share", F.col("total_votes") / F.sum("total_votes").over(
            Window.partitionBy("year")))
    )


def top_genres(popularity: DataFrame, k: int = 3) -> DataFrame:
    return popularity.where(F.col("rank") <= k).select(
        "year", "rank", "genre", "total_votes", "n_movies",
        F.round("avg_rating", 2).alias("avg_rating"),
        F.round(100 * F.col("vote_share"), 1).alias("vote_share_pct"),
    ).orderBy("year", "rank")


def top_vs_rest(popularity: DataFrame, k: int = 3) -> DataFrame:
    """Per year: aggregated metrics of the top-k genres versus the other genres."""
    grouped = popularity.withColumn("group", F.when(F.col("rank") <= k, "top3").otherwise("rest"))
    agg = grouped.groupBy("year", "group").agg(
        F.count("*").alias("n_genres"),
        F.sum("n_movies").alias("n_movies"),
        F.sum("total_votes").alias("total_votes"),
        F.round(100 * F.sum("vote_share"), 1).alias("vote_share_pct"),
        F.round(F.sum(F.col("avg_rating") * F.col("total_votes")) / F.sum("total_votes"), 2)
        .alias("avg_rating"),
    ).withColumn("votes_per_movie", F.round(F.col("total_votes") / F.col("n_movies"), 0))
    return agg.orderBy("year", F.desc("group"))


def main(start: int = 1980, end: int = 2025) -> None:
    spark = get_spark("q2-top-genres")
    popularity = genre_year_popularity(load(spark, "title.basics"), load(spark, "title.ratings"),
                                       start, end).cache()
    save(top_genres(popularity), "q2_top3_genres_per_year")
    comparison = top_vs_rest(popularity).cache()
    save(comparison, "q3_top3_vs_rest_per_year")
    # Overall picture: how often each genre reaches the top three over the period.
    save(popularity.where("rank <= 3").groupBy("genre")
         .agg(F.count("*").alias("years_in_top3"), F.sum(F.when(F.col("rank") == 1, 1).otherwise(0))
              .alias("years_ranked_1"))
         .orderBy(F.desc("years_in_top3")), "q3_genre_top3_frequency")
    save(comparison.groupBy("group").agg(
        F.round(F.avg("vote_share_pct"), 1).alias("mean_vote_share_pct"),
        F.round(F.avg("avg_rating"), 2).alias("mean_avg_rating"),
        F.round(F.avg("votes_per_movie"), 0).alias("mean_votes_per_movie"),
        F.round(F.avg("n_movies"), 0).alias("mean_movies_per_year")), "q3_top3_vs_rest_summary")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=1980)
    ap.add_argument("--end", type=int, default=2025)
    a = ap.parse_args()
    main(a.start, a.end)
