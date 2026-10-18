/* Reference attribution only; preserve native FormSubmit submission. */
(function () {
  'use strict';
  const pages = /* REFERENCE_PAGES_START */{"Resources-Mil-Spec-Reference.html": {"title": "Mil-Spec fastener reference"}, "Reference-Family-machine-screws.html": {"title": "Machine Screws"}, "Reference-Family-socket-screws.html": {"title": "Socket Screws"}, "Reference-Family-washers.html": {"title": "Washers"}, "Reference-Family-nuts.html": {"title": "Nuts"}, "Reference-Family-hex-cap-screws.html": {"title": "Hex Cap Screws"}, "Reference-Family-shoulder-screws.html": {"title": "Shoulder Screws"}, "Reference-Family-pins.html": {"title": "Pins"}, "Reference-Family-rivets.html": {"title": "Rivets"}, "Reference-Family-threaded-inserts.html": {"title": "Threaded Inserts"}, "Reference-Family-set-screws.html": {"title": "Set Screws"}, "Reference-Family-retaining-rings.html": {"title": "Retaining Rings"}, "Reference-Family-spacers-standoffs.html": {"title": "Spacers & Standoffs"}, "Reference-Family-safety-wire.html": {"title": "Safety Wire"}, "Resources-Mil-Spec-Cross-Reference.html": {"title": "Mil-Spec specification cross-reference"}, "Reference-MS51576.html": {"title": "MS51576 precision shoulder screws"}, "Reference-MS51575.html": {"title": "MS51575 precision shoulder screws"}, "Reference-MS51830.html": {"title": "MS51830 keylocking inserts"}, "Reference-MS16555-MS16556.html": {"title": "MS16555 and MS16556 dowel pins"}, "Reference-MS16562.html": {"title": "MS16562 slotted spring pins"}, "Reference-AN960-NAS1149.html": {"title": "AN960 and NAS1149 washers"}, "Reference-MS35307-MS35308.html": {"title": "MS35307 and MS35308 hex cap screws"}, "Reference-MS20426-MS20470.html": {"title": "MS20426 and MS20470 solid rivets"}, "Reference-MS21042.html": {"title": "MS21042 self-locking nuts"}, "Reference-MS24665-MS20392.html": {"title": "MS24665 cotter and MS20392 headed pins"}, "Reference-MS51957.html": {"title": "MS51957 pan head machine screws"}, "Resources-Mil-Spec-Tables.html": {"title": "Mil-Spec technical tables"}, "Resources-Mil-Spec-Terminology.html": {"title": "Mil-Spec purchasing terminology"}, "Resources-Mil-Spec-RFQ-Checklist.html": {"title": "Mil-Spec RFQ checklist"}, "Resources-Mil-Spec-Materials-Finishes.html": {"title": "Mil-Spec materials and finishes"}, "Resources-Mil-Spec-Purchasing-FAQ.html": {"title": "Mil-Spec purchasing questions"}}/* REFERENCE_PAGES_END */;
  const form = document.querySelector('form.rfq-form');
  const script = document.currentScript;
  if (!form || !script || !script.src) return;
  const reference = new URL(window.location.href).searchParams.get('reference');
  if (!reference || !Object.prototype.hasOwnProperty.call(pages, reference)) return;
  const source = pages[reference];
  const pageURL = new URL('../' + reference, script.src);
  if (pageURL.origin !== window.location.origin) return;
  function field(name, value) {
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = name;
    input.value = value;
    form.appendChild(input);
  }
  field('rfq_reference_page', source.title);
  field('rfq_reference_url', pageURL.href);
}());
