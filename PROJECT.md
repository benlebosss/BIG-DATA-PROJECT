# PROJECT

## Contributors

| Name | Email |
|------|-------|
| TODO | TODO  |
| TODO | TODO  |

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
  check the language coverage of `title.akas`. The interpretation of the results in REPORT.md
  is written by us.
- No AI tool was used to write explanations or reasoning in REPORT.md.
