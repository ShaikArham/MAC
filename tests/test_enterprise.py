import json, tempfile, unittest
from pathlib import Path
from pipelines.generate_enterprise import generate
from pipelines.export_enterprise import publish

class EnterpriseTest(unittest.TestCase):
    def test_pilot_relationships_and_reconciliation(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            counts=generate(root,orders=100)
            s=publish(root/'snapshot.json',root)
            self.assertEqual(s['summary']['entity_counts']['orders'],100)
            self.assertEqual(s['summary']['rejected_rows'],2)
            self.assertEqual(sum(m['orders'] for m in s['monthly']),100)
            self.assertEqual(sum(m['order_value_cents'] for m in s['monthly']),s['summary']['order_value_cents'])
            self.assertEqual(s['finance']['invoiced_cents']-s['finance']['paid_cents'],s['finance']['outstanding_cents'])
            self.assertEqual(len(s['operations']['warehouse_stats']),3)
            self.assertLess((root/'snapshot.json').stat().st_size,100_000)
            self.assertEqual(s['synthetic'],True)
            self.assertEqual(s['schema_version'],2)
            self.assertEqual(len(s['samples']['orders']),14)
            self.assertEqual(json.loads((root/'snapshot.json').read_text())['monthly'],s['monthly'])

if __name__=='__main__':unittest.main()
