"""Build the IMDb lookup table used to flag Wikipedia pages (stream-static join).

A Wikipedia page title is compared with popular IMDb titles and with the names of
people who acted in / directed popular titles. Popularity thresholds (numVotes) keep
the table small enough to broadcast and limit false positives on common words.
"""
import argparse

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from src.common.imdb_schemas import read_table
from src.common.spark_session import get_spark

REF_PATH = "data/parquet/streaming_reference"
TITLE_TYPES = ["movie", "tvSeries", "tvMiniSeries", "tvMovie"]
PEOPLE_CATEGORIES = ["actor", "actress", "director"]


def norm_key(col):
    """Lower-case, drop a trailing '(film)'-style disambiguation, trim spaces."""
    return F.trim(F.lower(F.regexp_replace(col, r"\s*\([^)]*\)\s*$", "")))


def build_reference(spark: SparkSession, min_title_votes: int = 5000,
                    min_person_votes: int = 20000, tables: dict = None) -> DataFrame:
    names = ["title.basics", "title.ratings", "title.principals", "name.basics"]
    t = tables or {n: read_table(spark, n) for n in names}
    ratings = t["title.ratings"]
    popular = (t["title.basics"].filter(F.col("titleType").isin(TITLE_TYPES))
               .join(ratings.filter(F.col("numVotes") >= min_title_votes), "tconst"))
    titles = popular.select(
        norm_key(F.col("primaryTitle")).alias("key"), F.lit("title").alias("kind"),
        F.col("tconst").alias("imdb_id"), F.col("primaryTitle").alias("imdb_name"),
        F.col("numVotes").cast("long").alias("votes"))
    people_votes = (t["title.principals"].filter(F.col("category").isin(PEOPLE_CATEGORIES))
                    .join(ratings.filter(F.col("numVotes") >= min_person_votes), "tconst")
                    .groupBy("nconst").agg(F.max("numVotes").cast("long").alias("votes")))
    people = (t["name.basics"].join(people_votes, "nconst")
              .select(norm_key(F.col("primaryName")).alias("key"), F.lit("person").alias("kind"),
                      F.col("nconst").alias("imdb_id"), F.col("primaryName").alias("imdb_name"),
                      "votes"))
    return titles.unionByName(people).filter(F.length("key") > 2)


def main(out: str = REF_PATH, min_title_votes: int = 5000, min_person_votes: int = 20000):
    spark = get_spark("streaming-reference")
    ref = build_reference(spark, min_title_votes, min_person_votes)
    ref.write.mode("overwrite").parquet(out)
    n = spark.read.parquet(out).groupBy("kind").count().collect()
    print({r["kind"]: r["count"] for r in n})


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=REF_PATH)
    ap.add_argument("--min-title-votes", type=int, default=5000)
    ap.add_argument("--min-person-votes", type=int, default=20000)
    a = ap.parse_args()
    main(a.out, a.min_title_votes, a.min_person_votes)
