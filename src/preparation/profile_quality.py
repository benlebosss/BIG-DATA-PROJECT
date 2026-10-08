"""Step 2a: data-quality profiling of the IMDb tables.

Outputs (CSV, in ``results/preparation/``):
  - null_profile.csv    : per table/column null, empty and missing percentages
  - top5_missing.csv    : the five columns with the highest missing percentage
  - quality_issues.csv  : orphan foreign keys, duplicate keys and inconsistent values

Usage: python -m src.preparation.profile_quality [--data-dir data/imdb] [--out results/preparation]
"""
import argparse
from pathlib import Path

import pandas as pd
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StringType

from src.common.imdb_schemas import TABLES, read_table
from src.common.spark_session import get_spark


def profile_columns(df: DataFrame, table: str) -> pd.DataFrame:
    """Null / empty / missing percentage for every column of ``df`` (one pass)."""
    aggs = [F.count(F.lit(1)).alias("__total")]
    for field in df.schema.fields:
        c = F.col(field.name)
        aggs.append(F.sum(c.isNull().cast("int")).alias(f"{field.name}__null"))
        if isinstance(field.dataType, StringType):
            aggs.append(F.sum((F.trim(c) == "").cast("int")).alias(f"{field.name}__empty"))
    row = df.agg(*aggs).first().asDict()
    total = row["__total"]
    out = []
    for field in df.schema.fields:
        nulls = row[f"{field.name}__null"] or 0
        empty = row.get(f"{field.name}__empty", 0) or 0
        out.append((
            table, field.name, str(field.dataType), total, nulls, empty,
            round(100.0 * nulls / total, 3) if total else None,
            round(100.0 * empty / total, 3) if total else None,
            round(100.0 * (nulls + empty) / total, 3) if total else None,
        ))
    cols = ["table", "column", "type", "rows", "null_count", "empty_count",
            "null_pct", "empty_pct", "missing_pct"]
    return pd.DataFrame(out, columns=cols)


def count_orphans(child: DataFrame, key: str, parent: DataFrame, parent_key: str) -> int:
    """Number of distinct non-null ``key`` values in ``child`` absent from ``parent``."""
    keys = child.select(F.col(key).alias("k")).where(F.col("k").isNotNull()).distinct()
    parents = parent.select(F.col(parent_key).alias("k")).distinct()
    return keys.join(parents, "k", "left_anti").count()


def explode_ids(df: DataFrame, col: str, alias: str) -> DataFrame:
    """One row per id of a comma-separated list column."""
    return (
        df.select(F.explode(F.split(F.col(col), ",")).alias(alias))
        .where(F.col(alias).isNotNull() & (F.trim(F.col(alias)) != ""))
    )


def quality_issues(t: dict) -> list:
    issues = []

    def add(table, issue, count, detail=""):
        print(f"[issue] {table}: {issue} = {count}")
        issues.append((table, issue, int(count), detail))

    basics, names = t["title.basics"], t["name.basics"]
    # --- missing parents (foreign keys)
    for child, col in [("title.akas", "titleId"), ("title.crew", "tconst"),
                       ("title.episode", "tconst"), ("title.episode", "parentTconst"),
                       ("title.principals", "tconst"), ("title.ratings", "tconst")]:
        add(child, f"{col} missing in title.basics",
            count_orphans(t[child], col, basics, "tconst"), "distinct orphan ids")
    add("title.principals", "nconst missing in name.basics",
        count_orphans(t["title.principals"], "nconst", names, "nconst"), "distinct orphan ids")
    for col in ("directors", "writers"):
        ids = explode_ids(t["title.crew"], col, "nconst")
        add("title.crew", f"{col} ids missing in name.basics",
            count_orphans(ids, "nconst", names, "nconst"), "distinct orphan ids")
    kft = explode_ids(names, "knownForTitles", "tconst")
    add("name.basics", "knownForTitles missing in title.basics",
        count_orphans(kft, "tconst", basics, "tconst"), "distinct orphan ids")

    # --- duplicate keys
    for table, key in [("title.basics", ["tconst"]), ("name.basics", ["nconst"]),
                       ("title.ratings", ["tconst"]), ("title.crew", ["tconst"]),
                       ("title.episode", ["tconst"]),
                       ("title.principals", ["tconst", "ordering"]),
                       ("title.akas", ["titleId", "ordering"])]:
        df = t[table]
        add(table, f"duplicate key {key}", df.count() - df.dropDuplicates(key).count())

    # --- inconsistent values
    add("title.basics", "endYear < startYear",
        basics.where(F.col("endYear") < F.col("startYear")).count())
    add("title.basics", "runtimeMinutes <= 0 or > 1000",
        basics.where((F.col("runtimeMinutes") <= 0) | (F.col("runtimeMinutes") > 1000)).count())
    add("title.basics", "startYear > 2026",
        basics.where(F.col("startYear") > 2026).count(), "future-dated titles")
    add("name.basics", "deathYear < birthYear",
        names.where(F.col("deathYear") < F.col("birthYear")).count())
    add("title.ratings", "averageRating outside [1,10]",
        t["title.ratings"].where((F.col("averageRating") < 1) | (F.col("averageRating") > 10)).count())
    add("title.principals", "unparseable rows in 'ordering'",
        t["title.principals"].where(F.col("ordering").isNull()).count())
    return issues


def main(data_dir: str = "data/imdb", out_dir: str = "results/preparation",
         spark: SparkSession = None) -> None:
    spark = spark or get_spark("imdb-profile-quality")
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    tables = {n: read_table(spark, n, data_dir) for n in TABLES}

    pdf = pd.concat([profile_columns(df, n) for n, df in tables.items()], ignore_index=True)
    pdf.to_csv(out / "null_profile.csv", index=False)
    top5 = pdf.sort_values("missing_pct", ascending=False).head(5)
    top5.to_csv(out / "top5_missing.csv", index=False)
    print(top5.to_string(index=False))

    pd.DataFrame(quality_issues(tables), columns=["table", "issue", "count", "detail"]) \
        .to_csv(out / "quality_issues.csv", index=False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/imdb")
    ap.add_argument("--out", default="results/preparation")
    a = ap.parse_args()
    main(a.data_dir, a.out)
