# anachonism

Minimal reproducible **rule-based** analysis package for a computational-discursive study of
Spanish party communication on Twitter/X using Political Science–related ideology terms.

This repository is the intended public software artifact for the academic salvage project
`anachonism`. It does **not** contain the manuscript, private audits, Odoo application, or
PostgreSQL dumps.

## Research purpose

The software measures **transparent heuristic indicators** on tweets that contain at least one of
33 documented ideology-related substrings:

- **H1** pragmatic-function patterns (`EVALUATIVO` / `DEFINICIONAL` / `MIXTO` / `OTRO`)
- **H2** historical vs metaphorical/anachronistic cues
- **H3** surface density / vacuity markers
- Informal-fallacy **lexical pattern** flags (`AD_*`)

## Relationship to the academic manuscript

The locked empirical results of the manuscript (raw N = 245,790; analytical N = 13,557;
Tables 2–3; 771 multi-label fallacy hits; 740 distinct tweets with ≥1 hit; `H3_VACIO` = 129)
were produced by the historical offline Python pipeline (see `docs/SOURCE_MAPPING.md`).

A later Odoo module (`tweet_test_battery`) reuses the **same rule source files** byte-for-byte,
but the PostgreSQL database `investigacion` currently stores **different** corpus runs and
**zero** human annotations. Those DB aggregates are **not** the manuscript tables.

## What this software does NOT validate

Outputs are **operational pattern labels**, not independently validated determinations of:

- rhetorical fallacies;
- discursive/conceptual anachronisms;
- semantic vacuity as a rhetorical construct.

No gold-standard human validation for these constructs is included in this artifact.

## Dataset provenance

- Public source referenced in historical methods notes:
  [OpenDataBay dataset](https://www.opendatabay.com/data/web-social/b44efd3f-e67d-4fe8-b11e-707c659dfa85)
- Local authoritative raw file used in verification (not redistributed here):
  `tweets_politica_kaggle.csv` (245,790 rows; SHA-256
  `755b8334e770a43bff2ae7e2edaa37c7ce9c459f683ca62e976114ea5f29835a`; coverage
  2013-03-22 to 2023-03-23).
- Filter terms: `config/filter_terms_33.txt` (33 terms).

**Redistribution:** raw tweet text is **not** shipped. Obtain the upstream dataset yourself and
respect Twitter/X and dataset license/terms. This package ships only synthetic examples plus
aggregate targets.

## Software requirements

- Python ≥ 3.10
- `pandas` ≥ 2.0

## Installation

```bash
cd anachonism
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Reproduction commands

### Smoke tests (no private data)

```bash
pytest -q tests/test_rules_smoke.py
```

### Full numerical reproduction (local raw TSV required)

```bash
export ANACHONISM_RAW_TSV=/absolute/path/to/tweets_politica_kaggle.csv
pytest -q tests/test_optional_full_reproduction.py
```

Or run the pipeline manually:

```bash
export PYTHONPATH=src
python scripts/filter_terms.py \
  --terms-file config/filter_terms_33.txt \
  --raw "$ANACHONISM_RAW_TSV" \
  --out /tmp/tweets_filtrados.csv
python scripts/classify_h1_fallacies.py --input /tmp/tweets_filtrados.csv --output /tmp/tweets_clasificados.csv
python scripts/classify_h2.py --input /tmp/tweets_clasificados.csv --output /tmp/tweets_h2.csv
python scripts/classify_h3.py --input /tmp/tweets_h2.csv --output /tmp/tweets_h3.csv
python scripts/verify_aggregates.py \
  --labelled /tmp/tweets_h3.csv \
  --expected config/expected_aggregates.json
```

## Expected verified outputs

See `config/expected_aggregates.json` (locked salvage numbers):

- raw rows: 245,790
- analytical rows: 13,557
- fallacy multi-label hits: 771
- distinct tweets with ≥1 fallacy hit: 740
- `H3_VACIO`: 129 (~0.95%)
- Table 2 party×H2 cells as documented in the JSON file

## Known limitations

- Heuristic / regex rules; high false-positive/negative risk for complex constructs.
- Public clone alone supports **partial** reproduction (rules + synthetic smoke tests).
- Full aggregate verification requires the raw corpus under local custody.
- Zenodo deposit v1.0.1 is archived under CC-BY-4.0; see `docs/LICENSE_DECISION.md`.
- Prefer the concept DOI for general citation and the version DOI for the exact archive.

## Data availability and restrictions

| Asset | In this repo? | Notes |
|-------|---------------|-------|
| Rule source modules | Yes | Transparent heuristics |
| 33 filter terms | Yes | Documented list |
| Expected aggregates | Yes | No tweet text |
| Synthetic examples | Yes | Non-empirical |
| Raw / filtered tweet CSVs | No | Obtain upstream; privacy/ToS |
| Odoo / PostgreSQL dumps | No | Private research infra |
| Manuscript / audits | No | Stay in private salvage tree |

## Zenodo archival status

| Identifier | Value | Use |
|------------|-------|-----|
| **Authoritative version DOI (v1.0.2)** | [10.5281/zenodo.23931188](https://doi.org/10.5281/zenodo.23931188) | **Cite this software release** |
| GitHub Release | https://github.com/cesar-andress/anachronism/releases/tag/v1.0.2 | Source tag matching the archive |
| Zenodo record | https://zenodo.org/records/23931188 | Landing page for v1.0.2 |

Do not cite earlier Zenodo version DOIs for this project in place of `10.5281/zenodo.23931188`.

## Citation

See `CITATION.cff`. Example:

```
Pinto Pajares, D., Andrés, C., & Baena Rojas, J. J. (2026).
Anachronism - Research Software (Version 1.0.2).
Zenodo. https://doi.org/10.5281/zenodo.23931188
```

## Release hygiene

Before any tag or GitHub Release, run the metadata gate (also enforced in CI):

```bash
pip install -e ".[dev]"
pytest -q tests/test_rules_smoke.py tests/test_release_metadata.py
python scripts/check_release_metadata.py
```

Full checklist: `docs/RELEASING.md`.
