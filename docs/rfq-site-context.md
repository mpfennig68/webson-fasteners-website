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

## Submission handoff feedback

October 19 follow-up: user reports approximately 30 seconds after pressing Submit Request before FormSubmit's CAPTCHA page appears, followed by normal email receipt. The form POST remains a direct browser navigation. Existing autofill scripts have no submit handlers, network calls or timers that could delay the POST. This points toward the external submission/verification handoff, but no live POST timing trace was captured and the root cause remains unconfirmed.

Quote.html adds a preconnect/DNS hint to formsubmit.co to begin connection setup while the buyer fills out the form. This may reduce initial connection overhead; it is not a guarantee against FormSubmit's processing delay. A small passive submit listener displays immediate verification-navigation feedback, updates the message after ten seconds, and clears the status when returning with the Back button. It never calls preventDefault, disables the submitter, invokes fetch, replaces the POST or changes CAPTCHA behavior. Invalid forms do not fire the submit handler. No test inquiry was sent.

The entire highlighted Southco manufacturer cell on Products.html is now a direct anchor to Products-Southco.html, including its padding and arrow. It stays a normal keyboard-accessible link.

## CAPTCHA disabled at user request

October 19, 2026: the user explicitly requested removing the checkbox and will reconsider if spam increases. Quote.html now sends `_captcha=false` and includes the FormSubmit `_honey` text input, hidden with CSS, excluded from keyboard navigation and autocomplete. A nonempty honeypot is discarded by FormSubmit. Submission feedback now says Sending rather than promising a verification screen. The POST action, encoding, existing fields, attachments, thank-you redirect, source attribution and autofill remain unchanged. No live inquiry was sent.

Manufacturer/provider documentation checked: https://formsubmit.co/documentation . Disabling CAPTCHA removes the normal checkbox step but does not guarantee provider processing time. To restore CAPTCHA, remove the `_captcha=false` hidden input (or set it to true); the honeypot can remain. Restore checkbox-specific messaging only when restoring CAPTCHA.
