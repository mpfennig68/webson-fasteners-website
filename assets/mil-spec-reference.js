/* Keep the HTML index and tables readable when scripting is unavailable. */
(function () {
  'use strict';
  document.querySelectorAll('[data-reference-block]').forEach(function (block) {
    const table = block.querySelector('[data-reference-table]');
    const controls = block.querySelector('[data-reference-filters]');
    if (!table || !controls) return;
    const search = controls.querySelector('[data-reference-search]');
    const family = controls.querySelector('[data-reference-family]');
    const columns = Array.from(controls.querySelectorAll('[data-reference-column]'));
    const clear = controls.querySelector('[data-reference-clear]');
    const count = block.querySelector('[data-reference-count]');
    const empty = block.querySelector('[data-reference-empty]');
    const rows = Array.from(table.querySelectorAll('tbody tr'));
    const keys = rows.map(function (row) { return normalize(row.cells[0].textContent); });
    function normalize(value) {
      return value.toLowerCase().replace(/[\u2010-\u2015]/g, '-').trim();
    }
    function update() {
      const query = normalize(search.value);
      const terms = query.split(/\s+/).filter(Boolean);
      const selected = family ? family.value : '';
      let exact = keys.indexOf(query);
      // A complete part can locate its series when only a series guide is indexed.
      if (exact === -1 && /^(?:an|ms|nas|nasm|as)\d+[-a-z0-9]*$/.test(query)) {
        let length = 0;
        keys.forEach(function (key, index) {
          if (/^(?:an|ms|nas|nasm|as)\d+$/.test(key) && query.startsWith(key) && !/\d/.test(query.charAt(key.length)) && key.length > length) {
            exact = index;
            length = key.length;
          }
        });
      }
      let visible = 0;
      rows.forEach(function (row, index) {
        const text = normalize((row.dataset.search || '') + ' ' + row.textContent);
        const matches = exact !== -1 ? index === exact : terms.every(function (term) { return text.includes(term); });
        const sizeMatch = columns.every(function (filter) {
          return !filter.value || row.cells[Number(filter.dataset.referenceColumn)].textContent.trim() === filter.value;
        });
        const show = (!selected || row.dataset.family === selected) && matches && sizeMatch;
        row.hidden = !show;
        if (show) visible += 1;
      });
      count.textContent = visible + ' of ' + rows.length + ' entries shown';
      empty.hidden = visible !== 0;
    }
    controls.hidden = false;
    search.addEventListener('input', update);
    if (family) family.addEventListener('change', update);
    columns.forEach(function (filter) { filter.addEventListener('change', update); });
    clear.addEventListener('click', function () {
      search.value = '';
      if (family) family.value = '';
      columns.forEach(function (filter) { filter.value = ''; });
      update();
      search.focus();
    });
    update();
  });
}());
