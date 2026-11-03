# Changelog

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
