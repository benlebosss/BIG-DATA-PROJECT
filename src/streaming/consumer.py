import argparse

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from src.common.spark_session import get_spark
from src.streaming.reference import REF_PATH, norm_key
from src.streaming.schema import CHANGE_SCHEMA, TOPIC


def parse_changes(raw: DataFrame) -> DataFrame:
    return (raw.select(F.from_json(F.col("value").cast("string"), CHANGE_SCHEMA).alias("c"))
            .select("c.*")
            .filter(F.col("title").isNotNull() & F.col("timestamp").isNotNull())
            .withColumn("event_time", F.col("timestamp").cast("timestamp")))


def match_entities(changes: DataFrame, ref: DataFrame) -> DataFrame:
    keyed = changes.withColumn("key", norm_key(F.col("title")))
    return keyed.join(F.broadcast(ref), "key", "inner")


def window_counts(matches: DataFrame, window: str = "30 minutes", slide: str = "5 minutes",
                  watermark: str = "10 minutes", min_matches: int = 3) -> DataFrame:
    return (matches.withWatermark("event_time", watermark)
            .groupBy(F.window("event_time", window, slide))
            .agg(F.count(F.lit(1)).alias("matches"),
                 F.approx_count_distinct("title").alias("distinct_pages"),
                 F.collect_set("title").alias("pages"))
            .withColumn("pages", F.slice("pages", 1, 10))
            .withColumn("flagged", F.col("matches") >= min_matches))


def read_source(spark: SparkSession, a) -> DataFrame:
    if a.source == "kafka":
        return (spark.readStream.format("kafka")
                .option("kafka.bootstrap.servers", a.bootstrap)
                .option("subscribe", a.topic)
                .option("startingOffsets", a.starting_offsets)
                .option("failOnDataLoss", "false").load()
                .select(F.col("value").cast("string").alias("value")))
    return spark.readStream.text(a.input_dir)


def positive_int(value):
    n = int(value)
    if n < 1:
        raise argparse.ArgumentTypeError("must be >= 1")
    return n


def main(a):
    spark = get_spark("wikipedia-imdb-consumer", with_kafka=(a.source == "kafka"))
    spark.sparkContext.setLogLevel("WARN")
    ref = spark.read.parquet(a.reference)
    matches = match_entities(parse_changes(read_source(spark, a)), ref)
    trig = {"processingTime": f"{a.trigger_seconds} seconds"}
    q1 = (matches.select("event_time", "wiki", "title", "kind", "imdb_id", "imdb_name", "user",
                         "bot", "url")
          .writeStream.outputMode("append").trigger(**trig)
          .option("checkpointLocation", f"{a.checkpoint}/matches")
          .format("parquet").option("path", f"{a.out}/matches").start()
          if a.out else
          matches.select("event_time", "title", "kind", "imdb_name").writeStream
          .outputMode("append").format("console").option("truncate", "false")
          .trigger(**trig).start())
    counts = window_counts(matches, a.window, a.slide, a.watermark, a.min_matches)
    w = counts.writeStream.trigger(**trig).option("checkpointLocation", f"{a.checkpoint}/windows")
    if a.out:
        q2 = (w.outputMode("append").format("parquet").option("path", f"{a.out}/windows").start())
    else:
        q2 = w.outputMode(a.window_mode).format("console").option("truncate", "false").start()
    spark.streams.awaitAnyTermination(a.timeout)
    for q in (q1, q2):
        q.stop()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["kafka", "files"], default="kafka")
    ap.add_argument("--bootstrap", default="localhost:9092")
    ap.add_argument("--topic", default=TOPIC)
    ap.add_argument("--starting-offsets", default="latest")
    ap.add_argument("--input-dir", default="data/stream_input")
    ap.add_argument("--reference", default=REF_PATH)
    ap.add_argument("--window", default="30 minutes")
    ap.add_argument("--slide", default="5 minutes")
    ap.add_argument("--watermark", default="10 minutes")
    ap.add_argument("--min-matches", type=positive_int, default=3)
    ap.add_argument("--window-mode", choices=["append", "update", "complete"], default="update")
    ap.add_argument("--out", default=None, help="write parquet here instead of the console")
    ap.add_argument("--checkpoint", default="checkpoints/streaming")
    ap.add_argument("--trigger-seconds", type=positive_int, default=30)
    ap.add_argument("--timeout", type=float, default=None, help="stop after N seconds")
    main(ap.parse_args())
