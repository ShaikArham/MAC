import shutil, sqlite3, tempfile, unittest
from pathlib import Path
from pipelines.ingest import ROOT, run
class SnapshotTest(unittest.TestCase):
    def test_repeatable_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            shutil.copytree(ROOT/"data/synthetic",root/"data/synthetic")
            first=run(root)
            self.assertEqual(first,run(root))
            self.assertEqual(first["order_value_cents"],210000)
            self.assertEqual(first["rejected_rows"],5)
            self.assertEqual(first["source_rows"],first["accepted_rows"]+first["rejected_rows"])
            with sqlite3.connect(root/"data/processed/mac.sqlite") as db:
                self.assertEqual(db.execute("PRAGMA foreign_key_check").fetchall(),[])
                self.assertEqual(db.execute("SELECT COUNT(*) FROM payments").fetchone()[0],2)
if __name__=="__main__": unittest.main()
