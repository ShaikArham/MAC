# Proposed architecture

Existing tools (synthetic files and mock APIs) -> Python ingestion -> raw records -> validated relational models -> SQL business views -> FastAPI -> Next.js interface.

Proposed PostgreSQL database. Track source IDs, import batches, validation results, reconciliation and execution logs. AI optional and read-only initially. No live integrations. Technology choices remain provisional until implementation review.
