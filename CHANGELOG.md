# Changelog

## 1.0.2 — 2026-11-03

- Record verified Zenodo identifiers after successful v1.0.1 archival:
  concept DOI `10.5281/zenodo.23930970`, version DOI `10.5281/zenodo.23930971`.
- Mirror the Zenodo deposit license (CC-BY-4.0) in `CITATION.cff` / `.zenodo.json`.
- Add hard release-metadata gate (`scripts/check_release_metadata.py`) and CI
  workflow so invalid `CITATION.cff` / `.zenodo.json` cannot ship unnoticed.
- Sync versions across package, CFF, Zenodo JSON, and `pyproject.toml`.
- Remove absolute private machine paths from public docs.
- Harden `.gitignore` against manuscript and dump formats.
- Document the release checklist in `docs/RELEASING.md`.
- Keep Git tag `v1.0.1` immutable (it matches the Zenodo source archive).

## 1.0.1 — 2026-11-03

- Fix Zenodo/GitHub archival metadata: remove invalid `CITATION.cff` field `notes`
  (CFF schema rejection) and drop unsupported `license: NOASSERTION`.
- Set package/citation version to 1.0.1.
- Add `.zenodo.json` with creators, software upload type, and scientific
  qualifications (heuristic indicators only; not independently validated
  fallacy/anachronism/vacuity detection).

## 1.0.0 — 2026-11-03

- First public Git tag of the research software reproduction package
  (rules, scripts, tests, aggregate targets, synthetic examples).
- Zenodo ingestion of the GitHub Release failed due to invalid `CITATION.cff`.
