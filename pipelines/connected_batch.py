"""Bridge registered MAC-05 sources to append-only MAC-06 batches."""
from pipelines.ingest import SPEC
from pipelines.incremental import run_batch
from integrations.snapshot import canonical_rows

def run_connected(path, batch_id, registry, bindings):
    if set(bindings)-set(SPEC):
        raise ValueError('unknown entity')
    records = {}
    for entity, (source_id, mapping) in bindings.items():
        pk, fields, _ = SPEC[entity]
        rows = canonical_rows(registry.read(source_id), mapping, [pk, *fields])
        records[entity] = [{k: str(v) if type(v) is int else v for k,v in row.items()} for row in rows]
    return run_batch(path, batch_id, records)
