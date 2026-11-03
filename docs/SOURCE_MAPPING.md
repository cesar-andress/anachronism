# Source mapping (historical → public package)

| Public path | Historical path | Classification |
|-------------|-----------------|----------------|
| `src/anachonism/label_functions.py` | `/home/cesar/proyectos-python/investigacion/src/label_functions.py` | DIRECTLY USED IN VERIFIED ANALYSIS |
| `src/anachonism/fallacies.py` | `.../src/fallacies.py` | DIRECTLY USED IN VERIFIED ANALYSIS |
| `src/anachonism/h2_semantics.py` | `.../src/h2_semantics.py` | DIRECTLY USED IN VERIFIED ANALYSIS |
| `src/anachonism/h3_vacuity.py` | `.../src/h3_vacuity.py` | DIRECTLY USED IN VERIFIED ANALYSIS |
| `src/anachonism/datasets.py` | `.../src/datasets2.py` | DIRECTLY USED IN VERIFIED ANALYSIS |
| `scripts/filter_terms.py` | `.../offline_main.py` | DIRECTLY USED IN VERIFIED ANALYSIS |
| `scripts/classify_h1_fallacies.py` | `.../classify_tweets.py` | DIRECTLY USED IN VERIFIED ANALYSIS |
| `scripts/classify_h2.py` | `.../h2_analyze.py` | DIRECTLY USED IN VERIFIED ANALYSIS |
| `scripts/classify_h3.py` | `.../h3_analyze.py` | DIRECTLY USED IN VERIFIED ANALYSIS |
| `config/filter_terms_33.txt` | Documented in `latex/nuevo_scorpus_ampliado.tex`; also Odoo dict `Terms - Ideology (Default)` | DIRECTLY USED IN VERIFIED ANALYSIS |

Identical SHA-256 rule modules also exist under:
`/home/cesar/papers_unir/investigacion/tweet_test_battery/tools/{label_functions,fallacies,h2_semantics,h3_vacuity}.py`
(HISTORICALLY RELATED IMPLEMENTATION — Odoo port; same rule bytes).

Odoo app + PostgreSQL `investigacion` store later/different corpus runs and empty annotation tables; they did **not** produce the locked manuscript tables (see internal PostgreSQL recovery audit).
