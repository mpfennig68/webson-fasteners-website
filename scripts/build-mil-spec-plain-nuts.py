"""Render reviewed plain-nut selections with explicit material and thread class."""
import json
DATA=json.loads((W/'scripts/mil-spec-plain-nut-data.json').read_text())
COPY={
 'MS51972':{
  'name':'stainless fine-thread hex nuts',
  'identity':'MS51972 identifies plain hexagon nuts in passivated 300-series corrosion-resisting steel with UNF-2B internal threads. The table covers all 14 reviewed Table I selections from 1/4-28 through 1-1/2-12. These are plain nuts; the family does not provide a prevailing-torque locking feature.',
  'ordering':'MS51972-1 identifies a 1/4-28 nut; MS51972-5 is 1/2-20. At 7/16-20, MS51972-4 has a 0.6750–0.6875-inch width across flats. Do not copy the smaller hex-head dimensions of a similarly sized cap screw into the nut requirement.',
  'material':'The reviewed issue specifies 300-series corrosion-resisting steel and passivation. The family number alone does not identify a particular 300-series grade. Include any specific material, finish and certification requirement with the inquiry.',
  'comparison':'MS51968 is a cadmium-plated carbon-steel fine-thread family with its own grade requirements. MS35650 is a fine-thread machine-screw nut family. Matching a nominal thread does not establish equal material, strength, thickness or wrench clearance.',
  'scope':'Dimensions identify the reviewed historical A issue. A document succession or an old cross-reference table does not by itself authorize a change to a complete ordering designation.',
  'related':['MS51968','MS35650','MS35690']},
 'MS35690':{
  'name':'plain hex nuts by grade and finish',
  'identity':'MS35690 covers plain hexagon nuts with UNC-2B or UNF-2B threads and multiple material/finish configurations. This selected table contains the nine references listed in Table II, Active for New Design, of the reviewed F issue. The F cover reactivates the specification in 2005; individual part-number status still depends on its table.',
  'ordering':'MS35690-424 is a 1/4-28 Grade B carbon-steel nut, uncoated; MS35690-427 is Grade C. MS35690-413 is a 1/4-28 nickel-plated brass nut. MS35690-613 is the nickel-plated brass 3/8-16 selection, while -633 is 3/8-24. Keep the material, finish and thread together with the dash number.',
  'material':'The selected carbon-steel nuts are uncoated Grade B or Grade C. The selected brass nuts are nickel plated. Grade B and Grade C are nut material classifications under the procurement requirements; do not relabel them as Grade 5 or Grade 8 bolts or infer proof load from the hex dimensions.',
  'comparison':'The reviewed F issue also contains Table III inactive-for-new-design references and Table IV canceled references. Those entries are outside this selection. Reactivating the family does not reactivate every historical dash number. MS51967/MS51968 and MS51972 have separate material, finish and thread requirements.',
  'scope':'The selected ordering rows come from Table II and use Table I dimensions. Other historical dash numbers, cancellation mappings and possible replacements require separate review against the governing issue.',
  'related':['MS51967','MS51968','MS51972']},
 'MS25082':{
  'name':'thin electrical hex nuts',
  'identity':'MS25082 identifies thin electrical plain hex nuts with several thread series and hex envelopes. This table selects 50 steel/cadmium and 303-stainless/passivated configurations from the reviewed 2004 Amendment 1 table. The complete designation includes any material letter after the hyphen. Brass configurations are outside this selection.',
  'ordering':'MS25082-3 and MS25082-12 both use 10-32 UNF-2B threads, but their widths across flats are 0.362–0.375 and 0.241–0.250 inch respectively. MS25082-C3 preserves the -3 geometry while selecting passivated 303 stainless. A common thread alone does not identify the same hex envelope.',
  'material':'The selected bare numeric dash numbers identify cadmium-plated steel. C followed by the size dash number identifies passivated Type 303 stainless steel in the reviewed table. Preserve the C: MS25082-1 and MS25082-C1 are different material/finish configurations. Include the required coating specification and issue with the quote.',
  'comparison':'Thickness matters even when the thread and hex match. MS25082-7 and -20 both have 3/8-32 UNEF-2B threads and the same across-flats limits, but use 0.078 and 0.093-inch nominal thicknesses, each with ±0.005-inch tolerance. The 0.4688-32 entries retain the drawing’s decimal nominal thread reference; do not round that callout to another nominal size.',
  'scope':'This page identifies the historical 2004 dimensional issue reviewed. A 2011 amendment and later validation notices exist; verify the issue required by your drawing or purchase order. A validation date is separate from the dimensional-issue date. Canceled -9 selections are not included.',
  'related':['MS35649','MS35650','MS51972']}
}
for root,data in DATA.items():
 c=COPY[root];file='Reference-'+root+'.html'
 rows=[]
 for r in data['rows']:
  rows.append({'cells':[h(r[k])for k in ['part','thread','thread_class','material_finish','across_flats_limits','thickness_limits']]+['<a href="Quote.html?reference='+file+'&amp;part='+h(r['part'])+'">Quote '+h(r['part'])+' →</a>'],'family':r['material_finish']})
 body='<p>Reference selections for purchasing identification and quotation. Webson confirms availability by inquiry; these rows do not indicate stocked inventory.</p>'
 body+=filtered(['Part number','Thread','Thread series / class','Material / finish','Width across flats limits (in)','Thickness limits (in)','Request pricing'],rows,root+' reference nut dimensions',list(dict.fromkeys(r['material_finish']for r in data['rows'])),'Material / finish')
 body+='<p>Dimensions are minimum–maximum limits in inches. Width across flats describes the nut, not the tolerance of a wrench or socket. Thickness is the nut’s axial height.</p>'
 if root=='MS25082':body+='<p>The thickness limits shown are calculated from the reviewed H nominal value and its ±0.005-inch tolerance. Across-flats values are the table’s listed minimum and maximum dimensions.</p>'
 guide(file,root+' Nuts | Thread Sizes & Dimensions',root+' '+c['name']+'.','Find '+root+' part numbers, thread classes, material and finish details, thickness and hex dimensions. Filter the reference table and request pricing.',[
 ('Identify the nut and its configuration','<p>'+c['identity']+'</p>','PART IDENTIFICATION'),
 (root+' part-number and dimension table',body,'REFERENCE SIZES'),
 ('Read the complete designation','<p>'+c['ordering']+'</p>','ORDERING EXAMPLES'),
 ('Preserve the material and finish','<p>'+c['material']+'</p>','MATERIAL AND FINISH'),
 ('Compare thread, envelope and part status','<p>'+c['comparison']+'</p>'+chips([(r+' reference','Reference-'+r+'.html')for r in c['related']]+[('Nut family directory','Reference-Family-nuts.html')]),'FAMILY COMPARISON'),
 ('Match the governing drawing issue','<p>Dimensions summarize '+h(data['reviewed_issue'])+'.</p><p>'+c['scope']+'</p><p>The controlling drawing and specification determine full dimensions, material, coating, inspection and documentation requirements. Include the quantity, required delivery date and controlling issue with your inquiry.</p>','DRAWING REQUIREMENTS')])
