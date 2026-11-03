# License decision

## Zenodo deposit (verified)

The authoritative Zenodo archive for GitHub Release **v1.0.2**
(`10.5281/zenodo.23931188`) is deposited under **CC-BY-4.0**
(Creative Commons Attribution 4.0 International). That assignment is visible on
the Zenodo record and is mirrored in `CITATION.cff` / `.zenodo.json` so citation
metadata matches the archived deposit.

## GitHub `LICENSE` file

A root `LICENSE` file is still recommended for GitHub license detection clarity.
If co-authors later authorize a different SPDX id for the source tree (e.g. MIT
for code), update:

1. `LICENSE`
2. `CITATION.cff` `license`
3. `.zenodo.json` `license`
4. this document

Do not use fake values such as `NOASSERTION` (they break Zenodo CFF validation).
