"""Verified lookup tables, integrated into the shared reference renderer."""
import json,re
from urllib.parse import quote
LOOKUP=json.loads((W/'scripts/mil-spec-lookup-data.json').read_text())
HEX='Reference-MS35307-MS35308.html'
HELICAL='Reference-Helical-Insert-Cross-Reference.html'
KEY='Reference-Keylocking-Insert-Comparison.html'
SHOULDER='Reference-Shoulder-Screw-Comparison.html'
LOOKUP_LINKS=[('MS35307 / MS35308 hex-screw size lookup',HEX),('MS35338 washer dimensions','Reference-MS35338.html'),('Helical insert manufacturer cross-reference',HELICAL),('Keylocking insert sizes and Keensert references',KEY),('Socket / slotted shoulder-screw comparison',SHOULDER)]
def inquiry(file,part,label=None):
 return '<a href="Quote.html?reference='+file+'&amp;part='+quote(part,safe='')+'">'+h(label or part)+'</a>'
def hex_tables():
 body=''
 intro='<p>Look up 283 base designations in each series. These are reference sizes, not a stock list. Request current availability and quote any required material or finish suffixes in full. Decimal lengths retain the published tables’ rounding.</p>'
 for root,items in LOOKUP['hex_cap_screws'].items():
  rows=[{'cells':[h(r['part']),h(r['thread']),h(r['length']),h(r['decimal_length']),h(r['material']),inquiry(HEX,r['part'],'Request quote →')],'search':' '.join(r.values()),'family':r['diameter']}for r in items]
  body+=section(root+' part-number and size lookup',intro+filtered(['Part number','Nominal thread','Length (in)','Length (decimal in)','Material / finish','Request pricing'],rows,root+' base-designation size reference',list(dict.fromkeys(r['diameter']for r in items)),'Diameter'),'SIZE LOOKUP')
  intro=''
 return body

def washer_tables():
 rows=[]
 for r in LOOKUP['washer_dimensions']:
  rows.append({'cells':[h(r['size']),h(r['id_min']+'–'+r['id_max']),h(r['od_max']),h(r['width_min']),h(r['thickness_min']+'–'+r['thickness_max'])],'search':' '.join(r.values()),'family':r['size']})
 body=section('MS35338 dimensional lookup','<p>Dimensions are in inches and summarize MS35338 revision L. A is the opening diameter, B the outside diameter, W the section width and C the section thickness. The nominal screw size is not the washer opening diameter.</p>'+filtered(['Nominal screw size','ID A limits (in)','OD B max (in)','Width W min (in)','Thickness C limits (in)'],rows,'MS35338 regular-series dimensions')+'<p>Section thickness is not the washer’s free spring height. The summary does not replace the controlling specification’s inspection and acceptance requirements.</p>','DIMENSIONAL REFERENCE')
 rows=[]
 for r in LOOKUP['washer_dimensions']:
  rows.append({'cells':[h(r['size'])]+[h('MS35338-'+r[k])if r[k]else''for k in ['steel_dash','phosphate_dash','bronze_dash','nickel_dash','cres_dash','magnetic_dash']],'search':' '.join(r.values())+' '+' '.join('MS35338-'+r[k]for k in ['steel_dash','phosphate_dash','bronze_dash','nickel_dash','cres_dash','magnetic_dash']if r[k])})
 body+=section('Size and material dash-number reference','<p>Compare the regular-series size across material groups. These reference designations are not an availability list. The selected stocked items remain identified in the stock table above.</p>'+filtered(['Nominal screw size','Carbon steel, cadmium / zinc','Carbon steel, phosphate','Phosphor bronze / tin brass','Nickel-copper-aluminum','CRES, 300 series','CRES, Type 420'],rows,'MS35338 material and size designations')+'<p>The CRES 300-series group uses Type 316 through 1/4 inch in revision L. The B suffix identifies the black-oxide option for the applicable CRES group; it is not added to the passivated designations shown here.</p>','PART-NUMBER LOOKUP')
 return body

def related_lookup(file):
 if file in ['Reference-MS21209.html','Reference-NAS1130.html']:
  return section('Compare manufacturer part numbers',chips([('MS21209 / NAS1130 locking-insert cross-reference',HELICAL)])+'<p>Keep tanged and tangless constructions separate when reviewing a manufacturer reference.</p>','MANUFACTURER REFERENCES')
 if file=='Reference-MS51830.html':return section('Compare related insert sizes and part numbers',chips([('MS51830 / MS51831 / MS51832 and Keensert references',KEY)]),'RELATED LOOKUP')
 if file in ['Reference-MS51575.html','Reference-MS51576.html']:return section('Compare socket and slotted designations',chips([('Match shoulder diameter, length and thread',SHOULDER)]),'SIZE COMPARISON')
 return ''
def enhance(file,body):
 if file==HEX:
  first=body.index('</section>')+len('</section>')
  body=body[:first]+hex_tables()+body[first:]
 if file=='Reference-MS35338.html':
  stock=re.search(r'<section class="ref-section "><p class="ref-kicker">// STOCKED SELECTION</p>.*?</section>',body,re.S)
  if stock:body=body[:stock.end()]+washer_tables()+body[stock.end():]
  else:body+=washer_tables()
 if file in ['Resources-Mil-Spec-Tables.html','Resources-Mil-Spec-Cross-Reference.html']:
  body=section('Part-number lookup and cross-reference tables',chips(LOOKUP_LINKS),'FIND A PART')+body
 body+=related_lookup(file)
 return body

def build_pages():
 body=section('Choose the insert construction','<p>Search selected inch-series screw-locking inserts by MS or NAS designation, KATO CoilThread number, Heli-Coil number or Recoil number. The tables cover 1D and 2D installed-length selections in bulk supply format, without the optional cadmium or dry-film finish suffixes.</p><p>Each table stays within one construction. A tanged MS21209 insert and a tangless NAS1130 insert are not presented as automatic substitutes. Installed lengths below are nominal diameter multiples; they are not free-coil lengths or tapped-hole depths.</p>'+chips([('Tanged MS21209 references','#tanged'),('Tangless NAS1130 references','#tangless')]),'USE THE CROSS-REFERENCE')
 for kind,label in [('tanged','Tanged screw-locking inserts — MS21209'),('tangless','Tangless screw-locking inserts — NAS1130')]:
  rows=[]
  for r in LOOKUP['helical_cross_references'][kind]:
   cells=[h(r['standard']),h(r['thread']),h(r['length_multiple'])+' / '+h(r['installed_length']),inquiry(HELICAL,r['kato']),inquiry(HELICAL,r['heli_coil'])if r['heli_coil']!='---'else'']
   if kind=='tanged':cells.append(inquiry(HELICAL,r['recoil']))
   cells.append(inquiry(HELICAL,r['standard'],'Quote '+r['standard']+' →'))
   rows.append({'cells':cells,'search':' '.join(r.values()),'family':r['thread']})
  headers=['Standard designation','Mating thread','Installed length (D / in)','KATO CoilThread','Heli-Coil']+(['Recoil']if kind=='tanged'else[])+['Request pricing']
  body+=section(label,filtered(headers,rows,label+' — selected manufacturer references',list(dict.fromkeys(r['thread']for r in LOOKUP['helical_cross_references'][kind])),'Mating thread'),'PART-NUMBER CROSS-REFERENCE').replace('<section class="ref-section ">','<section id="'+kind+'" class="ref-section ">',1)
 body+=section('Carry the full requirement into the quote','<p>These selected relationships follow manufacturer cross-reference listings. Blank manufacturer cells mean no part number is included in this selection. A listed relationship does not establish approved-source status or approval for a particular assembly.</p><p>Specify the required manufacturer, locking construction, finish, bulk or strip-feed supply, quantity and documents. Manufacturer names identify numbering systems; contact Webson to review the supply options.</p>'+chips([('MS21209 stocked selections','Reference-MS21209.html'),('NAS1130 stocked selections','Reference-NAS1130.html'),('RFQ checklist','Resources-Mil-Spec-RFQ-Checklist.html')]),'REQUEST THE RIGHT CONFIGURATION')
 page(HELICAL,'Helical Insert Cross-Reference | MS21209, NAS1130 & Brands | Webson','Compare selected MS21209 and NAS1130 screw-locking inserts with KATO CoilThread, Heli-Coil and Recoil part numbers, thread sizes and installed lengths.','Helical insert cross-reference.','Find selected manufacturer part numbers for tanged and tangless screw-locking inserts, with the construction and length kept clear.',body)
 body=section('Compare the complete insert envelope','<p>These selected nonlocking, passivated stainless references compare miniature, lightweight, heavy-duty and extra-heavy-duty inserts. The internal thread accepts the screw; the external thread fits the parent component. Matching the internal thread alone does not identify the same insert.</p><p>Keensert numbers below are selected manufacturer catalog relationships for the 303 CRES configuration. Material, finish, locking options and source requirements remain part of the full inquiry.</p>','FAMILY AND MANUFACTURER REFERENCE')
 rows=[]
 for r in LOOKUP['keylocking_comparison']:
  rows.append({'cells':[h(r['part']),inquiry(KEY,r['keensert']),h(r['family']),h(r['internal']),h(r['external']),h(r['length']),inquiry(KEY,r['part'],'Request quote →')],'search':' '.join(r.values()),'family':r['family']})
 body+=section('Selected MS and Keensert part numbers',filtered(['MS designation','Keensert reference','Family','Internal thread','External thread','Length (in)','Request pricing'],rows,'Selected nonlocking stainless keylocking insert references',['Miniature','Lightweight','Heavy duty','Extra heavy duty'],'Insert family'),'THREAD AND LENGTH LOOKUP')
 body+=section('The same screw thread can require a different outside fit','<p>For a 1/4-20 internal thread, MS51830-106 has a 3/8-16 external thread, MS51831-102 has 7/16-14, and MS51832-102 has 1/2-13. All three selected references have a nominal 0.370-inch length. Their outside fits are different.</p><p>The table covers nonlocking internal threads. Do not add L or carry another material or lubrication suffix across a manufacturer number without reviewing that configuration. Published lengths are identification references, not hole-preparation or installation instructions.</p>'+chips([('MS51830 complete thread relationships','Reference-MS51830.html'),('Helical inserts are a different construction',HELICAL),('Prepare an RFQ','Resources-Mil-Spec-RFQ-Checklist.html')]),'READING THE COMPARISON')
 page(KEY,'MS51830, MS51831 & MS51832 | Keensert Cross-Reference | Webson','Compare selected MS51830, MS51831 and MS51832 stainless keylocking inserts with Keensert numbers, internal/external threads and lengths.','Keylocking insert size and part-number comparison.','Compare selected MS designations and Keensert references across miniature, lightweight, heavy-duty and extra-heavy-duty families.',body)
 body=section('Match dimensions before comparing the designation','<p>These rows pair selected socket-head MS51576 and slotted-head MS51575 references sharing nominal shoulder diameter, shoulder length and male thread. The drive and head details remain different. A dimensional match is not approval to substitute one part for the other.</p><p>Lengths below are shoulder lengths, measured from the bearing surface beneath the head to the shoulder transition. They are not overall screw lengths.</p>','SOCKET AND SLOTTED COMPARISON')
 rows=[]
 for r in LOOKUP['shoulder_comparison']:
  rows.append({'cells':[h(r['diameter']),h(r['length']),h(r['thread']),inquiry(SHOULDER,r['socket']),inquiry(SHOULDER,r['slotted'])],'search':' '.join(r.values()),'family':r['diameter']})
 body+=section('Shared nominal shoulder sizes',filtered(['Shoulder diameter (in)','Shoulder length (in)','Male thread','Socket — MS51576','Slotted — MS51575'],rows,'Socket and slotted shoulder-screw dimensional comparison',list(dict.fromkeys(r['diameter']for r in LOOKUP['shoulder_comparison'])),'Shoulder diameter')+'<p>Click either complete designation to request a quote for that part. Only selected shared sizes are paired here; each series guide includes additional entries.</p>','PART-NUMBER LOOKUP')
 body+=section('A shared dash number can hide a different length','<p>MS51576-16 and MS51575-16 both have a 1/4-inch shoulder diameter, but their nominal shoulder lengths are 3/16 and 1/8 inch respectively. At a 1/4-inch shoulder diameter and 3/16-inch shoulder length, the selected pair is MS51576-16 and MS51575-17.</p>'+chips([('MS51576 socket shoulder-screw table','Reference-MS51576.html'),('MS51575 slotted shoulder-screw table','Reference-MS51575.html')]),'WHY THE COMPLETE PART MATTERS')
 page(SHOULDER,'MS51575 vs MS51576 | Shoulder Screw Size Comparison | Webson','Compare selected MS51575 slotted and MS51576 socket shoulder screws by shoulder diameter, shoulder length and male thread, then request a quote.','MS51575 and MS51576 shoulder-screw comparison.','Find socket and slotted designations sharing a selected nominal shoulder size, while keeping the head and drive differences clear.',body)
