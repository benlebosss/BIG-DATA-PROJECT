"""Contract of the Kafka messages produced by wikipedia_producer.py.

The Structured Streaming job (consumer) should parse the ``value`` of each Kafka record with
``from_json(col("value").cast("string"), CHANGE_SCHEMA)``. The record key is the page title.
"""
from pyspark.sql.types import (
    BooleanType,
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
)

TOPIC = "wikipedia-changes"

CHANGE_SCHEMA = StructType([
    StructField("event_id", StringType()),      # unique id of the event (meta.id)
    StructField("wiki", StringType()),          # e.g. "enwiki"
    StructField("title", StringType()),         # page title, e.g. "Inception (film)"
    StructField("type", StringType()),          # "edit" or "new"
    StructField("namespace", IntegerType()),    # 0 = articles
    StructField("user", StringType()),
    StructField("bot", BooleanType()),
    StructField("comment", StringType()),       # edit summary
    StructField("timestamp", LongType()),       # epoch seconds of the edit
    StructField("event_time", StringType()),    # ISO-8601 (meta.dt); use to_timestamp() as event time
    StructField("server_name", StringType()),   # e.g. "en.wikipedia.org"
    StructField("url", StringType()),           # link to the diff
])
