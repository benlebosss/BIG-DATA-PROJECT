#!/usr/bin/env bash
# Runs the data-quality checks one JVM per check (low memory), then merges the results.
set -euo pipefail
i=0
while true; do
  out=$(SPARK_DRIVER_MEMORY="${SPARK_DRIVER_MEMORY:-3g}" python -m src.preparation.profile_quality --only-issue "$i" 2>&1 | grep -E "^\[(issue|done)\]" || true)
  echo "$out"
  case "$out" in *"[done]"*) break;; esac
  i=$((i+1))
done
python -m src.preparation.profile_quality --merge
