"""Generate a static synthetic preview from validated ETL and reconciliation."""
import csv, json, sqlite3, tempfile, os
from pathlib import Path
from contextlib import closing
from pipelines.ingest import ROOT, SPEC
from pipelines.connected_batch import run_connected
from integrations.connectors import Source
from integrations.snapshot import PersistentRegistry
from pipelines.reconcile import reconcile
from pipelines.monitor import collect

def build():
    with tempfile.TemporaryDirectory() as d:
        path=Path(d)/"etl.sqlite"
        registry=PersistentRegistry(ROOT/"data/synthetic",Path(d)/"registry.sqlite")
        bindings={}
        for entity,(pk,fields,_) in SPEC.items():
            registry.register(Source(entity,"csv",entity+".csv"))
            bindings[entity]=(entity,{c:c for c in [pk,*fields]})
        summary=run_connected(path,"preview",registry,bindings)
        report=reconcile(path,[dict(product_id="P001",warehouse_id="W001",opening=0,observed=88)])
        rows={entity:[] for entity in SPEC}
        with closing(sqlite3.connect(path)) as db:
            for entity,record in db.execute("SELECT entity,record FROM silver ORDER BY entity,key"):
                rows[entity].append(json.loads(record))
        return dict(schema_version=1,synthetic=True,mode="generated_snapshot",summary=summary,records=rows,reconciliation=report,monitoring=collect(path,registry))
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
