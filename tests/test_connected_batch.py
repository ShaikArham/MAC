import tempfile, unittest, sqlite3, threading
from pathlib import Path
from integrations.connectors import Source
from integrations.snapshot import PersistentRegistry
from integrations.mock_http import server
from pipelines.connected_batch import run_connected
from pipelines.incremental import run_batch

class ConnectedBatchTest(unittest.TestCase):
    def test_http_csv_replay_and_recovery(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); db=p/'etl.sqlite'
            (p/'orders.csv').write_text('order_id,customer_id,amount_cents,status\nO1,C1,12500,pending\n')
            s=server({'/crm':[{'ID':'C1','Name':'Demo'}]})
            t=threading.Thread(target=s.serve_forever,daemon=True); t.start()
            try:
                r=PersistentRegistry(p,p/'registry.sqlite')
                r.register(Source('crm','crm_http',str(s.server_port)))
                r.register(Source('orders','csv','orders.csv'))
                bindings={'customers':('crm',{'customer_id':'ID','name':'Name'}),'orders':('orders',{k:k for k in ['order_id','customer_id','amount_cents','status']})}
                first=run_connected(db,'one',r,bindings)
                self.assertEqual((first['accepted'],first['rejected'],first['order_value_cents']),(2,0,12500))
                self.assertEqual(first,run_connected(db,'one',r,bindings))
                with self.assertRaises(ValueError): run_batch(db,'bad',{'orders':{}})
                with self.assertRaises(ValueError): run_batch(db,'bad',{'orders':{}})
                result=run_batch(db,'corrected',{'orders':[{'order_id':'O2','customer_id':'C1','amount_cents':'500','status':'pending'}]})
                self.assertEqual(result['order_value_cents'],13000)
                with sqlite3.connect(db) as c:
                    self.assertEqual(c.execute('SELECT COUNT(*) FROM bronze').fetchone()[0],3)
                    self.assertEqual(c.execute('SELECT status FROM batches WHERE id=\'bad\'').fetchone()[0],'failed')
            finally:
                s.shutdown(); s.server_close(); t.join()
