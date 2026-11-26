# Business discovery — fictional demonstration client
All findings below are scenario assumptions, not actual client interviews.

## Operating model
Wholesale distributor selling physical goods to business customers. Existing tools remain in place.

| Department | Current workflow | Proposed source | Pain point | Opportunity |
|---|---|---|---|---|
| Sales | Capture and confirm orders | CSV/CRM mock | Repeated entry | Unified order record |
| Procurement | Raise supplier orders | CSV | Unclear inbound stock | Purchase visibility |
| Inventory | Track available stock | Warehouse JSON | Stock discrepancies | Reconcile movements |
| Warehouse | Pick and dispatch | JSON | Delayed updates | Fulfilment status |
| Distribution | Track delivery | Mock API | Fragmented status | Delivery exceptions |
| Finance | Invoice and reconcile | Accounting mock | Manual matching | Invoice/payment reconciliation |

## Priority use cases
1. Order-to-cash visibility: link order, dispatch, invoice and payment by stable IDs.
2. Inventory reliability: reconcile opening stock and movements against closing balances.
3. Data reliability: quarantine invalid records, show source lineage and batch outcomes.
4. Management reporting: calculate order value, fulfilment and outstanding invoices from validated records.

## Discovery acceptance
Document source ownership, identifiers, expected frequency, data quality rules and business metrics before implementing each connector. No real customer information or live integration.
