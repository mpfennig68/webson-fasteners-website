# Mil-Spec reference maintenance

Regenerate the static HTML with `python3 scripts/build-mil-spec-reference.py` from the repository root. No third-party packages are required. The data register is `scripts/mil-spec-data.json`.

The data register separates catalog-level series descriptions from DLA document-status relationships. It records source names, URLs and scopes. Do not infer MS-to-NASM relationships or copy material/finish/locking codes between families.

The MS51576 table contains 41 nominal catalog entries; the MS51575 table contains 28 selected entries. Dash 26 is intentionally omitted from the slotted sample because it was not displayed in the manufacturer list reviewed. These are identification tables, not full tolerance or acceptance drawings. Threads are searchable data but are not displayed as a full thread specification.

The MS51830 table contains all 16 internal/external thread relationships checked against revision G (9 May 2022), Tables I and II, on October 18, 2026. Dash 102 has a .190-32UNF-2A external thread. The guide distinguishes L (aerospace) and LM (non-aerospace), includes QX zinc-nickel plating and the restriction on A for new designs, and confines the note 7 QX-for-A allowance to ground vehicle applications. The public government drawing mirror is registered with the official DLA status record. Modified minor diameters, full dimensions and acceptance requirements remain outside the summary.

The cross-reference table contains document relationships, including active records. No complete-part interchangeability is asserted. The MS20426 cancellation notice is separately noted because it explicitly preserves part numbers.

The original MS51957 guide body is retained when the pages are regenerated. Update that guide body before regeneration if its text needs revision. Existing quote form behavior is untouched.

Before publishing updates: verify sources and dates; inspect all changed links and table values; check filter behavior and no-JavaScript readability; review desktop and mobile layouts when browser tooling is available. Keep sitemap URLs canonical and unique. The separate downloadable review preview is not a production page.

October 18 verification: static HTML/link/metadata checks and filter behavior passed. Browser visual QA remains pending: the managed environment lacks the required control-browser capability. Before release, inspect desktop and phone layouts, horizontal table scrolling, and navigation to the existing Quote.html form; do not submit a test inquiry to the live form.

Public citations were moved to docs/mil-spec-research-notes.md on October 18, 2026. Keep docs and scripts excluded from Jekyll deployment through _config.yml. The public Sources page is deleted. The source JSON remains an internal generator input. Buyer resources add RFQ preparation, material/finish terminology and 17 purchasing FAQs. Customer-directed links stay within Webson.
