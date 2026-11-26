# MAC master tracker

## MAC-01 Foundation
- [x] Private repository verified; write access confirmed.
- [x] Project charter committed.
- [ ] Design reference binary committed.
- [x] Development branches created.
- [ ] Application shell implemented and validated.

## Ownership
Master: docs and integration. Frontend: frontend/. Data engineering: data/, pipelines/, database/. Backend: backend/, integrations/. Intelligence: intelligence/.

## Next
Build responsive dark command centre on isolated frontend branch. Coordinate data contracts before integration.

## Rules
Update tracker after meaningful changes; record commits, blockers and validation evidence. No public deployment or live external integrations without approval.

## 2026-11-26 — Preview checkpoint
Created mac-frontend, mac-data-engineering, mac-backend, mac-intelligence and gh-pages branches. Static HTML/CSS/JS shell committed to mac-frontend (564bdf4) and gh-pages (be30c7e). Navigation, mobile menu and scripted copilot controls implemented; metrics illustrative and remaining views placeholders. Frontend preview files currently at branch root. GitHub Pages publishing settings must be enabled manually; private repository plan eligibility unverified. No runtime/browser verification or backend integration yet. No custom Actions workflow created.

## Data engineering checkpoint
Branch mac-data-engineering: synthetic customers/orders CSV, Python validation and SQLite snapshot ingestion, JSON summary and rejection output committed through 04934ca. Source only; execution and tests pending. SQLite is provisional local prototype. Existing .gitignore prevented creation; review before generated outputs are committed. Repository remains private at latest metadata check; Pages activation unverified.

## MAC-03 Business discovery
Scenario discovery and initial data contracts documented in BUSINESS_DISCOVERY.md (9b28a5a) and DATA_CONTRACTS.md (fac0ba7). Documentation baseline complete; assumptions are fictional, not client-verified. Next: implement order-to-cash entities and reconciliation with runtime verification. Pages activation remains unverified.

## MAC-04
Ten synthetic entity CSVs, dependency-ordered SQLite ingestion, foreign keys, typed validation, raw/rejection/summary outputs, ignore rules and regression test committed on mac-data-engineering. Ingestion ecd59e2; test 53c53bd. Expected five rejects and EUR 2100 order value. Runtime not verified; source milestone complete, acceptance open. JSON exports not atomic with database; incremental lineage, reconciliation and PostgreSQL pending. Next verify runtime before MAC-05.
