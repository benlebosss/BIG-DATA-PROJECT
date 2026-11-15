"""Pick the films and people to enrich: top 10 films per genre and year (by votes),
and the first 3 principals of each film (actors, actresses and directors first).

Usage: python -m src.enrichment.select_films [--start 1980 --end 2025 --top 10 --people 3]
"""
import argparse

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F

from src.common.spark_session import get_spark
from src.exploration.common import feature_movies, load, rated, with_genre

OUT = "data/enrichment"


def top_films(basics: DataFrame, ratings: DataFrame, start: int, end: int, top: int) -> DataFrame:
    films = with_genre(rated(feature_movies(basics), ratings)).where(F.col("startYear").between(start, end))
    w = Window.partitionBy("startYear", "genre").orderBy(F.desc("numVotes"), "tconst")
    return (films.withColumn("rank", F.row_number().over(w)).where(F.col("rank") <= top)
            .select("tconst", "primaryTitle", F.col("startYear").alias("year"), "genre", "rank",
                    "averageRating", "numVotes"))


def film_people(films: DataFrame, principals: DataFrame, n: int) -> DataFrame:
    # actors, actresses and directors come first; when a film has fewer than n of them
    # (documentaries list people as "self"), the next principals fill the gap
    main_role = F.when(F.col("category").isin("actor", "actress", "director"), 0).otherwise(1)
    # a voice actor has one row per character: keep one row per person
    per_person = Window.partitionBy("tconst", "nconst").orderBy(main_role, "ordering")
    w = Window.partitionBy("tconst").orderBy(main_role, "ordering")
    return (principals.join(films.select("tconst").distinct(), "tconst")
            .withColumn("k", F.row_number().over(per_person)).where(F.col("k") == 1)
            .withColumn("r", F.row_number().over(w)).where(F.col("r") <= n)
            .select("tconst", "nconst", "category", "ordering"))


def main(start=1980, end=2025, top=10, people=3):
    spark = get_spark("enrichment-select")
    films = top_films(load(spark, "title.basics"), load(spark, "title.ratings"), start, end, top)
    films.write.mode("overwrite").parquet(f"{OUT}/selected_films")
    film_people(films, load(spark, "title.principals"), people) \
        .write.mode("overwrite").parquet(f"{OUT}/selected_people")
    films = spark.read.parquet(f"{OUT}/selected_films")
    print("films:", films.select("tconst").distinct().count(),
          "people:", spark.read.parquet(f"{OUT}/selected_people").select("nconst").distinct().count())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=1980)
    ap.add_argument("--end", type=int, default=2025)
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--people", type=int, default=3)
    a = ap.parse_args()
    main(a.start, a.end, a.top, a.people)
