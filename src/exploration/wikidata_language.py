"""Original language of movies from Wikidata (used by Q6).

IMDb does not publish the original language of a title. Wikidata, a human-curated open
database (CC0), links each film to its IMDb id (property P345) and to its original
language (P364). This module:

1. selects the movies to look up with Spark (by default the successful feature movies of Q6,
   but any list of tconst works: ``--all-rated`` takes every rated feature movie);
2. queries the Wikidata SPARQL endpoint in batches, one request at a time, with a
   descriptive User-Agent, a pause between requests and ``Retry-After`` on HTTP 429
   (limits: https://www.mediawiki.org/wiki/Wikidata_Query_Service/User_Manual);
3. stores the raw answers (JSON lines) and, with Spark, a typed Parquet table
   ``data/external/wikidata_language`` where every row keeps its source entity URL.

Usage: python -m src.exploration.wikidata_language [--min-rating 7 --min-votes 10000]
"""
import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from pyspark.sql import functions as F
from pyspark.sql.types import StringType, StructField, StructType

from src.common.spark_session import get_spark
from src.exploration.common import feature_movies, load, rated

ENDPOINT = "https://query.wikidata.org/sparql"
USER_AGENT = ("ECE-BigData-IMDb-student-project/1.0 "
              "(https://github.com/benlebosss/BIG-DATA-PROJECT; educational, non-commercial)")
RAW_FILE = "data/external/wikidata_language_raw.jsonl"
TABLE_DIR = "data/external/wikidata_language"

QUERY = """
SELECT ?imdb ?film ?lang ?iso1 ?iso3 ?wm ?langLabel WHERE {
  VALUES ?imdb { %s }
  ?film wdt:P345 ?imdb ; wdt:P364 ?lang .
  OPTIONAL { ?lang wdt:P218 ?iso1 }
  OPTIONAL { ?lang wdt:P220 ?iso3 }
  OPTIONAL { ?lang wdt:P424 ?wm }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
}"""

SCHEMA = StructType([
    StructField("tconst", StringType(), False),
    StructField("wikidata_id", StringType()),
    StructField("language_code", StringType()),
    StructField("language_label", StringType()),
    StructField("source_url", StringType()),
    StructField("retrieved_at", StringType()),
])


def sparql(ids: list, pause: float, retries: int = 5) -> list:
    """One SPARQL request for a batch of IMDb ids.

    HTTP 429 waits for ``Retry-After``; network errors and 5xx answers are retried with an
    exponential back-off (10 s, 20 s, 40 s ...).
    """
    values = " ".join(f'"{i}"' for i in ids)
    for attempt in range(retries):
        try:
            resp = requests.post(ENDPOINT, data={"query": QUERY % values},
                                 headers={"User-Agent": USER_AGENT,
                                          "Accept": "application/sparql-results+json"}, timeout=90)
            if resp.status_code == 429:
                time.sleep(int(resp.headers.get("Retry-After", 60)))
                continue
            resp.raise_for_status()
            bindings = resp.json()["results"]["bindings"]
        except (requests.RequestException, ValueError) as err:
            print(f"[wikidata] attempt {attempt + 1} failed: {err}", flush=True)
            time.sleep(10 * 2 ** attempt)
            continue
        time.sleep(pause)
        return bindings
    raise RuntimeError(f"Wikidata query failed {retries} times, stopping (the cache keeps the progress)")


def wikimedia_code(code: str) -> str:
    """Wikimedia language codes look like ``zh-yue``: keep the specific part."""
    return code.split("-")[-1] if code else None


def to_record(binding: dict, retrieved_at: str) -> dict:
    value = lambda k: binding[k]["value"] if k in binding else None  # noqa: E731
    film = value("film")
    return {
        "tconst": value("imdb"),
        "wikidata_id": film.rsplit("/", 1)[-1],
        # same convention as title.akas: ISO 639-1 when it exists (fr), else ISO 639-3 (cmn),
        # else the Wikimedia code (Cantonese has no ISO code on Wikidata but "zh-yue")
        "language_code": value("iso1") or value("iso3") or wikimedia_code(value("wm")),
        "language_label": value("langLabel"),
        "source_url": film.replace("http://www.wikidata.org/entity/", "https://www.wikidata.org/wiki/"),
        "retrieved_at": retrieved_at,
    }


def fetch(ids: list, raw_file: str = RAW_FILE, batch: int = 200, pause: float = 1.0) -> None:
    """Query every id not already in ``raw_file`` (the file doubles as a cache)."""
    raw = Path(raw_file)
    raw.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if raw.exists():
        done = {json.loads(line)["tconst"] for line in raw.open(encoding="utf-8")}
    todo = sorted(set(ids) - done)
    print(f"[wikidata] {len(done)} cached, {len(todo)} to query")
    with raw.open("a", encoding="utf-8") as out:
        for start in range(0, len(todo), batch):
            chunk = todo[start:start + batch]
            now = datetime.now(timezone.utc).isoformat(timespec="seconds")
            found = {}
            for b in sparql(chunk, pause):
                rec = to_record(b, now)
                found.setdefault(rec["tconst"], []).append(rec)
            for tconst in chunk:  # ids without answer are cached too, with a null language
                for rec in found.get(tconst, [{"tconst": tconst, "wikidata_id": None,
                                               "language_code": None, "language_label": None,
                                               "source_url": None, "retrieved_at": now}]):
                    out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(f"[wikidata] {min(start + batch, len(todo))}/{len(todo)}", flush=True)


def build_table(spark, raw_file: str = RAW_FILE, table_dir: str = TABLE_DIR) -> None:
    """Typed, de-duplicated table: one row per (tconst, language) with its lineage."""
    df = spark.read.schema(SCHEMA).json(raw_file) \
        .withColumn("language_code", F.lower(F.trim("language_code"))) \
        .withColumn("note", F.when(F.col("wikidata_id").isNull(), "no Wikidata item with this IMDb id")
                    .when(F.col("language_code").isNull(), "no ISO code for the original language")) \
        .dropDuplicates(["tconst", "language_code"])
    df.write.mode("overwrite").parquet(table_dir)
    print(f"[wikidata] table -> {table_dir}")


def main(min_rating: float = 7.0, min_votes: int = 10000, all_rated: bool = False) -> None:
    spark = get_spark("wikidata-language")
    movies = rated(feature_movies(load(spark, "title.basics")), load(spark, "title.ratings"),
                   0 if all_rated else min_votes)
    if not all_rated:
        movies = movies.where(F.col("averageRating") >= min_rating)
    fetch([r.tconst for r in movies.select("tconst").collect()])
    build_table(spark)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-rating", type=float, default=7.0)
    ap.add_argument("--min-votes", type=int, default=10000)
    ap.add_argument("--all-rated", action="store_true")
    a = ap.parse_args()
    main(a.min_rating, a.min_votes, a.all_rated)
