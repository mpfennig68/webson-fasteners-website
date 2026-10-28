# Electronic hardware category pages

## October 28, 2026: spacers and standoffs

Products-Spacers.html and Products-Standoffs.html are separately authored category pages linked from the Electronic Hardware hub. Adjacent electronics application, assembly-component and custom pages link to both. Each page has distinct configuration and measurement tables, a labeled SVG schematic, material-selection considerations, application guidance, native details/summary answers, contextual RFQ links, canonical and social metadata, and breadcrumb JSON-LD. Existing shared chrome and custom-fasteners layout styles are reused; electronic-products.css contains the small product-page additions.

These are sourcing and selection pages, not SKU catalogs. No size availability, live stock, manufacturer authorization or material performance rating is asserted. Diagrams are schematic and explicitly not to scale; manufacturer drawings control measurement conventions and tolerances. Standoff body length and stud projection remain distinct. A plain spacer bore must not be treated as a nominal thread size. Full thread depth must not be inferred from drilled depth.

Technical checks used the manufacturers’ own descriptions and categories:
- PennEngineering, standoff attachment definitions and installation styles: https://www.pemnet.com/products-overview/products-standoffs/
- Keystone, male/female metric standoffs and listed materials: https://www.keyelco.com/category.cfm/Spacers-Standoffs/Standoffs-Hex-Male-Female-Metric/p/495/id/502
- Keystone, female round/hex standoffs: https://www.keyelco.com/category.cfm/Spacers-Standoffs/Standoffs-Hex-Round/p/495/id/500
- Keystone, spacer/standoff organizers and through-hole versus threaded styles: https://www.keyelco.com/category.cfm/Spacers-Standoffs/Spacer-Standoff-Organizers/id/497

These sources support generic selection terminology, not a claim that Webson stocks every listed configuration or represents these manufacturers. Public pages retain the established policy of keeping external technical source links in internal documentation.

Maintenance: run build-site-rfq-context.py after adding/editing pages to update the RFQ allowlist and sitemap. Keep public pages linked from the hub and related pages. Reference-family content remains managed by the existing Mil-Spec generator.

Validation: site integrity passed with 140 indexable pages, no broken links/anchors, no orphan pages and no duplicate titles/descriptions. All 140 RFQ page routes passed prefill, customer-text preservation and attribution checks; existing Mil-Spec/Southco attribution checks passed. Browser QA inspected the desktop standoff layout and schematic, confirmed both product quote prefills, opened a spacer FAQ, and checked a 390px responsive spacer frame: page content stayed contained while wide tables scrolled in their own regions. No inquiry submitted.

## October 28: clearer spacer bore and handles/knobs

Redrew the spacer schematic with a larger end-view bore, smaller dimension arrowheads, OD above the part and ID on its own dimension line below. The bore is left unobstructed; caption explicitly identifies L, OD and ID. SVG has accessible title/description.

Added Products-Handles.html and Products-Knobs.html with distinct selection and measurement tables, schematic SVGs, FAQs and contextual RFQ links. Handles separate mounting centers, grip clearance and installed projection; knobs distinguish control shaft fits from threaded clamping interfaces. The Electronic Hardware hub links to both; spacer and standoff related-resource lists link to the new pages. Ratings, installation suitability and availability remain product-specific; generic appearance does not establish a lifting rating, shaft fit or material performance.

Technical terminology checked against primary manufacturer pages (not a representation or stock claim):
- Southco handle categories and mounting styles: https://southco.com/en_us_int/handles and https://southco.com/en_us_int/handles/surface-mount-handles
- Davies Molding control knob attachment options: https://daviesmolding.com/catalog/products/knobs/control

Validation: site integrity passed for 142 indexable pages, with no broken links/anchors, orphan pages or duplicate metadata. RFQ page-context checks passed for 142 content routes; existing reference and Southco tracking checks passed. Browser QA inspected all three diagrams, verified Handle and Knob quote prefills, checked the revised spacer diagram and knob page in a 390px responsive frame without page overflow, followed spacer-to-knob navigation and expanded a knob FAQ. No inquiry submitted.
