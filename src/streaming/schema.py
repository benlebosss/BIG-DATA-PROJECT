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
    StructField("event_id", StringType()),
    StructField("wiki", StringType()),
    StructField("title", StringType()),
    StructField("type", StringType()),
    StructField("namespace", IntegerType()),
    StructField("user", StringType()),
    StructField("bot", BooleanType()),
    StructField("comment", StringType()),
    StructField("timestamp", LongType()),
    StructField("event_time", StringType()),
    StructField("server_name", StringType()),
    StructField("url", StringType()),
])
