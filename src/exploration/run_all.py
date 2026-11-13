"""Run every exploration question and write the CSV results to ``results/exploration/``.

Usage: python -m src.exploration.run_all [--only q1 q4 ...]
"""
import argparse
import time

from src.exploration import (
    q1_runtime_outliers,
    q2_top_genres,
    q4_one_hit_directors,
    q5_series_decline,
    q6_multilingual_actors,
    q7_early_peak_actors,
    q8_multi_talented,
)

QUESTIONS = {
    "q1": q1_runtime_outliers.main,
    "q2": q2_top_genres.main,  # also answers Q3
    "q4": q4_one_hit_directors.main,
    "q5": q5_series_decline.main,
    "q6": q6_multilingual_actors.main,
    "q7": q7_early_peak_actors.main,
    "q8": q8_multi_talented.main,
}


def main(only: list = None) -> None:
    for key, run in QUESTIONS.items():
        if only and key not in only:
            continue
        start = time.time()
        run()
        print(f"[timing] {key}: {time.time() - start:.0f}s", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", choices=list(QUESTIONS))
    main(ap.parse_args().only)
