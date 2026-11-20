"""The delivery pipeline, as a script you run from a terminal.

The notebook builds this up step by step. This file is the finished thing,
so you can run the whole line with one command and watch it refuse to
continue when a stage fails.

    python pipeline.py              run every stage
    python pipeline.py --fail clean make the clean stage fail on purpose
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

FEATURES = ["distance_km", "prep_time_min", "traffic_level", "rain"]
TARGET = "delivery_min"


def find_data(name: str = "delivery_times.csv") -> Path:
    """Locate the shared dataset by walking upward from here."""
    here = Path.cwd().resolve()
    for folder in [here, *here.parents]:
        for candidate in (folder / "data" / name,
                          folder / "Practicals" / "data" / name):
            if candidate.exists():
                return candidate.resolve()
    raise FileNotFoundError(f"{name} not found at or above {here}")


def load() -> pd.DataFrame:
    frame = pd.read_csv(find_data())
    return frame


def clean(frame: pd.DataFrame) -> pd.DataFrame:
    """Drop rows that cannot be true. A delivery cannot take zero minutes."""
    before = len(frame)
    frame = frame[(frame[TARGET] > 0) & (frame["distance_km"] > 0)]
    print(f"   dropped {before - len(frame)} impossible rows")
    return frame


def train(frame: pd.DataFrame) -> float:
    train_rows, test_rows = train_test_split(frame, test_size=0.2,
                                             random_state=42)
    model = LinearRegression().fit(train_rows[FEATURES], train_rows[TARGET])
    mae = mean_absolute_error(test_rows[TARGET], model.predict(test_rows[FEATURES]))
    return float(mae)


def report(mae: float) -> None:
    Path("daily_report.txt").write_text(
        f"delivery time model\nMAE on held out orders: {mae:.2f} minutes\n")
    print(f"   wrote daily_report.txt, MAE {mae:.2f} minutes")


STAGES = ["load", "clean", "train", "report"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fail", choices=STAGES, default=None,
                        help="make this stage fail, to prove the line stops")
    args = parser.parse_args()

    frame, mae = None, None
    for stage in STAGES:
        print(f"-> {stage}")
        if stage == args.fail:
            print(f"   {stage} failed on purpose")
            print(f"\nthe line stopped at {stage}; "
                  f"{', '.join(STAGES[STAGES.index(stage) + 1:]) or 'nothing'} "
                  "never ran")
            return 1
        if stage == "load":
            frame = load()
            print(f"   loaded {len(frame)} orders")
        elif stage == "clean":
            frame = clean(frame)
        elif stage == "train":
            mae = train(frame)
            print(f"   trained, MAE {mae:.2f} minutes")
        elif stage == "report":
            report(mae)

    print("\nevery stage finished")
    return 0


if __name__ == "__main__":
    sys.exit(main())
