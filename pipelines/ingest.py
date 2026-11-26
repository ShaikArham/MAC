"""Local synthetic order ingestion. Run from repository root: python pipelines/ingest.py."""
import csv
import sqlite3
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
def run():
    with (ROOT / "data/synthetic/customers.csv").open(newline="", encoding="utf-8") as f:
        customers = list(csv.DictReader(f))
    with (ROOT / "data/synthetic/orders.csv").open(newline="", encoding="utf-8") as f:
        orders = list(csv.DictReader(f))
    ids = {c["customer_id"] for c in customers}
    accepted, rejected, seen = [], [], set()
    for row in orders:
        reasons = []
        key = row["order_id"]
        if not key or key in seen: reasons.append("missing or duplicate order ID")
        if row["customer_id"] not in ids: reasons.append("unknown customer")
        try:
            amount = int(row["amount_cents"])
            if amount < 0: reasons.append("negative amount")
        except ValueError:
            reasons.append("invalid amount")
        if row["status"] not in {"pending", "fulfilled"}: reasons.append("invalid status")
        if reasons:
            rejected.append({"record": row, "reasons": reasons})
        else:
            accepted.append((key, row["customer_id"], amount, row["status"]))
            seen.add(key)
    out = ROOT / "data/processed"
    out.mkdir(exist_ok=True)
    with sqlite3.connect(out / "mac.sqlite") as db:
        db.execute("PRAGMA foreign_keys=ON")
        with db:
            db.execute("CREATE TABLE IF NOT EXISTS customers (id TEXT PRIMARY KEY, name TEXT NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS orders (id TEXT PRIMARY KEY, customer_id TEXT REFERENCES customers(id), amount_cents INTEGER CHECK(amount_cents>=0), status TEXT)")
            db.execute("DELETE FROM orders")
            db.execute("DELETE FROM customers")
            db.executemany("INSERT INTO customers VALUES (:customer_id,:name)", customers)
            db.executemany("INSERT INTO orders VALUES (?,?,?,?)", accepted)
            count, total = db.execute("SELECT COUNT(*), COALESCE(SUM(amount_cents),0) FROM orders").fetchone()
    summary = {"source_rows":len(orders),"accepted_rows":count,"rejected_rows":len(rejected),"order_value_cents":total,"synthetic":True}
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    (out / "rejected.json").write_text(json.dumps(rejected, indent=2))
    return summary
if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
