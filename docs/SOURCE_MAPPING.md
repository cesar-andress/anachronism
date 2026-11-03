# Source mapping (historical → public package)

Paths below are **logical historical locations** for maintainers. They are not
shipped and must not be hardcoded as absolute machine paths in this public tree.

| Public path | Historical source (logical) | Classification |
|-------------|-----------------------------|----------------|
| `src/anachonism/label_functions.py` | offline investigacion `src/label_functions.py` | DIRECTLY USED IN VERIFIED ANALYSIS |
| `src/anachonism/fallacies.py` | offline investigacion `src/fallacies.py` | DIRECTLY USED IN VERIFIED ANALYSIS |
| `src/anachonism/h2_semantics.py` | offline investigacion `src/h2_semantics.py` | DIRECTLY USED IN VERIFIED ANALYSIS |
| `src/anachonism/h3_vacuity.py` | offline investigacion `src/h3_vacuity.py` | DIRECTLY USED IN VERIFIED ANALYSIS |
| `src/anachonism/datasets.py` | offline investigacion `src/datasets2.py` | DIRECTLY USED IN VERIFIED ANALYSIS |
| `scripts/filter_terms.py` | offline investigacion `offline_main.py` | DIRECTLY USED IN VERIFIED ANALYSIS |
| `scripts/classify_h1_fallacies.py` | offline investigacion `classify_tweets.py` | DIRECTLY USED IN VERIFIED ANALYSIS |
| `scripts/classify_h2.py` | offline investigacion `h2_analyze.py` | DIRECTLY USED IN VERIFIED ANALYSIS |
| `scripts/classify_h3.py` | offline investigacion `h3_analyze.py` | DIRECTLY USED IN VERIFIED ANALYSIS |
| `config/filter_terms_33.txt` | documented filter list (also Odoo dict `Terms - Ideology (Default)`) | DIRECTLY USED IN VERIFIED ANALYSIS |

Identical SHA-256 rule modules also existed in the Odoo port
`tweet_test_battery/tools/{label_functions,fallacies,h2_semantics,h3_vacuity}.py`
(HISTORICALLY RELATED IMPLEMENTATION; same rule bytes).

The Odoo application and PostgreSQL database `investigacion` store later/different
corpus runs and empty annotation tables; they did **not** produce the locked
manuscript tables (documented in the private salvage audit tree, outside this repo).
