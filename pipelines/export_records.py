"""Export validated order records into monthly JSON shards."""
import json, sqlite3, hashlib
from pathlib import Path
from datetime import date
from collections import defaultdict
from contextlib import closing

def export(root, destination):
    root, destination = Path(root), Path(destination)
    dates = json.loads((root/'data/synthetic/order_dates.json').read_text())
    mapping = {x['order_id']: date.fromisoformat(x['order_date']).isoformat() for x in dates}
    if len(mapping)!=len(dates): raise ValueError('Duplicate date mapping')
    months=defaultdict(list)
    with closing(sqlite3.connect(root/'data/processed/mac.sqlite')) as db:
        for oid,cid,amount,status in db.execute('SELECT order_id,customer_id,amount_cents,status FROM orders ORDER BY order_id'):
            day=mapping.pop(oid); months[day[:7]].append([oid,day,cid,amount,status])
    if mapping: raise ValueError('Unmatched dates')
    destination.mkdir(parents=True,exist_ok=True)
    manifest={'schema_version':1,'synthetic':True,'columns':['order_id','order_date','customer_id','amount_cents','status'],'months':[]}
    for month,rows in sorted(months.items()):
        rows.sort(key=lambda r:(r[1],r[0]))
        payload=json.dumps(rows,separators=(',',':')).encode()
        filename=month+'.json'; (destination/filename).write_bytes(payload)
        manifest['months'].append({'month':month,'file':filename,'count':len(rows),'amount_cents':sum(r[3] for r in rows),'sha256':hashlib.sha256(payload).hexdigest()})
    (destination/'manifest.json').write_text(json.dumps(manifest,separators=(',',':')))
    return manifest
if __name__=='__main__':
    import sys
    print(json.dumps(export(*sys.argv[1:]),indent=2))
