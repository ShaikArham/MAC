# MAC — About pages and historical order lookup

Release branch: `mac-about-order-filters`.

## About experience
Both About MAC and About the builder now present complete on-page explanations in responsive sections rather than sending visitors to other application tabs for each topic. External portfolio, LinkedIn and source links remain.

## Historical order search
The Sales orders workspace retains the verified 2025 order manifest and opens each order's order lines, dispatch, invoices and payments. Filters cover order ID substring, customer ID or synthetic customer name, inclusive From/To dates, and fulfilled/pending status. Filters combine with AND, can be cleared and update a paginated, sortable, CSV-downloadable result set. The shared monthly period is still available for order drill-down from the dashboard, while the search filters can narrow the loaded period further. Select **All 2025** to search the full year.

## Transparency
This demonstration is fully synthetic and read-only. Customer name lookup comes from validated local detail shards. No live accounting, CRM or warehouse systems are connected.

## Release gate
Source changes are isolated until focused browser validation. Do not claim a green browser suite until the CI result is confirmed. 
