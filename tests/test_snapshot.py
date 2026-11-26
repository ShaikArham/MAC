import tempfile, unittest, threading
from pathlib import Path
from integrations.connectors import Source
from integrations.snapshot import PersistentRegistry, canonical_rows
from integrations.mock_http import server, fetch

class IntegrationTests(unittest.TestCase):
    def test_persistence(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/"a.csv").write_text("id,name\n1,Demo\n")
            r=PersistentRegistry(p,p/"registry.sqlite")
            r.register(Source("a","csv","a.csv"))
            self.assertEqual(len(r.read("a")),1)
            r=PersistentRegistry(p,p/"registry.sqlite")
            self.assertEqual(r.health["a"]["status"],"healthy")
            self.assertEqual(r.read("a")[0]["id"],"1")
    def test_mapping(self):
        self.assertEqual(canonical_rows([{"ID":"1"}],{"id":"ID"},["id"]),[{"id":"1"}])
        with self.assertRaises(ValueError): canonical_rows([],{},["id"])
    def test_http(self):
        s=server({"/crm":[{"id":"C1"}],"/accounting":[{"id":"I1"}]})
        t=threading.Thread(target=s.serve_forever,daemon=True); t.start()
        try:
            self.assertEqual(fetch(s.server_port,"crm"),[{"id":"C1"}])
            self.assertEqual(fetch(s.server_port,"accounting"),[{"id":"I1"}])
        finally:
            s.shutdown(); s.server_close(); t.join()
