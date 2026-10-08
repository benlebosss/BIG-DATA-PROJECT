# IMDb Big Data Processing — ECE Fall 2026

Group project (PySpark + Apache Kafka) for the Adaltas Big Data Processing course.
Instructions: https://github.com/adaltas/ece-big-data-processing-fall-2026/blob/main/project_instructions.md

See [PROJECT.md](PROJECT.md) for setup/run instructions and [REPORT.md](REPORT.md) for results.
Git rules: [CONTRIBUTING.md](CONTRIBUTING.md).

## Layout

```
src/common/         shared helpers (Spark session)
src/preparation/    data quality & cleaning
src/exploration/    the 8 analytical questions
src/enrichment/     synopses & biographies
src/streaming/      Wikipedia -> Kafka -> Structured Streaming
src/open_question/  open question
scripts/            download & repo scripts
docker/             Dockerfile for the Spark/Python environment
```
