# MAC — About pages and historical order lookup

Release branch: `mac-about-order-filters`.

## About experience
Both About MAC and About the builder now present complete on-page explanations in responsive sections rather than sending visitors to other application tabs for each topic. External portfolio, LinkedIn and source links remain.

## Historical order search
The Sales orders workspace retains the verified 2025 order manifest and opens each order's order lines, dispatch, invoices and payments. Filters cover order ID substring, customer ID or synthetic customer name, inclusive From/To dates, month selection (including all of 2025), fulfilled/pending status and minimum/maximum trade order value in euro. Filters combine with AND, can be cleared and update a paginated, sortable, CSV-downloadable result set. The full-year dataset is searched with a dedicated month filter, initially matching the shared reporting period selected on the dashboard. Clear filters resets to the full 2025 year. Changing the order month synchronizes the shared period control.

## Transparency
This demonstration is fully synthetic and read-only. Customer name lookup comes from validated local detail shards. No live accounting, CRM or warehouse systems are connected.

## Release gate
Source changes are isolated until focused browser validation. Do not claim a green browser suite until the CI result is confirmed. 
