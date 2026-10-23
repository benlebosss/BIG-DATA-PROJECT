"""Step 6a: Wikipedia recent changes (Wikimedia EventStreams) -> Kafka topic.

Usage (from the repo root, with Kafka running):
    python -m src.streaming.wikipedia_producer                      # enwiki articles -> Kafka
    python -m src.streaming.wikipedia_producer --dry-run --max-events 5   # print only, no Kafka
"""
import argparse
import json
import logging
import os
import time
from typing import Iterable, Iterator, Optional, Tuple

import requests

STREAM_URL = "https://stream.wikimedia.org/v2/stream/recentchange"
USER_AGENT = "ece-bigdata-student-project (https://github.com/benlebosss/BIG-DATA-PROJECT)"
TOPIC = "wikipedia-changes"
KEPT_TYPES = {"edit", "new"}

log = logging.getLogger("wikipedia_producer")


def parse_event(data: str, wikis: Optional[set] = None, namespaces: Optional[set] = None) -> Optional[dict]:
    """Turn one raw EventStreams JSON payload into the flat message described in schema.py.

    Returns None for events we do not want (not an edit, wrong wiki/namespace, malformed).
    """
    try:
        obj = json.loads(data)
    except (TypeError, ValueError):
        return None
    if not isinstance(obj, dict) or obj.get("type") not in KEPT_TYPES:
        return None
    if wikis and obj.get("wiki") not in wikis:
        return None
    if namespaces is not None and obj.get("namespace") not in namespaces:
        return None
    if not obj.get("title"):
        return None
    meta = obj.get("meta") or {}
    return {
        "event_id": meta.get("id"),
        "wiki": obj.get("wiki"),
        "title": obj["title"],
        "type": obj["type"],
        "namespace": obj.get("namespace"),
        "user": obj.get("user"),
        "bot": bool(obj.get("bot")),
        "comment": obj.get("comment") or "",
        "timestamp": obj.get("timestamp"),
        "event_time": meta.get("dt"),
        "server_name": obj.get("server_name"),
        "url": obj.get("notify_url"),
    }


def iter_sse(lines: Iterable[str]) -> Iterator[Tuple[Optional[str], str]]:
    """Yield (last_event_id, data) for every Server-Sent Event found in ``lines``."""
    event_id = None
    for line in lines:
        if line.startswith("id:"):
            event_id = line[3:].strip()
        elif line.startswith("data:"):
            yield event_id, line[5:].strip()


def stream_changes(url: str = STREAM_URL) -> Iterator[str]:
    """Yield raw JSON payloads forever, reconnecting with exponential backoff."""
    last_id, delay = None, 1
    while True:
        headers = {"User-Agent": USER_AGENT, "Accept": "text/event-stream"}
        if last_id:
            headers["Last-Event-ID"] = last_id
        try:
            with requests.get(url, headers=headers, stream=True, timeout=(10, 60)) as resp:
                resp.raise_for_status()
                delay = 1
                lines = (raw.decode("utf-8") for raw in resp.iter_lines() if raw)
                for event_id, data in iter_sse(lines):
                    last_id = event_id or last_id
                    yield data
        except requests.RequestException as exc:
            log.warning("stream interrupted (%s), reconnecting in %ss", exc, delay)
        time.sleep(delay)
        delay = min(delay * 2, 60)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--bootstrap", default=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"))
    ap.add_argument("--topic", default=TOPIC)
    ap.add_argument("--wikis", default="enwiki", help="comma-separated, empty = all wikis")
    ap.add_argument("--namespaces", default="0", help="comma-separated, empty = all namespaces")
    ap.add_argument("--max-events", type=int, default=None, help="stop after N messages (smoke tests)")
    ap.add_argument("--dry-run", action="store_true", help="print messages instead of sending to Kafka")
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    wikis = {w for w in a.wikis.split(",") if w} or None
    namespaces = {int(n) for n in a.namespaces.split(",") if n} if a.namespaces else None

    producer = None
    if not a.dry_run:
        from kafka import KafkaProducer  # imported here so tests/dry-run need no Kafka client
        producer = KafkaProducer(
            bootstrap_servers=a.bootstrap,
            key_serializer=lambda k: k.encode("utf-8"),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            linger_ms=200,
        )

    sent = 0
    for data in stream_changes():
        msg = parse_event(data, wikis, namespaces)
        if msg is None:
            continue
        if producer:
            producer.send(a.topic, key=msg["title"], value=msg)
        else:
            print(json.dumps(msg, ensure_ascii=False))
        sent += 1
        if sent % 100 == 0:
            log.info("%d messages sent", sent)
        if a.max_events and sent >= a.max_events:
            break
    if producer:
        producer.flush()


if __name__ == "__main__":
    main()
