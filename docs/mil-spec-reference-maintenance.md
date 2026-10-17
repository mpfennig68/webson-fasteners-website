# Mil-Spec reference maintenance

Regenerate the static HTML with `python3 scripts/build-mil-spec-reference.py` from the repository root. No third-party packages are required. The data register is `scripts/mil-spec-data.json`.

The data register separates catalog-level series descriptions from DLA document-status relationships. It records source names, URLs and scopes. Do not infer MS-to-NASM relationships or copy material/finish/locking codes between families.

The MS51576 table contains 41 nominal catalog entries; the MS51575 table contains 28 selected entries. Dash 26 is intentionally omitted from the slotted sample because it was not displayed in the manufacturer list reviewed. These are identification tables, not full tolerance or acceptance drawings. Threads are searchable data but are not displayed as a full thread specification.

The MS51830 thread relationships and notation examples are explicitly from revision F (2012). DLA lists revision G (2022). The older drawing is not represented as the current controlling revision. Review the order-required issue before using it for acceptance.

The cross-reference table contains document relationships, including active records. No complete-part interchangeability is asserted. The MS20426 cancellation notice is separately noted because it explicitly preserves part numbers.

The original MS51957 guide body is retained when the pages are regenerated. Update that guide body before regeneration if its text needs revision. Existing quote form behavior is untouched.

Before publishing updates: verify sources and dates; inspect all changed links and table values; check filter behavior and no-JavaScript readability; review desktop and mobile layouts when browser tooling is available. Keep sitemap URLs canonical and unique. The separate downloadable review preview is not a production page.
