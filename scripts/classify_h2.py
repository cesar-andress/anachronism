#!/usr/bin/env python3
"""Apply H2 historical vs metaphorical/anachronistic labels (historical h2_analyze)."""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from anachonism.h2_semantics import classify_h2


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input)
    h2 = df["tweet"].apply(classify_h2).apply(pd.Series)
    out = pd.concat([df, h2], axis=1)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False, encoding="utf-8")
    print(f"[OK] {len(out)} rows -> {args.output}")
    print(out["h2_label"].value_counts())


if __name__ == "__main__":
    main()
