"""Selected carbon-steel flat- and drilled fillister-head screw references."""
import json
DATA=json.loads((W/'scripts/mil-spec-head-style-data.json').read_text())
COPY={
 'MS35190':{
  'name':'coarse-thread 82-degree flat-head screws',
  'identity':'MS35190 identifies cross-recessed, 82-degree flat countersunk-head machine screws in cadmium-plated carbon steel with UNC-2A threads. This selection covers 119 plain-screw references from 2-56 through 3/8-16. The reviewed drawing’s asterisked inactive-for-new-design #1 and 7/16-inch entries are outside this selection.',
  'example':'MS35190-221 identifies a 4-40 screw with a 0.250-inch overall reference length. MS35190-267 is a 10-24 by 0.250-inch reference. Dash numbers belong to this series; they cannot be reused as size codes for another MS family.',
  'related':['MS35191','MS51959','MS24693'],
 },
 'MS35191':{
  'name':'fine-thread 82-degree flat-head screws',
  'identity':'MS35191 identifies cross-recessed, 82-degree flat countersunk-head machine screws in cadmium-plated carbon steel with UNF-2A threads. This selection includes 122 plain-screw references across 0-80 and #2 through 3/8-inch sizes. The reviewed drawing’s asterisked #1 and 7/16-inch entries are omitted.',
  'example':'MS35191-224 identifies a 4-48 screw with a 0.250-inch overall reference length. MS35191-268 is a 10-32 by 0.250-inch reference. Compare these with the coarse threads of MS35190; matching length and head angle do not establish the same part.',
  'related':['MS35190','MS51960','MS35207'],
 },
 'MS35265':{
  'name':'coarse-thread drilled fillister-head screws',
  'identity':'MS35265 identifies slotted, drilled fillister-head machine screws in carbon steel with UNC-2A threads. The reviewed revision C specifies cadmium plating. This table covers 119 unsuffixed references from 2-56 through 3/8-16.',
  'example':'MS35265-17 identifies a 4-40 screw with a 0.50-inch under-head reference length. MS35265-63 is a 10-24 by 0.50-inch reference. The drilled head and slotted drive are part of the configuration; retain them in a purchasing comparison.',
  'related':['MS35266','MS35206','MS35190'],
 },
 'MS35266':{
  'name':'fine-thread drilled fillister-head screws',
  'identity':'MS35266 identifies slotted, drilled fillister-head machine screws in carbon steel with UNF-2A threads. The reviewed revision C specifies cadmium plating. This table covers 119 unsuffixed references from 2-64 through 3/8-24.',
  'example':'MS35266-17 identifies a 4-48 screw with a 0.50-inch under-head reference length. MS35266-63 is a 10-32 by 0.50-inch reference. Although the selected dash-number layout matches MS35265, the thread pitches differ.',
  'related':['MS35265','MS35207','MS35191'],
 }
}
for root,data in DATA.items():
 copy=COPY[root];file='Reference-'+root+'.html';flat=data['kind']=='flat'
 fields=['thread','length']+(['head_diameter_max','head_angle']if flat else['head_diameter_limits','total_head_height_limits'])
 headers=['Part number','Thread','Length per drawing (in)']+(['Sharp head diameter max (in)','Nominal head angle']if flat else['Head diameter limits (in)','Total head height limits (in)'])+['Request pricing']
 rows=[]
 for r in data['rows']:
  link='Quote.html?reference='+file+'&amp;part='+h(r['part'])
  rows.append([h(r['part'])]+[h(r[f])for f in fields]+['<a href="'+link+'">Quote '+h(r['part'])+' →</a>'])
 table='<p>Reference sizes for identification and quotation. Availability is confirmed by inquiry; the entries do not indicate Webson stock.</p>'+filtered(headers,rows,root+' reference screw dimensions')
 if flat:
  table+='<p>Head diameter is the maximum theoretical sharp-head diameter from the reviewed drawing, not the minimum finished head diameter. The head angle is nominally 82 degrees, with drawing limits of 80–82 degrees. Short screws can have undercut heads with separate height requirements.</p>'
  measurement='Length L includes the countersunk head. The length column preserves the decimal reference values printed in the reviewed table, including 0.125, 0.188 and 0.312. These are not added acceptance tolerances. Match the 82-degree head to the specified seat; MS24693 uses a different 100-degree head.'
  finish='The reviewed issue specifies carbon steel and Type II, Class 3 cadmium plating to QQ-P-416 or MIL-C-81562. The table lists plain screws. An L after the dash number identifies a self-locking version under the reviewed requirements. Preserve the complete locking callout and its required issue when requesting pricing.'
  extra=[]
 else:
  table+='<p>Head diameter and total head height are minimum–maximum limits from the reviewed revision C. Total axial head height O includes the domed portion. It differs from the straight head-side height H listed in the detail table.</p>'
  measurement='Length L is measured from the bearing surface beneath the head to the tip. The length column preserves the decimal reference values in the reviewed drawing, including 0.12, 0.19 and 0.62. Total head height O is a separate axial measurement and is not included in L. Use the governing issue for length tolerances and full thread-length requirements.'
  finish='The reviewed revision C specifies carbon steel with cadmium plating to QQ-P-416, Type II, Class 3. Its part-number format is the basic MS number plus the dash number. The drilled hole is approximately perpendicular to the slot; the reviewed notes permit it to break through the bottom of the slot. Head drilling does not change the under-head length convention.'
  gfields=['thread','head_side_height_limits','slot_width_limits','drilled_hole_diameter_nominal']
  geometry=filtered(['Thread','Head-side height H limits (in)','Slot width limits (in)','Drilled hole diameter nominal (in)'],[[h(r[f])for f in gfields]for r in data['head_geometry']],root+' head and drive dimensions')
  extra=[('Slotted drive and drilled-head details',geometry+'<p>H is the axial height of the straight head side, while O in the part table is the total axial head height. The hole diameter is nominal; the other dimensions shown here are limits. Use the full specification for drilling location, slot depth and acceptance requirements.</p>','HEAD DETAILS')]
 issue_note='Dimensions summarize '+data['reviewed_issue']+'. These selected historical values identify the reviewed issue; the specification required by your drawing governs the supplied part.'
 if root=='MS35265':issue_note+=' Later MS35265 revisions exist. Include the required issue with your inquiry so its dimensions and coating requirements can be reviewed.'
 guide(file,root+' Screws | Thread Sizes & Dimensions',root+' '+copy['name']+'.','Look up '+root+' part numbers, threads, lengths and head dimensions. Filter the reference table and request a quote for the selected screw.',[
  ('Identify the head, drive and thread','<p>'+copy['identity']+'</p>','PART IDENTIFICATION'),
  (root+' part-number and dimension table',table,'REFERENCE SIZES'),
  *extra,
  ('Measure the correct length','<p>'+measurement+'</p>','LENGTH CONVENTION'),
  ('Read the part number within its family','<p>'+copy['example']+'</p>','ORDERING EXAMPLES'),
  ('Preserve the finish and configuration','<p>'+finish+'</p>','MATERIAL AND CONFIGURATION'),
  ('Compare related screw families',chips([(other+' reference','Reference-'+other+'.html')for other in copy['related']]+[('Machine-screw directory','Reference-Family-machine-screws.html')]),'RELATED REFERENCES'),
  ('Match the governing drawing issue','<p>'+h(issue_note)+'</p>','DRAWING REQUIREMENTS')])
