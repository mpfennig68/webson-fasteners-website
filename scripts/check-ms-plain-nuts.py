"""Validate nut references, material/PIN distinctions and public lookup routes."""
from pathlib import Path
from decimal import Decimal
import json,re,html
W=Path(__file__).resolve().parents[1]
D=json.loads((W/'scripts/mil-spec-plain-nut-data.json').read_text())
D['MS51965']=json.loads((W/'scripts/mil-spec-set-screw-data.json').read_text())['MS51965']
index=json.loads((W/'assets/mil-spec-search-index.json').read_text())
lookup={r['part']:r for r in index['parts']}
parts={}
for root,expected in [('MS51972',14),('MS35690',9),('MS25082',50),('MS51965',52)]:
 data=D[root];page=(W/f'Reference-{root}.html').read_text()
 assert len(data['rows'])==len({r['part']for r in data['rows']})==expected
 assert 'Stocked item' not in page
 assert data['reviewed_issue'] in html.unescape(page)
 if root!='MS51965':assert 'Material / finish' in page
 for r in data['rows']:
  parts[r['part']]=r
  row=re.search(r'<tr\b[^>]*><th scope="row">'+re.escape(r['part'])+r'</th>.*?</tr>',page)
  assert row,r['part']
  for field,value in r.items():
   if field=='part':continue
   assert '>'+value+'<' in html.unescape(row[0]),(r['part'],field)
   if field.endswith('_limits'):
    low,high=map(Decimal,value.split('–'));assert 0<low<=high
  assert 'part='+r['part']+'"' in html.unescape(row[0])
  result=lookup[r['part']]
  assert not result['stocked'] and result['page']==f'Reference-{root}.html'
  assert 'id="'+result['anchor']+'"' in page
 assert next(s for s in index['series']if s['part']==root)['page']==f'Reference-{root}.html'
# Independently reviewed thread/PIN, geometry and configuration distinctions.
for part,thread in [('MS51972-1','1/4-28'),('MS51972-4','7/16-20'),('MS51972-13','1-3/8-12'),('MS35690-424','1/4-28'),('MS35690-613','3/8-16'),('MS35690-633','3/8-24'),('MS25082-1','6-32'),('MS25082-C12','10-32'),('MS25082-C26','1/4-36'),('MS25082-C8','0.4688-32'),('MS51965-21','6-32'),('MS51965-55','1/4-20'),('MS51965-69','5/16-18'),('MS51965-79','3/8-16'),('MS51965-92','1/2-13')]:assert parts[part]['thread']==thread,part
assert parts['MS51972-4']['across_flats_limits']=='0.6750–0.6875'
assert parts['MS51972-14']['thickness_limits']=='1.245–1.317'
assert parts['MS35690-424']['material_finish']=='Grade B carbon steel / uncoated'
assert parts['MS35690-427']['material_finish']=='Grade C carbon steel / uncoated'
assert parts['MS35690-413']['material_finish']=='Brass / nickel plated'
assert parts['MS25082-C3']['across_flats_limits']=='0.362–0.375'
assert parts['MS25082-C12']['across_flats_limits']=='0.241–0.250'
assert parts['MS25082-C7']['thickness_limits']=='0.073–0.083'
assert parts['MS25082-C20']['thickness_limits']=='0.088–0.098'
assert parts['MS25082-C26']['thickness_limits']=='0.058–0.068'
assert parts['MS25082-C8']['thread_class']=='UNS-2B'
assert parts['MS51965-55']['length']=='0.500'
assert parts['MS51965-69']['length']=='0.875'
assert parts['MS51965-79']['point_diameter_limits']=='0.194–0.212'
assert parts['MS51965-92']['length_tolerance']=='±0.020'
assert all('Configuration: Plain' in lookup[r['part']]['summary']for r in D['MS51965']['rows'])
for part in ['MS25082-9','MS25082-C9','MS35690-401','MS35690-404','MS35690-410','MS51965-107','MS51965-55L']:assert part not in lookup
for root in D:assert f'{root}-999'not in lookup
assert 'A 2011 amendment' in (W/'Reference-MS25082.html').read_text()
assert 'does not reactivate every historical dash number' in (W/'Reference-MS35690.html').read_text()
assert len(parts)==125
print('125 new references pass thread/PIN mappings, plain configuration, material/finish distinctions, dimensions, excluded parts and quote/search/stock boundaries.')
