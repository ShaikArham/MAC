import csv, tempfile, threading, unittest
from pathlib import Path
from integrations.connectors import Source
from integrations.snapshot import PersistentRegistry, ingest_snapshot
from integrations.mock_http import server
from pipelines import ingest
class EndToEnd(unittest.TestCase):
    def test_snapshot(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            fixtures=ingest.ROOT/"data/synthetic"
            def rows(table):
                with (fixtures/(table+".csv")).open() as f: return list(csv.DictReader(f))
            s=server({"/crm":rows("customers"),"/accounting":rows("invoices")})
            t=threading.Thread(target=s.serve_forever,daemon=True); t.start()
            try:
                registry=PersistentRegistry(fixtures,root/"registry.sqlite")
                bindings={}
                for table,(pk,fields,refs) in ingest.SPEC.items():
                    kind={"customers":"crm_http","invoices":"accounting_http"}.get(table,"csv")
                    registry.register(Source(table,kind,str(s.server_port) if kind.endswith("_http") else table+".csv"))
                    bindings[table]=(table,{c:c for c in [pk,*fields]})
                result=ingest_snapshot(registry,bindings,root/"snapshot",ingest)
                self.assertEqual(result["source_rows"],22)
                self.assertEqual(result["accepted_rows"],17)
                self.assertEqual(result["rejected_rows"],5)
                self.assertEqual(result["order_value_cents"],210000)
                self.assertTrue((root/"snapshot/mac.sqlite").exists())
                self.assertEqual(PersistentRegistry(fixtures,root/"registry.sqlite").health["customers"]["status"],"healthy")
            finally:
                s.shutdown(); s.server_close(); t.join()
