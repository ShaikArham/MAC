"""Deterministic, bounded-size public enterprise preview backed by validated SQLite.
Only synthetic summary information and labeled representative samples are published.
"""
import json, sqlite3, os, tempfile, calendar
from collections import Counter, defaultdict
from pathlib import Path
from pipelines.ingest import run, SPEC

ROOT = Path(__file__).resolve().parents[1]

def build(root=ROOT):
    root=Path(root)
    summary=run(root)
    source=root/'data/synthetic'
    dates=json.loads((source/'order_dates.json').read_text())
    counts=json.loads((source/'stock_counts.json').read_text())
    if len(dates)!=summary['entity_counts']['orders'] or len({x['order_id'] for x in dates})!=len(dates):
        raise ValueError('Order-date mapping incomplete or duplicated')
    if not counts or len({(x['product_id'],x['warehouse_id']) for x in counts})!=len(counts):
        raise ValueError('Stock counts missing or duplicated')
    db=sqlite3.connect(root/'data/processed/mac.sqlite')
    db.row_factory=sqlite3.Row
    try:
        db.execute('CREATE TEMP TABLE dates(order_id TEXT PRIMARY KEY, order_date TEXT NOT NULL)')
        db.executemany('INSERT INTO dates VALUES(?,?)',[(x['order_id'],x['order_date']) for x in dates])
        missing=db.execute('SELECT COUNT(*) FROM orders o LEFT JOIN dates d ON d.order_id=o.order_id WHERE d.order_id IS NULL').fetchone()[0]
        if missing: raise ValueError('Orders without history dates')
        monthly=[]
        for r in db.execute('''SELECT substr(d.order_date,1,7) month,COUNT(*) orders,SUM(o.amount_cents) amount,
            SUM(CASE WHEN o.status='fulfilled' THEN 1 ELSE 0 END) fulfilled
            FROM orders o JOIN dates d ON d.order_id=o.order_id
            GROUP BY month ORDER BY month'''):
            monthly.append(dict(month=r['month'],orders=r['orders'],order_value_cents=r['amount'],fulfilled=r['fulfilled']))
        if len(monthly)!=12 or {r['month'] for r in monthly}!={f'2025-{m:02}' for m in range(1,13)}:
            raise ValueError('Expected exactly twelve months in 2025')
        if sum(x['order_value_cents'] for x in monthly)!=summary['order_value_cents']:
            raise ValueError('Monthly totals disagree with orders')
        wrong_lines=db.execute('''SELECT COUNT(*) FROM orders o JOIN (SELECT order_id,SUM(quantity*unit_price_cents) total
             FROM order_lines GROUP BY order_id) l ON l.order_id=o.order_id WHERE o.amount_cents!=l.total''').fetchone()[0]
        missing_lines=db.execute('SELECT COUNT(*) FROM orders o LEFT JOIN order_lines l ON o.order_id=l.order_id WHERE l.line_id IS NULL').fetchone()[0]
        invoice_wrong=db.execute('''SELECT COUNT(*) FROM invoices i JOIN orders o ON i.order_id=o.order_id WHERE i.amount_cents!=o.amount_cents''').fetchone()[0]
        if wrong_lines or missing_lines or invoice_wrong: raise ValueError('Financial relationships do not reconcile')
        fin=db.execute('''SELECT COALESCE(SUM(i.amount_cents),0) invoiced,
               COALESCE(SUM(COALESCE(p.amount,0)),0) paid
               FROM invoices i LEFT JOIN (SELECT invoice_id,SUM(amount_cents) amount FROM payments GROUP BY invoice_id) p
               ON i.invoice_id=p.invoice_id''').fetchone()
        invoiced,paid=fin['invoiced'],fin['paid']
        if paid>invoiced: raise ValueError('Synthetic payments exceed invoices')
        stock=defaultdict(int)
        for row in db.execute('SELECT product_id,warehouse_id,SUM(quantity_delta) movement FROM stock_movements GROUP BY product_id,warehouse_id'):
            stock[(row['product_id'],row['warehouse_id'])]=row['movement']
        if set(stock)!={(x['product_id'],x['warehouse_id']) for x in counts}:
            raise ValueError('Stock-count locations differ from movements')
        warehouses={x:{'warehouse':x,'expected_units':0,'observed_units':0,'variance_units':0,'exceptions':0} for x in ('W001','W002','W003')}
        issues=[]
        for row in counts:
            key=row['product_id'],row['warehouse_id']
            expected=row['opening']+stock[key];observed=row['observed']
            if expected<0 or observed<0: raise ValueError('Invalid stock quantity')
            w=warehouses[key[1]];w['expected_units']+=expected;w['observed_units']+=observed
            delta=observed-expected;w['variance_units']+=delta
            if delta:
                w['exceptions']+=1
                if len(issues)<8:issues.append(dict(code='stock_mismatch',product_id=key[0],warehouse_id=key[1],delta=delta))
        def sample(sql): return [dict(x) for x in db.execute(sql)]
        raw=summary['source_rows'];accepted=summary['accepted_rows']
        # Financial data is sampled explicitly, never represented as the full ledger.
        invoice_rows=sample('''SELECT i.invoice_id,i.order_id,i.amount_cents,
               i.amount_cents-COALESCE(p.amount,0) balance_cents
               FROM invoices i LEFT JOIN (SELECT invoice_id,SUM(amount_cents) amount FROM payments GROUP BY invoice_id) p
               ON i.invoice_id=p.invoice_id ORDER BY i.invoice_id DESC LIMIT 10''')
        order_rows=sample('''SELECT o.order_id,o.customer_id,o.amount_cents,o.status,d.order_date
                          FROM orders o JOIN dates d ON d.order_id=o.order_id ORDER BY d.order_date DESC,o.order_id DESC LIMIT 14''')
        samples={'orders':order_rows,'invoices':invoice_rows,
                 'customers':sample('SELECT customer_id,name FROM customers LIMIT 10'),
                 'products':sample('SELECT product_id,sku,name FROM products LIMIT 10'),
                 'suppliers':sample('SELECT supplier_id,name FROM suppliers LIMIT 10'),
                 'purchase_orders':sample('SELECT purchase_id,supplier_id,status FROM purchase_orders LIMIT 10'),
                 'exceptions':issues}
        # Rejections are validated pipeline evidence (not artificial UI values).
        rejected=json.loads((root/'data/processed/rejected.json').read_text())
        quality=[dict(entity=k,accepted=v,source=v+sum(x['table']==k for x in rejected)) for k,v in summary['entity_counts'].items()]
        return {'schema_version':2,'synthetic':True,'mode':'enterprise_aggregate',
                'business':{'name':'Horizon Supplies','year':2025,'warehouses':3,'currency':'EUR'},
                'summary':summary,'monthly':monthly,
                'finance':{'invoiced_cents':invoiced,'paid_cents':paid,'outstanding_cents':invoiced-paid},
                'operations':{'fulfilled':sum(x['fulfilled'] for x in monthly),
                              'pending':sum(x['orders']-x['fulfilled'] for x in monthly),
                              'warehouse_stats':list(warehouses.values()),
                              'stock_exception_count':sum(x['exceptions'] for x in warehouses.values())},
                'quality':quality,'samples':samples,
                'monitoring':{'batch_status':'validated_sqlite_snapshot','accepted':accepted,'rejected':raw-accepted,
                              'source_rows':raw,'historical_period':'2025-01 through 2025-12'},
                'provenance':'Generated deterministically from synthetic fixtures; sampled rows are not complete ledgers.'}
    finally: db.close()

def publish(destination,root=ROOT):
    data=build(root)
    destination=Path(destination);destination.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile('w',encoding='utf-8',dir=destination.parent,delete=False) as f:
        path=f.name;json.dump(data,f,ensure_ascii=False,separators=(',',':'),allow_nan=False)
    try: os.replace(path,destination)
    finally:
        if os.path.exists(path):os.unlink(path)
    return data

if __name__=='__main__':
    import sys
    d=publish(sys.argv[1] if len(sys.argv)>1 else 'enterprise-snapshot.json')
    print(json.dumps({'business':d['business'],'summary':d['summary'],'finance':d['finance'],'operations':d['operations'],'bytes':Path(sys.argv[1] if len(sys.argv)>1 else 'enterprise-snapshot.json').stat().st_size},indent=2))
