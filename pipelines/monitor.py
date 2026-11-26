"""Read recorded execution evidence; no invented uptime or retry history."""
import sqlite3
from contextlib import closing

def collect(path, registry):
    with closing(sqlite3.connect(path)) as db:
        db.row_factory=sqlite3.Row
        db.execute('BEGIN')
        batches=[dict(r) for r in db.execute('SELECT id,status,started,finished,error FROM batches ORDER BY started,id')]
        rejects=[dict(r) for r in db.execute('SELECT batch_id,entity,ordinal,reason FROM quarantine ORDER BY batch_id,entity,ordinal')]
        counts={t:db.execute('SELECT COUNT(*) FROM '+t).fetchone()[0] for t in ('bronze','silver','quarantine')}
    sources=[dict(id=k,kind=registry.sources[k].kind,**v) for k,v in sorted(registry.health.items())]
    return dict(sources=sources,batches=batches,rejections=rejects,counts=counts,audit=[dict(event='batch_'+b['status'],reference=b['id'],timestamp=b['finished'] or b['started']) for b in batches])
