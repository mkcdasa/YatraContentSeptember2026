# Prasadam, Sweets & Savories Vertical

Business plan, presentation, mind map and project-management pack for turning
temple prasadam into a revenue vertical at Hare Krishna Golden Temple (ISKCON),
Hyderabad. It is built from the *Prasadam Revenue Generation Plan* meeting on
26 September 2026 (recording, transcript, summary) plus desk research.

| File | What it is |
| --- | --- |
| **[Living business plan](https://claude.ai/code/artifact/b1afdda0-456c-4e85-9ff6-d3f67c49028a)** | **The editable, shared version of everything below.** Status and action tracker, decisions with approval dropdowns, risk register with status, roadmap timeline, financial sensitivity chart, all flowcharts, change log |
| [`07_Complete_Compendium.pdf`](07_Complete_Compendium.pdf) | **Every document in one bookmarked PDF (about 205 pages):** leadership plan, detailed plan, deck, mind map and flowcharts, PM plan, tracker, and the meeting record with the full transcript |
| [`pdf/`](pdf) | One PDF per deliverable: `01_Business_Plan`, `02_Presentation`, `03_Mind_Map`, `04_Project_Management_Plan`, `05_Project_Tracker`, `06_Meeting_Record` |
| [`meeting/`](meeting) | The meeting summary and full transcript as received (the 11 MB audio file is not stored in git) |
| [`00_Leadership_Business_Plan.pdf`](00_Leadership_Business_Plan.pdf) | **For temple leadership and top management (48 pages).** Executive summary, decisions requested with phase-gated funding, market and SWOT, audiences, revenue streams, pricing, go-to-market, operations, governance, roadmap, financials with sensitivity analysis, risk heat map, KPIs, sign-off page, and appendices with everything said in the meeting and all flowcharts |
| [`01_Business_Plan.docx`](01_Business_Plan.docx) | Full business plan (about 29 pages): everything from the meeting, market research, SWOT, 14 audiences, 14 revenue streams, 16 new ideas, products, pricing, marketing, operations, roadmap, festival calendar, financials, risks, KPIs, diagrams, sources |
| [`02_Presentation.pptx`](02_Presentation.pptx) | 26-slide deck for the decision meeting |
| [`03_Mind_Map.html`](03_Mind_Map.html) | Interactive mind map covering every detail, with search and expand/collapse, plus all flowcharts. Open it in any browser; it works offline |
| [`04_Project_Management_Plan.docx`](04_Project_Management_Plan.docx) | Charter, objectives, scope, stakeholders, RACI, WBS & schedule, milestones, budget, risk register, quality, communications, governance, change control, decision log |
| [`05_Project_Tracker.xlsx`](05_Project_Tracker.xlsx) | Working tracker: WBS with a formula-driven Gantt, milestones, action items, RACI, risk register (auto score), financial model and unit economics (editable inputs), KPI tracker, ROI and hours log, reference sheets |
| [`06_Mind_Map_and_Flowcharts.md`](06_Mind_Map_and_Flowcharts.md) | Mind map, flowcharts and roadmap timeline in Mermaid (GitHub renders them) |
| [`diagrams/`](diagrams) | The same diagrams as PNG and SVG files |

## Headline

- **Two price tiers.** The mass tier brings volume and covers fixed costs; the premium tier adds margin.
- **Five audience circles:** people who come to us, our B2B network, the open public, digital buyers, and scale (QSR and export).
- **Start lean.** Phase 0 is two weeks (data, samples, pricing, sales kit, one hire). Dasara and Diwali 2026 are the pilot. A dedicated unit and QSRs come only after demand is proven.
- **Year-1 target** is about ₹2.2 crore in revenue [estimate]. Every rupee and every hour is tracked by DMTT for ROI.

Figures marked **[ESTIMATE]** are planning assumptions. Replace them with the
6–12 month order analysis (action item A4) before committing budget.

## Rebuilding

All files are generated from one content file, `src/content.py`. Edit it, then run:

```bash
pip install python-docx python-pptx openpyxl
python3 src/build_all.py
```

To rebuild the leadership PDF (needs Node with Playwright and the Noto fonts):

```bash
PLAYWRIGHT_MODULE=<path to playwright/index.mjs> CHROME=<path to chromium> python3 src/build_pdf.py
```

To rebuild the per-document PDFs and the compendium (needs LibreOffice too):

```bash
PLAYWRIGHT_MODULE=<path to playwright/index.mjs> CHROME=<path to chromium> python3 src/build_pdfs.py
```

To re-render the diagram images after you change a flowchart, install
`mermaid` and `playwright` with npm, then run
`node src/render_diagrams.mjs node_modules/mermaid/dist/mermaid.min.js`.
