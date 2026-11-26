# Architecture and data engineering

## Business context
Horizon Supplies is fictional. Its order-to-cash process connects customers, products, suppliers, purchasing, stock, dispatch, invoices and payments. MAC demonstrates how disconnected records can become a reconciled analytical view.

## Components
| Layer | Responsibility | Source |
|---|---|---|
| Ingestion | Typed conversion and canonical validation | [ingest.py](https://github.com/ShaikArham/MAC/blob/mac-data-engineering/pipelines/ingest.py) |
| Incremental prototype | Transactional Bronze/Silver/Gold and quarantine | [incremental.py](https://github.com/ShaikArham/MAC/blob/mac-data-engineering/pipelines/incremental.py) |
| Enterprise export | SQLite aggregation, monthly and financial integrity checks | [export_enterprise.py](https://github.com/ShaikArham/MAC/blob/mac-enterprise-data/pipelines/export_enterprise.py) |
| Presentation | Static HTML and JavaScript | [published source](https://github.com/ShaikArham/MAC/tree/gh-pages) |

The incremental prototype is a separate development component; do not assume every prototype is invoked by the published enterprise exporter. The inspected exporter invokes pipelines.ingest.run, joins order dates, validates twelve months and checks order-line and invoice amounts. Payment totals are aggregated by invoice before joining to prevent duplicate invoice totals. Currency uses integer cents.

## Incremental design
Batch ID and SHA-256 payload digest identify replay. A successful identical batch returns its stored result; a conflicting payload is rejected. Bronze preserves raw records, Silver stores validated records, quarantine stores rejection reasons, and Gold holds summary. SQLite transactions define the publication boundary. Insert-only semantics reject existing keys; updates and deletes are not supported.

## Trade-offs
SQLite simplifies reproducible local demonstration; a production system would need concurrency, migration, access-control and recovery design. Static JSON avoids exposing a database or credentials but is not a real-time API. The published data is synthetic.
