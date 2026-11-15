"""Download synopses (Plot section) and short biographies (article intro) from English Wikipedia.

IMDb id -> Wikipedia article goes through Wikidata (P345 + enwiki sitelink).
Requests are sent one at a time with a User-Agent and maxlag, results are appended to JSON
lines files that also act as a cache, so the script can be stopped and restarted.

Usage: python -m src.enrichment.wiki_texts
"""
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import requests

from src.common.spark_session import get_spark

UA = "ECE-BigData-IMDb-student-project/1.0 (https://github.com/benlebosss/BIG-DATA-PROJECT)"
WIKIDATA = "https://query.wikidata.org/sparql"
API = "https://en.wikipedia.org/w/api.php"
RAW = Path("data/enrichment/raw")
PLOT_HEADINGS = ("plot", "synopsis", "plot summary", "premise", "story")

SITELINKS = """
SELECT ?id ?article WHERE {
  VALUES ?id { %s }
  ?item wdt:P345 ?id .
  ?link schema:about ?item ; schema:isPartOf <https://en.wikipedia.org/> ; schema:name ?article .
}"""


def get(url, params=None, data=None, tries=5):
    for i in range(tries):
        try:
            r = requests.request("POST" if data else "GET", url, params=params, data=data,
                                 headers={"User-Agent": UA}, timeout=60)
            if r.status_code == 429 or "maxlag" in r.text[:200]:
                time.sleep(int(r.headers.get("Retry-After", 10)))
                continue
            r.raise_for_status()
            return r.json()
        except (requests.RequestException, ValueError) as e:
            print("retry", i + 1, e, flush=True)
            time.sleep(5 * 2 ** i)
    raise RuntimeError(f"giving up on {url}")


def cached(path):
    if not path.exists():
        return {}
    return {r["id"]: r for r in map(json.loads, path.open(encoding="utf-8"))}


def append(path, rows):
    with path.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def article_names(ids, path):
    """IMDb id -> English Wikipedia article title (None when there is none)."""
    done = cached(path)
    todo = [i for i in ids if i not in done]
    for k in range(0, len(todo), 200):
        chunk = todo[k:k + 200]
        res = get(WIKIDATA, data={"query": SITELINKS % " ".join(f'"{i}"' for i in chunk),
                                  "format": "json"})
        found = {b["id"]["value"]: b["article"]["value"] for b in res["results"]["bindings"]}
        append(path, [{"id": i, "article": found.get(i)} for i in chunk])
        print(f"wikidata {k + len(chunk)}/{len(todo)}", flush=True)
        time.sleep(1)
    return {i: r["article"] for i, r in cached(path).items()}


def plot_section(text):
    """Return the text of the Plot (or Synopsis...) section of a plain-text extract."""
    parts = re.split(r"\n==+\s*(.+?)\s*==+\n", "\n" + text)
    for title, body in zip(parts[1::2], parts[2::2]):
        if title.strip().lower() in PLOT_HEADINGS:
            return body.strip()
    return None


def fetch_texts(articles, path, intro_only):
    """Article -> plot (films) or intro (people). The API gives full extracts one page at a time,
    intros 20 pages at a time."""
    done = cached(path)
    todo = sorted({a for a in articles.values() if a and a not in done})
    step = 20 if intro_only else 1
    for k in range(0, len(todo), step):
        chunk = todo[k:k + step]
        params = {"action": "query", "format": "json", "formatversion": 2, "prop": "extracts",
                  "explaintext": 1, "redirects": 1, "maxlag": 5, "titles": "|".join(chunk)}
        if intro_only:
            params.update(exintro=1, exlimit=20)
        else:
            params["exsectionformat"] = "wiki"
        res = get(API, params=params)["query"]
        # follow redirects/normalisation back to the name we asked for
        alias = {x["to"]: x["from"] for x in res.get("normalized", []) + res.get("redirects", [])}
        rows = []
        for page in res.get("pages", []):
            asked = alias.get(page["title"], page["title"])
            asked = alias.get(asked, asked)
            text = page.get("extract") or ""
            rows.append({"id": asked, "text": text if intro_only else plot_section(text),
                         "source_url": "https://en.wikipedia.org/wiki/" + quote(page["title"].replace(" ", "_")),
                         "retrieved_at": now()})
        append(path, rows)
        if (k // step) % 50 == 0:
            print(f"{'bios' if intro_only else 'plots'} {k + len(chunk)}/{len(todo)}", flush=True)
        time.sleep(0.2)


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    spark = get_spark("enrichment-wikipedia")
    films = [r.tconst for r in spark.read.parquet("data/enrichment/selected_films")
             .select("tconst").distinct().collect()]
    people = [r.nconst for r in spark.read.parquet("data/enrichment/selected_people")
              .select("nconst").distinct().collect()]
    film_articles = article_names(sorted(films), RAW / "film_articles.jsonl")
    people_articles = article_names(sorted(people), RAW / "people_articles.jsonl")
    fetch_texts(film_articles, RAW / "film_plots.jsonl", intro_only=False)
    fetch_texts(people_articles, RAW / "people_bios.jsonl", intro_only=True)


if __name__ == "__main__":
    main()
