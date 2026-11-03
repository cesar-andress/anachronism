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
were produced by the historical offline Python pipeline archived under
`/home/cesar/proyectos-python/investigacion` (see `docs/SOURCE_MAPPING.md`).

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
- Licensing of this software package is **pending** owner decision (no LICENSE committed yet).
- No Zenodo DOI exists yet.

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

## Future Zenodo archival status

Not deposited. See the private salvage report `ZENODO_READINESS.md` (outside this Git tree).
A GitHub↔Zenodo link can be configured after the first reviewed public release.

## Citation

Use `CITATION.cff` once authorship/affiliations and license are finalized. Do not invent a DOI.
