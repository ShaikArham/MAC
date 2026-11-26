# Technical reviewer guide

MAC is an independent, fictional Irish trade-supplies demonstration, not a Consulting.ie product or client implementation.

## Review sequence
1. [Live business demonstration](https://shaikarham.github.io/MAC/): Business overview, process mapping, system mapping, Command Centre, then engineering and About.
2. [Published application source](https://github.com/ShaikArham/MAC/tree/gh-pages): index.html, app.js, enterprise.js, explorer.js, interactive.js, dashboard.js, analyst.js and copilot.js.
3. [Data engineering development](https://github.com/ShaikArham/MAC/tree/mac-enterprise-data): generator and export pipeline history.
4. [Connector development](https://github.com/ShaikArham/MAC/tree/mac-backend) and [ETL development](https://github.com/ShaikArham/MAC/tree/mac-data-engineering).
5. [Engineering history and acceptance evidence](MASTER_TRACKER.md).

## Architecture
Synthetic source records → Python ingestion and validation → SQLite reconciliation → generated JSON snapshot and partitioned records → static JavaScript application. Browser interactions are read-only; the assistant uses deterministic local analytical logic, not an external LLM. Simulated connectors are not live integrations.

## Published snapshot
2025 historical synthetic data: 500 customers, 2,000 products, 100 suppliers, 50,000 orders, 149,966 order lines, 140,954 stock movements. 483,369 source rows, 483,367 accepted and 2 rejected. Order value €54,751,013.48; invoiced €51,506,026.28; paid €46,400,074.98; outstanding €5,105,951.30. These values were read from the published snapshot, not inferred from earlier development runs.

## Validation and release boundaries
[Polish acceptance](https://github.com/ShaikArham/MAC/actions/runs/45900420983) and [Pages release](https://github.com/ShaikArham/MAC/actions/runs/45900814768) are recorded as successful for the earlier frozen release. Subsequent startup changes 896fe56 and f289cf3 select Business overview; their deployment and browser acceptance are not established by those historical runs. Mobile tests used Chromium emulation. Historical failed runs remain visible.

## Local review
Clone the repository and check out gh-pages. From its root, run `python -m http.server 8000` and open http://localhost:8000/ . HTTP serving is needed for JSON fetches. This is a static application review, not a full pipeline regeneration procedure.

## Production gaps
No live client data, authentication, multi-tenant isolation, scheduled ingestion, durable production monitoring or live external AI. Production adoption would require requirements discovery, access controls, secure connector credentials, operational monitoring and deployment governance. Do not treat synthetic metrics as real commercial outcomes.
