"""Generate a static synthetic preview from validated ETL and reconciliation."""
import csv, json, sqlite3, tempfile, os
from pathlib import Path
from contextlib import closing
from pipelines.ingest import ROOT, SPEC
from pipelines.incremental import run_batch
from pipelines.reconcile import reconcile

def build():
    records={}
    for entity in SPEC:
        with (ROOT/"data/synthetic"/(entity+".csv")).open(newline="",encoding="utf-8") as f:
            records[entity]=list(csv.DictReader(f))
    with tempfile.TemporaryDirectory() as d:
        path=Path(d)/"etl.sqlite"
        summary=run_batch(path,"preview",records)
        report=reconcile(path,[dict(product_id="P001",warehouse_id="W001",opening=0,observed=88)])
        rows={entity:[] for entity in SPEC}
        with closing(sqlite3.connect(path)) as db:
            for entity,record in db.execute("SELECT entity,record FROM silver ORDER BY entity,key"):
                rows[entity].append(json.loads(record))
        return dict(schema_version=1,synthetic=True,mode="generated_snapshot",summary=summary,records=rows,reconciliation=report)
def publish(destination):
    destination=Path(destination)
    payload=json.dumps(build(),indent=2,allow_nan=False)
    with tempfile.NamedTemporaryFile(mode="w",encoding="utf-8",dir=destination.parent,delete=False) as f:
        name=f.name
        f.write(payload)
    try: os.replace(name,destination)
    finally:
        if os.path.exists(name): os.unlink(name)
if __name__=="__main__":
    import sys
    publish(sys.argv[1])
