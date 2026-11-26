"""Validated synthetic snapshot; standard library only."""
import csv, json, sqlite3
from datetime import date, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
# Ordered dependencies; field types and references are fixed, never input SQL.
SPEC = {
"customers": ("customer_id", {"name":"text"}, {}),
"products": ("product_id", {"sku":"text","name":"text"}, {}),
"suppliers": ("supplier_id", {"name":"text"}, {}),
"orders": ("order_id", {"customer_id":"text","amount_cents":"nonnegative","status":"pending|fulfilled"}, {"customer_id":"customers"}),
"order_lines": ("line_id", {"order_id":"text","product_id":"text","quantity":"positive","unit_price_cents":"nonnegative"}, {"order_id":"orders","product_id":"products"}),
"purchase_orders": ("purchase_id", {"supplier_id":"text","status":"pending|received|cancelled"}, {"supplier_id":"suppliers"}),
"stock_movements": ("movement_id", {"product_id":"text","warehouse_id":"text","quantity_delta":"integer","timestamp":"timestamp"}, {"product_id":"products"}),
"dispatches": ("dispatch_id", {"order_id":"text","status":"pending|dispatched|delivered","timestamp":"timestamp"}, {"order_id":"orders"}),
"invoices": ("invoice_id", {"order_id":"text","amount_cents":"nonnegative","issued_date":"date"}, {"order_id":"orders"}),
"payments": ("payment_id", {"invoice_id":"text","amount_cents":"nonnegative","paid_date":"date"}, {"invoice_id":"invoices"})
}
NUM = {"integer","positive","nonnegative"}
def convert(value, kind):
    if not isinstance(value,str) or not value.strip(): raise ValueError("required value")
    value=value.strip()
    if kind in NUM:
        n=int(value)
        if not -(2**63)<=n<2**63: raise ValueError("integer out of range")
        if kind=="positive" and n<=0 or kind=="nonnegative" and n<0: raise ValueError("invalid range")
        return n
    if kind=="date":
        if date.fromisoformat(value).isoformat()!=value: raise ValueError("expected ISO date")
    elif kind=="timestamp":
        if datetime.fromisoformat(value).utcoffset() is None: raise ValueError("timezone required")
    elif "|" in kind and value not in kind.split("|"): raise ValueError("invalid status")
    return value
def run(root=ROOT):
    out=root/"data/processed"; out.mkdir(parents=True,exist_ok=True)
    accepted={}; rejected=[]; raw=[]; counts={}
    for table,(pk,fields,refs) in SPEC.items():
        cols={pk:"text",**fields}; accepted[table]={}
        with (root/"data/synthetic"/(table+".csv")).open(newline="",encoding="utf-8") as f:
            reader=csv.DictReader(f)
            if reader.fieldnames is None or len(reader.fieldnames)!=len(cols) or set(reader.fieldnames)!=set(cols): raise ValueError("invalid header: "+table)
            for row in reader:
                raw.append({"table":table,"line":reader.line_num,"record":row})
                reasons=[]; clean={}
                if None in row: reasons.append("extra fields")
                for col,kind in cols.items():
                    try: clean[col]=convert(row.get(col),kind)
                    except (ValueError,TypeError) as e: reasons.append(col+": "+str(e))
                if clean.get(pk) in accepted[table]: reasons.append("duplicate primary key")
                for col,target in refs.items():
                    if clean.get(col) not in accepted[target]: reasons.append("unknown "+col)
                if reasons: rejected.append({"table":table,"line":reader.line_num,"record":row,"reasons":reasons})
                else: accepted[table][clean[pk]]=clean
        counts[table]=len(accepted[table])
    db=sqlite3.connect(out/"mac.sqlite")
    try:
        db.execute("PRAGMA foreign_keys=ON")
        with db:
            db.execute("BEGIN")
            for table in reversed(SPEC): db.execute("DROP TABLE IF EXISTS "+table)
            for table,(pk,fields,refs) in SPEC.items():
                cols={pk:"text",**fields}
                defs=[c+(" INTEGER" if k in NUM else " TEXT")+" NOT NULL"+(" PRIMARY KEY" if c==pk else "")+(" REFERENCES "+refs[c]+"("+SPEC[refs[c]][0]+")" if c in refs else "") for c,k in cols.items()]
                db.execute("CREATE TABLE "+table+" ("+",".join(defs)+")")
                db.executemany("INSERT INTO "+table+" VALUES ("+",".join("?" for _ in cols)+")",[tuple(row[c] for c in cols) for row in accepted[table].values()])
            total=db.execute("SELECT COALESCE(SUM(amount_cents),0) FROM orders").fetchone()[0]
            assert not db.execute("PRAGMA foreign_key_check").fetchall()
    finally: db.close()
    summary={"synthetic":True,"source_rows":len(raw),"accepted_rows":sum(counts.values()),"rejected_rows":len(rejected),"entity_counts":counts,"order_value_cents":total}
    for name,value in [("raw",raw),("rejected",rejected),("summary",summary)]:
        (out/(name+".json")).write_text(json.dumps(value,indent=2),encoding="utf-8")
    return summary
if __name__=="__main__": print(json.dumps(run(),indent=2))
