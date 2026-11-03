# Releasing to GitHub and Zenodo

This checklist exists so archival failures like Zenodo `v1.0.0` (invalid
`CITATION.cff`) cannot recur unnoticed.

## Hard gates (must pass)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q tests/test_rules_smoke.py tests/test_release_metadata.py
python scripts/check_release_metadata.py
```

The metadata gate enforces:

1. `CITATION.cff` validates with `cffconvert` (CFF 1.2.0).
2. No unsupported CFF keys (the former `notes` field is forbidden).
3. No `license: NOASSERTION` / equivalent fake SPDX values.
4. `.zenodo.json` is present, valid JSON, `upload_type: software`, creators with
   bare ORCID ids.
5. Version equality across `CITATION.cff`, `.zenodo.json`, `pyproject.toml`,
   and `src/anachonism/__init__.py`.
6. `CHANGELOG.md` has a section for that version.
7. No absolute private machine paths (developer home directories) in tracked text.
8. No manuscript/agent files (`.tex`, `.bib`, `.cursor/`, …) in the tree.

CI runs the same gates on every push to `main`.

## Zenodo precedence

If both `.zenodo.json` and `CITATION.cff` exist, **Zenodo uses only
`.zenodo.json`** for the GitHub-release deposit. Keep both files consistent.
Do not invent a DOI in either file.

## License

Do not invent an SPDX license. When copyright holders authorize one (e.g. MIT):

1. Add `LICENSE`.
2. Set `license` in `CITATION.cff` (single string, e.g. `MIT`).
3. Set matching `license` in `.zenodo.json` (lowercase Zenodo id, e.g. `mit`).
4. Update `docs/LICENSE_DECISION.md`.

Until then, omit `license` from both metadata files rather than using
`NOASSERTION`.

## Tag and GitHub Release

1. Bump version in the four version locations above and add a CHANGELOG section.
2. Commit and push `main`.
3. Wait for CI green.
4. Create an annotated tag `vX.Y.Z` on that commit and push the tag.
5. Create a **GitHub Release** from that tag (Zenodo archives Releases, not bare
   tags alone once the webhook is release-based). The `GITHUB_TOKEN` used by
   automation must include permission to create releases; otherwise create the
   release in the GitHub UI.
6. Confirm Zenodo shows a successful deposit and record version + concept DOIs
   in a **follow-up** commit on `main` only (never rewrite the published tag).

## Scientific qualifications (release notes)

Release notes must preserve:

- heuristic / operational pattern labels only;
- not independently validated fallacy, anachronism, or vacuity detection;
- raw tweet corpora are not redistributed.
