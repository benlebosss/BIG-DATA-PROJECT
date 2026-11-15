"""Shared helpers for the exploration questions.

Every question reads the cleaned tables produced by ``src.preparation.clean``
(``data/clean/<table>``). When they are not there yet, it falls back to the raw
tables through ``read_table`` so the code can still run on a fresh clone.
"""
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from src.common.imdb_schemas import read_table

CLEAN_DIR = "data/clean"
RAW_DIR = "data/imdb"
RESULTS_DIR = "results/exploration"

# A feature film runs for more than 40 minutes (AMPAS / AFI / BFI definition).
FEATURE_MIN_RUNTIME = 40


def load(spark: SparkSession, name: str, clean_dir: str = CLEAN_DIR,
         raw_dir: str = RAW_DIR) -> DataFrame:
    """Load one IMDb table, cleaned version first."""
    path = Path(clean_dir) / name.replace(".", "_")
    if path.exists():
        return spark.read.parquet(str(path))
    return read_table(spark, name, raw_dir)


def split_list(col: str) -> F.Column:
    """IMDb list columns are comma separated strings (``"Drama,Romance"``)."""
    return F.split(F.col(col), ",")


def feature_movies(basics: DataFrame, min_runtime: int = FEATURE_MIN_RUNTIME) -> DataFrame:
    """Non-adult feature-length movies with a known release year and runtime."""
    not_adult = ~F.coalesce(F.col("isAdult").cast("boolean"), F.lit(False))
    return basics.where(
        (F.col("titleType") == "movie")
        & not_adult
        & F.col("startYear").isNotNull()
        & (F.col("runtimeMinutes") > min_runtime)
    )


def with_genre(df: DataFrame) -> DataFrame:
    """One row per (title, genre); titles without genre are dropped."""
    return df.withColumn("genre", F.explode(split_list("genres"))).where(F.col("genre").isNotNull())


def rated(df: DataFrame, ratings: DataFrame, min_votes: int = 0) -> DataFrame:
    """Inner join with the ratings, keeping titles with at least ``min_votes`` votes."""
    return df.join(ratings, "tconst").where(F.col("numVotes") >= min_votes)


def save(df: DataFrame, name: str, out_dir: str = RESULTS_DIR, limit: int = None) -> DataFrame:
    """Write a (small) result as a single CSV file ``<out_dir>/<name>.csv``."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    rows = df.limit(limit) if limit else df
    rows.toPandas().to_csv(out / f"{name}.csv", index=False)
    print(f"[result] {name}.csv")
    return df
