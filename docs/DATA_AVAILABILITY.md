# Data availability

## Shareable in this repository

- Rule definitions (`src/anachonism/*.py`)
- Filter term list (`config/filter_terms_33.txt`)
- Locked aggregate targets (`config/expected_aggregates.json`)
- Synthetic example rows (`examples/synthetic_tweets.csv`)

## Not redistributed here

- Raw tweet corpora (including `tweets_politica_kaggle.csv`)
- Filtered / classified CSVs containing tweet text or account identifiers
- PostgreSQL dumps from database `investigacion`
- Any Odoo attachments or export wizards containing user content

## Why

Tweet text and account fields may be personal data and are subject to platform terms and
dataset redistribution conditions. A SHA-256 digest of the verified raw file is published
so that local holders can confirm they have the same input without shipping the file.

## How to reproduce aggregates

1. Obtain the OpenDataBay / Kaggle politicians tweet file referenced in historical methods.
2. Confirm SHA-256 matches `config/expected_aggregates.json`.
3. Run the pipeline documented in `README.md` with `ANACHONISM_RAW_TSV` set.
