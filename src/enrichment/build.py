"""Clean the downloaded Wikipedia texts with Spark and join them to the selected films/people.

Output: data/enrichment/films and data/enrichment/people (Parquet), with a source_url for
every row and a note when the information is not available on Wikipedia.

Usage: python -m src.enrichment.build
"""
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from src.common.spark_session import get_spark
from src.exploration.common import load, save

RAW = "data/enrichment/raw"
OUT = "data/enrichment"

ARTICLE_SCHEMA = "id string, article string"
TEXT_SCHEMA = "id string, text string, source_url string, retrieved_at string"


def clean_text(col: str) -> F.Column:
    c = F.regexp_replace(F.col(col), r"\s+", " ")        # newlines, double spaces
    c = F.regexp_replace(c, r"\[\d+\]", "")              # leftover reference marks
    c = F.trim(c)
    return F.when(c == "", None).otherwise(c)


def texts(spark, articles_file: str, texts_file: str) -> DataFrame:
    """IMDb id -> cleaned text + lineage."""
    articles = spark.read.schema(ARTICLE_SCHEMA).json(f"{RAW}/{articles_file}").dropDuplicates(["id"])
    txt = (spark.read.schema(TEXT_SCHEMA).json(f"{RAW}/{texts_file}")
           .withColumn("text", clean_text("text"))
           .dropDuplicates(["id"])
           .withColumnRenamed("id", "article"))
    return (articles.join(txt, "article", "left")
            .withColumn("note", F.when(F.col("article").isNull(), "no English Wikipedia article")
                        .when(F.col("text").isNull(), "article found but no usable text")))


def build_films(spark) -> DataFrame:
    films = spark.read.parquet(f"{OUT}/selected_films")
    t = texts(spark, "film_articles.jsonl", "film_plots.jsonl").select(
        F.col("id").alias("tconst"), F.col("text").alias("synopsis"), "source_url", "retrieved_at",
        F.regexp_replace("note", "no usable text", "no Plot section").alias("note"),
        F.lit(True).alias("looked_up"))
    return (films.join(t, "tconst", "left")
            .withColumn("note", F.when(F.col("looked_up").isNull(), "not looked up yet")
                        .otherwise(F.col("note")))
            .drop("looked_up"))


def build_people(spark) -> DataFrame:
    people = spark.read.parquet(f"{OUT}/selected_people")
    names = load(spark, "name.basics").select("nconst", "primaryName", "birthYear", "deathYear")
    t = texts(spark, "people_articles.jsonl", "people_bios.jsonl") \
        .select(F.col("id").alias("nconst"), F.col("text").alias("biography"), "source_url",
                "retrieved_at", "note")
    return people.join(names, "nconst", "left").join(t, "nconst", "left")


def main():
    spark = get_spark("enrichment-build")
    films = build_films(spark).cache()
    people = build_people(spark).cache()
    films.write.mode("overwrite").parquet(f"{OUT}/films")
    people.write.mode("overwrite").parquet(f"{OUT}/people")

    out = "results/enrichment"
    save(films.groupBy(F.coalesce("note", F.lit("ok")).alias("status")).count(), "films_coverage", out)
    save(people.dropDuplicates(["nconst"]).groupBy(F.coalesce("note", F.lit("ok")).alias("status"))
         .count(), "people_coverage", out)
    sample = films.where("year = 2010 and rank = 1").select(
        "year", "genre", "primaryTitle", F.substring("synopsis", 1, 300).alias("synopsis_start"),
        "source_url", "note")
    save(sample.orderBy("genre"), "films_sample_2010", out)


if __name__ == "__main__":
    main()
