"""Shared Spark session factory."""
import os

from pyspark.sql import SparkSession


def get_spark(app_name: str = "imdb-project", with_kafka: bool = False) -> SparkSession:
    builder = (
        SparkSession.builder.appName(app_name)
        .config("spark.driver.memory", os.getenv("SPARK_DRIVER_MEMORY", "2g"))
        .config("spark.sql.shuffle.partitions", "8")
    )
    if with_kafka:
        builder = builder.config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3",
        )
    return builder.getOrCreate()
