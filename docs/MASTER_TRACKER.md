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

## MAC-07 local reconciliation checkpoint
Read-only Silver reconciliation engine 73a9b2d and fixture regression cc6df8e on mac-data-engineering. Both committed Git blob hashes match local tested files. Combined isolated suite 10/10 passed in 1.683s. Fixture: EUR 650 outstanding, stock expected 90 observed 88 delta -2, duplicate stock count rejected, additional EUR 1 overpayment detected. Order-line and invoice-order discrepancy rules implemented but positive mismatch cases not independently tested. Stock counts supplied by caller; all movements assumed within count period, no dated cutoff or persisted count source. Exceptions returned in memory, not persisted or exposed via API. Existing SQLite resource warnings remain. No merge or deployment. Local scoped reconciliation implemented and tested; further edge-case coverage and integration pending.

## MAC-08 workspace preview
Six read-only searchable fixture workspaces (sales, inventory, finance, customers, suppliers, exceptions) added to existing dark shell. Frontend f79e4f6 / 2b6e384; gh-pages 8f0ead6 / ac613f6. Both branches returned identical JS/CSS blob hashes. Data manually transcribed from synthetic fixtures and illustrative stock count; no live API, editing or exception persistence. Browser and runtime tests not executed; Pages availability unverified. Next verify browser behavior and connect command centre to actual outputs in MAC-09.

## MAC-09 exporter checkpoint
Versioned synthetic snapshot exporter committed 4f1ed77 on mac-data-engineering; docs/PREVIEW_CONTRACT.md added on main. Uses MAC-04 canonical fixture schema, MAC-06 ETL and MAC-07 reconciliation. MAC-05 connector integration, actual exporter execution, generated JSON publication, frontend replacement and runtime verification remain open. Preview branches unchanged. No deployment.

## MAC-09 static integration verification
Exporter baseline blob 0285f4c and registered CSV exporter blob 32ea66d matched local source; both executed and produced byte-identical JSON. Updated exporter bc577d6 uses ten MAC-05 registered CSV sources via connected_batch. Combined Python suite 10/10 passed in 1.666s; four additional snapshot assertions and six Node model assertions passed. Generated snapshot blob b79b355d7da5ed756f0df4243d2e6bef1de6adc9 matched both remote preview branches. Frontend commits bf20ae5 / 75604c2; gh-pages 3b47d4e / 9df71db. Seven views now derive metrics and records from snapshot; missing snapshot displays unavailable. Browser DOM and Pages availability not verified; Node test exercised model only. Existing SQLite resource warnings remain. Static fixture export uses CSV, not live HTTP, and combined checkout required. No merge or live deployment verified.

## MAC-10 monitoring checkpoint
Monitor 70c962e, regression 810f75d, exporter 93bc5b3: local Git blob hashes match committed source. Actual isolated Python suite 11/11 passed in 1.732s; six Node monitoring model assertions passed. Generated snapshot hash a29de414b4789eccfb36d8f5288144d80e2c7ee9 matches both preview branches. Frontend e75350c/a6bf787; gh-pages c4000e0/35f497b. Ten healthy CSV reads, 22 Bronze, 17 Silver, five quarantine, one successful batch and one derived audit event. Five monitoring views connected. Snapshot-only; temporary database resets history each export, no scheduler, immutable audit trail, failed extraction history or retry attempt history. Browser and Pages availability unverified; SQLite resource warnings remain. No production merge.

## MAC-11 / MAC-12 scoped runtime validation
MAC-11 rule-based read-only copilot source committed previously. MAC-12 isolated Python 3.13.5 suite 11/11 passed in 1.721s; fresh exporter summary, records and reconciliation equal published snapshot (3 checks). Original copilot blob e71f0bc reproduced malformed reconciliation crash; fixed top-level arrays and integer checks. Node 22.16.0 suite 13/13 passed in 81.077ms. Both branches verified fixed blob 4be0ceaaad82bf63bff1f4aaec184affffd779c7 and test blob f86d2fa787d3d776511bfe8b7b2c52ec1964c3c9; frontend 5ff3da7/d1e2bf9, Pages d53d798/71ab505. Five existing frontend files matched across branches before changes. Scoped copilot acceptance passed. MAC-12 remains open for browser/mobile testing, nested schema validation, SQLite resource warnings, persistent monitoring and public Pages verification. No live AI or production deployment.
