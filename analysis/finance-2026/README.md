# Finance deep-dive 2026 — working scripts

Supporting scripts for the *HKM Hyderabad Financial Deep-Dive and Optimisation Plan 2026*
(Claude Doc, October 2026). No source data is committed: the Drive workbooks contain
salary and donor information and stay in Google Drive.

## Pipeline (refresh monthly)

1. Download the workbooks from Google Drive (management decks, CTC lists, campaign ROI
   sheets, expenditure ledgers). With the Drive connector the download results are JSON
   files holding base64 content; decode them:
   `python3 -I scripts/decode.py <tool-results-dir> raw/`
2. Export every non-empty sheet to CSV:
   `cd <workdir> && python3 -I scripts/export_csv.py` (reads `raw/*.xlsx`, writes `parsed/*.csv`)
3. Print the key expenditure, salary and campaign tables and the 2025 salary
   apportionment aggregates:
   `python3 -I scripts/keytables.py > out/key_tables.txt`

Requirements: Python 3.11+, `openpyxl`, `pandas`.

## Charts

`charts/widget-w*.tsx` are the hand-drawn SVG chart and flowchart modules used in the
report (campaign returns, campaign-to-ledger flow, root-cause tree, fund flow between
trusts, roadmap, timeline, approval flow, campaign gate, hiring gate). They follow the
Claude Docs widget contract (one module, theme tokens, text ids on typed labels).
`charts/validate.js` parses a module with esbuild to catch JSX syntax errors before upload:
`node charts/validate.js charts/widget-w19.tsx`

## Headline findings (FY2022-23 to FY2025-26 YTD)

- Net fundraising surplus fell from about ₹1.9 crore a year to a ₹0.4 crore run-rate while
  income grew 35% and non-yatra cost grew 115%.
- DMT margin 45% → 51% → 42% → 30%; paid ads never met the 60–65% target and are now
  loss-making (−29.5%).
- Messaging spend (SMS, RCS, WhatsApp) ₹74.6 lakh → ₹1.43 crore a year; return per rupee
  falls with send size (₹2.1 on the largest 2025 send vs ₹6–12 on small sends).
- Payroll ₹4.3 lakh a month (2022) → ₹19.6 lakh a month (Sep 2026); 45 further hires
  proposed (+₹2.06 crore a year).
- Yatra: 16% gross margin wiped out by ₹1.1 crore of common cost in 10 months plus
  ₹5 lakh a month transfers; net loss ₹14.5 lakh.
- Plan: ₹1.5–2.15 crore recurring savings, ₹0.9–1.2 crore one-off recoveries, hiring
  gate avoiding ₹2.06 crore, and revenue growth from telecalling, retention, devaseva
  and service fees; net surplus restored to about ₹2.3 crore in FY2026-27.
