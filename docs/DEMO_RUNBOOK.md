# Demonstration runbook

## Live review
Open https://shaikarham.github.io/MAC/ in a fresh browser window. Expected initial workspace: Business overview. Source index.html and app.js on gh-pages select this workspace; live browser behaviour requires separate verification.

## Offline fallback (Windows or macOS)
Download the complete [gh-pages ZIP](https://github.com/ShaikArham/MAC/archive/refs/heads/gh-pages.zip). Extract it, retaining all files and nested data directories. In a terminal opened at the extracted root containing index.html, run `python -m http.server 8000 --bind 127.0.0.1` (Windows alternative: `py -m http.server 8000 --bind 127.0.0.1`). Open http://127.0.0.1:8000/ . Do not double-click index.html: JSON fetches require HTTP. Keep the terminal running. Verify in airplane mode before relying on this fallback.

## Ten-minute review
Business overview (1 min), process/system mapping (1.5), Command Centre (2), connected order records (2), ingestion/reconciliation (1.5), Copilot (1.5), limitations (0.5). Use a known customer ID C0001 or annual outstanding invoices. Demonstrate a supporting record rather than claiming generative AI.

## Acceptance checklist
- Fresh load starts at Business overview; no missing data or scripts.
- Command Centre totals match technical review.
- Order detail links and Copilot answer work.
- Offline clone performs the same steps with internet disabled.
- Screen sharing, zoom and microphone checked on interview device.

These are manual acceptance steps, not claims of completed tests. The archive is branch-based and should be saved locally before the meeting. No live integrations or real customer data.
