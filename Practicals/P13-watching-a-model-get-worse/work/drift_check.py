"""The weekly drift check, as a script you run from a terminal.

Compares a reference window against a current window and prints one row per
column, plus the dataset level share. Exit code 1 when the share crosses the
threshold, so a scheduler can treat it as a failed check.

    python drift_check.py                     reference against itself
    python drift_check.py --monsoon           corrupt rain and traffic
    python drift_check.py --monsoon --bar 0.4 a stricter threshold
"""
from __future__ import annotations

import argparse
import sys

import numpy as np
import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset

FEATURES = ["distance_km", "prep_time_min", "traffic_level", "rain"]


def orders(n: int, rain_p: float, traffic_hi: bool, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "distance_km":   rng.uniform(0.5, 12, n),
        "prep_time_min": rng.uniform(5, 30, n),
        "traffic_level": rng.choice([2, 3], n) if traffic_hi
                         else rng.choice([1, 2, 3], n),
        "rain":          rng.choice([0, 1], n, p=[1 - rain_p, rain_p]),
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--monsoon", action="store_true",
                        help="make the current window wetter and busier")
    parser.add_argument("--bar", type=float, default=0.5,
                        help="share of drifted columns that counts as drift")
    args = parser.parse_args()

    reference = orders(600, 0.20, False, seed=42)
    current = (orders(600, 0.75, True, seed=7) if args.monsoon
               else orders(600, 0.20, False, seed=7))

    result = Report(metrics=[DataDriftPreset()]).run(
        reference_data=reference, current_data=current)
    summary = result.dict()

    print(f"{'column':<16}{'test':<22}{'p value':>12}   verdict")
    share = None
    for metric in summary["metrics"]:
        config = metric.get("config", {})
        kind = config.get("type", "")
        if kind.endswith("DriftedColumnsCount"):
            share = float(metric["value"]["share"])
            continue
        if not kind.endswith("ValueDrift"):
            continue
        column = config.get("column", "?")
        test = config.get("method", "?")
        p_value = float(metric["value"])
        print(f"{column:<16}{test:<22}{p_value:>12.4g}   "
              f"{'DRIFTED' if p_value < 0.05 else 'not drifted'}")

    print(f"\nshare of drifted columns: {share}   bar: {args.bar}")
    if share is not None and share >= args.bar:
        print("verdict: DRIFT. Check the error before retraining; "
              "high drift with low error is not a reason to retrain.")
        return 1
    print("verdict: no dataset level drift. Read the rows anyway.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
