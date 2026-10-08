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

## AI / LLM usage declaration

- Claude (Anthropic) was used to generate the initial repository scaffolding
  (folder structure, Dockerfile, docker-compose, helper scripts) and may be used for code
  of later steps. This list will be updated for each step.
- No AI tool was used to write explanations or reasoning in REPORT.md.
