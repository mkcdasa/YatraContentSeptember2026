"""Builds every PDF in the pack.

  pdf/01_Business_Plan.pdf ... pdf/06_Meeting_Record.pdf   one PDF per deliverable
  07_Complete_Compendium.pdf                               all of them in one file, bookmarked

Needs LibreOffice (soffice) and the same Node/Playwright set-up as build_pdf.py:
  PLAYWRIGHT_MODULE=<playwright/index.mjs> CHROME=<chromium> python3 src/build_pdfs.py
Run build_all.py and build_pdf.py first.
"""
import html
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pymupdf

import content as C

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "pdf"
BUILD = ROOT / "src" / "pdf_build"
PDF.mkdir(exist_ok=True)
BUILD.mkdir(exist_ok=True)
E = html.escape


def office_to_pdf(src, dst):
    """LibreOffice conversion in a private profile/temp dir (it refuses some paths)."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        shutil.copy(src, tmp / src.name)
        subprocess.run(["soffice", f"-env:UserInstallation=file://{tmp}/profile", "--headless", "--convert-to", "pdf",
                        "--outdir", str(tmp), str(tmp / src.name)], check=True, capture_output=True)
        shutil.copy(tmp / (src.stem + ".pdf"), dst)


def meeting_html():
    summary = (ROOT / "meeting" / "Prasadam_Revenue_Generation_Plan_summary.txt").read_text(encoding="utf-8")
    transcript = (ROOT / "meeting" / "Prasadam_Revenue_Generation_Plan_transcript.txt").read_text(encoding="utf-8")
    turns = []
    lines = transcript.splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i].strip()
        if ln and i + 1 < len(lines) and lines[i + 1].strip() and "  " in lines[i]:
            who, _, ts = lines[i].rpartition("  ")
            turns.append((who.strip(), ts.strip(), lines[i + 1].strip()))
            i += 2
        else:
            i += 1
    insights = "".join(f"<h3>{E(t)}</h3><ul>" + "".join(f"<li>{E(p)}</li>" for p in pts) + "</ul>" for t, pts in C.MEETING_INSIGHTS)
    summ = "".join(f"<p>{E(l)}</p>" if not l.startswith("- ") else f"<p class='b'>• {E(l[2:])}</p>" for l in summary.splitlines() if l.strip())
    trans = "".join(f"<div class='turn'><div class='who'>{E(w)} <span>{E(t)}</span></div><div>{E(x)}</div></div>" for w, t, x in turns)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: A4; margin: 18mm 16mm; }} html{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body {{ font-family:'Noto Sans',sans-serif; font-size:9.5pt; line-height:1.5; color:#2B221E; }}
h1 {{ font-family:'Noto Serif',serif; color:#7A1F2B; font-size:20pt; margin:0 0 2mm; }}
h2 {{ font-family:'Noto Serif',serif; color:#7A1F2B; font-size:14pt; margin:7mm 0 2mm; break-after:avoid; }}
h3 {{ color:#C76A00; font-size:10.5pt; margin:4mm 0 1mm; break-after:avoid; }}
.k {{ color:#C76A00; font-weight:700; letter-spacing:.08em; font-size:9pt; }}
.note {{ background:#FBF3E6; border-left:1.4mm solid #C76A00; padding:3mm 4mm; margin:3mm 0; }}
.b {{ margin:0 0 1mm 4mm; }} p {{ margin:0 0 2mm; }}
.turn {{ margin:0 0 3mm; break-inside:avoid; }} .who {{ font-weight:700; color:#7A1F2B; }} .who span {{ color:#6B5E55; font-weight:400; }}
section {{ break-before:page; }}
</style></head><body>
<div class="k">MEETING RECORD</div><h1>Prasadam Revenue Generation Plan</h1>
<p>26 September 2026 · Hare Krishna Golden Temple (ISKCON), Hyderabad · speakers: Mukunda Dasa and the production team (labelled Speaker 1–5 in the transcript)</p>
<div class="note">This record holds three things: every point from the meeting grouped by theme (as used in the plan), the automatic meeting summary exactly as produced, and the full automatic transcript exactly as produced. The transcript was machine-generated from the audio recording (about 1 hour 3 minutes); some passages are garbled and are kept as they are. The audio file itself (Prasadam_Revenue_Generation_Plan.mp3, 11 MB) is kept with the meeting owner, not in this PDF.</div>
<h2>1. Everything said, grouped by theme</h2>{insights}
<section><h2>2. Meeting summary (verbatim)</h2>{summ}</section>
<section><h2>3. Full transcript (verbatim)</h2>{trans}</section>
</body></html>"""


def mindmap_print_html():
    src = (ROOT / "03_Mind_Map.html").read_text(encoding="utf-8")
    css = "<style>@page{size:A4;margin:14mm 12mm} .bar{display:none!important} li>ul{display:block!important} .node.has::before{content:''!important} .node{break-inside:avoid} .flow{break-inside:avoid;break-before:page} .flow img{display:block;margin:0 auto;max-width:100%!important;max-height:235mm!important;width:auto!important;height:auto} body{background:#fff!important} html{-webkit-print-color-adjust:exact;print-color-adjust:exact}</style>"
    return src.replace("</head>", css + "</head>").replace("localStorage.getItem('theme')", "null")


if __name__ == "__main__":
    # 1. Office files
    office_to_pdf(ROOT / "01_Business_Plan.docx", PDF / "01_Business_Plan.pdf")
    office_to_pdf(ROOT / "02_Presentation.pptx", PDF / "02_Presentation.pdf")
    office_to_pdf(ROOT / "04_Project_Management_Plan.docx", PDF / "04_Project_Management_Plan.pdf")
    office_to_pdf(ROOT / "05_Project_Tracker.xlsx", PDF / "05_Project_Tracker.pdf")
    # 2. HTML pages printed by Chromium
    (BUILD / "mindmap.html").write_text(mindmap_print_html(), encoding="utf-8")
    (BUILD / "meeting.html").write_text(meeting_html(), encoding="utf-8")
    subprocess.run(["node", str(Path(__file__).with_name("render_pdf.mjs")), "--pages",
                    f"{BUILD / 'mindmap.html'}={PDF / '03_Mind_Map.pdf'}",
                    f"{BUILD / 'meeting.html'}={PDF / '06_Meeting_Record.pdf'}"], check=True, env=os.environ)
    # 3. Compendium
    parts = [("Leadership business plan (board paper)", ROOT / "00_Leadership_Business_Plan.pdf"),
             ("Detailed business plan", PDF / "01_Business_Plan.pdf"),
             ("Presentation deck", PDF / "02_Presentation.pdf"),
             ("Mind map and flowcharts", PDF / "03_Mind_Map.pdf"),
             ("Project management plan", PDF / "04_Project_Management_Plan.pdf"),
             ("Project tracker (all sheets)", PDF / "05_Project_Tracker.pdf"),
             ("Meeting record: themes, summary, full transcript", PDF / "06_Meeting_Record.pdf")]
    doc = pymupdf.open()
    toc = []
    for title, f in parts:
        part = pymupdf.open(f)
        start = doc.page_count + 1
        doc.insert_pdf(part)
        toc.append([1, title, start])
        for lvl, t, pg in part.get_toc():
            toc.append([lvl + 1, t, start + pg - 1])
        print(f"{title}: {part.page_count} pages")
    doc.set_toc(toc)
    doc.set_metadata({"title": f"{C.TITLE} – Complete Compendium", "author": "Mukunda Dasa, DMTT – Hare Krishna Golden Temple, Hyderabad",
                      "subject": "Every document of the prasadam vertical in one file"})
    out = ROOT / "07_Complete_Compendium.pdf"
    doc.save(out, garbage=3, deflate=True)
    print(out, doc.page_count, "pages")
