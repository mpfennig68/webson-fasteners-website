# Southco product pages: evidence and maintenance

Reviewed October 19, 2026. The user supplied 14 lines containing 13 distinct numbers; 12-11020-13 was repeated. The public hub is Products-Southco.html. The 13 individual product pages use Southco-<manufacturer part number>.html.

Run `python3 scripts/build-southco-pages.py` from the repository root. The reviewed content register is scripts/southco-data.json. These two directories remain excluded from Jekyll by _config.yml. Keep research citations and supplier links in this file rather than customer pages.

## Manufacturer records

Each part's manufacturer URL is retained in the data register. Sources read through web retrieval/search:

- F6-3-1: https://southco.com/en_us_int/f6-3-1
- V4-0006-52: https://southco.com/en_us_int/v4-0006-52
- 96-50-510-50: https://southco.com/en_us_int/96-50-510-50
- C5-21-35: https://southco.com/en_us_int/c5-21-35
- 12-11020-13: https://southco.com/en_us_int/12-11020-13
- V7-20-101-50: https://southco.com/fr_eu_int/v7-20-101-50 and https://southco.com/de_eu_int/v7-20-101-50
- C3-805: https://southco.com/en_us_int/c3-805
- P2-54: https://southco.com/en_us_int/p2-54
- E3-16-21: https://southco.com/en_us_int/e3-16-21
- P2-43-1: https://southco.com/en_us_int/p2-43-1
- P1-33: https://southco.com/en_us_int/p1-33
- E6-10-208-50: https://southco.com/en_us_int/e6-10-208-50
- E3-16-35: https://southco.com/en_us_int/e3-16-35

Supporting manufacturer catalogs and family directories:

- P1: https://media.southco.com/media/static/Literature/p1.en.pdf
- P2: https://media.southco.com/media/static/Literature/p2.en.pdf
- E6 torque hinges: https://media.southco.com/media/static/Literature/e6-ct.en.pdf
- 96: https://southco.com/en_us_int/hinges/removable-hinges/96-removable-lift-off-hinges
- F6: https://southco.com/en_us_int/hinges/concealed-hinges/f6-concealed-door-removal-hinges
- C5: https://southco.com/en_us_int/latches/compression-latches/lever-latches/c5-sealed-lever-latches

## Conflicts and scope decisions

- **V4-0006-52:** Southco's page title describes steel with zinc plating, while the visible heading and specification table describe stainless steel, natural finish. Public content intentionally omits material/finish; requires manufacturer drawing or written confirmation before adding either.
- **C3-805:** current visible heading/family list says 25 N (5.6 lbf); specification table reports pullup 22.00; earlier indexed family content says 22 N (5 lbf). Public page omits force. No numeric performance claim should be added without reconciliation.
- **P1-33:** SEO title incorrectly describes 1.0–1.8 mm. Visible product description, family directory and catalog table agree on 1.8–3.3 mm, UL94-V0. Use that range.
- **P2-54:** SEO title conflicts with the product body. Detailed table, visible heading and P2 catalog agree: large; 2.1–2.5 mm; UL94-HB. Do not confuse with P2-54-1 or P2-43-1.
- **P2-43-1:** small; 1.8–2.1 mm; UL94-V0, supported by detailed page and P2 catalog.
- **12-11020-13:** this is the flat riveted medium-size stainless/passivated receptacle, not the stud. No complete-system compatibility is asserted without mating part numbers.
- **E6-10-208-50:** 0.9 N·m forward and reverse, aluminum, medium size. Page title calls finish powder coat, detailed table says paint, catalog says black paint. Public content states black only. Do not substitute E6-10E-208-50.
- **E3-16-35:** detailed table supports adjustable 38.9–54.6 mm grip, attached cam, Type A clockwise latching.
- **E3-16-21:** material, finish and 8 mm hex recess are included; no grip dimensions inferred from E3-16-35.
- No stock, price, guaranteed lead time, authorized-distributor, complete-system ingress rating or universal interchangeability claims are made. Material flammability values for the P1/P2 variants are labeled as material classifications.
- Body text is original purchasing-focused copy. No competitor stock data, product images, CAD files or manufacturer drawings were copied to the website.

## RFQ behavior

Quote.html adds assets/southco-rfq.js. A fixed allowlist validates ?southco=<complete part number> or catalog. Known product links add manufacturer, manufacturer_part_number and rfq_southco_source hidden fields and prefill rfq_details only when empty. Existing text is retained. Source URLs are constructed from the approved local page map and checked against the current origin. Invalid/external query values are ignored. There is no submit listener, fetch, cookie or local storage. Native FormSubmit configuration is unchanged; no live inquiry was sent. Mil-Spec reference attribution remains independent.

## Validation

Check HTML structure, local links and fragments, unique canonical URLs, parsed JSON-LD, sitemap coverage, idempotent generation, directory filter behavior, quote context and empty/existing-text behavior. Existing Mil-Spec RFQ attribution checks should continue to pass. Browser visual review remains pending because the supported control-browser capability is unavailable in this environment. Inspect desktop/phone layout, table scrolling and quote navigation before merging.
