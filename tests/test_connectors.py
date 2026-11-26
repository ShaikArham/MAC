import json, tempfile, unittest
from pathlib import Path
from openpyxl import Workbook
from integrations.connectors import Registry, Source
class Connectors(unittest.TestCase):
    def test_formats_and_health(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); r=Registry(p)
            (p/'a.csv').write_text('id\n1\n'); (p/'a.json').write_text('[{"id":1}]')
            (p/'api.json').write_text(json.dumps({'simulated':True,'records':[{'id':1}]}))
            w=Workbook(); w.active.append(['id']); w.active.append([1]); w.save(p/'a.xlsx'); w.close()
            for kind,name in [('csv','a.csv'),('json','a.json'),('excel','a.xlsx'),('accounting','api.json'),('crm','api.json')]:
                r.register(Source(kind,kind,name)); self.assertEqual(len(r.read(kind)),1); self.assertEqual(r.health[kind]['status'],'healthy')
            r.register(Source('bad','csv','missing.csv'))
            with self.assertRaises(FileNotFoundError): r.read('bad')
            self.assertEqual(r.health['bad']['status'],'failed')
            with self.assertRaises(ValueError): r.register(Source('bad','csv','a.csv'))
            r.register(Source('escape','json','../outside.json'))
            with self.assertRaises(ValueError): r.read('escape')
    def test_invalid_payload(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'bad.json').write_text('{"records":[]}'); r=Registry(p); r.register(Source('a','crm','bad.json'))
            with self.assertRaises(ValueError): r.read('a')
            self.assertEqual(r.health['a']['status'],'failed')
