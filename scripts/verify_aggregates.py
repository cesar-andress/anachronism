#!/usr/bin/env python3
"""Compare a fully labelled CSV against locked expected aggregates."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

TABLE3_TYPES = [
    "AD_ODIUM",
    "AD_HOMINEM",
    "AD_POPULUM",
    "AD_CONSEQUENTIAM",
    "AD_ANTIQUITATEM",
    "AD_NAUSEAM",
    "AD_NUMERUM",
    "AD_PERSONAM",
    "AD_VERECUNDIAM",
]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--labelled", type=Path, required=True, help="CSV with H1/H2/H3/AD_*")
    p.add_argument("--expected", type=Path, required=True)
    args = p.parse_args()
    exp = json.loads(args.expected.read_text(encoding="utf-8"))
    df = pd.read_csv(args.labelled)
    errors = []
    if len(df) != exp["analytical_rows"]:
        errors.append(f"rows {len(df)} != {exp['analytical_rows']}")
    for lab, n in exp["h1"].items():
        got = int((df["label_funcion"] == lab).sum())
        if got != n:
            errors.append(f"h1 {lab}: {got} != {n}")
    for lab, n in exp["h2"].items():
        got = int((df["h2_label"] == lab).sum())
        if got != n:
            errors.append(f"h2 {lab}: {got} != {n}")
    for lab, n in exp["h3"].items():
        got = int((df["h3_label"] == lab).sum())
        if got != n:
            errors.append(f"h3 {lab}: {got} != {n}")
    ad_all = [c for c in df.columns if c.startswith("AD_")]
    hits = int(df[ad_all].fillna(False).astype(bool).sum().sum())
    if hits != exp["fallacy_multilabel_hits"]:
        errors.append(f"fallacy hits {hits} != {exp['fallacy_multilabel_hits']}")
    distinct = int(df["has_fallacy"].sum()) if "has_fallacy" in df.columns else int(
        (df[ad_all].fillna(False).astype(bool).sum(axis=1) > 0).sum()
    )
    if distinct != exp["fallacy_distinct_tweets"]:
        errors.append(f"fallacy tweets {distinct} != {exp['fallacy_distinct_tweets']}")
    # Table 2 party×h2
    party_map = {k.casefold(): k for k in exp["party_totals"]}
    for party, total in exp["party_totals"].items():
        sub = df[df["partido"].astype(str).str.casefold() == party.casefold()]
        if len(sub) != total:
            errors.append(f"party {party} n={len(sub)} != {total}")
    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("PASS: aggregates match locked expected values")
    print("note: Table3 types used in manuscript:", ", ".join(TABLE3_TYPES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
