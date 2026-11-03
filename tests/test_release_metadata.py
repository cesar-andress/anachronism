"""Gates that must pass before tagging a GitHub/Zenodo release."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_release_metadata_gate():
    script = ROOT / "scripts" / "check_release_metadata.py"
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "Release metadata OK" in proc.stdout


def test_citation_cff_rejects_notes_regression(tmp_path: Path):
    """Guard the exact defect that broke Zenodo v1.0.0 ingestion."""
    import yaml
    from cffconvert.citation import Citation

    raw = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    data["notes"] = "this must never be allowed"
    bad = tmp_path / "CITATION.cff"
    bad.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    try:
        Citation(bad.read_text(encoding="utf-8")).validate()
        raised = False
    except Exception:
        raised = True
    assert raised, "invalid CFF key 'notes' must fail validation"
