# PROJECT

## Contributors

| Name | Email |
|------|-------|
| Benoit (GitHub: benlebosss) | benoitquaranta030405@gmail.com |
| Théodore Bricout (GitHub: TheodoreBricout) | TODO (Théo to fill in) |

## Setup (from scratch)

```bash
git clone <repo-url> && cd <repo>
docker compose up -d --build        # Kafka + Python/Spark container
./scripts/download_imdb.sh          # IMDb datasets into data/imdb/
docker compose exec app bash        # shell inside the Spark container
```

Run each module from inside the container, e.g. `python -m src.preparation.<script>`
(to be completed as steps are implemented).

### Data exploration

Requires the Parquet tables (`python -m src.preparation.to_parquet`); the cleaned tables of
`src.preparation.clean` are used automatically when `data/clean/` exists.

```bash
python -m src.exploration.wikidata_language  # original language of the movies (Q6), ~1 min, needs internet
python -m src.exploration.run_all            # all questions, CSV files in results/exploration/
python -m src.exploration.run_all --only q4  # a single question (q1, q2 (= Q2 + Q3), q4 ... q8)
python -m pytest -q tests/test_exploration.py
```

Each question is also a module with its own parameters, e.g.
`python -m src.exploration.q1_runtime_outliers --z 3` or
`python -m src.exploration.q6_multilingual_actors --min-rating 7 --min-votes 10000`.

## AI / LLM usage declaration

- Claude (Anthropic) was used to generate the initial repository scaffolding
  (folder structure, Dockerfile, docker-compose, helper scripts) and may be used for code
  of later steps. This list will be updated for each step.
- Data exploration (`src/exploration/`, `tests/test_exploration.py`): Claude (Anthropic, Claude Code)
  was used to write the PySpark code of the eight questions and their unit tests, and to
  check the language coverage of `title.akas`, and for the Wikidata gatherer of the original
  languages (`src/exploration/wikidata_language.py`). The language data itself comes from
  Wikidata (human-curated, CC0), never from an AI tool. The interpretation of the results in REPORT.md
  is written by us.
- No AI tool was used to write explanations or reasoning in REPORT.md.
- Data preparation (`src/preparation/`, `tests/test_preparation.py`): Claude (Anthropic, Claude Code) was used to write the profiling, cleaning and Parquet-conversion code and its tests. The cleaning choices and their explanation in REPORT.md are ours.
- Streaming (`src/streaming/`, `tests/test_streaming_*.py`): Claude (Anthropic, Claude Code) was used to write the Wikipedia -> Kafka producer, the IMDb lookup builder and the Structured Streaming consumer (join, windows, watermark) with their tests. The explanation of late-data handling in REPORT.md is written by us.
- Enrichment (`src/enrichment/`, `tests/test_enrichment.py`): Claude (Anthropic, Claude Code) was used to write the Wikipedia lookup code (rate limiting, retries, lineage columns) and its tests. The data comes from Wikipedia, never from an AI tool.
- REPORT.md is written by hand by the two contributors, without AI.

## Requirements

PySpark 3.5 needs Java 17. The Docker image provides Java 17 and Python 3.11. Outside Docker, export JAVA_HOME to a Java 17 install before running Spark.

## Run the tests

    python -m pytest -q

Spark tests start a local session and take a few seconds each.

## Pipeline order

    python -m src.preparation.to_parquet
    ./scripts/run_quality_checks.sh
    python -m src.preparation.clean
    python -m src.exploration.run_all
    python -m src.enrichment.wikipedia
    python -m src.streaming.reference
    python -m src.open_question.duos_by_period

## Streaming run

Start Kafka with docker compose up -d kafka, then run the producer (python -m src.streaming.wikipedia_producer) and the consumer (python -m src.streaming.consumer) in two terminals. Details in src/streaming/README.md.
