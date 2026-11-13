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

## Consumer (Structured Streaming)
1. `python -m src.streaming.reference` builds `data/parquet/streaming_reference`: popular IMDb titles
   and people (actors/directors of popular titles), keyed by lower-cased name without a trailing `(...)`.
2. `python -m src.streaming.consumer --source kafka` reads the topic, parses JSON, joins each page title
   with the reference (stream-static broadcast join) and counts matches in sliding windows
   (`--window 30 minutes --slide 5 minutes`). A window with at least `--min-matches` matches is `flagged`.
3. Late data: `--watermark 10 minutes` on `event_time`. State of a window is kept until the watermark
   passes its end; events older than the watermark are dropped from the aggregation.
4. No Kafka at hand: `--source files --input-dir DIR` reads JSON-lines files instead (same pipeline).
   `--out results/streaming` writes parquet instead of printing to the console.

## Local test
    docker compose up -d kafka
    python -m src.streaming.wikipedia_producer --max-events 20
