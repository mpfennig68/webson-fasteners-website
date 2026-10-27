"""Render selected plain-nut references without creating inventory claims."""
import json
DATA=json.loads((W/'scripts/mil-spec-additional-nut-data.json').read_text())
COPY={
 'MS35649':{
  'name':'coarse-thread hex machine-screw nuts',
  'identity':'MS35649 covers plain hexagon machine-screw nuts with UNC-2B internal threads. This selection includes 37 material and finish configurations from 2-56 through 3/8-16. These are plain nuts; they do not provide the prevailing-torque locking feature found in the MS21042 or MS21044 families.',
  'example':'MS35649-222 is a 2-56 carbon-steel nut with cadmium plating; MS35649-224 is the passivated CRES version. MS35649-225B identifies brass with black oxide, while MS35649-225T identifies tin-plated brass. The finish letter is part of the designation.',
  'compare':'MS35650 is the fine-thread machine-screw nut family. MS51967 is a finished hex nut family with separate strength grades and thickness requirements. For example, MS35649-2252 and MS51967-2 both have 1/4-20 threads, but their thickness limits differ.',
  'related':['MS35650','MS51967','MS21042'],
 },
 'MS35650':{
  'name':'fine-thread hex machine-screw nuts',
  'identity':'MS35650 covers plain hexagon machine-screw nuts with UNF-2B internal threads. This selection includes 50 material and finish configurations from 0-80 through 5/8-18. The dimensional table uses MS35650G Amendment 1, which replaces the original Table I.',
  'example':'MS35650-322 is a 2-64 carbon-steel nut with cadmium plating; MS35650-324 is passivated CRES. MS35650-325B identifies brass with black oxide, while MS35650-325T identifies tin-plated brass. A 4-48 thread belongs to this fine-thread family; it must not be confused with 4-40.',
  'compare':'MS35649 is the coarse-thread machine-screw nut family. MS51968 is a finished hex nut family with separate grade and thickness requirements. The amended MS35650 width limits must be checked within this issue; they should not be copied from the coarse-thread table.',
  'related':['MS35649','MS51968','MS51958'],
 },
 'MS51967':{
  'name':'coarse-thread finished hex nuts',
  'identity':'MS51967 identifies plain hexagon carbon-steel nuts with cadmium plating and UNC-2B internal threads. This table selects 20 Grade B and Grade C references from 1/4-20 through 1-8. Canceled Grade A dash numbers are omitted.',
  'example':'MS51967-2 and MS51967-3 both have 1/4-20 threads and the same listed dimensional limits. The dash numbers distinguish Grade B from Grade C. MS51967-14 is a 1/2-13 Grade B reference; MS51967-15 is Grade C. Keep the required grade with the complete part number.',
  'compare':'MS51968 uses fine internal threads. MS35649 is a machine-screw nut family with a different thickness envelope. A shared hex shape or nominal thread does not establish that the families have the same strength or geometry.',
  'related':['MS51968','MS35649','NAS671'],
 },
 'MS51968':{
  'name':'fine-thread finished hex nuts',
  'identity':'MS51968 identifies plain hexagon carbon-steel nuts with cadmium plating and UNF-2B internal threads. This table selects 20 Grade B and Grade C references from 1/4-28 through 1-12. Canceled Grade A dash numbers are omitted.',
  'example':'MS51968-2 is a 1/4-28 Grade B reference; MS51968-3 is Grade C. MS51968-14 is a 1/2-20 Grade B reference; MS51968-15 is Grade C. The diameter and grade can match a coarse-thread nut while the pitch remains different.',
  'compare':'MS51967 uses coarse internal threads. MS35650 is a fine-thread machine-screw nut family with its own thickness limits. Confirm the complete thread, grade, material, finish and dimensional envelope when reviewing a requirement.',
  'related':['MS51967','MS35650','NAS671'],
 }
}
for root,data in DATA.items():
 copy=COPY[root];file='Reference-'+root+'.html'
 rows=[]
 for r in data['rows']:
  link='Quote.html?reference='+file+'&amp;part='+h(r['part'])
  rows.append({'cells':[h(r['part']),h(r['thread']),h(r['material_finish']),h(r['across_flats_limits']),h(r['thickness_limits']),'<a href="'+link+'">Quote '+h(r['part'])+' →</a>'],'family':r['material_finish']})
 table='<p>Reference selections for identification and quotation. Webson confirms availability by inquiry; these rows do not indicate stocked inventory.</p>'
 table+=filtered(['Part number','Thread','Material / finish','Width across flats limits (in)','Thickness limits (in)','Request pricing'],rows,root+' reference nut dimensions',list(dict.fromkeys(r['material_finish']for r in data['rows'])),'Material / finish')
 table+='<p>Dimensions are minimum–maximum limits in inches from the reviewed reference. Width across flats is the distance between opposite hex faces; thickness is the nut’s axial height. Across-flats limits describe the part, not the tolerance of a wrench or socket.</p>'
 if root in ['MS35649','MS35650']:
  finish='The selected carbon-steel dash numbers distinguish cadmium plating from phosphate coating; neither uses an added finish letter. The CRES rows are passivated. Brass rows use B for black oxide or T for tin plating. Other configurations in the standard are outside this selection. Preserve all finish letters instead of reducing the order to a bare dash number.'
 else:
  finish='The selected rows are cadmium-plated carbon steel in Grade B or Grade C. The reviewed specification requires finished nuts to meet the proof-load requirements of its procurement specification. The grade letters belong to the material classification; the listed ordering number uses the MS series and dash number. Do not infer proof load from dimensions alone.'
 links=[(other+' reference','Reference-'+other+'.html')for other in copy['related']]+[('All nut families','Reference-Family-nuts.html')]
 guide(file,root+' Nuts | Thread Sizes & Dimensions',root+' '+copy['name']+'.','Find '+root+' nut part numbers, thread sizes, material and finish details, thickness and hex dimensions. Filter the table and request pricing for a selected part.',[
  ('Identify the nut family','<p>'+copy['identity']+'</p>','PART IDENTIFICATION'),
  (root+' part-number and dimension table',table,'REFERENCE SIZES'),
  ('Read the complete part number','<p>'+copy['example']+'</p>','ORDERING EXAMPLES'),
  ('Retain the material and finish requirement','<p>'+finish+'</p>','MATERIAL AND FINISH'),
  ('Compare related nut families','<p>'+copy['compare']+'</p>'+chips(links),'FAMILY COMPARISON'),
  ('Match the governing specification issue','<p>Dimensions summarize '+h(data['reviewed_issue'])+'.</p><p>'+h(data['status_note'])+'</p><p>Include the complete designation, quantity, required delivery date and certificate or traceability requirements with your inquiry.</p>','DRAWING REQUIREMENTS')])
