const fs=require('fs'),vm=require('vm'),assert=require('assert');
const path=require('path'),root=path.resolve(__dirname,'..');
const code=fs.readFileSync(path.join(root,'assets/southco-rfq.js'),'utf8');
const parts=JSON.parse(fs.readFileSync(path.join(root,'scripts/southco-data.json'),'utf8')).parts;
function run(key,text='',hasForm=true,asset='https://www.websonfasteners.com/assets/southco-rfq.js'){
 const fields=[],details={value:text};
 vm.runInNewContext(code,{URL,window:{location:{href:'https://www.websonfasteners.com/Quote.html'+(key===null?'':'?southco='+encodeURIComponent(key)),origin:'https://www.websonfasteners.com'}},document:{currentScript:{src:asset},querySelector(s){return s==='form.rfq-form'?(hasForm?{appendChild(x){fields.push(x)}}:null):details},createElement(){return {}}}});
 return {fields,details};
}
for(const p of parts){const r=run(p.part);assert.equal(r.fields.length,3);assert.equal(r.fields[1].value,'Southco');assert.equal(r.fields[2].value,p.part);assert.equal(r.fields[0].value,'https://www.websonfasteners.com/Southco-'+p.part+'.html');assert(r.details.value.includes(p.part));assert.equal(run(p.part,'Customer text').details.value,'Customer text');assert.equal(run(p.part,'',false).fields.length,0);}
assert.equal(run('catalog').fields.length,1);assert.equal(run('catalog').details.value,'');
for(const key of [null,'','__proto__','constructor','../../secret','https://evil.test','<script>','12-11020-13-P'])assert.equal(run(key).fields.length,0);
assert.equal(run(parts[0].part,'',true,'https://evil.test/southco-rfq.js').fields.length,0);
console.log('All 13 Southco parts pass attribution, prefill, existing-text retention, missing-form, invalid-input and origin checks. Catalog adds source attribution only.');
