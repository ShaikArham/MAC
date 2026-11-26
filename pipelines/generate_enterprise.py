"""Deterministic synthetic wholesale fixture generator; no personal data."""
import random,csv,calendar
from datetime import date,timedelta
from pathlib import Path
from pipelines.ingest import SPEC
from pipelines.business_names import CUSTOMERS, SUPPLIERS
GOODS=[("Cement","General purpose cement 25kg","bag",850),("Cement","Ready-mix mortar 20kg","bag",1100),("Masonry","Concrete block 440mm","each",220),("Insulation","PIR insulation board","board",4200),("Insulation","Mineral wool insulation","pack",3800),("Timber","Structural timber C24","length",1800),("Timber","OSB sheathing board","sheet",2600),("Drylining","Moisture resistant plasterboard","sheet",1900),("Paint","Interior emulsion 10L","tin",4500),("Paint","Exterior masonry paint 10L","tin",6500),("Plumbing","Copper pipe 3m","length",2400),("Plumbing","PVC drainage pipe 3m","length",1600),("Plumbing","Compression fitting","each",650),("Electrical","Electrical conduit 3m","length",450),("Electrical","Twin and earth cable 100m","roll",11500),("Roofing","Roofing membrane","roll",8500),("Fixings","Galvanised fixings","box",1200),("Tiling","Tile adhesive 20kg","bag",1900),("Sealants","Silicone sealant","tube",750),("Safety","Safety work gloves","pair",550)]
def product(i):
    category,name,unit,base=GOODS[(i-1)%20]
    variant=(i-1)//20
    return dict(product_id=f"P{i:04}",category=category,unit=unit,name=f"{name} / range {variant+1:02}",price_cents=base*(100+variant%10*5)//100)
def generate(root,year=2025,seed=42,orders=50000):
    rng=random.Random(seed)
    rows={k:[] for k in SPEC}
    def add(k,**row): rows[k].append(row)
    for i in range(1,501): add("customers",customer_id=f"C{i:04}",name=CUSTOMERS[i-1])
    for i in range(1,2001): add("products",product_id=f"P{i:04}",sku=f"SKU-{i:04}",name=product(i)["name"])
    for i in range(1,101): add("suppliers",supplier_id=f"S{i:03}",name=SUPPLIERS[i-1])
    dates=[]; stock={}
    for i in range(1,orders+1):
        oid=f"O{i:06}"; month=rng.choices(range(1,13),weights=[7,7,8,8,9,9,8,8,10,11,14,13])[0]
        day=date(year,month,rng.randint(1,calendar.monthrange(year,month)[1]))
        fulfilled=rng.random()<.94; total=0
        for j in range(rng.randint(2,4)):
            p=f"P{rng.randint(1,2000):04}"; qty=rng.randint(1,20); rng.randint(200,15000); price=product(int(p[1:]))["price_cents"]; total+=qty*price
            add("order_lines",line_id=f"L{i:06}-{j}",order_id=oid,product_id=p,quantity=qty,unit_price_cents=price)
            if fulfilled:
                w=f"W{rng.randint(1,3):03}"; stock[p,w]=stock.get((p,w),0)+qty
                add("stock_movements",movement_id=f"M{i:06}-{j}",product_id=p,warehouse_id=w,quantity_delta=-qty,timestamp=day.isoformat()+"T12:00:00+00:00")
        add("orders",order_id=oid,customer_id=f"C{rng.randint(1,500):04}",amount_cents=total,status="fulfilled" if fulfilled else "pending")
        dates.append(dict(order_id=oid,order_date=day.isoformat()))
        if fulfilled:
            add("dispatches",dispatch_id=f"D{i:06}",order_id=oid,status="delivered",timestamp=day.isoformat()+"T13:00:00+00:00")
            inv=f"I{i:06}"; add("invoices",invoice_id=inv,order_id=oid,amount_cents=total,issued_date=day.isoformat())
            paid=rng.choices([total,total//2,0],[85,10,5])[0]
            if paid: add("payments",payment_id=f"PAY{i:06}",invoice_id=inv,amount_cents=paid,paid_date=day.isoformat())
    for i in range(1,1201): add("purchase_orders",purchase_id=f"PO{i:05}",supplier_id=f"S{rng.randint(1,100):03}",status="received")
    counts=[]
    for (p,w),qty in sorted(stock.items()):
        opening=qty+100; counts.append(dict(product_id=p,warehouse_id=w,opening=opening,observed=98 if rng.random()<.02 else 100))
    rows["orders"].append(dict(rows["orders"][0]))
    rows["orders"].append(dict(order_id="BAD-ORDER",customer_id="MISSING",amount_cents=100,status="pending"))
    dest=Path(root)/"data/synthetic"; dest.mkdir(parents=True,exist_ok=True)
    for entity,(pk,fields,_) in SPEC.items():
        with (dest/(entity+".csv")).open("w",newline="",encoding="utf-8") as f:
            writer=csv.DictWriter(f,fieldnames=[pk,*fields]);writer.writeheader();writer.writerows(rows[entity])
    import json
    (dest/"catalogue.json").write_text(json.dumps([product(i) for i in range(1,2001)]),encoding="utf-8")
    (dest/"warehouses.json").write_text(json.dumps({"W001":"Dublin","W002":"Cork","W003":"Galway"}),encoding="utf-8")
    (dest/"order_dates.json").write_text(json.dumps(dates),encoding="utf-8")
    (dest/"stock_counts.json").write_text(json.dumps(counts),encoding="utf-8")
    return {k:len(v) for k,v in rows.items()}
if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser();p.add_argument("root");p.add_argument("--orders",type=int,default=50000);a=p.parse_args()
    print(generate(a.root,orders=a.orders))
