"""Validate nut references, material/PIN distinctions and public lookup routes."""
from pathlib import Path
from decimal import Decimal
import json,re,html
W=Path(__file__).resolve().parents[1]
D=json.loads((W/'scripts/mil-spec-additional-nut-data.json').read_text())
index=json.loads((W/'assets/mil-spec-search-index.json').read_text())
lookup={r['part']:r for r in index['parts']}
parts={}
for root,expected in [('MS35649',37),('MS35650',50),('MS51967',20),('MS51968',20)]:
 data=D[root];page=(W/f'Reference-{root}.html').read_text()
 assert len(data['rows'])==len({r['part']for r in data['rows']})==expected
 assert 'Stocked item' not in page
 assert data['reviewed_issue'] in html.unescape(page)
 assert 'Material / finish' in page
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
# Independently read examples, unusual dash numbers, and amendment changes.
for part,thread,finish in [
 ('MS35649-222','2-56','Carbon steel / cadmium'),
 ('MS35649-23','2-56','Carbon steel / phosphate'),
 ('MS35649-225B','2-56','Brass / black oxide'),
 ('MS35649-286T','8-32','Brass / tin'),
 ('MS35649-2254','1/4-20','CRES / passivated'),
 ('MS35650-312','0-80','Carbon steel / cadmium'),
 ('MS35650-386B','8-36','Brass / black oxide'),
 ('MS35650-3252','1/4-28','Carbon steel / cadmium'),
 ('MS51967-2','1/4-20','Grade B carbon steel / cadmium'),
 ('MS51967-15','1/2-13','Grade C carbon steel / cadmium'),
 ('MS51968-2','1/4-28','Grade B carbon steel / cadmium'),
 ('MS51968-30','1-12','Grade C carbon steel / cadmium')]:
 assert parts[part]['thread']==thread and parts[part]['material_finish']==finish,part
assert parts['MS35650-312']['thickness_limits']=='0.043–0.050'
assert parts['MS35650-322']['across_flats_limits']=='0.180–0.189'
assert parts['MS35650-3252']['across_flats_limits']=='0.423–0.440'
assert parts['MS35649-2252']['thickness_limits']=='0.178–0.193'
assert parts['MS51967-2']['thickness_limits']=='0.212–0.226'
assert parts['MS51968-11']['thickness_limits']=='0.365–0.385'
for root in ['MS51967','MS51968']:
 for dash in range(1,31,3):assert f'{root}-{dash}' not in parts # canceled Grade A
for part in ['MS35649-225','MS35650-325','MS35649-285B','MS35650-385B']:
 assert part not in parts # omitted brass finish, or wrong special dash number
assert len(parts)==127
print('127 nut references pass drawing examples, amended limits, grade/finish distinctions, quote links and search/stock boundaries.')
