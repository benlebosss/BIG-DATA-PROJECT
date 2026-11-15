"""Q5: TV series whose worst episode is in the last season and best episode in the first two.

Conditions on a series (``titleType`` tvSeries or tvMiniSeries):
  - at least 3 seasons containing >= 10 episodes (episodes listed in ``title.episode``);
  - among its rated episodes, the lowest rated one belongs to the last season
    (highest ``seasonNumber``) and the highest rated one to season 1 or 2.

Ties are broken by the number of votes (the most voted episode wins), so each series has
exactly one best and one worst episode. Episodes need ``min_votes`` votes to be ranked.

Usage: python -m src.exploration.q5_series_decline [--min-votes 20]
"""
import argparse

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F

from src.common.spark_session import get_spark
from src.exploration.common import load, save


def series_decline(basics: DataFrame, episode: DataFrame, ratings: DataFrame,
                   min_votes: int = 20, min_seasons: int = 3, min_episodes: int = 10) -> DataFrame:
    series = basics.where(F.col("titleType").isin("tvSeries", "tvMiniSeries")) \
        .select(F.col("tconst").alias("parentTconst"), "primaryTitle", "startYear", "endYear")
    eps = episode.where(F.col("seasonNumber").isNotNull()).join(series.select("parentTconst"),
                                                                 "parentTconst")

    season_sizes = eps.groupBy("parentTconst", "seasonNumber").agg(F.count("*").alias("n_episodes"))
    eligible = season_sizes.groupBy("parentTconst").agg(
        F.sum((F.col("n_episodes") >= min_episodes).cast("int")).alias("n_big_seasons"),
        F.max("seasonNumber").alias("last_season"),
    ).where(F.col("n_big_seasons") >= min_seasons)

    rated_eps = eps.join(eligible, "parentTconst") \
        .join(ratings.where(F.col("numVotes") >= min_votes), "tconst")
    by_series = Window.partitionBy("parentTconst")
    ranked = rated_eps \
        .withColumn("best_rank", F.row_number().over(
            by_series.orderBy(F.desc("averageRating"), F.desc("numVotes")))) \
        .withColumn("worst_rank", F.row_number().over(
            by_series.orderBy("averageRating", F.desc("numVotes"))))

    def pick(rank_col: str, prefix: str) -> DataFrame:
        return ranked.where(F.col(rank_col) == 1).select(
            "parentTconst", "last_season", "n_big_seasons",
            F.col("tconst").alias(f"{prefix}_episode"),
            F.col("seasonNumber").alias(f"{prefix}_season"),
            F.col("episodeNumber").alias(f"{prefix}_number"),
            F.col("averageRating").alias(f"{prefix}_rating"))

    best = pick("best_rank", "best")
    worst = pick("worst_rank", "worst").drop("last_season", "n_big_seasons")
    return (
        best.join(worst, "parentTconst")
        .where((F.col("worst_season") == F.col("last_season")) & (F.col("best_season") <= 2))
        .join(series, "parentTconst")
        .join(ratings.withColumnRenamed("tconst", "parentTconst"), "parentTconst", "left")
        .select("parentTconst", "primaryTitle", "startYear", "endYear", "last_season",
                "n_big_seasons", "best_episode", "best_season", "best_number", "best_rating",
                "worst_episode", "worst_season", "worst_number", "worst_rating",
                F.col("averageRating").alias("series_rating"), F.col("numVotes").alias("series_votes"))
        .orderBy(F.desc_nulls_last("series_votes"))
    )


def main(min_votes: int = 20) -> None:
    spark = get_spark("q5-series-decline")
    result = series_decline(load(spark, "title.basics"), load(spark, "title.episode"),
                            load(spark, "title.ratings"), min_votes)
    save(result, "q5_series_decline")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-votes", type=int, default=20)
    main(ap.parse_args().min_votes)
