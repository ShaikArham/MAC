"""Transactional append-only batch ETL. SQLite is the publication boundary."""
import hashlib, json, sqlite3
from datetime import datetime, timezone
from pipelines.ingest import SPEC, convert

def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",",":"), allow_nan=False)
def now():
    return datetime.now(timezone.utc).isoformat()
def run_batch(path, batch_id, records):
    """records: mapping entity -> list of canonical string-valued rows.
    Insert-only: existing keys are rejected, not updated. Retry failed batches.
    """
    if not isinstance(batch_id,str) or not batch_id.strip(): raise ValueError("batch ID required")
    if not isinstance(records,dict) or set(records)-set(SPEC): raise ValueError("unknown entity")
    payload=encode(records); digest=hashlib.sha256(payload.encode()).hexdigest()
    db=sqlite3.connect(path)
    try:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS batches(id TEXT PRIMARY KEY,digest TEXT,status TEXT,started TEXT,finished TEXT,error TEXT,result TEXT);
        CREATE TABLE IF NOT EXISTS bronze(batch_id TEXT,entity TEXT,ordinal INTEGER,raw TEXT,PRIMARY KEY(batch_id,entity,ordinal));
        CREATE TABLE IF NOT EXISTS silver(entity TEXT,key TEXT,record TEXT,batch_id TEXT,ordinal INTEGER,PRIMARY KEY(entity,key));
        CREATE TABLE IF NOT EXISTS quarantine(batch_id TEXT,entity TEXT,ordinal INTEGER,reason TEXT,PRIMARY KEY(batch_id,entity,ordinal));
        CREATE TABLE IF NOT EXISTS gold(id INTEGER PRIMARY KEY CHECK(id=1),summary TEXT);
        """)
        db.execute("BEGIN IMMEDIATE")
        old=db.execute("SELECT digest,status,result FROM batches WHERE id=?",(batch_id,)).fetchone()
        if old and old[0]!=digest: raise ValueError("batch ID payload conflict")
        if old and old[1]=="success":
            db.rollback(); return json.loads(old[2])
        db.execute("INSERT OR REPLACE INTO batches VALUES (?,?,?,?,?,?,?)",(batch_id,digest,"running",now(),None,None,None))
        db.execute("SAVEPOINT work")
        try:
            accepted=rejected=0
            for entity,(pk,fields,refs) in SPEC.items():
                rows=records.get(entity,[])
                if not isinstance(rows,list): raise ValueError("entity rows must be list")
                for ordinal,row in enumerate(rows):
                    db.execute("INSERT INTO bronze VALUES (?,?,?,?)",(batch_id,entity,ordinal,encode(row)))
                    try:
                        if not isinstance(row,dict) or set(row)!={pk,*fields}: raise ValueError("invalid columns")
                        clean={c:convert(row[c],kind) for c,kind in {pk:"text",**fields}.items()}
                        if db.execute("SELECT 1 FROM silver WHERE entity=? AND key=?",(entity,clean[pk])).fetchone(): raise ValueError("duplicate key")
                        for col,target in refs.items():
                            if not db.execute("SELECT 1 FROM silver WHERE entity=? AND key=?",(target,clean[col])).fetchone(): raise ValueError("unknown "+col)
                    except (ValueError,TypeError) as exc:
                        db.execute("INSERT INTO quarantine VALUES (?,?,?,?)",(batch_id,entity,ordinal,str(exc))); rejected+=1; continue
                    db.execute("INSERT INTO silver VALUES (?,?,?,?,?)",(entity,clean[pk],encode(clean),batch_id,ordinal)); accepted+=1
            counts=dict(db.execute("SELECT entity,COUNT(*) FROM silver GROUP BY entity"))
            total=sum(json.loads(r[0])["amount_cents"] for r in db.execute("SELECT record FROM silver WHERE entity='orders'"))
            result={"batch_id":batch_id,"accepted":accepted,"rejected":rejected,"entity_counts":counts,"order_value_cents":total}
            db.execute("INSERT OR REPLACE INTO gold VALUES (1,?)",(encode(result),))
            db.execute("UPDATE batches SET status='success',finished=?,result=? WHERE id=?",(now(),encode(result),batch_id))
            db.execute("RELEASE work"); db.commit(); return result
        except Exception as exc:
            db.execute("ROLLBACK TO work"); db.execute("RELEASE work")
            db.execute("UPDATE batches SET status='failed',finished=?,error=? WHERE id=?",(now(),type(exc).__name__,batch_id))
            db.commit(); raise
    finally: db.close()
