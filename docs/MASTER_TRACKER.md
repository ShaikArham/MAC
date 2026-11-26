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

## MAC-04 runtime acceptance — PASS
Baseline f253e1f; 12 local files matched retrieved Git blob hashes. Local pipeline executed successfully: 10 entities, 22 rows, 17 accepted, 5 rejected, EUR 2100 order value. Regression suite 1/1 passed including repeatability and foreign key check. No evidenced defect in scoped checks; no code fixes required. Verification report on mac-data-engineering at docs/MAC04_VERIFICATION.md. MAC-04 local snapshot scope accepted. Remaining production gaps: PostgreSQL, incremental lineage, atomic JSON publication, reconciliation, frontend integration. Next MAC-05 connected systems. No deployment or Actions run.

## MAC-05 connector prototype
mac-backend commits 8ca9b76 (connectors), 9c4b66c (tests), 139de72 (dependency), f2f48fd (docs). Local isolated unittest run: 2 tests passed, covering five connector types, duplicate registration, missing file, path escape and invalid simulation envelope. Registry and health are in-memory, read-triggered. Accounting/CRM are local response fixtures, not HTTP endpoints. Canonical mapping, durable registry, scheduled monitoring and integration with MAC-04 remain open. No deployment or external calls. Committed source not independently hash-verified. Next complete connector integration before MAC-06 acceptance.

## MAC-05 integration checkpoint
Backend source commits f269ce0 (persistent registry, canonical mapping and MAC-04 snapshot adapter), e491d6d (loopback fixture HTTP server/client), tests/test_snapshot.py added. Source only this checkpoint; tests not executed. Adapter requires combined checkout with MAC-04 pipeline; HTTP client not yet wired into registry. Single-process registry; snapshot copy is not atomic; scheduled monitoring remains open. Next run combined isolated tests and wire HTTP sources before acceptance.

## MAC-05 scoped runtime acceptance — PASS
HTTP registry wiring 6783562; combined regression 284ceb8. Isolated combined checkout: 7/7 tests passed in 1.127s; six backend Python blob hashes matched remote. End-to-end 10 sources (2 loopback HTTP, 8 CSV), 22 rows, 17 accepted, 5 rejected, EUR 2100 order value. Persistent health verified. No failing tests observed. Verification report docs/MAC05_VERIFICATION.md on mac-backend. Local on-demand integration accepted; scheduled monitoring, atomic publication, multi-process registry, durable endpoint configuration and branch integration remain open. Next MAC-06 advanced ETL. No deployment or merge.

## MAC-06 source checkpoint
Incremental append-only SQLite ETL in pipelines/incremental.py (c5a200b), regression source tests/test_incremental.py. Bronze raw, Silver validated records, quarantine, Gold summary and batch status published in one SQLite transaction; lineage via batch/entity/ordinal; same batch digest replay returns prior result; failed transaction rolls back data and records failure. Source only: runtime not executed or independently verified. Existing keys rejected; updates/deletes, attempt history, crash recovery tests, connector wiring and PostgreSQL pending. Next verify actual runtime before acceptance.

## MAC-06 measured local acceptance
Reconstructed incremental.py and test_incremental.py; verified their Git blob hashes plus ingest.py and snapshot.py against retrieved source. Combined local suite 8/8 passed in 1.151s. Added connected_batch.py (1cc12db) and test_connected_batch.py (318a2ec); both committed blob hashes match tested local files. Extended suite 9/9 passed in 1.667s. CRM loopback and CSV orders: 2 accepted, 0 rejected, 12500 cents; replay unchanged; malformed batch failed twice; corrected new batch raised cumulative total to 13000 cents, 3 Bronze rows. Existing regression verifies rollback, quarantine and lineage. Local append-only acceptance passed; resource warnings for unclosed SQLite connections observed, not fixed; attempt history, original source IDs/raw pre-mapping lineage, extraction failure audit, crash recovery and updates/deletes remain open. No merge/deployment. Next MAC-07 or hardening.
