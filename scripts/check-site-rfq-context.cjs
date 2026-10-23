const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const root=path.resolve(__dirname,'..');const pages=JSON.parse(fs.readFileSync(path.join(root,'scripts/rfq-site-context-pages.json')));
const scripts=['rfq-reference-tracking.js','southco-rfq.js','rfq-site-context.js'];
function run(query,initial='',hasForm=true,origin='https://www.websonfasteners.com',assetOrigin=origin){
 const fields=[],details={value:initial},form={appendChild(x){fields.push(x)}};const doc={currentScript:null,querySelector(s){return s==='form.rfq-form'?(hasForm?form:null):details},createElement(){return {}}};
 for(const script of scripts){doc.currentScript={src:assetOrigin+'/assets/'+script};vm.runInNewContext(fs.readFileSync(path.join(root,'assets',script),'utf8'),{URL,window:{location:{href:origin+'/Quote.html'+query,origin}},document:doc});}
 return {fields,details};
}
for(const [key,source] of Object.entries(pages)){
 const query='?context='+encodeURIComponent(key),r=run(query);assert.equal(r.details.value,source.prefill);assert(r.fields.some(f=>f.name==='rfq_source_url'&&f.value==='https://www.websonfasteners.com/'+key));assert.equal(run(query,'Already entered text').details.value,'Already entered text');assert.equal(run(query,'',false).fields.length,0);
}
for(const key of ['Reference-MS51957.html','Reference-MS51576.html','Reference-Family-washers.html']){const r=run('?reference='+key);assert.equal(r.details.value,pages[key].prefill);assert(r.fields.some(f=>f.name==='rfq_reference_page'));}
for(const p of JSON.parse(fs.readFileSync(path.join(root,'scripts/southco-data.json'))).parts){const r=run('?southco='+p.part);assert.equal(r.details.value,'Southco '+p.part+' - '+p.name+'\n');assert(r.fields.some(f=>f.name==='manufacturer_part_number'&&f.value===p.part));}
assert.equal(run('?southco=catalog').details.value,pages['Products-Southco.html'].prefill);
for(const part of ['MS51021-9','MS51021-10','MS51021-11','MS51021-21']){
 const query='?reference=Reference-MS51021.html&part='+part,r=run(query);
 assert.equal(r.details.value,part+' - MS51021 stainless cup-point set screw\n');
 assert(r.fields.some(f=>f.name==='rfq_source_url'&&f.value==='https://www.websonfasteners.com/Reference-MS51021.html'));
 assert.equal(run(query,'Customer specifications already entered').details.value,'Customer specifications already entered');
}
for(const part of ['MS51021-999','MS51021-9<script>','https://evil.test/','__proto__'])assert.equal(run('?reference=Reference-MS51021.html&part='+encodeURIComponent(part)).details.value,pages['Reference-MS51021.html'].prefill);
assert.equal(run('?context=index.html&part=MS51021-9').details.value,pages['index.html'].prefill);
const stockedGuides=JSON.parse(fs.readFileSync(path.join(root,'scripts/mil-spec-data.json'))).stocked_part_guides;
for(const [key,guide] of Object.entries(stockedGuides)){
 for(const part of guide.parts){
  const query='?reference='+encodeURIComponent(key)+'&part='+encodeURIComponent(part),r=run(query);
  assert.equal(r.details.value,part+' - '+guide.description+'\n');
  assert.equal(run(query,'Existing customer requirement').details.value,'Existing customer requirement');
  assert(r.fields.some(f=>f.name==='rfq_source_url'&&f.value==='https://www.websonfasteners.com/'+key));
 }
 assert.equal(run('?reference='+key+'&part=__proto__').details.value,pages[key].prefill);
}
const referenceGuides=JSON.parse(fs.readFileSync(path.join(root,'scripts/mil-spec-lookup-data.json'))).reference_part_guides;
for(const [key,guide] of Object.entries(referenceGuides)){
 for(const part of guide.parts){
  const query='?reference='+encodeURIComponent(key)+'&part='+encodeURIComponent(part);
  assert.equal(run(query).details.value,part+' - '+guide.description+'\n');
  assert.equal(run(query,'Customer drawing requirements').details.value,'Customer drawing requirements');
 }
 assert.equal(run('?reference='+key+'&part='+encodeURIComponent('<script>')).details.value,pages[key].prefill);
}
assert.equal(run('?reference=Reference-Keylocking-Insert-Comparison.html&part=MS35307-303').details.value,pages['Reference-Keylocking-Insert-Comparison.html'].prefill);
assert.equal(run('?reference=Reference-NAS671.html&part=NAS1291C4M').details.value,pages['Reference-NAS671.html'].prefill);
for(const key of ['__proto__','constructor','../secret.html','https://evil.test','Quote.html','missing.html']){const r=run('?context='+encodeURIComponent(key));assert.equal(r.details.value,'');assert.equal(r.fields.length,0);}
assert.equal(run('').details.value,'');assert.equal(run('').fields.length,0);assert.equal(run('?context=index.html','',true,'https://www.websonfasteners.com','https://evil.test').fields.length,0);
for(const key of Object.keys(pages)){
 const html=fs.readFileSync(path.join(root,key),'utf8');for(const match of html.matchAll(/href="(Quote\.html[^" ]*)"/g))assert(/[?](?:context|reference|southco)=/.test(match[1]),key+': '+match[1]);
}
console.log(Object.keys(pages).length+' pages pass prefill, preserved customer text, source attribution and complete quote-link coverage. Mil-Spec and all 13 Southco routes pass together. Direct/invalid/external visits remain blank.');
