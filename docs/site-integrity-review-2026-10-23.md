# Website integrity review — October 23, 2026

## Scope and findings

Reviewed 124 public HTML files: 111 content pages and 13 legacy redirect pages. There are 110 indexable canonical content pages; the RFQ confirmation page is intentionally noindex. The local audit checks 7,011 HTML/CSS destinations, including images, scripts, stylesheets, fragments and local absolute URLs.

Initial scan found no broken local destinations, missing anchors, duplicate titles/descriptions, missing canonicals or orphan content pages. It identified two footer variants; main navigation had consistent destinations but inconsistent selected-section styling. Four legacy aliases had correct redirects/canonicals with generic fallback links instead of their actual destination. RFQ failure messages retained an outdated individual email address.

## Changes

- Shared header and footer templates are applied to every public content page. The selected page/section uses aria-current and consistent styling. The existing compact main menu is preserved.
- The footer consistently provides Mil-Spec series, Mil-Spec buyer guide and custom fastener guide links. Telephone and email are clickable. Certification wording is consistent.
- A keyboard skip link and main landmark are available on every content page.
- Legacy alias fallback links now agree with their redirect and canonical destination. Aliases remain noindex.
- RFQ input hints now request custom drawing revision, material, finish and delivery date. Both error paths direct buyers to info@websonfasteners.com. Provider, field names, required fields and submission behavior are preserved.
- The new custom measurement guide covers screw-length datums, separate shoulder/thread dimensions and spacer/standoff end configurations. Relevant custom and electronic hardware pages link to it; both electronic product pages also link directly to custom fasteners for electronics.
- Sitemap generated from actual canonical, indexable content. Existing modification dates retained; substantive updated custom/electronic/RFQ pages dated October 23. The confirmation page and 13 aliases are excluded.

## Repeatable maintenance

`python scripts/build-site-rfq-context.py` now applies shared chrome and regenerates the sitemap along with the existing RFQ mapping. Both Mil-Spec and Southco builders already call it. Running both builders produced no further changes after normalization.

`python scripts/check-site-integrity.py` verifies all public HTML/CSS local destinations and anchors, metadata, schema JSON syntax, shared header/footer, active navigation, main landmarks, home-page reachability, aliases, sitemap coverage and selected RFQ invariants. It excludes repository-only scripts/templates/docs from the public crawl.

RFQ regression suites pass for 110 content source pages, all 66 Mil-Spec tracking pages and all 13 Southco part routes. Stock data and technical part allowlists are unchanged. No live RFQ was submitted.

## Custom guide technical verification

Public text is original and contains no external research links. The measurement conventions are general descriptions; the applicable drawing or specification controls. Existing verified shoulder schematic is reused. No new compatibility or dimension values are inferred from examples.

- Portland Bolt, Bolt Length: https://www.portlandbolt.com/technical/faqs/bolt-length/ — manufacturer search result supports under-head conventions and including countersunk-head thickness in overall length. Full page fetch returned 403; used as corroboration with Accu, not a sole source.
- Accu, How To Measure A Screw: https://www.accu.co.uk/p/123-how-to-measure-a-screw — reviewed full article; supports raised-head, countersunk, raised-countersunk and separate shoulder/thread length conventions, pitch/TPI terminology.
- PennEngineering, Products — Standoffs: https://www.pemnet.com/products-overview/products-standoffs/ — manufacturer search result describes male external vs female internal threads and exceptions using nonthreaded attachments. Full fetch returned 401; exact configuration table uses explicit geometry, avoiding universal terminology claims.
- PennEngineering manufacturer catalog: https://catalog.pemnet.com/category/uts-and-spacers-standoffs-surface-mount-type-smtso — manufacturer result independently confirms threaded and unthreaded standoff configurations.

## Privacy and indexing boundaries

The user does not want customer photos or project descriptions because of confidentiality. Do not request or publish them as a future SEO step. This batch contains only generic buying/measurement guidance and established company information.

The sitemap, canonicals, robots.txt and noindex controls are locally verified. Google Search Console submission, crawl/index status and performance require the property's authenticated account; repository checks cannot establish that Google has indexed every page. No Search Console submission or request-indexing action is claimed.
