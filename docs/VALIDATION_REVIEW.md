# Validation and operational limitations

The canonical ingestion reads CSV files in dependency order, validates field types and references, records raw and rejected rows, rebuilds SQLite tables in a transaction, and writes JSON reports. SQL identifiers come from a fixed schema and values use placeholders. JSON report writes occur after the database transaction and are not an atomic multi-file publication. The ingestion retains records in memory; larger production volumes require streaming or staged bulk loads.

The enterprise exporter checks twelve months, order-date coverage, order-line sums, invoice amounts and aggregate payments. The separate incremental prototype provides batch replay and transactional raw/validated/quarantine/summary tables. These are distinct paths.

Historical acceptance: [polish browser suite](https://github.com/ShaikArham/MAC/actions/runs/45900420983), [Pages deployment](https://github.com/ShaikArham/MAC/actions/runs/45900814768). See MASTER_TRACKER.md for exact release commits and earlier failures. Later Business overview startup edits are not covered by that evidence. No new test execution is claimed by this documentation change.

Production priorities: authenticated API, role-based access, tenant boundaries, credential management, streaming ingestion, schema evolution, durable scheduling, retry and alerting, atomic publication, backup/recovery, privacy and security review. No production SLA is claimed.
