"""Check reviewed mappings, table visibility and new reference/stock boundaries."""
from pathlib import Path
from decimal import Decimal
import json,re,html
W=Path(__file__).resolve().parents[1]
D=json.loads((W/'scripts/mil-spec-additional-screw-data.json').read_text())
index=json.loads((W/'assets/mil-spec-search-index.json').read_text())
lookup={r['part']:r for r in index['parts']}
parts={}
for root,expected in [('MS35207',119),('MS51958',119),('MS51960',112),('MS16997',49)]:
 data=D[root];page=(W/f'Reference-{root}.html').read_text()
 assert len(data['rows'])==expected
 assert len({r['part']for r in data['rows']})==expected
 assert 'Stocked item' not in page
 assert data['reviewed_issue'] in html.unescape(page)
 for row in data['rows']:
  parts[row['part']]=row
  visible=re.search(r'<tr\b[^>]*><th scope="row">'+row['part']+r'</th>.*?</tr>',page)
  assert visible,row['part']
  for field,value in row.items():
   if field=='part':continue
   assert '>'+value+'<' in html.unescape(visible[0]),(row['part'],field)
   if field.endswith('_limits'):
    a,b=map(Decimal,value.split('–'));assert 0<a<=b
  assert 'part='+row['part']+'"' in html.unescape(visible[0])
  item=lookup[row['part']];assert not item['stocked']
  assert item['page']==f'Reference-{root}.html'
 assert next(r for r in index['series']if r['part']==root)['page']==f'Reference-{root}.html'
# Independent drawing examples and size-boundary checks.
for part,thread,length in [('MS35207-202','2-64','3/16'),('MS35207-259','10-32','1/4'),('MS35207-276','1/4-28','5/16'),('MS51958-13','4-48','1/4'),('MS51958-63','10-32','1/2'),('MS51960-65','10-32','0.50'),('MS51960-78','1/4-28','0.25'),('MS16997-32','8-32','1/2'),('MS16997-58','1/4-20','1/2')]:
 assert parts[part]['thread']==thread and parts[part]['length']==length,part
assert parts['MS35207-201']['head_diameter_limits']=='0.155–0.167'
assert parts['MS51958-1']['head_diameter_limits']=='0.157–0.167'
assert parts['MS16997-43']['head_diameter_limits']=='0.303–0.3125'
assert parts['MS16997-43']['head_height_max']=='0.190'
assert parts['MS51960-65']['head_diameter_max']=='0.385'
for dash in [56,57,58,59,76,77,93,94,108,109,123,174]:
 assert f'MS51960-{dash}' not in parts
assert len(parts)==399
print('399 reference screws pass drawing examples, dimension bounds, visible values, quote links, search destinations and stock boundaries.')
