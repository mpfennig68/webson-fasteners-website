"""Check dimensional bounds, visible stock rows and selected drawing references."""
from pathlib import Path
from html import unescape
from decimal import Decimal
import json,re

W=Path(__file__).resolve().parents[1]
D=json.loads((W/'scripts/mil-spec-data.json').read_text())
groups=[('nut_sizes',root)for root in ['MS21042','MS21044','MS21083']]+[('socket_screw_sizes',root)for root in ['MS16995','MS16996']]+[('stocked_washer_sizes','MS35338')]
parts={}
total=0
for key,root in groups:
 page=(W/('Reference-'+root+'.html')).read_text()
 for record in D[key][root]:
  parts[record['part']]=record
  row=re.search(r'<tr\b[^>]*><th scope="row">'+re.escape(record['part'])+r'</th>.*?</tr>',page)
  assert row,record['part']
  for field,value in record.items():
   if field.endswith('_limits'):
    lower,upper=map(Decimal,value.split('–'))
    assert 0<lower<=upper,(record['part'],field,value)
    assert '>'+value+'<' in unescape(row[0]),(record['part'],field,'not visible')
  assert 'Stocked item' in row[0]
  assert 'part='+record['part']+'"' in unescape(row[0])
  total+=1
# Independent spot values from enlarged drawing regions, including easily confused cells.
assert parts['MS21044N04']['height_limits']=='0.133–0.157'
assert parts['MS21042L3']['across_flats_limits']=='0.243–0.252'
assert parts['MS21083C08']['across_flats_limits']=='0.336–0.345'
assert parts['MS16996-10']['head_diameter_limits']=='0.303–0.313'
assert parts['MS16996-2']['socket_width_limits']=='0.0500–0.0510'
assert parts['MS16995-2']['socket_width_limits']=='0.0781–0.0791'
assert parts['MS35338-40']['inside_diameter_limits']=='.114–.120'
assert parts['MS35338-40']['section_thickness_limits']=='.025–0.033'
assert total==39,total
print(f'{total} MS stock rows pass visible dimensions, ordered bounds, quote links and drawing spot checks.')
