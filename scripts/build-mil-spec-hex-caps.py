"""Reviewed Grade 5/8 hex cap screw references; no inventory additions."""
import json
DATA=json.loads((W/'scripts/mil-spec-hex-cap-data.json').read_text())
for root,data in DATA.items():
 file='Reference-'+root+'.html';grade=data['grade'];coarse=data['thread_series']=='UNC-2A'
 scope='129 selected references across 1/4 through 3/4-inch diameters'if grade=='5'else'97 selected references across 1/4, 5/16, 3/8, 1/2, 5/8 and 3/4-inch diameters'
 identity=root+' identifies '+('medium-carbon-steel Grade 5'if grade=='5'else'alloy-steel Grade 8')+' hexagon-head cap screws with '+data['thread_series']+' threads. The reviewed issue specifies '+data['coating']+' parts. The table covers '+scope+', with listed under-head lengths through 3.000 inches.'
 if grade=='8':identity+=' The 7/16 and 9/16-inch columns marked inactive for new design in the reviewed drawing are omitted. The reviewed issue states that this standard is not intended for aerospace applications.'
 rows=[]
 for r in data['rows']:
  link='Quote.html?reference='+file+'&amp;part='+h(r['part'])
  rows.append([h(r[f])for f in ['part','thread','length','across_flats_limits','head_height_limits']]+['<a href="'+link+'">Quote '+h(r['part'])+' →</a>'])
 table='<p>Reference sizes for identification and quotation. Webson confirms availability by inquiry; these rows do not indicate stocked inventory.</p>'
 table+=filtered(['Part number','Thread','Length per drawing (in)','Head across flats limits (in)','Head height limits (in)','Request pricing'],rows,root+' reference hex cap screw dimensions')
 table+='<p>Head across-flats width and axial head height are minimum–maximum drawing limits in inches. Length values preserve the reviewed table’s decimal references, including 0.438 and 0.562; they do not add acceptance tolerances. Across-flats limits describe the screw head, not the tolerance of a wrench or socket.</p>'
 example=root+'-3 is a 1/4-'+('20'if coarse else'28')+' reference with a 0.500-inch under-head length. '+root+'-109 is a 1/2-'+('13'if coarse else'20')+' reference with a 1.000-inch under-head length. Use the full series and dash number when ordering.'
 measurement='<p>Length L runs from the bearing surface beneath the head to the tip. H is the axial head height; F is the width between opposite hex faces. The head is outside the under-head length measurement.</p><p>Thread length is a separate requirement. The reviewed issue uses a minimum rule of twice the nominal diameter plus 1/4 inch, with a positive allowance and separate provisions for screws too short to provide that thread length. Use the full governing issue for those limits. A listed screw length is not a fixed grip length or a claim that the screw is fully threaded.</p>'
 if grade=='5':
  finish='<p>The reviewed '+h(data['reviewed_issue'].split(',')[0])+' reference specifies medium carbon steel, Grade 5, with cadmium plating under its procurement specification. Include the required issue, finish and certification requirements with the quote request.</p>'
 else:
  finish='<p>The reviewed '+h(data['reviewed_issue'].split(',')[0])+' reference specifies alloy steel, Grade 8, with zinc coating. Earlier issues used cadmium plating; retain the coating and specification issue called out by your drawing.</p><p>The table lists plain screws. The reviewed part-number requirements use an L after the dash number for a self-locking element. Preserve that suffix and the locking requirement when applicable; a plain screw and a locking configuration are separate selections.</p>'
 comparison=[]
 for other,d in DATA.items():comparison.append(['<a href="Reference-'+other+'.html">'+other+'</a>','Grade '+d['grade'],d['thread_series'],d['coating'].capitalize()])
 related=filtered(['Series','Steel grade','Thread series','Finish in reviewed issue'],comparison,'Grade 5 and Grade 8 hex cap screw comparison')
 related+='<p>Compare grade, thread, finish and governing issue together. A similar head size does not establish an approved substitution. Select mating nuts and washers to the application’s strength, finish and dimensional requirements.</p>'+chips([('Hex cap screw family directory','Reference-Family-hex-cap-screws.html'),('Coarse-thread finished hex nuts','Reference-MS51967.html'),('Fine-thread finished hex nuts','Reference-MS51968.html'),('Stainless MS35307/MS35308 cap screws','Reference-MS35307-MS35308.html')])
 guide(file,root+' Hex Cap Screws | Thread Sizes & Dimensions',root+' Grade '+grade+' '+('coarse'if coarse else'fine')+'-thread hex cap screws.','Find '+root+' threads, under-head lengths, hex head dimensions and finish details. Filter the reference table and request a quote for a selected screw.',[
  ('Identify the grade, thread and finish','<p>'+identity+'</p>','PART IDENTIFICATION'),
  (root+' part-number and dimension table',table,'REFERENCE SIZES'),
  ('Measure under-head length and head dimensions',measurement,'MEASUREMENT GUIDE'),
  ('Read the complete part number','<p>'+example+'</p>','ORDERING EXAMPLES'),
  ('Preserve the finish and locking requirement',finish,'MATERIAL AND CONFIGURATION'),
  ('Compare the four hex cap screw families',related,'FAMILY COMPARISON'),
  ('Match the governing drawing issue','<p>Dimensions summarize '+h(data['reviewed_issue'])+'. These are selected historical references for purchasing identification. The issue required by your drawing controls full dimensions, thread length, material, coating, locking and inspection requirements.</p>','DRAWING REQUIREMENTS')])
