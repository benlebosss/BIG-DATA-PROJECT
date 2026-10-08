"""One-off conversion of the gzipped IMDb TSV files to Parquet (data/parquet/).

gzip is not splittable, so reading the TSV files is single-threaded and slow. Converting once
makes every later step fast. Usage: python -m src.preparation.to_parquet [--data-dir data/imdb]
"""
import argparse

from src.common.imdb_schemas import SCHEMAS, read_table
from src.common.spark_session import get_spark


def main(data_dir: str = "data/imdb") -> None:
    spark = get_spark("imdb-to-parquet")
    for name in SCHEMAS:
        target = f"data/parquet/{name.replace('.', '_')}"
        tmp = f"{target}.tmp"
        read_table(spark, name, data_dir).write.mode("overwrite").parquet(tmp)
        spark.read.parquet(tmp).write.mode("overwrite").parquet(target)  # atomic-ish: finished tables only
        print(f"[parquet] {name} -> {target}", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/imdb")
    main(ap.parse_args().data_dir)
