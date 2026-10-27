# Mil-Spec reference maintenance

Regenerate the static HTML with `python3 scripts/build-mil-spec-reference.py` from the repository root. No third-party packages are required. The data register is `scripts/mil-spec-data.json`.

The data register separates catalog-level series descriptions from DLA document-status relationships. It records source names, URLs and scopes. Do not infer MS-to-NASM relationships or copy material/finish/locking codes between families.

The MS51576 table contains 41 nominal catalog entries; the MS51575 table contains 28 selected entries. Dash 26 is intentionally omitted from the slotted sample because it was not displayed in the manufacturer list reviewed. These are identification tables, not full tolerance or acceptance drawings. Male thread sizes are displayed for every selected shoulder row. Catalog thread length, head diameter/height and socket width (socket family only) were added October 27, 2026; thread class and tolerances are not inferred.

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


Layout revision 2026-10-22: reference navigation uses six concise destinations; glossary and materials/finishes remain linked in the guide and contextual resources. Series without a detailed guide render a plain series label and blank Resource cell. The renderer combines dimension and identification content in one responsive section on 23 pages; the preserved MS51957 source is unpacked before rebuilding to keep builds idempotent. Do not restore the decorative supplier identity card. The buyer guide keeps a plain question index, now with stock availability, photo identification and unlisted-parts questions.

The expanded lookup data is maintained in `scripts/mil-spec-lookup-data.json`, with renderers in `scripts/build-mil-spec-lookups.py`. Rebuild using the main generator. Reference inquiry allowlists are separate from `stocked_part_guides`; never mark all matrix or cross-reference rows stocked. Add tests for a new page's explicit part allowlist and reject unrelated/invalid parts. Source evidence and historical issue limits are recorded in the research notes. Keep the existing compact menu and split construction-specific helical tables.

## October 27: MS purchasing tables

The two shoulder tables display all 69 existing selected entries with visible male thread, shoulder diameter/length, catalog thread length, head diameter/height and socket width where applicable. Common material is stated as stainless steel. The row allowlists in build-site-rfq-context.py come from the shoulder data arrays; these are reference parts, not new stock claims. Preserve the omitted MS51575-26 unless independently verified.

The shared filtered renderer adds exact visible-cell size selectors where applicable. Filters combine with search and the existing family filter; Clear filters resets all selectors. Shared styles tighten rows and pin table headers and row labels within the scroll region. All technical values and links are rendered in HTML without JavaScript.

## October 27: next MS families

Nut rows in MS21042/MS21044/MS21083 now include height and across-flats limits. MS16995/MS16996 rows include head diameter, head height and socket AF limits. The 12 MS35338 stock rows now carry geometry from the existing verified dash-number matrix. All 39 existing stocked identifiers and their RFQ allowlists are preserved. Keep limits separate from nominal tool sizes, and washer section thickness separate from free height. Read the October 27 research notes for corrected historical scan revision/date attributions.

The builder now preserves a newer sitemap lastmod instead of overwriting it with the October 22/23 baseline during regeneration. Run scripts/check-ms-purchasing-dimensions.py after changing these dimensional fields.

## October 27: global part search and machine-screw dimensions

Every reference/resource page and the Mil-Spec supplier landing page has one shared GET search form targeting Resources-Mil-Spec-Part-Search.html. The search index is generated from published HTML tables by scripts/build-mil-spec-part-search.py at the end of the main build. It currently covers 1,086 unique exact designations plus 129 family roots. Prefer a stocked row and then a part's own guide when the same designation occurs in comparison tables. The index contains only already-public part information, not private stock quantities or original workbook data.

Exact entries link to stable table anchors with ?part=...; mil-spec-reference.js initializes only the table blocks containing that exact designation. Complete unlisted sizes return their known family guide without assuming a listed size, part equivalence, stock status or MS/NASM prefix conversion. Series searches browse the listed sizes. Search results are paged in groups of 40. The JSON and result script load only on the search page, so the shared forms do not add a search-index download on every reference page. Without JavaScript the series/table directories remain available.

Run node scripts/check-mil-spec-part-search.cjs along with the dimensional, RFQ and site-integrity checks. Preserve query escaping, exact-prefix boundaries, textContent-only result rendering, local result links and static canonical URLs. Regeneration must preserve exactly one shared search form, including on the retained MS51957 guide and supplier landing page.

Eighty existing machine-screw rows now show added head data: MS35206 (10) and MS51957 (33) use head diameter/height limits; MS24693 (27) and MS51959 (10) show maximum sharp-head diameter and nominal head angle. Countersunk head reference heights and minimum-sharp diameters are not presented as actual measured acceptance limits.

Exact search results also offer a direct quote link through the search page. The RFQ generator reads only the generated index's exact designations into a dedicated allowlist, preserving customer-entered text and rejecting unlisted or out-of-context values. Build order is public tables → search index → RFQ context; never derive stocked status from this allowlist.

Browser checks passed for landing-page search → MS51576-16 result → filtered dimensions → prefilled RFQ; unlisted MS51576-999 family fallback; direct quoting of the unstocked reference MS35338-153; and MS35307 browsing/pagination from 40 to 80 of 283 matches. No live inquiry submitted.

## October 27: additional screw and nut reference families

Additional reference data is separate from stock data: `mil-spec-additional-screw-data.json` owns 399 entries across MS35207/MS51958/MS51960/MS16997; `mil-spec-additional-nut-data.json` owns 127 across MS35649/MS35650/MS51967/MS51968. Each corresponding `build-mil-spec-additional-*.py` renderer runs inside the main build. Preserve the source issue attached to each table and the distinction between nominal values and limits. MS35650 uses Amendment 1, not the original G table. Brass nut references include the selected B or T finish letter. Finished hex nut Grade A dash numbers remain omitted as canceled.

Both additional registers feed explicit part-specific RFQ allowlists; the global index independently reads the published tables. The lookup now contains 1,612 exact entries across 129 series. Run `check-ms-additional-screws.py` and `check-ms-additional-nuts.py` with the existing checks after edits. These additions are references for quotation, not new stock evidence.

## October 27: flat and drilled fillister screw families

`mil-spec-head-style-data.json` owns 479 selected references for MS35190 (119), MS35191 (122), MS35265 (119), MS35266 (119). Its renderer runs in the main build. MS35190/35191 are plain-screw selections with asterisked #1/7/16 inactive references omitted; do not synthesize L variants. The fillister tables separate total axial head height O from head-side height H and show nominal drilled-hole diameters separately from dimensional limits. Preserve printed decimal length values and the historical issue identified on each guide. MS35265 has later revisions; these C dimensions must not be labeled current F values.

New schematic assets are `countersunk-82-screw-dimensions.svg` and `drilled-fillister-screw-dimensions.svg`. The earlier 100-degree asset is unchanged. Run `check-ms-head-styles.py` with all existing reference/search/RFQ checks. Global search now contains 2,091 exact entries and 129 series, with 80 shared forms. Browser QA checks filtering and quote prefill without submitting a live inquiry.

## October 27: Grade 5/8 hex cap screw guides

`mil-spec-hex-cap-data.json` adds 129 MS90725, 129 MS90726, 97 MS90727 and 97 MS90728 references. Its renderer runs in the main build; RFQ context reads the explicit register, while search independently indexes published HTML. Preserve grade, coarse/fine pitches, historical issue and coating; the reviewed Grade 8 F/G issues use zinc and exclude aerospace applications. Omit their inactive 7/16 and 9/16 columns. Do not extend past 3-inch lengths into ambiguous MS90727F long-row numbering. Preserve MS90728G's .405 maximum head height at 5/8. Run `check-ms-hex-caps.py` with the existing dimensional, integrity, search and RFQ checks. Search now contains 2,543 exact entries and 129 series, with 84 shared search forms. Stock evidence and existing Formcarry submission behavior are unchanged.

Validation passed: all existing dimension suites plus the new 452-row hex cap suite, site integrity (zero broken links/anchors), search and RFQ context checks, and repeat-build idempotence. Browser QA verified MS90728 thread/length filtering to -109 and quote prefill, plus MS90726-109 global search with 1/2-20 dimensions. No inquiry submitted.

## October 27: additional set-screw families

`mil-spec-set-screw-data.json` adds 36 MS51023 plain cup-point, 17 MS51031 self-locking flat-point, 33 MS51047 historical half-dog and 85 MS51963 plain alloy cup-point selections. Preserve sparse dash-to-length mappings, the selected configuration, nominal socket J versus point limits, and cup C versus optional alternate-point geometry. MS51047B is explicitly inactive for new design. L includes the dog projection Q. Length tolerances remain visible beside the printed decimal values. Run `check-ms-set-screws.py` with all existing suites. The global index now covers 2,714 exact references and 129 series; shared upper-right search appears on 88 pages. Existing inventory and Formcarry behavior are preserved.

Validation passed: 171 sourced set-screw selections plus all existing dimension suites, search/RFQ checks and site integrity (zero broken links/anchors). Browser QA checked both new schematics, MS51047 1/4-28 × .500 filtering and quote prefill, plus MS51031-107 global search with explicit self-locking configuration and direct quote selection. No inquiry submitted.
