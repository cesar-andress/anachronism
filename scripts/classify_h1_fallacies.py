#!/usr/bin/env python3
"""Apply H1 function labels and fallacy pattern flags (historical classify_tweets)."""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from anachonism.fallacies import detect_fallacies
from anachonism.label_functions import classify_function


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input)
    if "tweet" not in df.columns:
        raise SystemExit(f"Missing tweet column; got {list(df.columns)}")
    results = df["tweet"].apply(classify_function).apply(pd.Series)
    fallacy_results = df["tweet"].apply(detect_fallacies).apply(pd.Series)
    out = pd.concat([df, results, fallacy_results], axis=1)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False, encoding="utf-8")
    print(f"[OK] {len(out)} rows -> {args.output}")
    print(out["label_funcion"].value_counts())


if __name__ == "__main__":
    main()
