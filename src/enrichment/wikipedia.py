import argparse
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

API = "https://en.wikipedia.org/api/rest_v1/page/summary/"
USER_AGENT = "ece-bigdata-project/1.0 (student project; https://github.com/benlebosss/BIG-DATA-PROJECT)"
TITLE_HINT = re.compile(r"film|series|television|miniseries|movie|sitcom|drama", re.I)
PERSON_HINT = re.compile(r"actor|actress|director|filmmaker|producer|screenwriter|comedian|singer|born", re.I)
COLUMNS = ["imdb_id", "kind", "imdb_name", "status", "wikipedia_title", "description", "extract",
           "source_url", "revision", "wiki_timestamp", "fetched_at"]


class RateLimiter:

    def __init__(self, per_second: float = 5.0, clock=time.monotonic, sleep=time.sleep):
        self.interval, self.clock, self.sleep, self.last = 1.0 / per_second, clock, sleep, None

    def wait(self):
        now = self.clock()
        if self.last is not None and now - self.last < self.interval:
            self.sleep(self.interval - (now - self.last))
        self.last = self.clock()


def candidates(kind: str, name: str, year=None) -> list:
    base = name.replace(" ", "_")
    if kind == "title":
        out = [f"{base}_({year}_film)"] if year else []
        out += [f"{base}_(film)"]
        out += [f"{base}_({year}_TV_series)"] if year else []
        return out + [f"{base}_(TV_series)", base]
    return [base, f"{base}_(actor)", f"{base}_(director)", f"{base}_(actress)"]


def is_relevant(kind: str, data: dict) -> bool:
    if data.get("type") != "standard":
        return False
    text = (data.get("description") or "") + " " + (data.get("extract") or "")[:300]
    return bool((TITLE_HINT if kind == "title" else PERSON_HINT).search(text))


def to_record(row: dict, data: dict) -> dict:
    page = (data.get("content_urls") or {}).get("desktop", {}).get("page")
    return {"imdb_id": row["imdb_id"], "kind": row["kind"], "imdb_name": row["imdb_name"], "status": "ok",
            "wikipedia_title": data.get("title"), "description": data.get("description"),
            "extract": data.get("extract"), "source_url": page, "revision": data.get("revision"),
            "wiki_timestamp": data.get("timestamp"),
            "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}


def enrich_row(row: dict, fetch) -> dict:
    for cand in candidates(row["kind"], row["imdb_name"], row.get("year")):
        data = fetch(cand)
        if data and is_relevant(row["kind"], data):
            return to_record(row, data)
    return {"imdb_id": row["imdb_id"], "kind": row["kind"], "imdb_name": row["imdb_name"],
            "status": "not_found",
            "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}


def retry_delay(headers, attempt):
    try:
        return min(float(headers.get("Retry-After", 2 ** attempt)), 60.0)
    except ValueError:
        return float(2 ** attempt)


def make_fetch(per_second: float = 5.0, retries: int = 5, session=None, sleep=time.sleep):
    import requests
    session = session or requests.Session()
    limiter = RateLimiter(per_second)

    def fetch(title):
        url = API + quote(title, safe="()_,'")
        for attempt in range(retries):
            limiter.wait()
            r = session.get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (429, 500, 502, 503, 504):
                sleep(retry_delay(r.headers, attempt))
                continue
            return None
        return None
    return fetch


def run(entities: list, cache_path: str, fetch=None, per_second: float = 5.0) -> list:
    fetch = fetch or make_fetch(per_second)
    cache = Path(cache_path)
    cache.parent.mkdir(parents=True, exist_ok=True)
    done = {}
    if cache.exists():
        for line in cache.read_text().splitlines():
            rec = json.loads(line)
            done[(rec["imdb_id"], rec["kind"])] = rec
    with cache.open("a") as f:
        for row in entities:
            key = (row["imdb_id"], row["kind"])
            if key in done:
                continue
            done[key] = enrich_row(row, fetch)
            f.write(json.dumps(done[key]) + "\n")
            f.flush()
    return [done[(r["imdb_id"], r["kind"])] for r in entities]


def select_entities(spark, n_titles: int, n_people: int) -> list:
    from pyspark.sql import functions as F
    from src.common.imdb_schemas import read_table
    basics, ratings = read_table(spark, "title.basics"), read_table(spark, "title.ratings")
    top = (basics.filter(F.col("titleType").isin("movie", "tvSeries")).join(ratings, "tconst")
           .orderBy(F.desc("numVotes")).limit(n_titles))
    titles = top.select(F.col("tconst").alias("imdb_id"), F.lit("title").alias("kind"),
                        F.col("primaryTitle").alias("imdb_name"), F.col("startYear").cast("string").alias("year"))
    people = (read_table(spark, "title.principals")
              .filter(F.col("category").isin("actor", "actress", "director"))
              .join(top.select("tconst"), "tconst").groupBy("nconst").count()
              .orderBy(F.desc("count")).limit(n_people)
              .join(read_table(spark, "name.basics"), "nconst")
              .select(F.col("nconst").alias("imdb_id"), F.lit("person").alias("kind"),
                      F.col("primaryName").alias("imdb_name"), F.lit(None).cast("string").alias("year")))
    return [r.asDict() for r in titles.unionByName(people).collect()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--titles", type=int, default=200)
    ap.add_argument("--people", type=int, default=200)
    ap.add_argument("--per-second", type=float, default=5.0)
    ap.add_argument("--cache", default="data/enrichment/wikipedia.jsonl")
    ap.add_argument("--out", default="results/enrichment/wikipedia_enrichment.csv")
    a = ap.parse_args()
    import pandas as pd
    from src.common.spark_session import get_spark
    entities = select_entities(get_spark("enrichment"), a.titles, a.people)
    records = run(entities, a.cache, per_second=a.per_second)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(records).reindex(columns=COLUMNS)
    df.to_csv(a.out, index=False)
    print(df.groupby(["kind", "status"]).size())


if __name__ == "__main__":
    main()
