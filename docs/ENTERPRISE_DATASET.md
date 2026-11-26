# MAC — Enterprise Synthetic Dataset Acceptance

Independent, unaffiliated technical demonstration. No real business/customer data, connectors or LLM calls.

## Reproducible 2025 dataset
- Branch: `mac-enterprise-data` (source `pipelines/generate_enterprise.py`, seed 42).
- Generate: `PYTHONPATH=. python pipelines/generate_enterprise.py . --orders 50000`.
- Export: `PYTHONPATH=. python pipelines/export_enterprise.py enterprise-snapshot.json`.
- Date coverage: January–December 2025, via `data/synthetic/order_dates.json`. Core order schema intentionally unchanged. Three synthetic warehouses W001–W003.
- Generated files are **not** versioned into the repository. The exporter uses validated SQLite ingestion and publishes only a limited, labeled JSON sample and aggregates.
- All source values are synthetic. Order value is **not recognized revenue**.
- Validated entity totals: customers 500, products 2000, suppliers 100, orders 50000, order lines 149966, purchase orders 1200, stock movements 140954, dispatches 47008, invoices 47008, payments 44631.
- Source records 483369, accepted 483367, quarantined 2 (duplicate order; unknown customer), €119761892.38 sales order value.
- Invoiced €112610212.80, paid €101476023.30, outstanding €11134189.50. Fulfilled 47008; pending 2992. Stock exceptions 131 across three warehouses.
- Monthly sum, order-to-order-line amounts, invoice-to-order amounts, foreign keys, payments and stock movement counts validated.

## Published preview
- Branches: `mac-frontend`, `gh-pages`, snapshot schema v2 `enterprise_aggregate`, 8665 UTF-8 bytes.
- Exact local source/remote Git blob: `ee4ad99e4d093ce336f64d460980d451b938ae61`.
- Summary totals use **all validated rows**; tables explicitly label only displayed **sample** rows (14 orders, 10 invoices, 10 customers, 10 products, 10 suppliers, 10 purchase orders, 8 stock discrepancies).
- There is **no** full-browser transaction search across the 50,000 orders, scheduled ingestion, production ETL, active connection, persistent monitoring, or live backend.
- Dashboard uses 12 genuine synthetic monthly order totals; no fake time series.
- Original working `gh-pages` baseline saved as branch `mac-preview-baseline`.

## Measured local execution
- Full generation, SQLite ingestion, reconciliation, reporting export: completed (full 50k orders).
- Python legacy suite: 9/9 passed; enterprise pilot regression: 1/1 passed. Node enterprise interface/snapshot/copilot suite: 10/10 passed.
- Original Python suite still emits unclosed SQLite ResourceWarnings; remediation pending.
- New published JS/Python Git blobs verified against locally executed exact files (including `enterprise.js`, exporter, test, snapshot).
- GitHub Pages workflow was observed successful for gh-pages head b11a01b; direct external browser/mobile rendering still not independently verified. Node suite re-run 10/10 after precise EUR-cent formatting, test blob d8930fdec0421b040a0302caeef9b12a35a90b8d.

## Constraints / next acceptance
Retain sampled-display labeling, add date validation to production schema when migrating the model, improve ingestion memory (observed peak about 750MB; raw JSON about 103MB), clear SQLite warnings, and verify GitHub Pages build & browser/mobile interactions. Generated fixtures and processed SQLite/raw files remain local; they must not be mistaken for committed transactional datasets.
