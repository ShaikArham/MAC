# Initial data contracts — proposed
All identifiers are synthetic strings. Monetary amounts are integer EUR cents. Dates use ISO 8601. Source timestamps should carry timezone offsets.

| Entity | Primary key | Relationships | Required fields |
|---|---|---|---|
| Customer | customer_id | — | name |
| Order | order_id | customer_id | amount_cents, status |
| Product | product_id | — | sku, name |
| Order line | line_id | order_id, product_id | quantity, unit_price_cents |
| Supplier | supplier_id | — | name |
| Purchase order | purchase_id | supplier_id | status |
| Stock movement | movement_id | product_id | warehouse_id, quantity_delta, timestamp |
| Dispatch | dispatch_id | order_id | status, timestamp |
| Invoice | invoice_id | order_id | amount_cents, issued_date |
| Payment | payment_id | invoice_id | amount_cents, paid_date |

Existing ingestion implements Customer and Order only. Other contracts are proposed, not implemented. Order value is distinct from recognized revenue. Invoice balance = invoice amount minus allocated payments; overpayments must be flagged. Stock reconciliation compares opening quantity plus signed movements to observed closing quantity. Reject invalid foreign keys and duplicate primary keys; preserve raw inputs and rejection reasons. Batch IDs and lineage are required for later incremental ingestion.
