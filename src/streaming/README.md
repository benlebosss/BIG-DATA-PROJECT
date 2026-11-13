# Streaming: Wikipedia -> Kafka -> Structured Streaming

## Producer (this PR)
`python -m src.streaming.wikipedia_producer --wikis enwiki --namespaces 0`

Reads the Wikimedia EventStreams `recentchange` SSE feed, keeps `edit`/`new` events,
flattens them and publishes JSON to Kafka topic `wikipedia-changes` (key = page title).
Options: `--bootstrap` (env KAFKA_BOOTSTRAP_SERVERS, default localhost:9092), `--topic`,
`--wikis`, `--namespaces`, `--max-events`, `--dry-run` (print instead of publishing).
Auto-reconnects with Last-Event-ID and exponential backoff.

## Topic contract (for the consumer job)
Value = JSON matching `CHANGE_SCHEMA` in `src/streaming/schema.py`:
event_id, wiki, title, type, namespace, user, bot, comment,
timestamp (epoch seconds), event_time (ISO string), server_name, url.
Use `event_time` as the event-time column with a watermark for late data.

## Next (consumer, to do)
Read the topic with `get_spark(app_name, with_kafka=True)`, `from_json(value, CHANGE_SCHEMA)`,
match `title` against IMDb titles/names, and flag matches over a 15-30 min window with a watermark.

## Local test
    docker compose up -d kafka
    python -m src.streaming.wikipedia_producer --max-events 20

## Message example

    {"event_id": "...", "wiki": "enwiki", "title": "Inception (film)", "type": "edit", "namespace": 0, "user": "...", "bot": false, "timestamp": 1790000000, "event_time": "2026-10-23T16:00:00Z"}

## Filters

Only edit and new events are kept. By default only enwiki and namespace 0 (articles) pass, which removes talk pages, users pages and categories.
