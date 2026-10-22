const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const root=path.resolve(__dirname,'..');
const script=fs.readFileSync(path.join(root,'assets/rfq-reference-tracking.js'),'utf8');
const pages=JSON.parse(fs.readFileSync(path.join(root,'scripts/mil-spec-build-summary.json'))).pages;
function run(url,hasForm=true,asset='https://www.websonfasteners.com/assets/rfq-reference-tracking.js') {
 const fields=[];const form={appendChild(el){fields.push(el)}};
 vm.runInNewContext(script,{URL,window:{location:{href:url,origin:new URL(url).origin}},document:{currentScript:{src:asset},querySelector(){return hasForm?form:null},createElement(){return {}}}});
 return fields;
}
for (const page of pages) {
 const f=run('https://www.websonfasteners.com/Quote.html?reference='+encodeURIComponent(page));
 assert.equal(f.length,2);assert.equal(f[0].name,'rfq_reference_page');assert(f[0].value);
 assert.equal(f[1].name,'rfq_reference_url');assert.equal(f[1].value,'https://www.websonfasteners.com/'+page);
 assert(f.every(x=>x.type==='hidden'));
}
for(const reference of ['', 'https://evil.test/', '../Quote.html','__proto__','constructor','<script>alert(1)</script>','Resources-Mil-Spec-Sources.html']) assert.equal(run('https://www.websonfasteners.com/Quote.html?reference='+encodeURIComponent(reference)).length,0);
assert.equal(run('https://www.websonfasteners.com/Quote.html').length,0);
assert.equal(run('https://www.websonfasteners.com/Quote.html?reference='+pages[0],false).length,0);
assert.equal(run('https://www.websonfasteners.com/Quote.html?reference='+pages[0],true,'https://other.test/assets/rfq-reference-tracking.js').length,0);
assert.equal(run('https://www.websonfasteners.com/Quote.html?reference='+pages[0]+'&reference=bad').length,2);
console.log('All '+pages.length+' source pages produce two named RFQ fields. Direct visits, missing forms, invalid/external inputs and cross-origin assets are ignored.');
