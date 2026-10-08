"""Explicit schemas and reader for the IMDb non-commercial TSV datasets."""
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import (
    BooleanType,
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

S, I, B = StringType(), IntegerType(), BooleanType()

SCHEMAS = {
    "name.basics": StructType([
        StructField("nconst", S), StructField("primaryName", S),
        StructField("birthYear", I), StructField("deathYear", I),
        StructField("primaryProfession", S), StructField("knownForTitles", S),
    ]),
    "title.akas": StructType([
        StructField("titleId", S), StructField("ordering", I),
        StructField("title", S), StructField("region", S),
        StructField("language", S), StructField("types", S),
        StructField("attributes", S), StructField("isOriginalTitle", B),
    ]),
    "title.basics": StructType([
        StructField("tconst", S), StructField("titleType", S),
        StructField("primaryTitle", S), StructField("originalTitle", S),
        StructField("isAdult", B), StructField("startYear", I),
        StructField("endYear", I), StructField("runtimeMinutes", I),
        StructField("genres", S),
    ]),
    "title.crew": StructType([
        StructField("tconst", S), StructField("directors", S),
        StructField("writers", S),
    ]),
    "title.episode": StructType([
        StructField("tconst", S), StructField("parentTconst", S),
        StructField("seasonNumber", I), StructField("episodeNumber", I),
    ]),
    "title.principals": StructType([
        StructField("tconst", S), StructField("ordering", I),
        StructField("nconst", S), StructField("category", S),
        StructField("job", S), StructField("characters", S),
    ]),
    "title.ratings": StructType([
        StructField("tconst", S), StructField("averageRating", DoubleType()),
        StructField("numVotes", I),
    ]),
}

TABLES = list(SCHEMAS)


def read_table(spark: SparkSession, name: str, data_dir: str = "data/imdb") -> DataFrame:
    """Read one IMDb table (``<name>.tsv.gz``) with its explicit schema.

    IMDb encodes missing values as the literal ``\\N``; they become real nulls.
    """
    parquet = Path(data_dir).parent / "parquet" / name.replace(".", "_")
    if parquet.exists():  # fast path: see src/preparation/to_parquet.py
        return spark.read.parquet(str(parquet))
    path = Path(data_dir) / f"{name}.tsv.gz"
    return (
        spark.read.option("sep", "\t")
        .option("header", True)
        .option("nullValue", "\\N")
        .option("quote", "")
        .option("mode", "PERMISSIVE")
        .schema(SCHEMAS[name])
        .csv(str(path))
    )
