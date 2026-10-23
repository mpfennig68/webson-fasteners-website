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


## Dimension illustrations and RFQ attribution

Three schematic SVGs in `assets/diagrams` illustrate raised-head machine screws, shoulder screws and flat washers. The generator places them on seven relevant guides/family pages. They show measurement locations with letter keys, not numeric acceptance data or official drawing symbols. Preserve the not-to-scale and scope text. The retained MS51957 body has its generated dimension section removed before regeneration to avoid duplication.

The generator adds `?reference=<page filename>` to Quote.html links on all reference pages. `assets/rfq-reference-tracking.js`, loaded only by Quote.html, validates this filename against a generated allowlist and appends two ordinary hidden fields: `rfq_reference_page` and `rfq_reference_url`. FormSubmit includes named fields in the email. Public documentation checked October 18, 2026: https://formsubmit.co/ . The native form HTML, destination, method, attachment behavior, CAPTCHA settings and redirect remain unchanged. There is no submit interception, analytics account, dashboard, cookie or browser-storage dependency. Direct quote visits and invalid source values add no fields. With scripting blocked, the existing form works without attribution. This captures the reference page whose quote link was followed, not a complete multi-page customer journey or a qualification decision. The field values appear on submitted inquiries; do not treat quote-link clicks as qualified leads.

Run `node scripts/check-rfq-reference-tracking.cjs` from any directory to verify all source routes and invalid-input handling. No live test RFQ was sent. The added fields were verified with automated DOM behavior checks; first real inbound inquiry is the delivery-level confirmation.

October 18 site-wide cleanup: added the Mil-Spec Reference footer link to 28 remaining content pages, including Quote.html and thank-you.html; all 60 content pages now include it exactly once. The 13 legacy redirects have no content footer. Declared English on 17 pages missing a lang attribute. Verified local file links across all 73 HTML files and preserved RFQ form markup and attribution. The reference generator reuses the updated footer without adding a duplicate link.

## October 22: MS51021 extension

The generator now includes Reference-MS51021.html, a four-row selected plain set-screw table in set_screw_sizes, and assets/diagrams/cup-point-set-screw-dimensions.svg. The directory, set-screw family, technical-table directory, document cross-reference, sitemap and both RFQ context registers include the new guide. Only the four selected plain MS51021 designations are accepted by the part-specific RFQ prefill; an unsupported or out-of-context part parameter falls back to the normal page context. Keep the same validation in scripts/build-site-rfq-context.py and its generated asset. Research scope is recorded in mil-spec-research-notes.md.

## October 22: stocked nut reference expansion

NAS671 and NAS1291 are now directory series; MS21083 now has its own guide. Data-driven selected tables include stock status with a prior-sale disclaimer. The nut_sizes register owns the 11 selected nut rows; stocked_part_guides owns all 15 supported part-specific RFQs. The site RFQ generator reads that allowlist so rebuilding does not lose part prefill. NAS671/NAS1291/MS21083 use the generic hex-nut measurement schematic, which omits locking geometry. Update row data, allowlists and source notes together when extending the selection.


The buyer’s guide is authored in scripts/mil-spec-buyers-guide.py and invoked by the main generator. Edit it there, then run python scripts/build-mil-spec-reference.py. The commercial supplier page is maintained directly with assets/mil-spec-landing.css. Keep FAQ JSON-LD identical to visible supplier answers. Reference pages inherit the supplier nav/footer. Recheck certificate validity and public RFQ file instructions before updating certification or upload claims.
