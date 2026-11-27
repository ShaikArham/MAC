# MAC interview freeze — 27 November 2026

Interview: 30 November 2026, 13:30 Irish time. Demonstration target: 10 minutes.

Use the stable `gh-pages` branch at https://shaikarham.github.io/MAC/. Business overview startup confirmed in source; prior user live checks covered startup, Command Centre, connected order O001586 and annual finance Copilot. This is not a fresh full browser regression. Offline backup excluded at user's request.

The experimental `mac-copilot-date-queries` branch is excluded from release. Reference January calculations verified (1 January 100 orders, 3 pending; 2 January 94 orders, 7 pending; 1–7 January 706 orders, 50 pending). Runtime acceptance and browser regression remain unverified; combined commit status returned no statuses. Do not merge or deploy without passing acceptance.

Demo sequence: introduction (1 min), business overview (1), connected systems (1.5), Command Centre (1.5), order O001586 (1.5), ETL and validation (1.5), stable Copilot (1.5), close (0.5).

Use synthetic 2025 data only. 483369 source records, 483367 accepted, 2 rejected, 50000 orders. Order value EUR 54751013.48; invoiced EUR 51506026.28; collected EUR 46400074.98; outstanding EUR 5105951.30. Copilot is deterministic, read-only, not an LLM. Integrations simulated; browser reads exported JSON, not live ERP or SQLite. Explain AI-assisted development transparently.

Reviewer guides: TECHNICAL_REVIEW.md, ARCHITECTURE_REVIEW.md, APPLICATION_REVIEW.md, DATA_DICTIONARY_REVIEW.md, VALIDATION_REVIEW.md, DEMO_RUNBOOK.md. Freeze is a documented release decision, not a branch protection setting. No application changes or deployment in this audit.
