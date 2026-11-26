# Preview contract v1
Generate with python -m pipelines.export_preview snapshot.json from mac-data-engineering.
Top-level schema_version=1, synthetic=true, mode=generated_snapshot, summary, records, reconciliation.
Summary contains batch_id, accepted, rejected, entity_counts and order_value_cents. Records are validated Silver rows grouped by the ten canonical entities. Reconciliation contains invoice balances, outstanding_cents, overpaid_cents, stock and exceptions. Stock count 88 is a synthetic observation, opening zero; not a live count. Currency is integer EUR cents. Order value is not recognized revenue. Static preview has no live refresh. Missing or invalid snapshot must display unavailable, not fabricated metrics. MAC-05 connector adapter is not used by this fixture exporter.
