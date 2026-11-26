"""Read-only reconciliation of a consistent Silver snapshot."""
import json, sqlite3
from collections import defaultdict
from contextlib import closing

def reconcile(path, stock_counts=()):
    with closing(sqlite3.connect(path)) as db:
        db.execute('BEGIN')
        rows=defaultdict(list)
        for entity,record in db.execute('SELECT entity,record FROM silver ORDER BY entity,key'):
            rows[entity].append(json.loads(record))
    exceptions=[]
    def flag(code,key,delta=None):
        exceptions.append(dict(code=code,key=key,delta=delta))
    paid=defaultdict(int); billed=defaultdict(int); lines=defaultdict(int)
    for p in rows['payments']: paid[p['invoice_id']]+=p['amount_cents']
    for l in rows['order_lines']: lines[l['order_id']]+=l['quantity']*l['unit_price_cents']
    balances=[]
    for i in rows['invoices']:
        key=i['invoice_id']; amount=i['amount_cents']; balance=amount-paid[key]
        billed[i['order_id']]+=amount
        balances.append(dict(invoice_id=key,balance_cents=balance))
        if balance<0: flag('overpayment',key,balance)
    for o in rows['orders']:
        key=o['order_id']; amount=o['amount_cents']
        if key not in lines: flag('missing_order_lines',key)
        elif lines[key]!=amount: flag('order_line_mismatch',key,lines[key]-amount)
        if key not in billed and o['status']=='fulfilled': flag('missing_invoice',key)
        elif key in billed and billed[key]!=amount: flag('invoice_order_mismatch',key,billed[key]-amount)
    movements=defaultdict(int)
    for m in rows['stock_movements']: movements[(m['product_id'],m['warehouse_id'])]+=m['quantity_delta']
    stock=[]; seen=set()
    for c in stock_counts:
        key=(c['product_id'],c['warehouse_id'])
        if key in seen: raise ValueError('duplicate stock count')
        seen.add(key)
        if any(type(c[k]) is not int or c[k]<0 for k in ('opening','observed')): raise ValueError('invalid stock count')
        expected=c['opening']+movements[key]; delta=c['observed']-expected
        stock.append(dict(product_id=key[0],warehouse_id=key[1],expected=expected,observed=c['observed'],delta=delta))
        if delta: flag('stock_mismatch',list(key),delta)
    for key in sorted(set(movements)-seen): flag('stock_count_missing',list(key))
    return dict(invoices=balances,outstanding_cents=sum(max(0,b['balance_cents']) for b in balances),overpaid_cents=sum(max(0,-b['balance_cents']) for b in balances),stock=stock,exceptions=exceptions)
