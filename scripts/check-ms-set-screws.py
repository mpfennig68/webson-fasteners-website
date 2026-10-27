"""Check sourced screw mappings, dimension bounds and reference-only routes."""
from pathlib import Path
from decimal import Decimal
import json,re,html
W=Path(__file__).resolve().parents[1]
D=json.loads((W/'scripts/mil-spec-set-screw-data.json').read_text())
index=json.loads((W/'assets/mil-spec-search-index.json').read_text());lookup={r['part']:r for r in index['parts']};parts={}
for root,count in [('MS51023',36),('MS51031',17),('MS51047',33),('MS51963',85)]:
 data=D[root];page=(W/f'Reference-{root}.html').read_text()
 assert len(data['rows'])==len({r['part']for r in data['rows']})==count
 assert data['reviewed_issue'] in html.unescape(page)
 assert 'Stocked item' not in page and 'ref-dimension-figure' in page
 for r in data['rows']:
  parts[r['part']]=r
  row=re.search(r'<tr\b[^>]*><th scope="row">'+re.escape(r['part'])+r'</th>.*?</tr>',page);assert row,r['part']
  for field,value in r.items():
   if field=='part':continue
   assert '>'+value+'<' in html.unescape(row[0]),(r['part'],field)
   if field.endswith('_limits'):
    low,high=map(Decimal,value.split('–'));assert 0<low<=high
  assert 'part='+r['part']+'"' in html.unescape(row[0])
  assert 'Configuration: '+data['configuration'] in lookup[r['part']]['summary']
  assert lookup[r['part']]['page']==f'Reference-{root}.html' and not lookup[r['part']]['stocked']
 assert next(s for s in index['series']if s['part']==root)['page']==f'Reference-{root}.html'
 for r in data.get('head_geometry',[]):
  for field,value in r.items():
   assert '>'+value+'<' in html.unescape(page)
   if field.endswith('_limits'):
    low,high=map(Decimal,value.split('–'));assert 0<low<=high
# Drawing examples and sparse dash columns, independent of the data builder.
for part,thread,length in [('MS51023-12','2-64','0.312'),('MS51023-31','6-40','0.375'),('MS51023-32','6-40','0.500'),('MS51023-52','10-32','0.500'),('MS51023-64','1/4-28','0.500'),('MS51031-102','10-32','0.188'),('MS51031-107','10-32','0.500'),('MS51031-115','1/4-28','0.375'),('MS51031-117','1/4-28','0.500'),('MS51031-124','1/4-28','1.750'),('MS51047-47','1/4-28','0.500'),('MS51047-65','3/8-24','0.750'),('MS51047-73','1/2-20','0.750'),('MS51963-27','6-32','0.625'),('MS51963-51','10-24','0.500'),('MS51963-67','1/4-20','0.500'),('MS51963-112','3/8-16','2.500')]:
 assert (parts[part]['thread'],parts[part]['length'])==(thread,length),part
assert parts['MS51047-47']['point_length_limits']=='0.059–0.067'
assert parts['MS51047-65']['point_diameter_limits']=='0.241–0.250'
assert parts['MS51963-112']['length_tolerance']=='±0.031'
assert parts['MS51023-52']['length_tolerance']=='±0.010'
assert parts['MS51047-73']['length_tolerance']=='±0.020'
assert parts['MS51031-107']['point_diameter_limits']=='0.088–0.102'
assert D['MS51031']['configuration']=='Self-locking'
for dash in [101,105,106,108,114,116,118]:assert f'MS51031-{dash}'not in parts
for root in D:
 assert f'{root}-999'not in lookup and f'{root}-107L'not in lookup
for root in ['MS51023','MS51963']:
 assert 'C applies to the plain cup profile' in (W/f'Reference-{root}.html').read_text()
assert 'inactive for new design after 29 December 1972' in (W/'Reference-MS51047.html').read_text()
assert 'not by adding an L suffix' in (W/'Reference-MS51031.html').read_text()
assert len(parts)==171
print('171 set screw references pass sparse dash mappings, thread/length/socket/point dimensions, configuration and search/stock boundaries.')
