"""Builds the leadership PDF (00_Leadership_Business_Plan.pdf) from content.py.

Writes two HTML files (cover + body) next to the diagrams; render_pdf.mjs prints
them with headless Chromium and merges them into one PDF.
"""
import html
from pathlib import Path

import content as C

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "src" / "pdf_build"
BUILD.mkdir(exist_ok=True)
E = html.escape

# Chart palette, validated with the dataviz validator (light surface):
# maroon, blue, saffron, green. Used in this fixed order; gaps + direct labels.
CAT = ["#A3303F", "#2B7BB9", "#D97A00", "#5BA05A"]
MAROON, SAFFRON, GOLD, INK, MUTED, LINE, PALE = "#7A1F2B", "#C76A00", "#B8901F", "#2B221E", "#6B5E55", "#E6D9C6", "#FBF3E6"

Y1 = sum(r[1] for r in C.REVENUE_Y1)
Y2 = sum(r[1] * r[2] for r in C.REVENUE_Y1)
Y3 = sum(r[1] * r[2] * r[3] for r in C.REVENUE_Y1)
GP = sum(r[1] * r[4] / 100 for r in C.REVENUE_Y1)
OPEX = sum(o[1] for o in C.OPEX_Y1)
NET = GP - OPEX
GM = GP / Y1


def table(headers, rows, widths=None, cls=""):
    cols = "".join(f'<col style="width:{w}%">' for w in widths) if widths else ""
    th = "".join(f"<th>{E(str(h))}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f"<td>{E(str(c))}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><colgroup>{cols}</colgroup><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'


def ul(items, cls=""):
    return f'<ul class="{cls}">' + "".join(f"<li>{E(i)}</li>" for i in items) + "</ul>"


def callout(title, body, kind=""):
    return f'<div class="callout {kind}"><div class="ct">{E(title)}</div><div>{body}</div></div>'


def figure(svg, caption):
    return f'<figure>{svg}<figcaption>{E(caption)}</figcaption></figure>'


# --------------------------------------------------------------------------- charts
def chart_stacked():
    groups = [("Gifting (R4, R5, R14)", ("R4", "R5", "R14")), ("Festival & restaurant (R2, R3)", ("R2", "R3")),
              ("Internal & retail (R1, R6)", ("R1", "R6")), ("Online, catering & others", ("R7", "R8", "R9", "R10", "R11", "R12"))]
    data = []
    for name, ids in groups:
        v = [0, 0, 0]
        for n, a, m2, m3, _, _ in C.REVENUE_Y1:
            if any(f"({i})" in n for i in ids):
                v[0] += a
                v[1] += a * m2
                v[2] += a * m2 * m3
        data.append((name, v))
    W, H, L, B, T = 620, 250, 54, 36, 20
    top = 800
    sy = lambda v: H - B - (v / top) * (H - B - T)
    out = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="Revenue by stream group, Year 1 to Year 3">']
    for g in range(0, top + 1, 200):
        out.append(f'<line x1="{L}" x2="{W - 170}" y1="{sy(g):.1f}" y2="{sy(g):.1f}" class="grid"/><text x="{L - 8}" y="{sy(g) + 4:.1f}" class="ax" text-anchor="end">{g}</text>')
    bw = 74
    for i, yr in enumerate(["Year 1", "Year 2", "Year 3"]):
        x = L + 30 + i * 125
        base = 0
        for k, (name, v) in enumerate(data):
            y0, y1 = sy(base), sy(base + v[i])
            h = max(y0 - y1 - 2, 0)
            out.append(f'<rect x="{x}" y="{y1:.1f}" width="{bw}" height="{h:.1f}" fill="{CAT[k]}" rx="{3 if k == 3 else 0}"/>')
            if v[i] > 35:
                out.append(f'<text x="{x + bw / 2}" y="{y1 + h / 2 + 4:.1f}" class="in" text-anchor="middle">{v[i]:.0f}</text>')
            base += v[i]
        out.append(f'<text x="{x + bw / 2}" y="{sy(base) - 6:.1f}" class="tot" text-anchor="middle">₹{base:.0f} L</text>')
        out.append(f'<text x="{x + bw / 2}" y="{H - B + 18}" class="ax" text-anchor="middle">{yr}</text>')
    for k, (name, _) in enumerate(data):
        y = 40 + k * 26
        out.append(f'<rect x="{W - 160}" y="{y - 10}" width="12" height="12" rx="2" fill="{CAT[k]}"/><text x="{W - 142}" y="{y}" class="lg">{E(name)}</text>')
    out.append(f'<text x="{L}" y="12" class="ax">₹ lakh</text></svg>')
    return "".join(out)


def chart_streams_y1():
    rows = sorted([r for r in C.REVENUE_Y1 if r[1] > 0], key=lambda r: -r[1])
    W, rowh, L = 620, 19, 230
    H = len(rows) * rowh + 20
    mx = max(r[1] for r in rows)
    out = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="Year-1 revenue by stream">']
    for i, r in enumerate(rows):
        y = 6 + i * rowh
        w = (r[1] / mx) * (W - L - 60)
        out.append(f'<text x="{L - 8}" y="{y + 12}" class="ax" text-anchor="end">{E(r[0])}</text>'
                   f'<rect x="{L}" y="{y + 2}" width="{w:.1f}" height="14" rx="3" fill="{CAT[0]}"/>'
                   f'<text x="{L + w + 6:.1f}" y="{y + 13}" class="lv">₹{r[1]} L</text>')
    return "".join(out) + "</svg>"


def chart_sensitivity():
    pts = [(-30, None), (-20, None), (-10, None), (0, None), (10, None), (20, None), (30, None)]
    vals = [(p, Y1 * (1 + p / 100) * GM - OPEX) for p, _ in pts]
    W, H, L, B, T = 620, 240, 60, 36, 16
    lo, hi = -30, 50
    sy = lambda v: T + (hi - v) / (hi - lo) * (H - B - T)
    out = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="Net contribution sensitivity to revenue">']
    for g in range(-20, hi + 1, 20):
        out.append(f'<line x1="{L}" x2="{W - 10}" y1="{sy(g):.1f}" y2="{sy(g):.1f}" class="{"zero" if g == 0 else "grid"}"/><text x="{L - 8}" y="{sy(g) + 4:.1f}" class="ax" text-anchor="end">{g}</text>')
    out.append(f'<line x1="{L}" x2="{W - 10}" y1="{sy(0):.1f}" y2="{sy(0):.1f}" class="zero"/>')
    bw = 52
    for i, (p, v) in enumerate(vals):
        x = L + 22 + i * 78
        y0, y1 = sy(0), sy(v)
        top_, h = (y1, y0 - y1) if v >= 0 else (y0, y1 - y0)
        col = CAT[3] if v >= 0 else CAT[0]
        out.append(f'<rect x="{x}" y="{top_:.1f}" width="{bw}" height="{max(h, 1):.1f}" rx="3" fill="{col}"/>')
        ty = y1 - 6 if v >= 0 else y1 + 14
        out.append(f'<text x="{x + bw / 2}" y="{ty:.1f}" class="lv" text-anchor="middle">{v:+.0f}</text>')
        out.append(f'<text x="{x + bw / 2}" y="{H - B + 18}" class="ax" text-anchor="middle">{p:+d}%</text>')
    out.append(f'<text x="{L}" y="10" class="ax">Net contribution, ₹ lakh</text><text x="{W - 10}" y="{H - 2}" class="ax" text-anchor="end">Change in Year-1 revenue vs plan</text></svg>')
    return "".join(out), vals


def chart_heatmap():
    W, H, L, B, cell = 620, 330, 80, 50, 50
    out = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="Risk heat map, likelihood by impact">']
    ramp = ["#FBF0E3", "#F6D9B5", "#EFB679", "#E08A3C", "#B85A1E"]
    grid = {}
    for r in C.RISKS:
        grid.setdefault((r[2], r[3]), []).append(r[0].replace("R-", ""))
    for li in range(1, 6):
        for im in range(1, 6):
            x = L + (im - 1) * (cell + 2)
            y = 10 + (5 - li) * (cell + 2)
            sc = li * im
            col = ramp[0 if sc < 4 else 1 if sc < 8 else 2 if sc < 12 else 3 if sc < 16 else 4]
            out.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="4" fill="{col}"/>')
            ids = grid.get((li, im), [])
            for j, idn in enumerate(ids[:4]):
                fill = "#fff" if sc >= 12 else INK
                out.append(f'<text x="{x + cell / 2}" y="{y + 14 + j * 12}" class="hm" fill="{fill}" text-anchor="middle">R{idn}</text>')
    for k in range(1, 6):
        out.append(f'<text x="{L + (k - 1) * (cell + 2) + cell / 2}" y="{10 + 5 * (cell + 2) + 16}" class="ax" text-anchor="middle">{k}</text>')
        out.append(f'<text x="{L - 10}" y="{10 + (5 - k) * (cell + 2) + cell / 2 + 4}" class="ax" text-anchor="end">{k}</text>')
    out.append(f'<text x="{L + 2.5 * (cell + 2)}" y="{H - 8}" class="ax" text-anchor="middle">Impact →</text>')
    out.append(f'<text x="18" y="{10 + 2.5 * (cell + 2)}" class="ax" text-anchor="middle" transform="rotate(-90 18 {10 + 2.5 * (cell + 2)})">Likelihood →</text>')
    lx = L + 5 * (cell + 2) + 40
    out.append(f'<text x="{lx}" y="24" class="lg" font-weight="700">Score = likelihood × impact</text>')
    for k, (lab, c) in enumerate([("1–3 low", ramp[0]), ("4–7 moderate", ramp[1]), ("8–11 elevated", ramp[2]), ("12–15 high", ramp[3]), ("16–25 critical", ramp[4])]):
        out.append(f'<rect x="{lx}" y="{40 + k * 24}" width="14" height="14" rx="2" fill="{c}" stroke="#d8c8b0"/><text x="{lx + 22}" y="{51 + k * 24}" class="lg">{lab}</text>')
    out.append(f'<text x="{lx}" y="{190}" class="lg">Labels are risk IDs (see register).</text>')
    return "".join(out) + "</svg>"


def chart_matrix():
    cap = {"Low": 1, "Low (packaging)": 1, "Low–Medium": 1.6, "Medium": 2.2, "Medium (pagodas)": 2.2, "High (at scale)": 3, "Partner-funded": 1.6}
    mar = {"Low–Medium": 1.4, "Medium": 2, "Medium–High": 2.5, "High": 3, "Royalty 4–8% [ESTIMATE]": 1.8}
    W, H, L, B, T = 620, 250, 60, 40, 14
    sx = lambda v: L + (v - 0.6) / 2.8 * (W - L - 20)
    sy = lambda v: T + (3.4 - v) / 2.4 * (H - B - T)
    out = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="Revenue streams by investment and margin">']
    mx, my = sx(1.8), sy(2.2)
    out.append(f'<rect x="{L}" y="{T}" width="{mx - L:.0f}" height="{my - T:.0f}" fill="#EEF6EE"/>')
    out.append(f'<text x="{L + 8}" y="{T + 16}" class="lg" font-weight="700" fill="{INK}">Quick wins: low investment, high margin</text>')
    out.append(f'<line x1="{mx:.0f}" x2="{mx:.0f}" y1="{T}" y2="{H - B}" class="grid"/><line x1="{L}" x2="{W - 20}" y1="{my:.0f}" y2="{my:.0f}" class="grid"/>')
    placed = {}
    for s in C.STREAMS:
        x, y = sx(cap.get(s["capex"], 1.5)), sy(mar.get(s["margin"], 2))
        k = (round(x), round(y))
        n = placed.get(k, 0)
        placed[k] = n + 1
        xo = x + (n % 4) * 34 - 30
        yo = y + (n // 4) * 22
        out.append(f'<circle cx="{xo:.0f}" cy="{yo:.0f}" r="13" fill="{CAT[1] if cap.get(s["capex"], 1.5) < 1.8 and mar.get(s["margin"], 2) >= 2.2 else CAT[2] if mar.get(s["margin"], 2) >= 2.2 else "#9C8E83"}" stroke="#fff" stroke-width="2"/>'
                   f'<text x="{xo:.0f}" y="{yo + 4:.0f}" class="dot" text-anchor="middle">{s["id"]}</text>')
    out.append(f'<text x="{(L + W) / 2}" y="{H - 8}" class="ax" text-anchor="middle">Up-front investment (capex) →</text>')
    out.append(f'<text x="16" y="{(T + H - B) / 2}" class="ax" text-anchor="middle" transform="rotate(-90 16 {(T + H - B) / 2})">Margin →</text>')
    return "".join(out) + "</svg>"


def chart_roadmap():
    # months from Sep 2026
    spans = [(0, 0.5), (0.5, 2.2), (2.2, 6.2), (6.2, 12.2), (12.2, 24.2), (24.2, 36)]
    W, H, L = 660, 230, 230
    sx = lambda m: L + m / 36 * (W - L - 10)
    out = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="Roadmap phases on a timeline">']
    for m, lab in [(0, "Sep 26"), (6, "Mar 27"), (12, "Sep 27"), (18, "Mar 28"), (24, "Sep 28"), (36, "2029–31 →")]:
        out.append(f'<line x1="{sx(m):.0f}" x2="{sx(m):.0f}" y1="14" y2="{H - 24}" class="grid"/><text x="{sx(m):.0f}" y="{H - 8}" class="ax" text-anchor="middle">{lab}</text>')
    for i, (p, (a, b)) in enumerate(zip(C.PHASES, spans)):
        y = 18 + i * 31
        out.append(f'<text x="{L - 8}" y="{y + 16}" class="ax" text-anchor="end">{E(p["name"].split(" – ")[0])}: {E(p["name"].split(" – ")[1])}</text>')
        out.append(f'<rect x="{sx(a):.1f}" y="{y + 4}" width="{max(sx(b) - sx(a) - 2, 4):.1f}" height="18" rx="4" fill="{CAT[0] if i < 2 else CAT[1] if i < 4 else CAT[2]}"/>')
    x = sx(1.7)
    out.append(f'<line x1="{x:.0f}" x2="{x:.0f}" y1="10" y2="{H - 24}" stroke="{INK}" stroke-dasharray="3 3"/><text x="{x + 4:.0f}" y="12" class="lg">Today (13 Oct 2026)</text>')
    return "".join(out) + "</svg>"


def chart_circles():
    W, H = 620, 290
    cx, cy = 135, 145
    names = list(dict.fromkeys(a["circle"] for a in C.AUDIENCES))
    out = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="Five audience circles">']
    fills = ["#F7E1C4", "#F2D0A6", "#EBBF8B", "#E3AD70", "#D99A55"][::-1]
    for i in range(5):
        r = 135 - i * 25
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fills[i]}" stroke="#fff" stroke-width="2"/>')
        out.append(f'<text x="{cx}" y="{cy - r + 16}" text-anchor="middle" class="hm" fill="{INK}">{5 - i}</text>')
    out.append(f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" class="tot">Temple</text>')
    for i, n in enumerate(names):
        num, desc = n.split(": ")
        y = 30 + i * 54
        out.append(f'<text x="295" y="{y}" class="lg" font-weight="700">{E(num)}: {E(desc)}</text>')
        members = ", ".join(a["name"] for a in C.AUDIENCES if a["circle"] == n)
        line, lines = "", []
        for w in members.split(" "):
            if len(line) + len(w) > 58:
                lines.append(line)
                line = w
            else:
                line = (line + " " + w).strip()
        lines.append(line)
        for j, ln in enumerate(lines[:2]):
            out.append(f'<text x="295" y="{y + 15 + j * 13}" class="ax">{E(ln)}</text>')
    return "".join(out) + "</svg>"


def chart_unit():
    W, rowh, L = 620, 25, 170
    H = len(C.UNIT_ECONOMICS) * rowh + 40
    out = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="Cost and margin per item as share of net price">']
    labs = ["Ingredients", "Packaging", "Labour & overhead", "Gross profit"]
    for k, lab in enumerate(labs):
        out.append(f'<rect x="{L + k * 112}" y="2" width="12" height="12" rx="2" fill="{CAT[k]}"/><text x="{L + 18 + k * 112}" y="12" class="lg">{lab}</text>')
    for i, (n, p, ing, pk, lb) in enumerate(C.UNIT_ECONOMICS):
        net = p / 1.05
        parts = [ing, pk, lb, net - ing - pk - lb]
        y = 28 + i * rowh
        out.append(f'<text x="{L - 8}" y="{y + 14}" class="ax" text-anchor="end">{E(n)}</text>')
        x = L
        for k, v in enumerate(parts):
            w = v / net * (W - L - 50)
            out.append(f'<rect x="{x:.1f}" y="{y + 2}" width="{max(w - 2, 1):.1f}" height="18" fill="{CAT[k]}"/>')
            if w > 34:
                out.append(f'<text x="{x + w / 2:.1f}" y="{y + 15}" class="in" text-anchor="middle">{v / net * 100:.0f}%</text>')
            x += w
    return "".join(out) + "</svg>"


# --------------------------------------------------------------------------- pages
sens_svg, sens_vals = chart_sensitivity()
breakeven = OPEX / (GM * Y1) - 1

decisions = [
    ("1", "Approve the Prasadam, Sweets & Savories vertical as a temple revenue vertical with its own cost centre", "Strategic approval"),
    ("2", f"Approve Year-1 incremental operating budget of about ₹{OPEX} lakh, released by phase", "Budget"),
    ("3", "Approve staged capex under ₹30 lakh (machines, pagodas, storage), each item released only after the previous phase meets its targets", "Budget"),
    ("4", "Decide the brand name on packs (ISKCON Hyderabad / Hare Krishna Golden Temple / a sub-brand) and give written approval for its commercial use", "Brand"),
    ("5", "Mandate that all departments place prasadam orders only with the in-house production team", "Policy"),
    ("6", "Approve one immediate hire for production/order coordination and seasonal staff for hero campaigns", "People"),
    ("7", "Authorise an FSSAI State Licence covering manufacturing, e-commerce and off-site stalls", "Compliance"),
    ("8", "Adopt the governance rhythm: monthly ROI report from DMTT, quarterly steering review", "Governance"),
]

css = f"""
@page {{ size: A4; margin: 18mm 16mm 18mm 16mm; }}
* {{ box-sizing: border-box; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ font-family: 'Noto Sans', 'DejaVu Sans', sans-serif; font-size: 9.6pt; line-height: 1.5; color: {INK}; margin: 0; }}
h1 {{ font-family: 'Noto Serif', serif; font-size: 21pt; color: {MAROON}; margin: 0 0 4mm; line-height: 1.2; break-after: avoid; }}
h1 .num {{ color: {SAFFRON}; font-size: 12pt; display: block; font-family: 'Noto Sans'; letter-spacing: .08em; text-transform: uppercase; margin-bottom: 1mm; }}
h2 {{ font-family: 'Noto Serif', serif; font-size: 13pt; color: {MAROON}; margin: 6mm 0 2mm; break-after: avoid; }}
h3 {{ font-size: 10.5pt; color: {SAFFRON}; margin: 4mm 0 1mm; break-after: avoid; }}
p {{ margin: 0 0 2.5mm; }}
.lead {{ font-size: 11pt; color: {INK}; }}
section {{ break-before: page; }}
section.first {{ break-before: auto; }}
.rule {{ width: 22mm; height: 1.2mm; background: {GOLD}; margin: 0 0 5mm; border-radius: 1mm; }}
table {{ width: 100%; border-collapse: collapse; margin: 2mm 0 4mm; font-size: 8.2pt; table-layout: fixed; }}
thead {{ display: table-header-group; }}
tr {{ break-inside: avoid; }}
th {{ background: {MAROON}; color: #fff; text-align: left; padding: 1.6mm 2mm; font-weight: 600; }}
td {{ padding: 1.1mm 2mm; border-bottom: .3mm solid {LINE}; vertical-align: top; }}
tbody tr:nth-child(even) td {{ background: {PALE}; }}
table.num td:not(:first-child), table.num th:not(:first-child) {{ text-align: right; font-variant-numeric: tabular-nums; }}
table.num td:last-child, table.num th:last-child {{ text-align: left; }}
tr.total td {{ font-weight: 700; background: #F3E3CC !important; }}
ul {{ margin: 0 0 3mm; padding-left: 5mm; }} li {{ margin: 0 0 1mm; }}
.cols {{ display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; }}
.cols3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 4mm; }}
.card {{ border: .3mm solid {LINE}; border-radius: 2.5mm; padding: 3mm 3.5mm; break-inside: avoid; background: #fff; }}
.card h3 {{ margin-top: 0; }}
.kpis {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 3mm; margin: 3mm 0 5mm; }}
.kpi {{ border: .3mm solid {LINE}; border-radius: 2.5mm; padding: 3mm; background: #fff; }}
.kpi .v {{ font-family: 'Noto Serif'; font-size: 19pt; font-weight: 700; color: {MAROON}; line-height: 1.1; }}
.kpi .l {{ font-size: 8pt; color: {MUTED}; margin-top: 1mm; }}
.callout {{ border-left: 1.4mm solid {SAFFRON}; background: {PALE}; padding: 3mm 4mm; border-radius: 0 2mm 2mm 0; margin: 3mm 0 4mm; break-inside: avoid; }}
.callout .ct {{ font-weight: 700; color: {MAROON}; margin-bottom: 1mm; }}
.callout.warn {{ border-color: {MAROON}; }}
figure {{ margin: 2mm 0 5mm; break-inside: avoid; }}
figcaption {{ font-size: 8pt; color: {MUTED}; margin-top: 1mm; }}
svg.chart {{ width: 100%; height: auto; font-family: 'Noto Sans'; }}
svg .grid {{ stroke: #E9E1D6; stroke-width: 1; }} svg .zero {{ stroke: {MUTED}; stroke-width: 1.2; }}
svg .ax {{ font-size: 10px; fill: {MUTED}; }} svg .lg {{ font-size: 10.5px; fill: {INK}; }}
svg .in {{ font-size: 10px; fill: #fff; font-weight: 700; }} svg .tot {{ font-size: 12px; fill: {INK}; font-weight: 700; }}
svg .lv {{ font-size: 10px; fill: {INK}; font-weight: 600; }} svg .hm {{ font-size: 10px; font-weight: 700; }}
svg .dot {{ font-size: 9px; fill: #fff; font-weight: 700; }}
.toc {{ columns: 2; column-gap: 10mm; font-size: 10pt; }} .toc div {{ padding: 1.2mm 0; border-bottom: .3mm dotted {LINE}; break-inside: avoid; }}
.toc b {{ color: {SAFFRON}; display: inline-block; width: 9mm; }}
.small {{ font-size: 8pt; color: {MUTED}; }}
.tag {{ display: inline-block; font-size: 7.5pt; padding: .3mm 2mm; border-radius: 3mm; background: #F3E3CC; color: {MAROON}; font-weight: 600; }}
.diagram img {{ display: block; margin: 0 auto; max-width: 100%; max-height: 228mm; object-fit: contain; }}
.sign td {{ height: 12mm; }}
.swot {{ font-size: 8.4pt; }} .swot li {{ margin: 0; }}
"""

sec = []
TOC = []


def section(num, title, body, first=False):
    TOC.append((num, title))
    sec.append(f'<section class="{"first" if first else ""}"><h1><span class="num">{E(num)}</span>{E(title)}</h1><div class="rule"></div>{body}</section>')


# 1 Executive summary --------------------------------------------------------
section("Section 1", "Executive summary", f"""
<p class="lead">{E(C.ONE_LINE_PITCH)}</p>
<div class="kpis">
 <div class="kpi"><div class="v">₹6 L</div><div class="l">Janmashtami 2026 counter sales, sold out with limited stalls</div></div>
 <div class="kpi"><div class="v">₹{Y1 / 100:.1f} Cr</div><div class="l">Year-1 revenue target (Oct 2026–Sep 2027) [estimate]</div></div>
 <div class="kpi"><div class="v">₹{NET:.0f} L</div><div class="l">Year-1 net contribution after new costs, before capex [estimate]</div></div>
 <div class="kpi"><div class="v">₹{Y3 / 100:.1f} Cr</div><div class="l">Year-3 revenue as channels and capacity scale [estimate]</div></div>
</div>
<h2>The opportunity</h2>
<p>Demand already exists and is not being served. Janmashtami 2026 counters sold out at about ₹6 lakh. Three companies asked for Dasara gift boxes that we could not supply. Chinmaya Mission has asked for 50,000 meals over two days. Big donors ask for 5 kg tins of namkeen every monsoon. India's packaged-sweets market is growing at about 16% a year, and corporate gifting is expected to exceed ₹27,000 crore by 2030.</p>
<h2>Why we can win</h2>
<p>People trust the ISKCON name. A satvik, preservative-free product, prepared in a temple kitchen and offered to Sri Sri Radha Krishna, is something no local sweet shop can claim. We already have the network (company owners, MNR's 42 institutions, chambers of commerce, BNI, Rotary, 100 gated communities, donor databases), the systems (donor dispatch, Shopify, negotiated vendor rates) and the people (a production lead for the kitchen; Mukunda Dasa and the DMTT team for marketing, technology and sales). The piece that was missing in earlier attempts, an owner for production, is now in place.</p>
<h2>The plan</h2>
<ul>
<li><b>Two price tiers.</b> A competitive mass tier for volume, which keeps the kitchen busy and covers fixed costs, and a premium tier for margin.</li>
<li><b>14 revenue streams in five audience circles.</b> Start with those that need little capital: internal supply, festival stalls, corporate and white-label gifting.</li>
<li><b>Six phases.</b> Dasara and Diwali 2026 are the pilot. E-commerce, communities and catering follow. A dedicated unit, QSRs and exports come only after demand is proven.</li>
<li><b>Accountability.</b> DMTT tracks every rupee and every hour, with a monthly ROI report to leadership.</li>
</ul>
{callout("What we are asking leadership for", "Approval of the vertical, a Year-1 operating budget of about ₹" + str(OPEX) + " lakh released by phase, staged capex under ₹30 lakh, a decision on the brand name used on packs, and a policy that all prasadam orders go to the in-house kitchen. The full list is in Section 2.")}
<p class="small">All financial figures marked [estimate] are planning assumptions built from the meeting and desk research. They will be replaced by the 6–12 month order analysis (action A4) before money is committed.</p>
""")

# 2 Decisions ------------------------------------------------------------------
section("Section 2", "Decisions requested from leadership", f"""
<p>Each decision below is needed for the plan to proceed. Budgets are released in stages, each tied to a phase gate (see Section 11).</p>
{table(["#", "Decision", "Type", "Approved / Comments"], [d + ("",) for d in decisions], [5, 63, 13, 19])}
<h2>Phase-gate funding</h2>
{table(["Gate", "When", "Release", "Condition to pass"], [
    ("G0 Charter", "October 2026", "Foundation and pilot opex (packaging, samples, 1 hire, seasonal staff)", "Plan approved; brand and licence decisions made"),
    ("G1 Pilot review", "30 Nov 2026", "Phase 2 opex (e-commerce, sales executive, catering pilot)", "Pilot cash-positive; on-time delivery ≥ 95%; no food-safety incidents"),
    ("G2 Channel review", "31 Mar 2027", "Phase 3 capex (pagodas, small machines, storage)", "Monthly revenue run-rate ≥ ₹15 lakh; online store live"),
    ("G3 Year-1 review", "30 Sep 2027", "Business case for a dedicated unit and QSR pilot", "Year-1 revenue ≥ 80% of plan; positive ROI"),
], [16, 14, 36, 34])}
""")

# 3 Context ------------------------------------------------------------------
section("Section 3", "Strategic context and market", f"""
<h2>Evidence from our own temple</h2>
<div class="cols">
<div class="card"><h3>Demand we have seen</h3>{ul(["Janmashtami 2026: almost all prasadam counters sold out (≈ ₹6 lakh)", "A single stall draws queues of 10–50 people; many walk away", "Three companies asked for Dasara gift boxes, calendars and gifts", "Chinmaya Mission asked for 50,000 meals over two days", "Big donors order 5 kg namkeen tins in monsoon", "A partner has offered funds and execution for 100 QSRs in Hyderabad", "A new 250 g weekly item in a see-through box had very good response"])}</div>
<div class="card"><h3>Assets we already own</h3>{ul(["ISKCON brand, and our pages rank first when people search for ISKCON Hyderabad", "Donor databases; WhatsApp, SMS, RCS, Google and Meta ads skills", "System to dispatch prasadam to online donors across India", "Shopify experience; about 15,000 Amazon parcels shipped", "Negotiated vendor rates, HR, spaces, new kitchen", "AI engineers and data scientists in DMTT", "Wooden gift boxes in stock; see-through boxes in use"])}</div>
</div>
<h2>Market research</h2>
{table(["Topic", "Finding", "Source"], [(a, b, c) for a, b, c, _ in C.MARKET_FACTS], [18, 62, 20])}
{callout("What this means for us", "Boxes are the leading format in a market growing about 16% a year, and corporate buyers drive most festival gifting, so gift boxes sold through our owner-level network are the fastest route to revenue. The cut in GST on packaged namkeen to 5% helps the mass tier. Under the April 2026 FSSAI limits, turnover of ₹1.5–50 crore needs a State Licence, which we should plan for from the start.")}
""")

section("Section 3 (contd.)", "Competition and SWOT", f"""
{table(["Competitor", "Profile", "Tier", "Our edge"], C.COMPETITORS, [20, 30, 12, 38])}
<h2>SWOT analysis</h2>
<div class="cols">
<div class="card swot" style="border-top:1.2mm solid {CAT[3]}"><h3>Strengths</h3>{ul(C.SWOT["Strengths"])}</div>
<div class="card swot" style="border-top:1.2mm solid {CAT[0]}"><h3>Weaknesses</h3>{ul(C.SWOT["Weaknesses"])}</div>
<div class="card swot" style="border-top:1.2mm solid {CAT[1]}"><h3>Opportunities</h3>{ul(C.SWOT["Opportunities"])}</div>
<div class="card swot" style="border-top:1.2mm solid {CAT[2]}"><h3>Threats</h3>{ul(C.SWOT["Threats"])}</div>
</div>
""")

# 4 Vision --------------------------------------------------------------------
section("Section 4", "Vision, mission and positioning", f"""
<div class="cols">
<div class="card"><h3>Vision</h3><p>{E(C.VISION)}</p></div>
<div class="card"><h3>Mission</h3><p>{E(C.MISSION)}</p></div>
</div>
<h2>Positioning statement</h2>
<p class="lead">For families, companies and devotees who want sweets they can trust, our prasadam is the only satvik, preservative-free range prepared in a temple kitchen and offered to Sri Sri Radha Krishna, backed by decades of ISKCON goodwill. Unlike local shops that use colours and chemicals, every pack is pure, and every purchase supports the temple's service.</p>
<h2>Brand pillars</h2>
{table(["Pillar", "Promise"], [("Purity", "Satvik (no onion, garlic or eggs), no preservatives, no artificial colours"), ("Devotion", "Prepared with care and offered to the Deity first"), ("Trust", "The ISKCON / Hare Krishna name and a long record in Hyderabad"), ("Service", "Proceeds support temple activities and food-for-all programmes"), ("Delight", "Packaging that makes a gift feel special")], [18, 82])}
<h2>Guiding principles</h2>
{ul(["Passive selling, not pushing: stalls go where people already are, and people choose to buy.", "Start with what we have; invest only after demand is proven.", "Technology is the engine of scale (as with Zomato, Swiggy, Amazon): data, e-commerce, automation.", "Every rupee and every hour is tracked; ROI is visible to anyone who asks.", "Quality and food safety are never traded for volume."])}
""")

# 5 Audiences -----------------------------------------------------------------
aud_rows = [(a["name"], a["circle"].split(":")[0], a["offer"], a["channel"], a["price"]) for a in C.AUDIENCES]
section("Section 5", "Target audiences", f"""
<p>Different audiences, different circles, different products for each. We start inside (Circle 1 funds the kitchen from day one), then go to our B2B network (Circle 2) for the big festival orders. Circles 3 and 4 add year-round volume; Circle 5 is the long-term scale play.</p>
{figure(chart_circles(), "Figure 1. The five audience circles, from those who already come to us (inner) to scale markets (outer).")}
{table(["Audience", "Circle", "Our offer", "Channel", "Price point"], aud_rows, [18, 9, 32, 27, 14])}
""")

# 6 Business model ------------------------------------------------------------
section("Section 6", "Business model and revenue streams", f"""
<p>Fourteen revenue streams, sequenced by how much capital they need and how fast they pay back. The quick wins (top left in Figure 2) start in the Dasara–Diwali pilot.</p>
{figure(chart_matrix(), "Figure 2. Revenue streams by up-front investment and margin. Blue = quick wins; saffron = high margin but more investment; grey = volume or strategic streams. IDs match the table.")}
{table(["ID", "Stream", "Phase", "Capex", "Margin"], [(s["id"], s["name"], s["phase"], s["capex"], s["margin"]) for s in C.STREAMS], [7, 43, 18, 16, 16])}
""")

section("Section 6 (contd.)", "Revenue streams in detail", "".join(
    f'<div class="card" style="margin-bottom:3mm"><h3>{E(s["id"])} · {E(s["name"])} <span class="tag">{E(s["phase"])}</span></h3>'
    f'<p><b>What:</b> {E(s["what"])}</p><p><b>Why:</b> {E(s["why"])}</p><p><b>How:</b> {E(s["how"])}</p><p class="small"><b>KPIs:</b> {E(s["kpi"])}</p></div>'
    for s in C.STREAMS))

# 7 Products & pricing ---------------------------------------------------------
section("Section 7", "Products, packaging and pricing", f"""
<p>First criterion: a shelf life of at least 15–20 days, so stock can be made ahead of festivals and any surplus can be sold online. Shelf-life figures are typical values and will be confirmed by lab tests on our own recipes and packs.</p>
{table(["Product", "Category", "Shelf life (days)", "Tier", "Sweetener", "Packs"], [p[:6] for p in C.PRODUCTS], [24, 15, 12, 13, 17, 19])}
<h2>Gift-box tiers</h2>
{table(["Tier", "Price", "Contents", "Best for"], C.GIFT_TIERS, [15, 15, 42, 28])}
<h2>Packaging</h2>
{ul(C.PACKAGING)}
""")

ue_rows = []
for n, p, i, pk, lb in C.UNIT_ECONOMICS:
    net = p / 1.05
    g = net - i - pk - lb
    ue_rows.append((n, f"₹{p}", f"₹{net:.0f}", f"₹{i}", f"₹{pk}", f"₹{lb}", f"₹{g:.0f}", f"{g / net * 100:.0f}%"))
section("Section 7 (contd.)", "Pricing strategy and unit economics", f"""
{callout("Why two tiers", "Premium alone means limited customers and limited business, and it cannot pay for rent, power and salaries. Competitive pricing alone means thin margins. Running both lets volume keep the kitchen busy while premium boxes add margin.")}
{table(["Tier", "Logic", "Used for"], C.PRICING, [20, 55, 25])}
<h2>Illustrative unit economics [estimate]</h2>
{figure(chart_unit(), "Figure 3. Where each rupee of net price goes (after 5% GST). To be replaced by production's costing sheets (task 3.3).")}
{table(["Item", "MRP", "Net of GST", "Ingredients", "Packaging", "Labour & OH", "Gross profit", "GM %"], ue_rows, [24, 9, 11, 11, 11, 12, 12, 10], "num")}
""")

# 8 GTM ----------------------------------------------------------------------
section("Section 8", "Go-to-market: marketing and sales", f"""
{table(["Lever", "Plan"], C.MARKETING, [20, 80])}
<h2>Customer funnel</h2>
{table(["Stage", "Activities"], C.MARKETING_FUNNEL, [22, 78])}
<div class="cols">
<div class="card"><h3>Corporate gifting sales process</h3><ol style="margin:0;padding-left:5mm">
<li>Build the target list from chamber, BNI, Rotary, T-Hub, donor and MNR contacts; rank by staff size.</li>
<li>Warm introduction by Mukunda Dasa; meet the owner/HR with a sample box, catalogue and price list.</li>
<li>Offer own-brand or white-label; share the mock-up within 48 hours.</li>
<li>Quote with volume slab, delivery date and 50% advance.</li>
<li>Confirm PO, lock the production slot, approve the sticker proof.</li>
<li>Dispatch with story card; feedback call; reminder for the next festival.</li></ol></div>
<div class="card"><h3>Festival stall playbook</h3>{ul(["Put stalls where footfall is: entrance, darshan exit queue, Goshala walking path, staircases, garden, waterfall and benches, Goshala entrance to Samskara hall.", "Several counters in a row instead of one crowded counter.", "Pre-packed combos (₹100 / ₹200 / ₹500) and UPI at every counter.", "Runners restock hourly; stock-out alerts on WhatsApp.", "Restaurant takes over the lawn with chairs and round tables on festival days.", "Permanent rain-proof pagodas.", "Leftover shelf-stable stock goes online within 48 hours."])}</div>
</div>
{callout("If someone says the temple is becoming commercial", "This is passive selling. We are not pushing anyone; we place stalls where devotees already are, and they choose to approach. Prasadam is offered to the Deity first and the proceeds support temple service.")}
""")

# 9 Operations ----------------------------------------------------------------
section("Section 9", "Operations and compliance", f"""
{table(["Area", "Plan"], C.OPERATIONS, [20, 80])}
<h2>Compliance checklist</h2>
{ul(["FSSAI State Licence (manufacturing), covering e-commerce and off-site stalls.", "Labels: product name, ingredients, allergens (nuts, milk, sesame), net weight, MRP, date of manufacture, best-before, batch, FSSAI logo and number, veg mark, customer-care contact.", "Voluntary best-before boards on loose sweets at counters.", "GST registration; 5% GST on sweets and packaged namkeen (check HSN for each SKU).", "Legal metrology for pre-packed goods; trade licence; fire NOC; pest control; water testing; staff medical fitness.", "Written approval for using the temple / ISKCON name and logo on commercial packs."])}
<h2>Quality management</h2>
{ul(["Standard recipes and yield sheets for every SKU; taste-panel sign-off before launch.", "Shelf-life lab test per SKU and pack before selling online.", "Batch codes and FIFO; retained samples of each batch for 30 days.", "Hygiene SOP: head covers, gloves, hand-wash, cleaning log, pest control.", "Complaint log with 48-hour response and root-cause review; monthly internal audit."])}
""")

# 10 Organisation ----------------------------------------------------------------
raci = [r for r in C.RACI_ACTIVITIES]
section("Section 10", "Organisation and governance", f"""
{table(["Role", "Person", "Responsibility"], C.ORG_ROLES, [32, 26, 42])}
<h2>Responsibility matrix (RACI)</h2>
<p class="small">R = Responsible · A = Accountable · C = Consulted · I = Informed</p>
{table(["Activity"] + C.RACI_ROLES, raci, [24] + [9.5] * 8)}
<h2>Governance rhythm</h2>
{table(["Cadence", "Forum", "Chair"], C.GOVERNANCE, [22, 53, 25])}
""")

# 11 Roadmap -------------------------------------------------------------------
section("Section 11", "Roadmap", f"""
{figure(chart_roadmap(), "Figure 4. Baseline roadmap (dated 26 Sep 2026). Phases 0 and 1 overlap with the Dasara–Diwali season now under way.")}
{"".join(f'<div class="card" style="margin-bottom:3mm"><h3>{E(p["name"])} <span class="tag">{E(p["window"])}</span></h3><p><b>Goal:</b> {E(p["goal"])}</p>{ul(p["items"])}</div>' for p in C.PHASES)}
""")

section("Section 11 (contd.)", "Milestones and hero-campaign calendar", f"""
{table(["Milestone", "Target", "Gate criteria"], [
    ("M1 Plan circulated", "30 Sep 2026", "Plan shared with production lead and manager"),
    ("M2 Decision meeting / charter signed", "Oct 2026", "Products, quantities, budget, pricing agreed"),
    ("M3 Sales kit ready", "12 Oct 2026", "Catalogue, prices, 10 sample boxes"),
    ("M4 Dasara delivered", "20 Oct 2026", "Stalls live, first corporate orders delivered"),
    ("M5 Diwali delivered", "6 Nov 2026", "All Diwali orders dispatched on time"),
    ("M6 Pilot review (gate G1)", "30 Nov 2026", "P&L, ROI, lessons; go/no-go for Phase 2"),
    ("M7 Online store live", "15 Jan 2027", "Shopify live with ≥ 12 SKUs"),
    ("M8 Pagodas installed", "30 Jun 2027", "Permanent stalls in place"),
    ("M9 Janmashtami 2027", "Sep 2027", "Counter sales ≥ ₹30 L (base) / ₹60 L (stretch)"),
    ("M10 Year-1 review (gate G3)", "30 Sep 2027", "Annual report and Year-2 budget approved"),
], [34, 16, 50])}
<h2>Hero-campaign calendar</h2>
<p class="small">Dates are approximate; confirm against the temple Panchang.</p>
{table(["Festival", "When", "Opportunity", "Demand"], C.FESTIVALS, [28, 22, 38, 12])}
""")

# 12 Financials ---------------------------------------------------------------
fin_rows = []
for n, a, m2, m3, gm, basis in C.REVENUE_Y1:
    fin_rows.append((n, f"{a:.0f}", f"{a * m2:.0f}", f"{a * m2 * m3:.0f}", f"{gm}%", basis))
fin_tbl = table(["Stream", "Y1", "Y2", "Y3", "GM", "Basis"], fin_rows, [27, 7, 7, 7, 7, 45], "num").replace(
    "</tbody>", f'<tr class="total"><td>Total (₹ lakh)</td><td>{Y1:.0f}</td><td>{Y2:.0f}</td><td>{Y3:.0f}</td><td>{GM * 100:.0f}%</td><td>Year 3 excludes QSR royalty</td></tr></tbody>')
section("Section 12", "Financial plan [estimate]", f"""
<div class="kpis">
 <div class="kpi"><div class="v">₹{Y1:.0f} L</div><div class="l">Year-1 revenue</div></div>
 <div class="kpi"><div class="v">{GM * 100:.0f}%</div><div class="l">Blended gross margin</div></div>
 <div class="kpi"><div class="v">₹{OPEX} L</div><div class="l">Year-1 incremental opex</div></div>
 <div class="kpi"><div class="v">₹{NET:.0f} L</div><div class="l">Year-1 net contribution (before capex)</div></div>
</div>
{figure(chart_stacked(), "Figure 5. Revenue by stream group, ₹ lakh. Year 2 and Year 3 apply the growth multipliers in the table below.")}
{fin_tbl}
""")

opex_tbl = table(["Item", "₹ lakh", "Note"], list(C.OPEX_Y1), [36, 10, 54], "num").replace(
    "</tbody>", f'<tr class="total"><td>Total</td><td>{OPEX}</td><td></td></tr></tbody>')
section("Section 12 (contd.)", "Costs, sensitivity and funding", f"""
{figure(chart_streams_y1(), "Figure 6. Year-1 revenue by stream, ₹ lakh.")}
<div>
<h3 style="margin-top:0">Year-1 summary (₹ lakh)</h3>
{table(["Line", "₹ lakh"], [("Gross revenue", f"{Y1:.0f}"), ("Gross profit (after ingredients, packaging, direct labour)", f"{GP:.0f}"), ("Incremental operating costs", f"{OPEX}"), ("Net contribution before capex", f"{NET:.0f}"), ("Net margin", f"{NET / Y1 * 100:.1f}%")], [75, 25], "num")}
</div>
<h2>Year-1 incremental operating costs</h2>
{opex_tbl}
<h2>Sensitivity: what if revenue misses plan?</h2>
{figure(sens_svg, "Figure 7. Year-1 net contribution if revenue lands above or below plan, holding opex and gross margin constant.")}
{callout("Reading the sensitivity", f"The new costs are covered at about {(1 + breakeven) * 100:.0f}% of planned revenue (≈ ₹{Y1 * (1 + breakeven):.0f} lakh). A 20% shortfall means the vertical roughly breaks even rather than losing money, so the downside is limited. That is why opex and capex are released only at the phase gates.", "warn")}
<h2>Capital expenditure (staged)</h2>
{table(["Item", "Estimate", "When"], C.CAPEX, [58, 18, 24])}
<h2>Funding</h2>
{ul(["Phases 0–1: existing kitchen budget plus 50% customer advances on B2B orders.", "Phases 2–3: reinvested surplus; sponsors and donors for pagodas and machines.", "Phase 4 onward: surplus plus partner capital (the QSR partner has offered funds); CSR support where appropriate."])}
""")

# 13 Risks -------------------------------------------------------------------
section("Section 13", "Risks and mitigation", f"""
{figure(chart_heatmap(), "Figure 8. Risk heat map. Two risks score 15 or more: Diwali peak capacity (R01) and QSR partner quality (R13).")}
{table(["ID", "Risk", "L", "I", "Score", "Mitigation", "Owner"], [(r[0], r[1], r[2], r[3], r[2] * r[3], r[4], r[5]) for r in sorted(C.RISKS, key=lambda r: -r[2] * r[3])], [7, 23, 4, 4, 7, 40, 15])}
""")

# 14 KPIs -----------------------------------------------------------------------
section("Section 14", "KPIs and ROI accountability", f"""
<p>DMTT will track the vertical so that the question "we spent this much; what did we get back?" always has a clear answer.</p>
{table(["KPI", "Definition", "Unit", "Frequency"], C.KPIS, [18, 52, 15, 15])}
{callout("ROI formula", "ROI % = (Revenue − ingredients − packaging − direct labour − marketing − allocated overheads − value of hours invested) ÷ total cost including capex depreciation × 100. Hours are logged weekly by each team and valued at a standard hourly cost, so staff time is never treated as free.")}
<h2>Objectives and targets</h2>
{table(["#", "Objective", "Measure"], C.OBJECTIVES, [7, 33, 60])}
""")

# 15 Actions --------------------------------------------------------------------
section("Section 15", "Immediate actions and open questions", f"""
{table(["#", "Action", "Owner", "Due"], C.ACTION_ITEMS, [6, 56, 22, 16])}
<h2>Open questions for leadership and the production team</h2>
{ul(C.OPEN_QUESTIONS)}
<h2>New ideas to test cheaply</h2>
{table(["Idea", "Description"], C.BUSINESS_IDEAS, [27, 73])}
""")

section("Section 16", "Approval and sign-off", f"""
<p>By signing below, leadership approves the vertical, the phase-gated budget and the decisions recorded in Section 2.</p>
<h2>Sign-off</h2>
{table(["Role", "Name", "Signature", "Date"], [("Executive sponsor (temple leadership)", "", "", ""), ("Vertical lead: marketing, sales & technology", "Mukunda Dasa", "", ""), ("Production lead", "", "", ""), ("Finance", "", "", "")], [36, 24, 24, 16], "sign")}
<h2>Decisions recorded</h2>
{table(["#", "Decision", "Approved (Y/N)", "Comments"], [(d[0], d[1], "", "") for d in decisions], [5, 55, 14, 26])}
""")

# Appendices -----------------------------------------------------------------------
section("Appendix A", "Everything said in the planning meeting", f"<p>From the {E(C.SOURCE_MEETING)}: recording, transcript and summary. Grouped by theme; nothing omitted.</p>" + "".join(
    f'<h3>{E(t)}</h3>{ul(pts)}' for t, pts in C.MEETING_INSIGHTS))

diag_html = []
for slug, title in [("mind_map", "Mind map overview"), ("order_flow", "Order-to-delivery flow (all channels)"), ("corporate_gifting_flow", "Corporate gifting sales flow"),
                    ("festival_stall_flow", "Festival stall operations"), ("phase_gate_flow", "Decision and phase-gate flow"), ("roi_tracking_flow", "DMTT ROI tracking flow")]:
    f = ROOT / "diagrams" / f"{slug}.png"
    if f.exists():
        diag_html.append(f'<div class="diagram" style="break-before:page"><h2>{E(title)}</h2><img src="{f.as_uri()}"></div>')
section("Appendix B", "Mind map and process flowcharts", "<p>The interactive version with every detail is <b>03_Mind_Map.html</b>.</p>" + "".join(diag_html).replace('style="break-before:page"', "", 1))

section("Appendix C", "Audience profiles and sources", "".join(
    f'<div class="card" style="margin-bottom:2.5mm"><h3>{E(a["name"])} <span class="tag">{E(a["circle"])}</span></h3><p><b>Who:</b> {E(a["who"])} · <b>Needs:</b> {E(a["needs"])}</p></div>'
    for a in C.AUDIENCES) + "<h2>Sources</h2>" + ul([f"{n}: {u}" for n, u in C.SOURCES]))

# --------------------------------------------------------------------------- assemble
toc_html = '<section class="first"><h1><span class="num">Contents</span>What this document covers</h1><div class="rule"></div><div class="toc">' + "".join(
    f"<div><b>{E(n.replace('Section ', '').replace(' (contd.)', ''))}</b>{E(t)}</div>" for n, t in TOC if "contd" not in n) + "</div>" + callout(
    "How to read this document", "Sections 1–2 are the summary and the decisions requested; they can be read on their own. Sections 3–15 hold the detail behind each decision. Appendix A records everything said in the planning meeting.") + "</section>"

body = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{E(C.TITLE)} – Leadership Business Plan</title><style>{css}</style></head>
<body>{toc_html}{''.join(sec)}</body></html>"""
(BUILD / "body.html").write_text(body, encoding="utf-8")

cover = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: A4; margin: 0; }} html{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body {{ margin:0; font-family:'Noto Sans'; }}
.c {{ width:210mm; height:297mm; background:{MAROON}; color:#fff; position:relative; overflow:hidden; }}
.band {{ position:absolute; left:0; right:0; top:205mm; height:2.2mm; background:{GOLD}; }}
.k {{ position:absolute; left:20mm; top:38mm; font-size:11pt; letter-spacing:.14em; color:#E9C46A; font-weight:700; }}
.t {{ position:absolute; left:20mm; top:52mm; right:20mm; font-family:'Noto Serif'; font-size:34pt; line-height:1.15; font-weight:700; }}
.s {{ position:absolute; left:20mm; top:118mm; right:24mm; font-size:14pt; color:#F6E7D3; line-height:1.45; }}
.m {{ position:absolute; left:20mm; top:218mm; right:20mm; font-size:10.5pt; color:#F6E7D3; line-height:1.8; }}
.m b {{ color:#fff; }}
.conf {{ position:absolute; left:20mm; bottom:16mm; font-size:8.5pt; color:#E0C7B0; letter-spacing:.08em; }}
.orn {{ position:absolute; right:-30mm; top:120mm; width:120mm; height:120mm; border-radius:50%; border:1.2mm solid rgba(233,196,106,.25); }}
.orn2 {{ position:absolute; right:-10mm; top:140mm; width:80mm; height:80mm; border-radius:50%; border:1mm solid rgba(233,196,106,.18); }}
</style></head><body><div class="c"><div class="orn"></div><div class="orn2"></div>
<div class="k">HARE KRISHNA GOLDEN TEMPLE (ISKCON) · HYDERABAD</div>
<div class="t">Prasadam, Sweets &amp; Savories<br>A New Revenue Vertical</div>
<div class="s">Business plan and roadmap for temple leadership and top management<br><span style="font-size:11pt;color:#E9C46A">From the house of Radha Krishna: satvik, pure, no preservatives</span></div>
<div class="band"></div>
<div class="m"><b>Prepared for:</b> Temple leadership and top management<br><b>Prepared by:</b> Mukunda Dasa, with DMTT and the production team<br><b>Based on:</b> {E(C.SOURCE_MEETING)}, plus market research<br><b>Version:</b> 1.1 · 13 October 2026</div>
<div class="conf">CONFIDENTIAL · FOR INTERNAL DECISION-MAKING · FIGURES MARKED [ESTIMATE] ARE PLANNING ASSUMPTIONS</div>
</div></body></html>"""
(BUILD / "cover.html").write_text(cover, encoding="utf-8")
print("html written", BUILD)

# --------------------------------------------------------------------------- render + merge
if __name__ == "__main__":
    import os
    import subprocess

    import pymupdf

    subprocess.run(["node", str(Path(__file__).with_name("render_pdf.mjs"))], check=True, env=os.environ)
    doc = pymupdf.open()
    for part in ("cover.pdf", "body.pdf"):
        doc.insert_pdf(pymupdf.open(BUILD / part))
    doc.set_metadata({"title": f"{C.TITLE} – Leadership Business Plan", "author": "Mukunda Dasa, DMTT – Hare Krishna Golden Temple, Hyderabad",
                      "subject": "Business plan, roadmap and decisions for temple leadership"})
    toc = [[1, "Cover", 1]]
    body = pymupdf.open(BUILD / "body.pdf")
    for i, pg in enumerate(body):
        txt = pg.get_text()
        for n, t in TOC:
            lines = [ln.strip() for ln in txt.splitlines()]
            if "contd" not in n and t in lines and not any(e[1].endswith(t) for e in toc) and i > 0:
                toc.append([1, f"{n.replace('Section ', '')}. {t}" if n.startswith("Section") else f"{n}: {t}", i + 2])
    doc.set_toc(toc)
    out = ROOT / "00_Leadership_Business_Plan.pdf"
    doc.save(out, garbage=3, deflate=True)
    print(out, doc.page_count, "pages")
