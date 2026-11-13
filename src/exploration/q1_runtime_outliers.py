"""Q1: feature-length movies whose runtime is notably different from their genre's average.

Two criteria are computed per genre and kept side by side:
  - z-score: runtime more than ``z`` standard deviations away from the genre mean;
  - IQR (Tukey fences): runtime below Q1 - 1.5 IQR or above Q3 + 1.5 IQR.
The z-score is sensitive to the extreme values it tries to detect (they inflate the standard
deviation) and, because feature films start at 40 minutes, it can only flag long movies.
The quartiles are robust to both. A movie is listed when at least one criterion flags it.

Usage: python -m src.exploration.q1_runtime_outliers [--z 3]
"""
import argparse

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from src.common.spark_session import get_spark
from src.exploration.common import feature_movies, load, save, with_genre


def genre_runtime_stats(movies: DataFrame) -> DataFrame:
    """Mean, standard deviation and quartiles of the runtime for every genre."""
    return movies.groupBy("genre").agg(
        F.count("*").alias("n_movies"),
        F.avg("runtimeMinutes").alias("mean_runtime"),
        F.stddev("runtimeMinutes").alias("std_runtime"),
        F.percentile_approx("runtimeMinutes", [0.25, 0.5, 0.75], 10000).alias("q"),
    ).select(
        "genre", "n_movies", "mean_runtime", "std_runtime",
        F.col("q")[0].alias("q1"), F.col("q")[1].alias("median"), F.col("q")[2].alias("q3"),
    )


def runtime_outliers(basics: DataFrame, z: float = 3.0) -> DataFrame:
    movies = with_genre(feature_movies(basics)).select(
        "tconst", "primaryTitle", "startYear", "runtimeMinutes", "genre")
    stats = genre_runtime_stats(movies)
    iqr = F.col("q3") - F.col("q1")
    return (
        movies.join(F.broadcast(stats), "genre")
        .withColumn("z_score", (F.col("runtimeMinutes") - F.col("mean_runtime")) / F.col("std_runtime"))
        .withColumn("z_outlier", F.abs(F.col("z_score")) > z)
        .withColumn("iqr_outlier",
                    (F.col("runtimeMinutes") < F.col("q1") - 1.5 * iqr)
                    | (F.col("runtimeMinutes") > F.col("q3") + 1.5 * iqr))
        .where(F.col("z_outlier") | F.col("iqr_outlier"))
        .withColumn("direction", F.when(F.col("runtimeMinutes") > F.col("median"), "longer")
                    .otherwise("shorter"))
        .select("genre", "tconst", "primaryTitle", "startYear", "runtimeMinutes",
                F.round("mean_runtime", 1).alias("genre_mean"),
                F.round("std_runtime", 1).alias("genre_std"), F.col("median").alias("genre_median"),
                F.round("z_score", 2).alias("z_score"), "direction", "z_outlier", "iqr_outlier")
    )


def main(z: float = 3.0) -> None:
    spark = get_spark("q1-runtime-outliers")
    basics = load(spark, "title.basics")
    stats = genre_runtime_stats(with_genre(feature_movies(basics)))
    save(stats.orderBy("genre"), "q1_genre_runtime_stats")
    outliers = runtime_outliers(basics, z).cache()
    save(outliers.groupBy("genre", "direction").agg(
        F.sum(F.col("z_outlier").cast("int")).alias("z_outliers"),
        F.sum(F.col("iqr_outlier").cast("int")).alias("iqr_outliers"),
        F.sum((F.col("z_outlier") & F.col("iqr_outlier")).cast("int")).alias("both"))
        .orderBy("genre", "direction"), "q1_outliers_per_genre")
    save(outliers.orderBy(F.desc(F.abs("z_score"))), "q1_runtime_outliers")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--z", type=float, default=3.0)
    main(ap.parse_args().z)
