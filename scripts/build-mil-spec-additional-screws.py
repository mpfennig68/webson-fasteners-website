"""Publish reviewed reference sizes without adding inventory claims."""
import json
D=json.loads((W/'scripts/mil-spec-additional-screw-data.json').read_text())
COPY={
 'MS35207': {
  'name':'fine-thread carbon-steel pan-head screws',
  'identity':'MS35207 identifies cross-recessed pan-head machine screws in carbon steel, cadmium plated, with UNF-2A threads. The table covers dash numbers 201–319, from 2-64 through 3/8-24. These are separate thread and dash-number selections from the coarse-thread MS35206 family.',
  'finish':'The reviewed MS35207F notes specify cadmium plating to QQ-P-416, Type II, Class 3. Its part-number example is MS35207-201. Include any additional finish or drawing requirements with your inquiry.',
  'length':'Length is measured from the bearing surface beneath the head to the tip. MS35207-202 is a 2-64 by 3/16-inch reference; MS35207-259 is a 10-32 by 1/4-inch reference. Fractional lengths below are nominal size names corresponding to the drawing’s decimal length rows.',
  'links':[('MS35206: coarse-thread carbon-steel pan head','Reference-MS35206.html'),('MS51958: fine-thread stainless pan head','Reference-MS51958.html')],
 },
 'MS51958': {
  'name':'fine-thread stainless pan-head screws',
  'identity':'MS51958 identifies cross-recessed pan-head machine screws in corrosion-resistant steel with UNF-2A threads. This selection covers dash numbers 1–119, from 2-64 through 3/8-24. MS51957 is the related coarse-thread family; its dash numbers do not identify the same sizes.',
  'finish':'The reviewed MS51958C reference specifies 300-series corrosion-resistant steel and a cleaned and descaled surface treatment. A B following the dash number identifies black oxide; for example, MS51958-45B. The table lists unsuffixed reference sizes. Retain the finish and governing issue called out by your drawing.',
  'length':'Length is measured beneath the head to the tip. MS51958-13 is a 4-48 by 1/4-inch reference; MS51958-63 is a 10-32 by 1/2-inch reference. The reviewed drawing also contains 0-80 entries, outside this selected table. Historical manufacturer production annotations are not a statement of Webson inventory.',
  'links':[('MS51957: coarse-thread stainless pan head','Reference-MS51957.html'),('MS35207: fine-thread carbon-steel pan head','Reference-MS35207.html'),('MS51960: fine-thread stainless flat head','Reference-MS51960.html')],
 },
 'MS51960': {
  'name':'fine-thread 82-degree flat-head screws',
  'identity':'MS51960 identifies cross-recessed, 82-degree flat countersunk-head machine screws in corrosion-resistant steel with UNF-2A threads. This table selects 112 unsuffixed references from 0-80 through 3/8-24. Entries marked inactive for new design in the reviewed MS51960D table are omitted.',
  'finish':'MS51960D specifies 300-series corrosion-resistant steel and passivation. B identifies black oxide and L identifies a self-locking element; the order is BL when both apply. MS51960-65BL is the drawing’s example of a 10-32, 0.50-inch screw with black oxide and a self-locking element. Suffixes are not interchangeable with the unsuffixed references in this table.',
  'length':'Overall length includes the countersunk head. The length column preserves the decimal values printed in MS51960D Table I, including 0.12, 0.19 and 0.62; these are reference table values, not an added acceptance tolerance. MS51960-65 identifies a 10-32 by 0.50-inch reference.',
  'links':[('MS51959: coarse-thread 82-degree flat head','Reference-MS51959.html'),('MS24693: 100-degree flat head','Reference-MS24693.html'),('MS51958: fine-thread stainless pan head','Reference-MS51958.html')],
 },
 'MS16997': {
  'name':'alloy-steel UNC socket-head cap screws',
  'identity':'MS16997 identifies cadmium-plated alloy-steel socket-head cap screws with UNC-3A threads. This selected table covers 49 plain-screw references from 2-56 through 1/4-20. The stainless MS16995 family has a different material requirement; a matching thread and length alone does not establish interchangeability.',
  'finish':'The reviewed MS16997D notes specify alloy steel and cadmium plating under the procurement specification. An L after the dash number identifies the self-locking version: MS16997-1 is plain, while MS16997-1L has a self-locking element. The rows in this table identify plain screws; preserve any required locking suffix in the inquiry.',
  'length':'Length is measured from beneath the head to the tip. MS16997-32 is an 8-32 by 1/2-inch reference; MS16997-58 is a 1/4-20 by 1/2-inch reference. Longer screws can have an unthreaded body. Overall under-head length is not the same as thread length or grip length.',
  'links':[('MS16995: stainless UNC socket head','Reference-MS16995.html'),('MS16996: stainless UNF socket head','Reference-MS16996.html'),('NAS1352: coarse-thread socket screws','Reference-NAS1352.html')],
 }
}
for root,data in D.items():
 copy=COPY[root];file='Reference-'+root+'.html'
 flat=root=='MS51960';socket=root=='MS16997'
 fields=['thread','length']+(['head_diameter_max','head_angle']if flat else['head_diameter_limits','head_height_max'if socket else'head_height_limits'])+(['socket_width_limits']if socket else[])
 headers=['Part number','Thread','Length per drawing (in)'if flat else'Nominal length (in)']+(['Sharp head diameter max (in)','Nominal head angle']if flat else['Head diameter limits (in)','Head height max (in)'if socket else'Head height limits (in)'])+(['Socket AF limits (in)']if socket else[])+['Request pricing']
 rows=[]
 for r in data['rows']:
  link='Quote.html?reference='+file+'&amp;part='+r['part']
  rows.append([h(r['part'])]+[h(r[f])for f in fields]+['<a href="'+link+'">Quote '+h(r['part'])+' →</a>'])
 note='<p>Reference sizes for identification and quotation; availability is confirmed by inquiry. These rows do not indicate Webson stock.</p>'
 note+=filtered(headers,rows,root+' reference screw dimensions')
 if flat:
  note+='<p>Head diameter is the maximum theoretical sharp-head diameter from the reviewed drawing, not the minimum finished head diameter. The included head-angle limits are 80–82 degrees. Short screws may have undercut heads with separate height limits. Use the governing drawing for countersink design and inspection.</p>'
 else:
  note+='<p>Head diameter'+(' and socket AF are minimum–maximum limits; head height is a maximum from the reviewed 'if socket else' and height are minimum–maximum limits from the reviewed ')+h(data['reviewed_issue'].split(',')[0])+' reference. Length is nominal and measured beneath the head.'+(' Socket AF means socket width across flats; these limits are not a nominal hex-key size.'if socket else'')+'</p>'
 guide(file,root+' Screws | Thread Sizes & Dimensions',root+' '+copy['name']+'.','Find '+root+' part numbers, thread sizes, lengths and head dimensions. Filter the reference table and request a quote for a selected size.',[
  ('Identify the thread, head and material','<p>'+copy['identity']+'</p>','PART IDENTIFICATION'),
  (root+' part-number and dimension table',note,'REFERENCE SIZES'),
  ('Measure the correct length','<p>'+copy['length']+'</p>','LENGTH CONVENTION'),
  ('Keep finish and locking codes with the part','<p>'+copy['finish']+'</p>','ORDERING DETAILS'),
  ('Compare related screw families',chips(copy['links']+[('Machine-screw directory'if not socket else'Socket-screw directory','Reference-Family-machine-screws.html'if not socket else'Reference-Family-socket-screws.html')]),'RELATED REFERENCES'),
  ('Use the issue required by your drawing','<p>Dimensions summarize '+h(data['reviewed_issue'])+'. This is a selected purchasing reference. Send the complete part designation and governing specification issue for quotation; the required issue controls full dimensions, tolerances, material, finish and documentation.</p>','DRAWING REQUIREMENTS')])
