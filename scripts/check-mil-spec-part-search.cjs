const fs = require('fs');
const path = require('path');
const assert = require('assert');
const root = path.resolve(__dirname, '..');
const {search} = require(path.join(root, 'assets/mil-spec-part-search.js'));
const index = JSON.parse(fs.readFileSync(path.join(root, 'assets/mil-spec-search-index.json')));
assert.equal(new Set(index.parts.map(p => p.part)).size, index.parts.length);
for (const part of ['MS51576-16', 'MS35338-40', 'MS35206-213', 'MS51957-124', 'MS24693C218']) {
  const result = search(index, part);
  assert(result.exact);
  assert.deepEqual(result.parts.map(p => p.part), [part]);
}
assert.equal(search(index, ' ms 51576 – 16 ').parts[0].part, 'MS51576-16');
assert.equal(search(index, 'MS51576').parts.length, 41);
assert.equal(search(index, 'MS35307').parts.length, 283);
assert.equal(search(index, 'MS51576-999').parts.length, 0);
assert.equal(search(index, 'MS51576-999').series[0].part, 'MS51576');
assert.equal(search(index, 'MS353070-303').series.length, 0);
assert.equal(search(index, 'NASM51576-16').parts.length, 0); // No assumed MS/NASM conversion.
assert.equal(search(index, '<script>alert(1)</script>').parts.length, 0);
assert.equal(search(index, '').parts.length, 0);
assert.equal(search(index, 'MS51576-16').parts[0].stocked, false);
assert.equal(search(index, 'MS35338-40').parts[0].stocked, true);
for (const item of [...index.parts, ...index.series]) {
  assert(/^(?:Reference|Resources)-[A-Za-z0-9-]+\.html$/.test(item.page));
  const html = fs.readFileSync(path.join(root, item.page), 'utf8');
  if (item.anchor) assert(html.includes('id="' + item.anchor + '"'), item.part);
}
const pages = fs.readdirSync(root).filter(p => /^(Reference-|Resources-Mil-Spec-)/.test(p) && p.endsWith('.html'));
pages.push('Products-Mil-Spec-Hardware.html');
for (const name of pages) {
  const html = fs.readFileSync(path.join(root, name), 'utf8');
  assert.equal((html.match(/id="mil-spec-part-search"/g) || []).length, 1, name);
  assert(html.includes('action="Resources-Mil-Spec-Part-Search.html"'), name);
}
console.log(index.parts.length + ' exact entries and ' + index.series.length + ' series pass normalization, exact matching, family fallback, stock distinctions, anchors and ' + pages.length + ' search forms.');
