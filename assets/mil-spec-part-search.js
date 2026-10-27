/* Search only the published reference index; availability is confirmed by quotation. */
(function () {
  'use strict';
  function compact(value) { return value.toUpperCase().replace(/[\u2010-\u2015]/g, '-').replace(/\s+/g, ''); }
  function search(index, value) {
    const query = compact(value);
    const exact = index.parts.find(function (item) { return compact(item.part) === query; });
    if (exact) return { parts: [exact], series: [], exact: true };
    const standard = query.match(/^((?:NASM|NAS|MS|AN|AS)\d+)([-A-Z0-9.]*)$/);
    if (standard) {
      const series = index.series.filter(function (item) { return item.part === standard[1]; });
      const browse = !standard[2] || standard[2] === '-';
      return { parts: browse ? index.parts.filter(function (item) { return item.series === standard[1]; }) : [], series: series, exact: false, unlisted: !browse };
    }
    const terms = value.toUpperCase().replace(/[\u2010-\u2015]/g, '-').trim().split(/\s+/).filter(Boolean);
    if (!terms.length) return { parts: [], series: [], exact: false };
    function matches(item) { const text = (item.part + ' ' + item.summary).toUpperCase(); return terms.every(function (term) { return text.includes(term); }); }
    return { parts: index.parts.filter(matches), series: index.series.filter(matches), exact: false };
  }
  if (typeof module === 'object' && module.exports) module.exports = { search: search, compact: compact };
  if (typeof document === 'undefined') return;
  const output = document.querySelector('[data-part-search-results]');
  if (!output) return;
  const status = document.querySelector('[data-part-search-status]');
  const field = document.querySelector('#mil-spec-part-search');
  const query = (new URL(window.location.href).searchParams.get('q') || '').trim().slice(0, 100);
  field.value = query;
  if (!query) { status.textContent = 'Enter a part number or series above to search the reference tables.'; return; }
  status.textContent = 'Searching the Mil-Spec references…';
  const indexURL = new URL('mil-spec-search-index.json', document.currentScript.src);
  function link(text, page, item) {
    const a = document.createElement('a');
    a.textContent = text;
    if (!/^(?:Reference|Resources)-[A-Za-z0-9-]+\.html$/.test(page)) return a;
    a.href = page + (item ? '?part=' + encodeURIComponent(item.part) + '#' + item.anchor : '');
    return a;
  }
  fetch(indexURL).then(function (response) {
    if (!response.ok) throw new Error('Index unavailable');
    return response.json();
  }).then(function (index) {
    const result = search(index, query);
    status.textContent = result.exact ? '1 exact part match for “' + query + '”.' : result.unlisted ? 'No exact part entry is listed for “' + query + '”.' : result.parts.length + ' listed part matches for “' + query + '”.';
    const familyLinks = document.createElement('div');
    familyLinks.className = 'ref-search-family-links';
    result.series.slice(0, 12).forEach(function (item) { familyLinks.appendChild(link(item.part + ' family guide →', item.page)); });
    output.appendChild(familyLinks);
    if (!result.parts.length) {
      const p = document.createElement('p');
      p.textContent = result.series.length ? 'The family guide may help identify this requirement. Send Webson the complete part number to review unlisted sizes.' : 'This entry is not in the reference index. Browse the series directory or send Webson the complete part number for review.';
      output.appendChild(p);
    }
    const list = document.createElement('ul');
    list.className = 'ref-search-results';
    output.appendChild(list);
    let shown = 0;
    const more = document.createElement('button');
    more.type = 'button'; more.className = 'ref-clear'; more.textContent = 'Show more matches';
    function showMore() {
      result.parts.slice(shown, shown + 40).forEach(function (item) {
        const li = document.createElement('li');
        li.appendChild(link(item.part + ' →', item.page, item));
        const quote = document.createElement('a');
        quote.className = 'ref-search-quote'; quote.textContent = 'Request quote →';
        quote.href = 'Quote.html?reference=Resources-Mil-Spec-Part-Search.html&part=' + encodeURIComponent(item.part);
        quote.setAttribute('aria-label', 'Request a quote for ' + item.part);
        li.appendChild(quote);
        const detail = document.createElement('p'); detail.textContent = item.summary; li.appendChild(detail);
        const note = document.createElement('span'); note.className = 'ref-search-stock-note';
        note.textContent = item.stocked ? 'Selected stocked part — confirm current availability.' : 'Reference size — request availability.';
        li.appendChild(note); list.appendChild(li);
      });
      shown = Math.min(shown + 40, result.parts.length);
      more.hidden = shown >= result.parts.length;
    }
    showMore();
    more.addEventListener('click', showMore);
    output.appendChild(more);
  }).catch(function () { status.textContent = 'Part search could not load. Use the series directory below or contact Webson with the complete part number.'; });
}());
