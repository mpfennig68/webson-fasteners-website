/* Progressive enhancement: the complete directory is readable without JavaScript. */
(function () {
  'use strict';
  const table = document.querySelector('[data-reference-table]');
  const controls = document.querySelector('[data-reference-filters]');
  if (!table || !controls) return;
  const search = controls.querySelector('[data-reference-search]');
  const family = controls.querySelector('[data-reference-family]');
  const clear = controls.querySelector('[data-reference-clear]');
  const count = document.querySelector('[data-reference-count]');
  const empty = document.querySelector('[data-reference-empty]');
  const rows = Array.from(table.querySelectorAll('tbody tr'));
  function normalize(value) {
    return value.toLowerCase().replace(/[\u2010-\u2015]/g, '-').trim();
  }
  function update() {
    const terms = normalize(search.value).split(/\s+/).filter(Boolean);
    const selected = family ? family.value : '';
    let visible = 0;
    rows.forEach(function (row) {
      const text = normalize(row.dataset.search || row.textContent);
      const show = (!selected || row.dataset.family === selected) && terms.every(function (term) { return text.includes(term); });
      row.hidden = !show;
      if (show) visible += 1;
    });
    count.textContent = visible + ' of ' + rows.length + ' series shown';
    empty.hidden = visible !== 0;
  }
  controls.hidden = false;
  search.addEventListener('input', update);
  if (family) family.addEventListener('change', update);
  clear.addEventListener('click', function () {
    search.value = '';
    if (family) family.value = '';
    update();
    search.focus();
  });
  update();
}());
