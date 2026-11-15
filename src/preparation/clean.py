"""Step 2b: cleaning of the IMDb tables -> Parquet in ``data/clean/``.

Strategies applied (each one is a Spark transformation, nothing is done in pandas):
  1. Drop duplicated primary keys.
  2. Drop rows of child tables whose parent key does not exist (orphans, left_semi joins).
  3. Replace impossible values by null (runtime <= 0 or > 1000 min, endYear < startYear,
     deathYear < birthYear, rating outside [1, 10]) instead of dropping the whole row.
  4. Keep remaining nulls as null (never invent values); empty strings become null.

Usage: python -m src.preparation.clean [--data-dir data/imdb] [--out data/clean]
"""
import argparse

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import StringType

from src.common.imdb_schemas import TABLES, read_table
from src.common.spark_session import get_spark


def empty_to_null(df: DataFrame) -> DataFrame:
    for f in df.schema.fields:
        if isinstance(f.dataType, StringType):
            c = F.col(f.name)
            df = df.withColumn(f.name, F.when(F.trim(c) == "", None).otherwise(c))
    return df


def keep_with_parent(child: DataFrame, key: str, parent: DataFrame, parent_key: str) -> DataFrame:
    parents = parent.select(F.col(parent_key).alias(key)).distinct()
    return child.join(parents, key, "left_semi")


def clean_basics(df: DataFrame) -> DataFrame:
    df = empty_to_null(df).dropDuplicates(["tconst"])
    df = df.withColumn("runtimeMinutes",
                       F.when((F.col("runtimeMinutes") > 0) & (F.col("runtimeMinutes") <= 1000),
                              F.col("runtimeMinutes")))
    return df.withColumn("endYear",
                         F.when(F.col("endYear") >= F.col("startYear"), F.col("endYear"))
                         .when(F.col("endYear").isNull(), None))


def clean_names(df: DataFrame) -> DataFrame:
    df = empty_to_null(df).dropDuplicates(["nconst"])
    return df.withColumn("deathYear",
                         F.when(F.col("deathYear") >= F.col("birthYear"), F.col("deathYear"))
                         .when(F.col("birthYear").isNull(), F.col("deathYear")))


def main(data_dir: str = "data/imdb", out_dir: str = "data/clean", spark=None) -> None:
    spark = spark or get_spark("imdb-clean")
    raw = {n: read_table(spark, n, data_dir) for n in TABLES}

    basics = clean_basics(raw["title.basics"])
    names = clean_names(raw["name.basics"])

    ratings = empty_to_null(raw["title.ratings"]).dropDuplicates(["tconst"]) \
        .where(F.col("averageRating").between(1, 10))
    crew = empty_to_null(raw["title.crew"]).dropDuplicates(["tconst"])
    episode = empty_to_null(raw["title.episode"]).dropDuplicates(["tconst"])
    principals = empty_to_null(raw["title.principals"]).dropDuplicates(["tconst", "ordering"])
    akas = empty_to_null(raw["title.akas"]).dropDuplicates(["titleId", "ordering"])

    ratings = keep_with_parent(ratings, "tconst", basics, "tconst")
    crew = keep_with_parent(crew, "tconst", basics, "tconst")
    episode = keep_with_parent(episode, "tconst", basics, "tconst")
    episode = keep_with_parent(episode, "parentTconst", basics, "tconst")
    principals = keep_with_parent(principals, "tconst", basics, "tconst")
    principals = keep_with_parent(principals, "nconst", names, "nconst")
    akas = keep_with_parent(akas, "titleId", basics, "tconst")

    cleaned = {"title.basics": basics, "name.basics": names, "title.ratings": ratings,
               "title.crew": crew, "title.episode": episode,
               "title.principals": principals, "title.akas": akas}
    for name, df in cleaned.items():
        target = f"{out_dir}/{name.replace('.', '_')}"
        df.write.mode("overwrite").parquet(target)
        print(f"[clean] {name} -> {target}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/imdb")
    ap.add_argument("--out", default="data/clean")
    a = ap.parse_args()
    main(a.data_dir, a.out)
