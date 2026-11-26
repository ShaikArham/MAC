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

## Premium visual refinement
Approved reference reopened. Added snapshot-driven order value bars, order status donut, pipeline stages, entity acceptance bars, business exceptions, insights and tenant identity. Frontend 14c55da/e044ecf/263432f/515a775; Pages d44d144/4d9c602/fd44590/1c961de. Existing exact copilot and snapshot blobs verified locally; Node regression 13/13 passed in 74.321ms. New dashboard browser and mobile tests not executed; public deployment unverified. No invented time series; existing workspace tables retained.

## MAC enterprise 50,000-order expansion — executed 2026-11-26
Accepted locally: exact `mac-enterprise-data` generator blob f06ac061eacc7324dc1c83044ec4e56138d8ed7a; `pipelines/export_enterprise.py` source blob e1c67f8d285aa99e84c639eb62b010b8e5e82864, test 0a11e45573487efc4ea9bd895e79e2b41c6d88ed. Full seed-42 2025 generation 50,000 accepted orders and 149,966 lines; 483,369 source rows, 483,367 accepted, 2 rejected. Order value €119,761,892.38; invoices €112,610,212.80, payments €101,476,023.30, outstanding €11,134,189.50, 131 warehouse variances across three warehouses. Twelve monthly totals matched annual order sum; order line and invoice totals validated; three-warehouse counts reconciled. Local validated SQLite processed output, not committed. 2025 order dates kept in keyed fixture for backward compatible core schema.
Pages `snapshot.json` v2 (8665 bytes), Git blob ee4ad99e4d093ce336f64d460980d451b938ae61, exactly matched local exporter. Frontend + gh-pages also identical: `enterprise.js` a10f7c44e954521825ff5d5d7f8b126f2567649e; `test_enterprise.js` 0aacbffe7f2ce7c43b4120f990ca1e4960f68452; updated app, copilot, CSS, HTML. Sampled table rows are explicitly distinguished from validated enterprise totals. Legacy Python 9/9, enterprise Python 1/1, Node 10/10, all actually executed; baseline Python ResourceWarnings remain. Public deployment and browser/mobile rendering **not** independently verified. Snapshot published on gh-pages; `mac-preview-baseline` remains rollback. See docs/ENTERPRISE_DATASET.md.

## Enterprise release deployment verification addendum
Published GitHub Pages workflow run successful for current gh-pages head `b11a01b983482549532b77a94c9a7f84a7a34eee` (2026-11-26T19:36:32Z). Exact-cent enterprise UI change on gh-pages `b54130a` and Node tests `b11a01b`; frontend corresponding `207f651`, `da2a23b`. Verified Git blobs: enterprise.js e5264ca878933475d22dabc08ed76884d3fa316a and test d8930fdec0421b040a0302caeef9b12a35a90b8d; Node 10/10 rerun locally. Browser/mobile rendering was attempted but Chromium headless execution timed out; do not claim a browser pass. Source snapshot preserved exact local exporter hash ee4ad99e4d093ce336f64d460980d451b938ae61. Pending: browser/mobile acceptance, full-order UI pagination beyond labeled sample, source ingestion memory and SQLite ResourceWarnings.

## Historical record explorer checkpoint
Committed monthly exporter on mac-enterprise-data 523993d (blob 02486e77ee5aa2ed5e6edd35bdcfb0e442264e29). Executed against existing validated SQLite: 12 shards, 50,000 unique orders, 11976189238 cents, 2,588,346 bytes including manifest. All shard SHA-256, month, counts and monetary totals checked. Local explorer source implements lazy month loading, all-month lookup, status filter, 25-row pagination and CSV. Node four assertions passed; local load/filter/CSV combined 193ms. Local archive prepared. Bulk shard upload and frontend integration not completed; gh-pages unchanged to preserve working site. Browser/mobile acceptance pending.

## Explorer release
GitHub isolated workflow regenerated twelve shards and matched exact local SHA-256 manifest (blob 5d9abbd8f7ea9f2430c5dba702d251345a9556e0); workflow success, generated commit cbcffb04. Integrated explorer with Sales orders, lazy month/all-year lookup, status, 25-row pagination, CSV and responsive controls. Fast-forwarded gh-pages from b11a01b to 22768c2; previous baseline retained. New browser runtime and mobile tests not executed; frontend branch sync pending. Workflow scoped to release branch only.

## Interactive application sprint
User requires every record, meaningful chart and navigation tab to be functional, with linked detail views and shared filters. Acceptance contract: docs/INTERACTIVE_ACCEPTANCE.md. Implementation and browser acceptance pending.

## Interactive sprint verification
66 relational partitions generated successfully (run 45886665836). Browser acceptance run 45886799369 succeeded at dcb0ed0; logs confirm chart, order detail, CSV, pagination, navigation and four viewport overflow checks. Added discovery/engineering drill-down and inventory movement browsing b5b50c2, routed all enterprise workspaces 7565fe0, expanded tests 1f9723c, regression trigger e9be424. Latest regression pending; gh-pages unchanged pending exact release verification. Remaining acceptance includes deeper finance/customer relationships, copilot evidence scope, individual mobile interactions and live publication.

## Final candidate
Expanded browser regression e9be424 passed (run 45887066879). Added customer order totals and invoice-specific payment detail 445fb55; selected-month sales copilot fed1401; expanded browser tests 97a05d2; final candidate f538927. Final candidate workflow triggered; promotion requires successful exact-head result. Annual stock and finance copilot figures remain annual, no live writes.

## Presentation readiness
Final interactive candidate f538927 passed browser run 45887255675. Added Command Centre business introduction, About MAC and About the builder with real workspace links and transparent independent synthetic scope (35055c9, d6758db, 179ac53). Consolidated browser test includes narrative navigation (95a0397); one new regression triggered at 6ce0a6c. Publish only after exact-head success. No repeated per-feature workflows.

## Presentation release promotion
Consolidated browser run 45887555751 completed successfully at 6ce0a6c898461e858cf7a3a7bde772718a1a281a. Logs confirm navigation, detail, CSV, pagination and four viewport checks; suite includes About MAC and builder navigation. Fast-forwarded gh-pages from 22768c2 to exact tested commit. Standard Pages run 45887643518 in progress at inspection. No extra custom workflow triggered. Visual screenshot review and exhaustive individual control acceptance remain unverified; checkout v4 Node 20 deprecation warning nonblocking.
