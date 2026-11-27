# MAC — Modular Architecture & Connectivity

**Connecting data. Transforming businesses.**

[Open the interactive application](https://shaikarham.github.io/MAC/)

MAC is an independent data engineering and custom business software initiative for a fictional Irish building materials and trade supplies distributor, Horizon Supplies.

## Start here for technical review

- [Technical reviewer guide](docs/TECHNICAL_REVIEW.md) — architecture, source locations, local startup, dataset totals, validation and limitations.
- [Published application code](https://github.com/ShaikArham/MAC/tree/gh-pages)
- [Architecture and data engineering](docs/ARCHITECTURE_REVIEW.md)
- [Application and Copilot review](docs/APPLICATION_REVIEW.md)
- [Canonical data dictionary](docs/DATA_DICTIONARY_REVIEW.md)
- [Validation and operational limitations](docs/VALIDATION_REVIEW.md)
- [Demonstration and offline recovery runbook](docs/DEMO_RUNBOOK.md)
- [Engineering tracker](docs/MASTER_TRACKER.md)

## Explore
- Command Centre: historical orders, fulfilment and financial controls.
- Operations: sales, inventory, customers, products, suppliers and invoices.
- Engineering: ingestion, validation, reconciliation and audit evidence.
- About MAC and About the builder: motivation, architecture and professional background.

## Data and architecture
50,000 synthetic orders, 500 trade accounts, 2,000 catalogue products, 100 suppliers and three warehouses. Python ingestion, SQLite validation and integrity-checked JSON partitions support a read-only browser application. Industry names are deterministic fictional source records; no real customer or supplier relationships are claimed. No live integrations or external AI service.

[Project tracker](docs/MASTER_TRACKER.md)

## Verified industry release
Release `fa98587` passed consolidated workflow [45888840034](https://github.com/ShaikArham/MAC/actions/runs/45888840034) and was promoted to gh-pages. Actual regenerated totals: 50,000 orders, EUR 54,751,013.48 order value, EUR 51,506,026.28 invoiced, EUR 46,400,074.98 paid, EUR 5,105,951.30 outstanding; 483,367 accepted and 2 rejected. Fictional customer and supplier names are generated source records, not display aliases. Catalogue categories, units and illustrative prices are joined from generated metadata; named warehouses appear in detail shards, aggregate warehouse IDs remain W001–W003. Browser regression passed locally in CI; live user navigation remains to be confirmed.

## About and historical order search — 26 November 2026
The About MAC and About the builder pages now contain complete, self-contained explanations. The Sales orders workspace searches the complete validated 2025 order history by order ID, customer name or ID, month, inclusive date range, status and minimum/maximum order value. Filters combine, and matching orders remain sortable, paginated, downloadable as CSV and clickable through to related lines, dispatches, invoices and payments. Browser acceptance run [45891495494](https://github.com/ShaikArham/MAC/actions/runs/45891495494) passed and the release was promoted as `54859dfd`. See [implementation notes](https://github.com/ShaikArham/MAC/blob/gh-pages/docs/ABOUT_AND_ORDER_SEARCH.md). The demonstration remains fictional and read-only.
