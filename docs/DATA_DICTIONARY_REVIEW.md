# Canonical data dictionary

Source: [pipelines/ingest.py](https://github.com/ShaikArham/MAC/blob/mac-data-engineering/pipelines/ingest.py), SPEC and convert. This describes the canonical ingestion schema, not every enriched browser field.

| Entity | Primary key | Other fields | References |
|---|---|---|---|
| customers | customer_id | name | — |
| products | product_id | sku, name | — |
| suppliers | supplier_id | name | — |
| orders | order_id | customer_id, amount_cents, status | customers |
| order_lines | line_id | order_id, product_id, quantity, unit_price_cents | orders, products |
| purchase_orders | purchase_id | supplier_id, status | suppliers |
| stock_movements | movement_id | product_id, warehouse_id, quantity_delta, timestamp | products |
| dispatches | dispatch_id | order_id, status, timestamp | orders |
| invoices | invoice_id | order_id, amount_cents, issued_date | orders |
| payments | payment_id | invoice_id, amount_cents, paid_date | invoices |

## Validation
All fields required; text trimmed. Numeric fields are signed 64-bit integers; monetary amounts nonnegative, order quantities positive, stock movement signed. Dates use ISO calendar dates and timestamps require timezone offsets. Orders: pending/fulfilled; purchase orders: pending/received/cancelled; dispatches: pending/dispatched/delivered. Duplicate primary keys and unknown references are rejected. Header mismatches abort ingestion. SQLite foreign keys are enabled. Warehouse ID is text, not a canonical foreign key in this schema. Order dates and catalogue metadata are joined separately by the enterprise exporter.

## Financial definitions
Order value = sum of order amounts; invoiced = sum of invoice amounts; paid = sum of payment amounts associated with invoices; outstanding = invoiced minus paid. Amounts stored as integer euro cents. Order value is not recognised revenue or profit.
