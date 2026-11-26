# Application review

The published entry point is [index.html](https://github.com/ShaikArham/MAC/blob/gh-pages/index.html). Its script order is copilot.js, dashboard.js, enterprise.js, explorer.js, interactive.js, analyst.js and app.js. The application loads snapshot.json over HTTP. The initial heading and startup call now select Business overview. The source change is not a new browser acceptance result.

## Review journey
Business overview explains the fictional organisation; Process mapping follows buying, storing, selling, delivering, invoicing and payment; System mapping describes disconnected sources and the proposed unified view. Command Centre presents operational and financial metrics. Workspaces provide record search, filters, pagination and drill-downs. Engineering views expose validation and reconciliation evidence.

## Intelligence
The Copilot is deterministic and read-only, not an LLM. app.js calls macAnalyst with the current snapshot and question, displays the answer and evidence, and provides navigation links. A sequence token prevents older asynchronous replies from overwriting newer ones. No external AI service is claimed.

## Local inspection
Clone the repository, check out gh-pages and run python -m http.server 8000 from the branch root. Open localhost:8000. This serves existing generated data, not a live ingestion backend.

## Security boundaries
No production credentials or real customer records are required for the static demonstration. Production adoption would require authentication, authorisation, tenant isolation, secrets management, privacy assessment and operational controls. This document is not a security audit.
