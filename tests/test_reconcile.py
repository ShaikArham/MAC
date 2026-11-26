import csv, tempfile, unittest
from pathlib import Path
from pipelines.ingest import ROOT, SPEC
from pipelines.incremental import run_batch
from pipelines.reconcile import reconcile
class ReconcileTest(unittest.TestCase):
    def test_fixture(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'etl.sqlite'; records={}
            for table in SPEC:
                with (ROOT/'data/synthetic'/f'{table}.csv').open() as f: records[table]=list(csv.DictReader(f))
            run_batch(p,'base',records)
            count=dict(product_id='P001',warehouse_id='W001',opening=0,observed=88)
            result=reconcile(p,[count])
            self.assertEqual(result['outstanding_cents'],65000)
            self.assertEqual(result['stock'][0]['delta'],-2)
            self.assertEqual([e['code'] for e in result['exceptions']],['stock_mismatch'])
            with self.assertRaises(ValueError): reconcile(p,[count,count])
            run_batch(p,'extra',{'payments':[dict(payment_id='PAY004',invoice_id='I001',amount_cents='100',paid_date='2026-01-06')]})
            self.assertEqual(reconcile(p,[count])['overpaid_cents'],100)
