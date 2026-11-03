#!/usr/bin/env python3
"""Filter raw Spanish-politicians tweet CSV by ideology substrings (historical offline_main)."""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from anachonism.datasets import load_spanish_politicians


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--terms-file", type=Path, required=True, help="One term per line")
    p.add_argument("--raw", type=Path, required=True, help="Raw TSV/CSV path")
    p.add_argument("--out", type=Path, required=True, help="Filtered CSV output")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    terms = [
        t.strip().casefold()
        for t in args.terms_file.read_text(encoding="utf-8").splitlines()
        if t.strip() and not t.strip().startswith("#")
    ]
    df = load_spanish_politicians(str(args.raw))
    if "tweet" not in df.columns:
        raise SystemExit(f"Missing tweet column; got {list(df.columns)}")
    df = df.copy()
    df["tweet_str"] = df["tweet"].fillna("").astype(str)
    df["tweet_lower"] = df["tweet_str"].str.casefold()
    mask = pd.Series(False, index=df.index)
    for term in terms:
        mask |= df["tweet_lower"].str.contains(term, na=False, regex=False)
    out = df.loc[mask].copy()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, index=False, encoding="utf-8")
    print(f"[OK] {len(out)} rows -> {args.out}")


if __name__ == "__main__":
    main()
