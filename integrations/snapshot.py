"""Single-process persistent registry and canonical snapshot adapter."""
import csv, json, sqlite3, tempfile
from pathlib import Path
from dataclasses import asdict
from integrations.connectors import Registry, Source

class PersistentRegistry(Registry):
    def __init__(self, root, database):
        super().__init__(root)
        self.database = database
        with sqlite3.connect(database) as db:
            db.execute("CREATE TABLE IF NOT EXISTS sources (id TEXT PRIMARY KEY, config TEXT NOT NULL, health TEXT NOT NULL)")
            for key, config, health in db.execute("SELECT id,config,health FROM sources"):
                self.sources[key]=Source(**json.loads(config))
                self.health[key]=json.loads(health)
    def register(self, source):
        super().register(source)
        try:
            with sqlite3.connect(self.database) as db:
                db.execute("INSERT INTO sources VALUES (?,?,?)",(source.id,json.dumps(asdict(source)),json.dumps(self.health[source.id])))
        except Exception:
            self.sources.pop(source.id); self.health.pop(source.id)
            raise
    def read(self, source_id):
        if source_id not in self.sources: raise KeyError(source_id)
        try: return super().read(source_id)
        finally:
            with sqlite3.connect(self.database) as db:
                db.execute("UPDATE sources SET health=? WHERE id=?",(json.dumps(self.health[source_id]),source_id))

def canonical_rows(rows, mapping, columns):
    if set(mapping)!=set(columns) or len(set(mapping.values()))!=len(mapping):
        raise ValueError("mapping must cover canonical columns uniquely")
    return [{col: row[mapping[col]] for col in columns} for row in rows]

def ingest_snapshot(registry, bindings, output_root, pipeline):
    """Use MAC-04 run(root) and SPEC from a combined checkout."""
    if set(bindings)!=set(pipeline.SPEC): raise ValueError("complete snapshot required")
    with tempfile.TemporaryDirectory() as d:
        root=Path(d); folder=root/"data/synthetic"; folder.mkdir(parents=True)
        for table,(pk,fields,refs) in pipeline.SPEC.items():
            source_id,mapping=bindings[table]; columns=[pk,*fields]
            rows=canonical_rows(registry.read(source_id),mapping,columns)
            with (folder/(table+".csv")).open("w",newline="",encoding="utf-8") as f:
                writer=csv.DictWriter(f,fieldnames=columns); writer.writeheader(); writer.writerows(rows)
        summary=pipeline.run(root)
        # Publish one directory only to a new destination; never overwrite a prior snapshot.
        import shutil
        destination=Path(output_root)
        if destination.exists(): raise FileExistsError(destination)
        shutil.copytree(root/"data/processed",destination)
        return summary
