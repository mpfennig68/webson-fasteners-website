"""Check sourced screw mappings, dimension bounds and reference-only routes."""
from pathlib import Path
from decimal import Decimal
import json,re,html
W=Path(__file__).resolve().parents[1]
D=json.loads((W/'scripts/mil-spec-head-style-data.json').read_text())
index=json.loads((W/'assets/mil-spec-search-index.json').read_text());lookup={r['part']:r for r in index['parts']};parts={}
for root,count in [('MS35190',119),('MS35191',122),('MS35265',119),('MS35266',119)]:
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
  assert lookup[r['part']]['page']==f'Reference-{root}.html' and not lookup[r['part']]['stocked']
 assert next(s for s in index['series']if s['part']==root)['page']==f'Reference-{root}.html'
 for r in data.get('head_geometry',[]):
  for field,value in r.items():
   assert '>'+value+'<' in html.unescape(page)
   if field.endswith('_limits'):
    low,high=map(Decimal,value.split('–'));assert 0<low<=high
# Drawing examples and easy-to-confuse coarse/fine dash boundaries.
for part,thread,length in [('MS35190-209','2-56','0.125'),('MS35190-221','4-40','0.250'),('MS35190-267','10-24','0.250'),('MS35190-284','1/4-20','0.312'),('MS35191-201','0-80','0.125'),('MS35191-221','2-64','0.750'),('MS35191-224','4-48','0.250'),('MS35191-268','10-32','0.250'),('MS35191-285','1/4-28','0.250'),('MS35265-17','4-40','0.50'),('MS35265-63','10-24','0.50'),('MS35266-17','4-48','0.50'),('MS35266-63','10-32','0.50'),('MS35266-119','3/8-24','3.00')]:
 assert parts[part]['thread']==thread and parts[part]['length']==length,part
assert parts['MS35190-221']['head_diameter_max']=='0.225'
assert parts['MS35191-201']['head_diameter_max']=='0.119'
assert parts['MS35265-63']['total_head_height_limits']=='0.165–0.180'
assert parts['MS35266-119']['head_diameter_limits']=='0.590–0.622'
for root in ['MS35265','MS35266']:
 assert D[root]['head_geometry'][4]['head_side_height_limits']=='0.123–0.130'
 assert D[root]['head_geometry'][4]['drilled_hole_diameter_nominal']=='0.046'
for root,dashes in [('MS35190',range(201,209)),('MS35191',range(206,213)),('MS35190',range(328,340)),('MS35191',range(330,342))]:
 for dash in dashes:assert f'{root}-{dash}'not in parts
assert len(parts)==479
print('479 screw references pass drawing examples, coarse/fine mappings, dimension bounds, head details, quote links and search/stock boundaries.')
