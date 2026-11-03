"""Optional full reproduction against a local raw corpus.

Set environment variable ANACHONISM_RAW_TSV to the absolute path of
`tweets_politica_kaggle.csv` (not redistributed here). Skips otherwise.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = json.loads((ROOT / "config/expected_aggregates.json").read_text(encoding="utf-8"))


@pytest.mark.skipif(
    not os.environ.get("ANACHONISM_RAW_TSV"),
    reason="ANACHONISM_RAW_TSV not set; public package cannot ship raw tweets",
)
def test_full_pipeline_matches_locked_aggregates(tmp_path: Path):
    raw = Path(os.environ["ANACHONISM_RAW_TSV"])
    assert raw.exists()
    digest = hashlib.sha256(raw.read_bytes()).hexdigest()
    assert digest == EXPECTED["raw_sha256"]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")
    filtrados = tmp_path / "filtrados.csv"
    clas = tmp_path / "clas.csv"
    h2 = tmp_path / "h2.csv"
    h3 = tmp_path / "h3.csv"

    def run(cmd: list[str]) -> None:
        subprocess.check_call(cmd, cwd=ROOT, env=env)

    run(
        [
            sys.executable,
            "scripts/filter_terms.py",
            "--terms-file",
            "config/filter_terms_33.txt",
            "--raw",
            str(raw),
            "--out",
            str(filtrados),
        ]
    )
    run([sys.executable, "scripts/classify_h1_fallacies.py", "--input", str(filtrados), "--output", str(clas)])
    run([sys.executable, "scripts/classify_h2.py", "--input", str(clas), "--output", str(h2)])
    run([sys.executable, "scripts/classify_h3.py", "--input", str(h2), "--output", str(h3)])
    subprocess.check_call(
        [
            sys.executable,
            "scripts/verify_aggregates.py",
            "--labelled",
            str(h3),
            "--expected",
            "config/expected_aggregates.json",
        ],
        cwd=ROOT,
        env=env,
    )
