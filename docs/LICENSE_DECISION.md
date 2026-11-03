# License decision (pending)

No OSI `LICENSE` file is included in this repository yet.

**Reason:** inventing a software license without copyright-holder authorization is forbidden.
Historical Odoo / offline trees did not document a clear redistributable license for this
extracted package. `CITATION.cff` therefore omits `license` (an invalid `NOASSERTION`
value previously broke Zenodo CFF validation).

**Owner action required:** choose and commit an SPDX license (e.g. MIT, Apache-2.0, or
GPL-3.0) after confirming co-author agreement, then add `LICENSE` and set matching
`license` fields in `CITATION.cff` and `.zenodo.json`.
