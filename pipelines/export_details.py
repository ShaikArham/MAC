"""Publish relational detail shards from validated SQLite, never fabricated links."""
import json,sqlite3,hashlib
from pathlib import Path
from contextlib import closing
from collections import defaultdict
def export(root,dest):
 root,dest=Path(root),Path(dest);dest.mkdir(parents=True,exist_ok=True)
 dates={x['order_id']:x['order_date'] for x in json.loads((root/'data/synthetic/order_dates.json').read_text())}
 catalogue={x['product_id']:x for x in json.loads((root/'data/synthetic/catalogue.json').read_text())}
 warehouses=json.loads((root/'data/synthetic/warehouses.json').read_text())
 manifest={}
 def write(name,rows):
  data=json.dumps(rows,separators=(',',':')).encode();(dest/(name+'.json')).write_bytes(data);manifest[name]={'count':len(rows),'sha256':hashlib.sha256(data).hexdigest()}
 with closing(sqlite3.connect(root/'data/processed/mac.sqlite')) as db:
  db.row_factory=sqlite3.Row
  for entity in ['customers','products','suppliers','purchase_orders','stock_movements','order_lines','dispatches','invoices','payments']:
   rows=[dict(x) for x in db.execute('SELECT * FROM '+entity)]
   if entity=='products':rows=[{**x,**catalogue[x['product_id']]} for x in rows]
   if entity=='stock_movements':rows=[{**x,'warehouse':warehouses[x['warehouse_id']]} for x in rows]
   if entity in ['customers','products','suppliers','purchase_orders']:write(entity,rows);continue
   groups=defaultdict(list)
   for row in rows:
    if entity=='stock_movements': key=row['timestamp'][:7]
    elif entity=='payments':key=row['paid_date'][:7]
    else:key=dates[row['order_id']][:7]
    groups[key].append(row)
   for month in sorted(set(d[:7] for d in dates.values())):write(entity+'-'+month,groups[month])
  stock=[]
  movements={(x[0],x[1]):x[2] for x in db.execute('SELECT product_id,warehouse_id,SUM(quantity_delta) FROM stock_movements GROUP BY product_id,warehouse_id')}
  for x in json.loads((root/'data/synthetic/stock_counts.json').read_text()):
   expected=x['opening']+movements[(x['product_id'],x['warehouse_id'])];stock.append({**x,'warehouse':warehouses[x['warehouse_id']],'expected':expected,'delta':x['observed']-expected})
  write('stock_counts',stock)
 write('rejections',json.loads((root/'data/processed/rejected.json').read_text()))
 (dest/'manifest.json').write_text(json.dumps(manifest,separators=(',',':')))
if __name__=='__main__':
 import sys
 export(*sys.argv[1:])
