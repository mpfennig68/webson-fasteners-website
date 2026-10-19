# Site-wide RFQ context

Implemented October 19, 2026. Quote links on 73 content pages retain the selected Southco part, Mil-Spec guide/series or general page topic in the PART NUMBERS / SPECIFICATIONS field.

- Source pages carry explicit allowlisted parameters; no referrer guessing, redirect, additional network request, submit interception, analytics dependency or browser storage is used.
- Existing `?southco=` part routes and `?reference=` Mil-Spec routes remain valid. Other pages use `?context=<source filename>`.
- Southco fills its part number and product description first. The site-wide script respects that value. Reference guides fill their heading; broad pages identify the topic as an inquiry. No particular size, dash number or dimensional variant is inferred from a family page.
- Autofill only occurs when the details field is empty. Customer/restored text is never replaced. Direct Quote.html visits and unknown/external parameters remain blank.
- Existing Southco/Mil-Spec attribution fields remain. `rfq_source_page` and `rfq_source_url` add consistent named source fields to contextual inquiries across the site.
- The FormSubmit form markup, POST destination, required fields, attachments, CAPTCHA configuration and redirect remain unchanged. No live test inquiry was submitted.

Run `python3 scripts/build-site-rfq-context.py` after adding pages or changing titles. Both Southco and Mil-Spec generators invoke it automatically after regeneration; they normalize inherited quote links before applying page-specific routes. Source/maintenance inputs remain excluded from Jekyll through _config.yml.

Validation: `node scripts/check-site-rfq-context.cjs`, `node scripts/check-southco-rfq.cjs` and `node scripts/check-rfq-reference-tracking.cjs` pass together. They cover all allowed page contexts, all 13 Southco part prefills, Mil-Spec routes, existing text, missing forms, invalid/prototype/external parameters, source attribution and quote-button coverage. Both generators produce stable output on repeated runs. Local HTML links/fragments and sitemap XML pass; the native form was compared byte-for-byte against the prior production form.
