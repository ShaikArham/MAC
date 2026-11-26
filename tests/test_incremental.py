import tempfile, unittest, sqlite3, json
from pathlib import Path
from pipelines.incremental import run_batch
class IncrementalTest(unittest.TestCase):
    def test_append_replay_and_rollback(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"etl.sqlite"
            a={"customers":[{"customer_id":"C1","name":"Demo"}]}
            first=run_batch(p,"a",a)
            self.assertEqual(first,run_batch(p,"a",a))
            with self.assertRaises(ValueError): run_batch(p,"a",{})
            b={"orders":[{"order_id":"O1","customer_id":"C1","amount_cents":"100","status":"pending"},{"order_id":"O2","customer_id":"missing","amount_cents":"200","status":"pending"}]}
            result=run_batch(p,"b",b)
            self.assertEqual((result["accepted"],result["rejected"],result["order_value_cents"]),(1,1,100))
            with self.assertRaises(ValueError): run_batch(p,"c",{"customers":[{"customer_id":"C2","name":"Demo"}],"orders":{}})
            with sqlite3.connect(p) as db:
                self.assertEqual(db.execute("SELECT COUNT(*) FROM silver").fetchone()[0],2)
                self.assertEqual(db.execute("SELECT status FROM batches WHERE id='c'").fetchone()[0],"failed")
                self.assertEqual(json.loads(db.execute("SELECT summary FROM gold").fetchone()[0]),result)
                self.assertEqual(db.execute("SELECT COUNT(*) FROM bronze").fetchone()[0],3)
                self.assertEqual(db.execute("SELECT COUNT(*) FROM silver s JOIN bronze b ON s.batch_id=b.batch_id AND s.entity=b.entity AND s.ordinal=b.ordinal").fetchone()[0],2)
