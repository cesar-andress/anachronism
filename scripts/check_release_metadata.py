#!/usr/bin/env python3
"""Pre-release gate for Zenodo/GitHub archival metadata.

Fails hard on the classes of defect that previously blocked Zenodo ingestion
(invalid CITATION.cff keys, NOASSERTION license, version drift, private paths).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Top-level Citation File Format 1.2.0 keys we allow in this repository.
# Unknown keys (e.g. former invalid ``notes``) must fail the gate.
ALLOWED_CFF_TOP_LEVEL = frozenset(
    {
        "abstract",
        "authors",
        "cff-version",
        "commit",
        "contact",
        "date-released",
        "doi",
        "identifiers",
        "keywords",
        "license",
        "license-url",
        "message",
        "preferred-citation",
        "references",
        "repository",
        "repository-artifact",
        "repository-code",
        "title",
        "type",
        "url",
        "version",
    }
)

FORBIDDEN_LICENSE_VALUES = frozenset(
    {
        "NOASSERTION",
        "NONE",
        "NOTASSERTED",
        "UNLICENSED",
    }
)

# Build without embedding contiguous absolute prefixes in this file's text,
# so the gate does not flag its own source.
PRIVATE_PATH_RE = re.compile(
    r"(?:"
    + re.escape("/" + "home" + "/")
    + r"[A-Za-z0-9._-]+"
    + r"|"
    + re.escape("/" + "Users" + "/")
    + r"[A-Za-z0-9._-]+"
    + r"|"
    + re.escape("C:\\" + "Users" + "\\")
    + r"[A-Za-z0-9._-]+"
    + r"|"
    + re.escape("/" + "root" + "/")
    + r")",
    re.IGNORECASE,
)

TRACKED_TEXT_GLOBS = (
    "*.md",
    "*.toml",
    "*.json",
    "*.cff",
    "*.py",
    "*.txt",
    "*.yml",
    "*.yaml",
    ".gitignore",
)


def _load_yaml(path: Path) -> dict:
    try:
        import yaml  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "PyYAML is required for CITATION.cff checks. "
            "Install with: pip install pyyaml cffconvert"
        ) from exc
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: expected a YAML mapping at top level")
    return data


def _read_pyproject_version(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r'(?m)^version\s*=\s*"([^"]+)"', text)
    if not match:
        raise SystemExit(f"{path}: could not find project version")
    return match.group(1)


def _read_package_version(path: Path) -> str | None:
    if not path.is_file():
        return None
    match = re.search(
        r'(?m)^__version__\s*=\s*"([^"]+)"',
        path.read_text(encoding="utf-8"),
    )
    return match.group(1) if match else None


def check_citation_cff() -> str:
    path = ROOT / "CITATION.cff"
    if not path.is_file():
        raise SystemExit("CITATION.cff is missing")
    data = _load_yaml(path)

    unknown = sorted(set(data) - ALLOWED_CFF_TOP_LEVEL)
    if unknown:
        raise SystemExit(
            "CITATION.cff has unsupported top-level keys "
            f"(Zenodo/cffconvert reject these): {unknown}"
        )

    for required in ("cff-version", "message", "title", "authors", "version"):
        if required not in data:
            raise SystemExit(f"CITATION.cff missing required field: {required}")

    if data.get("type") not in (None, "software", "dataset"):
        raise SystemExit(f"CITATION.cff unexpected type: {data.get('type')!r}")

    license_value = data.get("license")
    if license_value is not None:
        if isinstance(license_value, list):
            raise SystemExit(
                "CITATION.cff license must be a single string for Zenodo "
                f"(arrays fail ingestion); got {license_value!r}"
            )
        if str(license_value).upper() in FORBIDDEN_LICENSE_VALUES:
            raise SystemExit(
                f"CITATION.cff license {license_value!r} is forbidden; "
                "omit license until an SPDX id is authorized, or set a real SPDX id"
            )

    try:
        from cffconvert.citation import Citation
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "cffconvert is required. Install with: pip install cffconvert"
        ) from exc

    Citation(path.read_text(encoding="utf-8")).validate()

    doi = data.get("doi")
    if doi is not None:
        if not str(doi).startswith("10."):
            raise SystemExit(f"CITATION.cff doi looks invalid: {doi!r}")

    return str(data["version"])


def check_zenodo_json() -> str:
    path = ROOT / ".zenodo.json"
    if not path.is_file():
        raise SystemExit(
            ".zenodo.json is missing; Zenodo GitHub integration should use an "
            "explicit software deposit metadata file in this repository"
        )
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f".zenodo.json is not valid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise SystemExit(".zenodo.json must be a JSON object")

    for required in ("title", "version", "upload_type", "description", "creators"):
        if required not in data or data[required] in (None, "", []):
            raise SystemExit(f".zenodo.json missing required field: {required}")

    if data["upload_type"] != "software":
        raise SystemExit(
            f".zenodo.json upload_type must be 'software', got {data['upload_type']!r}"
        )

    creators = data["creators"]
    if not isinstance(creators, list) or not creators:
        raise SystemExit(".zenodo.json creators must be a non-empty list")
    for idx, creator in enumerate(creators):
        if not isinstance(creator, dict) or "name" not in creator:
            raise SystemExit(f".zenodo.json creators[{idx}] must include name")
        orcid = creator.get("orcid")
        if orcid is not None and (
            orcid.startswith("http") or not re.fullmatch(r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]", orcid)
        ):
            raise SystemExit(
                f".zenodo.json creators[{idx}].orcid must be bare ORCID id, got {orcid!r}"
            )

    license_value = data.get("license")
    if license_value is not None:
        if not isinstance(license_value, str):
            raise SystemExit(".zenodo.json license must be a string SPDX/Zenodo id")
        if license_value.upper() in FORBIDDEN_LICENSE_VALUES:
            raise SystemExit(f".zenodo.json license {license_value!r} is forbidden")

    # Prefer ASCII hyphen in titles for archival metadata robustness.
    title = str(data["title"])
    if "\u2014" in title or "---" in title:
        raise SystemExit(
            ".zenodo.json title must not contain em-dash characters; "
            "use ASCII hyphen or en-dash"
        )

    return str(data["version"])


def check_version_consistency(cff_version: str, zenodo_version: str) -> None:
    pyproject_version = _read_pyproject_version(ROOT / "pyproject.toml")
    package_version = _read_package_version(ROOT / "src" / "anachonism" / "__init__.py")

    versions = {
        "CITATION.cff": cff_version,
        ".zenodo.json": zenodo_version,
        "pyproject.toml": pyproject_version,
    }
    if package_version is not None:
        versions["src/anachonism/__init__.py __version__"] = package_version

    unique = set(versions.values())
    if len(unique) != 1:
        raise SystemExit(f"Version mismatch across release metadata: {versions}")

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    heading = f"## {cff_version} "
    if heading not in changelog and f"## {cff_version}\n" not in changelog:
        # Allow en-dash/em-dash/hyphen variants after version.
        if not re.search(rf"(?m)^## {re.escape(cff_version)}\b", changelog):
            raise SystemExit(
                f"CHANGELOG.md has no section heading for version {cff_version}"
            )


def check_no_private_machine_paths() -> None:
    offenders: list[str] = []
    for pattern in TRACKED_TEXT_GLOBS:
        for path in ROOT.rglob(pattern):
            if any(part in {".git", ".venv", "__pycache__", ".pytest_cache"} for part in path.parts):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if PRIVATE_PATH_RE.search(text):
                offenders.append(str(path.relative_to(ROOT)))
    if offenders:
        raise SystemExit(
            "Tracked files contain absolute private machine paths "
            f"(forbidden in the public artifact): {offenders}"
        )


def check_no_forbidden_publication_files() -> None:
    forbidden_suffixes = (
        ".tex",
        ".bib",
        ".bbl",
        ".aux",
        ".docx",
        ".doc",
        ".odt",
    )
    forbidden_names = {
        "AGENTS.md",
        "CLAUDE.md",
        ".env",
    }
    hits: list[str] = []
    for path in ROOT.rglob("*"):
        if any(part in {".git", ".venv", "__pycache__", ".pytest_cache"} for part in path.parts):
            continue
        if not path.is_file():
            continue
        rel = str(path.relative_to(ROOT))
        if path.name in forbidden_names or path.suffix.lower() in forbidden_suffixes:
            hits.append(rel)
        if rel.startswith(".cursor/") or rel.startswith(".claude/"):
            hits.append(rel)
    if hits:
        raise SystemExit(f"Forbidden publication files present: {hits}")


def main() -> int:
    cff_version = check_citation_cff()
    zenodo_version = check_zenodo_json()
    check_version_consistency(cff_version, zenodo_version)
    check_no_private_machine_paths()
    check_no_forbidden_publication_files()
    print(f"Release metadata OK (version {cff_version})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
