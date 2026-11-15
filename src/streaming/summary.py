import argparse
from pathlib import Path

import pandas as pd
from pyspark.sql import functions as F

from src.common.spark_session import get_spark


def summarize(spark, out: str, produced: int) -> dict:
    matches = spark.read.parquet(f"{out}/matches")
    windows = spark.read.parquet(f"{out}/windows")
    stats = matches.agg(F.count(F.lit(1)).alias("n"), F.countDistinct("title").alias("pages"),
                        F.min("event_time").alias("first"), F.max("event_time").alias("last")).collect()[0]
    by_kind = {r["kind"]: r["count"] for r in matches.groupBy("kind").count().collect()}
    top = (matches.groupBy("title", "kind", "imdb_name").count().orderBy(F.desc("count"), "title").limit(15))
    wins = (windows.select(F.col("window.start").alias("window_start"), F.col("window.end").alias("window_end"),
                           "matches", "distinct_pages", "flagged").orderBy("window_start"))
    Path(out).mkdir(parents=True, exist_ok=True)
    top.toPandas().to_csv(f"{out}/top_matched_pages.csv", index=False)
    wins.toPandas().to_csv(f"{out}/windows.csv", index=False)
    rows = [("events_in_topic", produced), ("matched_events", stats["n"]), ("distinct_matched_pages", stats["pages"]),
            ("matched_title_pages", by_kind.get("title", 0)), ("matched_person_pages", by_kind.get("person", 0)),
            ("first_matched_event", stats["first"]), ("last_matched_event", stats["last"]),
            ("windows_written", windows.count()), ("windows_flagged", windows.where("flagged").count())]
    pd.DataFrame(rows, columns=["metric", "value"]).to_csv(f"{out}/summary.csv", index=False)
    return dict(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/streaming")
    ap.add_argument("--produced", type=int, required=True)
    a = ap.parse_args()
    print(summarize(get_spark("streaming-summary"), a.out, a.produced))
