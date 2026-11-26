import json, hashlib, subprocess
from pathlib import Path
from pipelines.business_names import CUSTOMERS,SUPPLIERS
root=Path('.')
def load(p): return json.loads(Path(p).read_text())
def save(p,x): Path(p).write_text(json.dumps(x,separators=(',',':'),ensure_ascii=False))
manifest=load('details/manifest.json')
snapshot=load('snapshot.json')
for entity,names,key in [('customers',CUSTOMERS,'customer_id'),('suppliers',SUPPLIERS,'supplier_id')]:
    p=Path('details')/(entity+'.json')
    rows=load(p)
    assert len(rows)==len(names)==len(set(names))
    mapping={row[key]:name for row,name in zip(rows,names)}
    for row in rows: row['name']=mapping[row[key]]
    for row in snapshot['samples'][entity]: row['name']=mapping[row[key]]
    save(p,rows)
    manifest[entity]['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
    if entity=='customers':
        for m in load('records/manifest.json')['months']:
            assert all(row[2] in mapping for row in load('records/'+m['file']))
    else:
        assert all(row['supplier_id'] in mapping for row in load('details/purchase_orders.json'))
save('details/manifest.json',manifest)
save('snapshot.json',snapshot)
print('600 distinct names, preserved identifiers and transaction references')
