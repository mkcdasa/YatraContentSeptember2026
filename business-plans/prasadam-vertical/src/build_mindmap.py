"""Builds 03_Mind_Map.html (interactive, self-contained) and 06_Mind_Map_and_Flowcharts.md (Mermaid)."""
import html
import json
from pathlib import Path

import content as C

ROOT = Path(__file__).resolve().parent.parent


def n(label, children=None, color=None):
    d = {"t": label}
    if children:
        d["c"] = [x if isinstance(x, dict) else {"t": x} for x in children]
    if color:
        d["k"] = color
    return d


circles = {}
for a in C.AUDIENCES:
    circles.setdefault(a["circle"], []).append(n(a["name"], [
        f"Who: {a['who']}", f"Needs: {a['needs']}", f"Offer: {a['offer']}", f"Channel: {a['channel']}", f"Price: {a['price']}"]))

prod_groups = {}
for p in C.PRODUCTS:
    prod_groups.setdefault(p[1].split(" –")[0], []).append(n(p[0], [f"Shelf life {p[2]} days", f"Tier: {p[3]}", f"Sweetener: {p[4]}", f"Packs: {p[5]}", p[6]]))

TREE = n("Prasadam, Sweets & Savories Vertical", [
    n("Vision & why now", [n("Vision", [C.VISION]), n("Mission", [C.MISSION]), n("One-line pitch", [C.ONE_LINE_PITCH])] +
      [n(t, pts) for t, pts in C.MEETING_INSIGHTS[:1]], "maroon"),
    n("Meeting insights (everything said)", [n(t, pts) for t, pts in C.MEETING_INSIGHTS], "maroon"),
    n("Market research", [n(a, [b, f"Source: {c}"]) for a, b, c, _ in C.MARKET_FACTS] +
      [n("Competitors", [n(c[0], [c[1], f"Tier: {c[2]}", f"Our edge: {c[3]}"]) for c in C.COMPETITORS]),
       n("SWOT", [n(k, v) for k, v in C.SWOT.items()])], "blue"),
    n("Target audiences (5 circles)", [n(k, v) for k, v in circles.items()], "saffron"),
    n("Revenue streams (14)", [n(f"{s['id']} {s['name']}", [f"What: {s['what']}", f"Why: {s['why']}", f"How: {s['how']}",
                                                              f"Phase: {s['phase']} · Capex: {s['capex']} · Margin: {s['margin']}", f"KPIs: {s['kpi']}"]) for s in C.STREAMS], "saffron"),
    n("New business ideas", [n(a, [b]) for a, b in C.BUSINESS_IDEAS], "gold"),
    n("Products", [n(k, v) for k, v in prod_groups.items()], "gold"),
    n("Gift boxes & packaging", [n("Gift tiers", [n(f"{t[0]} ({t[1]})", [t[2], f"Best for: {t[3]}"]) for t in C.GIFT_TIERS]), n("Packaging", C.PACKAGING)], "gold"),
    n("Pricing", [n(p[0], [p[1], f"Used for: {p[2]}"]) for p in C.PRICING], "green"),
    n("Marketing & sales", [n(m[0], [m[1]]) for m in C.MARKETING] + [n("Funnel", [f"{a}: {b}" for a, b in C.MARKETING_FUNNEL])], "blue"),
    n("Operations", [n(o[0], [o[1]]) for o in C.OPERATIONS], "green"),
    n("Team & roles", [n(r[0], [r[1], r[2]]) for r in C.ORG_ROLES], "green"),
    n("Roadmap", [n(f"{p['name']} · {p['window']}", [f"Goal: {p['goal']}"] + p["items"]) for p in C.PHASES], "maroon"),
    n("Hero campaign calendar", [n(f"{f[0]} · {f[1]}", [f[2], f"Demand: {f[3]}"]) for f in C.FESTIVALS], "maroon"),
    n("Financials [estimate]", [n(f"{r[0]}: Y1 ₹{r[1]} L", [r[5], f"Gross margin {r[4]}%"]) for r in C.REVENUE_Y1] +
      [n("Year-1 opex", [f"{o[0]}: ₹{o[1]} L ({o[2]})" for o in C.OPEX_Y1]), n("Capex (staged)", [f"{c[0]}: {c[1]} ({c[2]})" for c in C.CAPEX])], "blue"),
    n("Risks", [n(f"{r[0]} {r[1]} (score {r[2] * r[3]})", [f"Mitigation: {r[4]}", f"Owner: {r[5]}"]) for r in C.RISKS], "grey"),
    n("KPIs & ROI (DMTT)", [n(k[0], [k[1], f"{k[3]} · {k[2]}"]) for k in C.KPIS], "grey"),
    n("Governance", [n(g[0], [g[1], f"Chair: {g[2]}"]) for g in C.GOVERNANCE], "grey"),
    n("Action items", [n(f"{a[0]} {a[1]}", [f"Owner: {a[2]}", f"Due: {a[3]}"]) for a in C.ACTION_ITEMS], "saffron"),
    n("Open questions", C.OPEN_QUESTIONS, "saffron"),
])

MERMAID_ORDER = """flowchart TD
  A[Order comes in] --> B{Channel?}
  B -->|Internal dept| C[Weekly standing order<br/>fixed delivery day]
  B -->|Corporate / white-label| D[Quote + 50% advance<br/>sticker proof approved]
  B -->|Online store / Amazon| E[Shopify / Amazon order]
  B -->|Festival stall| F[Pre-packed combos<br/>UPI at counter]
  C --> G[Order system<br/>tag stream + campaign]
  D --> G
  E --> G
  F --> G
  G --> H[Production plan<br/>weekly + festival calendar]
  H --> I[Cook in temple kitchen]
  I --> J[QC + shelf-life check]
  J --> K[Pack + label<br/>MFD, best-before, FSSAI]
  K --> L{Delivery}
  L -->|Hyderabad B2B| M[Own vehicle]
  L -->|Pan-India| N[Courier aggregator / Amazon]
  L -->|On campus| O[Stall / restaurant]
  M --> P[Payment + feedback]
  N --> P
  O --> P
  P --> Q[DMTT ROI dashboard]"""

MERMAID_CORP = """flowchart TD
  A[Build target list<br/>chamber, BNI, Rotary, T-Hub, MNR, donors] --> B[Rank by staff size]
  B --> C[Warm intro by Mukunda Dasa]
  C --> D[Owner / HR meeting<br/>sample box + catalogue + price list]
  D --> E{Own brand or white-label?}
  E -->|Own brand| F[Pick tier: Seva / Utsav / Vaikuntha]
  E -->|White-label| G[Logo mock-up within 48 h]
  F --> H[Quote with volume slab + delivery date]
  G --> H
  H --> I{PO + 50% advance?}
  I -->|No| J[Follow up; next festival reminder]
  I -->|Yes| K[Lock production slot]
  K --> L[Produce, pack, sticker]
  L --> M[Dispatch before cut-off]
  M --> N[Collect balance; feedback call]
  N --> O[Add to festival calendar for repeat]"""

MERMAID_FESTIVAL = """flowchart TD
  A[Festival on calendar] --> B[Forecast from last year + pre-orders]
  B --> C[Book seasonal staff + raw material]
  C --> D[Produce shelf-stable stock early]
  D --> E[Map footfall: entrance, exit queue,<br/>Goshala path, stairs, garden, waterfall]
  E --> F[Set up row of stalls / pagodas<br/>+ lawn food court]
  F --> G[Sell: combos + UPI + hourly restock]
  G --> H{Stock left?}
  H -->|Yes| I[Sell online / Instagram within 48 h]
  H -->|No| J[Record stock-out time for next year]
  I --> K[Post-festival review: sales, margin, hours]
  J --> K"""

MERMAID_DECISION = """flowchart TD
  A[Plan sent by Mukunda Dasa] --> B[Production lead reviews with his manager]
  B --> C[Decision meeting: Mukunda Dasa + production lead + manager]
  C --> D{Approved?}
  D -->|Changes| A
  D -->|Yes| E[Foundation sprint: data, samples, pricing, sales kit, hire]
  E --> F[Pilot: Dasara + Diwali]
  F --> G{Pilot ROI positive?}
  G -->|No| H[Fix pricing / capacity / channels]
  H --> F
  G -->|Yes| I[Phase 2: e-commerce, communities, catering]
  I --> J[Phase 3: pagodas, pickles, 10x Janmashtami]
  J --> K{Demand proven?}
  K -->|Yes| L[Phase 4: dedicated unit + QSR pilot]
  L --> M[Phase 5: national + export]"""

MERMAID_ROI = """flowchart LR
  A[Every order tagged<br/>stream R1-R14 + campaign] --> D[Monthly P&L by stream]
  B[Costs: ingredients, packaging,<br/>labour, marketing, overheads] --> D
  C[Weekly hours log<br/>DMTT, production, sales] --> D
  D --> E[ROI % = contribution / total cost]
  E --> F[One-page report to leadership]"""

OVERVIEW = [
    ("Audiences", ["Visitors & festivals", "Donors", "Internal depts", "Companies & institutions", "Communities", "Online & NRI"]),
    ("Revenue streams", ["Stalls & restaurant", "Corporate gifting", "White-label", "E-commerce", "Catering", "QSR & export"]),
    ("Products", ["Chikkis & laddus", "Kaja & khara", "Namkeen", "Puri unde", "Pickles & powders", "Gift boxes"]),
    ("Pricing", ["Mass tier", "Premium tier", "Internal price", "B2B volume slabs"]),
    ("Marketing", ["ISKCON brand", "Databases & AI", "WhatsApp & SMS", "Google & Meta ads", "Owner meetings"]),
    ("Operations", ["Kitchen + 1 hire", "Recipes & costing", "Shelf-life tests", "Dispatch", "FSSAI & GST"]),
    ("Roadmap", ["0 Foundation", "1 Dasara-Diwali pilot", "2 Launch channels", "3 Scale Hyderabad", "4 Unit & QSR", "5 National & export"]),
    ("Governance", ["DMTT ROI", "Weekly review", "Risk register", "KPIs"]),
]
MERMAID_MINDMAP = "mindmap\n  root((Prasadam Vertical))\n" + "\n".join(
    f"    {b}\n" + "\n".join(f"      {c}" for c in cs) for b, cs in OVERVIEW)

FLOWS = [("Order-to-delivery flow (all channels)", MERMAID_ORDER), ("Corporate gifting sales flow", MERMAID_CORP),
         ("Festival stall operations", MERMAID_FESTIVAL), ("Decision and phase-gate flow", MERMAID_DECISION),
         ("DMTT ROI tracking flow", MERMAID_ROI)]

DIAG = ROOT / "diagrams"
DIAG.mkdir(exist_ok=True)
SLUGS = ["mind_map"] + ["order_flow", "corporate_gifting_flow", "festival_stall_flow", "phase_gate_flow", "roi_tracking_flow"]
for slug, code in zip(SLUGS, [MERMAID_MINDMAP] + [c for _, c in FLOWS]):
    (DIAG / f"{slug}.mmd").write_text(code, encoding="utf-8")


def svg_for(slug):
    """The pre-rendered diagram as an embedded PNG (renders offline and in print)."""
    import base64
    f = DIAG / f"{slug}.png"
    if not f.exists():
        return None
    return f'<img alt="{slug.replace("_", " ")}" style="max-width:100%;height:auto" src="data:image/png;base64,{base64.b64encode(f.read_bytes()).decode()}">'


# ---------------------------------------------------------------------------
md = [f"# {C.TITLE}: Mind Map & Flowcharts", "",
      f"{C.ORG} · {C.VERSION}", "",
      "GitHub renders these Mermaid diagrams. The fully detailed, clickable mind map is `03_Mind_Map.html` (open it in any browser).", "",
      "## Mind map (overview)", "", "```mermaid", MERMAID_MINDMAP, "```", ""]
for title, code in FLOWS:
    md += [f"## {title}", "", "```mermaid", code, "```", ""]
md += ["## Roadmap timeline", "", "```mermaid", "timeline", "  title Prasadam vertical roadmap"]
for p in C.PHASES:
    md.append(f"  {p['window'].split(' (')[0]} : {p['name'].split('– ')[1]} : {p['goal']}")
md += ["```", ""]
(ROOT / "06_Mind_Map_and_Flowcharts.md").write_text("\n".join(md), encoding="utf-8")

# ---------------------------------------------------------------------------
flows_html = "\n".join(
    f'<section class="flow"><h3>{html.escape(t)}</h3>' + (f'<div class="svg">{svg_for(slug)}</div>' if svg_for(slug) else f'<pre>{html.escape(c)}</pre>') + '</section>'
    for slug, (t, c) in zip(SLUGS[1:], FLOWS))
overview = svg_for("mind_map")
overview_html = f'<h2>Overview</h2><div class="flow svg">{overview}</div>' if overview else ""
page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Prasadam Vertical Mind Map</title>
<style>
:root{--bg:#fff8ec;--card:#fff;--ink:#2b221e;--muted:#6b5e55;--line:#e3d3bb;--maroon:#7a1f2b;--saffron:#d06f00;--gold:#a8841a;--green:#2e7d32;--blue:#1f5f8b;--grey:#6b5e55}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#1d1714;--card:#2a211d;--ink:#f3e9dc;--muted:#bba99a;--line:#4a3b32;--maroon:#e0788a;--saffron:#f0a040;--gold:#e0c060;--green:#7cc47f;--blue:#7fb6e0;--grey:#bba99a}}
:root[data-theme="dark"]{--bg:#1d1714;--card:#2a211d;--ink:#f3e9dc;--muted:#bba99a;--line:#4a3b32;--maroon:#e0788a;--saffron:#f0a040;--gold:#e0c060;--green:#7cc47f;--blue:#7fb6e0;--grey:#bba99a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
header{padding:24px 16px 8px;max-width:1200px;margin:auto}h1{margin:0;color:var(--maroon);font-size:clamp(22px,4vw,32px)}
.sub{color:var(--muted);margin:4px 0 12px}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;max-width:1200px;margin:auto;padding:0 16px 12px}
button,input{font:inherit;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:8px;padding:6px 12px}
button{cursor:pointer}input{flex:1;min-width:180px}
main{max-width:1200px;margin:auto;padding:0 16px 32px}
.root{display:inline-block;background:var(--maroon);color:#fff;padding:10px 18px;border-radius:14px;font-weight:700;font-size:18px;margin-bottom:8px}
ul.tree{list-style:none;margin:0;padding-left:22px;border-left:2px solid var(--line)}
ul.tree li{position:relative;margin:4px 0;padding-left:14px}
ul.tree li::before{content:"";position:absolute;left:-2px;top:14px;width:14px;border-top:2px solid var(--line)}
.node{display:inline-flex;gap:6px;align-items:flex-start;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:4px 10px;max-width:100%}
.node.has{cursor:pointer;font-weight:600}.node.has::before{content:"+";color:var(--muted);font-weight:700;width:10px}
li.open>.node.has::before{content:"–"}
li>ul{display:none}li.open>ul{display:block}
.l1>.node{border-left:6px solid var(--k);font-size:16px}
.hit>.node{outline:2px solid var(--saffron)}
.flows{display:grid;gap:16px;margin-top:24px}.flow{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px;overflow-x:auto}
.flow h3{margin:0 0 8px;color:var(--maroon)}
h2{color:var(--maroon);margin-top:32px}.svg svg{max-width:100%;height:auto;background:#fff;border-radius:8px}
</style></head><body>
<header><h1>Prasadam, Sweets &amp; Savories Vertical</h1>
<p class="sub">Mind map of the full business plan · __ORG__ · __VER__. Click any node to expand; use search to find a detail.</p></header>
<div class="bar"><button id="ex">Expand all</button><button id="co">Collapse all</button><button id="l1">Main branches</button>
<input id="q" type="search" placeholder="Search (e.g. chikki, Diwali, ROI, MNR)"><button id="th">Theme</button></div>
<main><div class="root">Prasadam Vertical</div><div id="tree"></div>
__OVERVIEW__<h2>Flowcharts</h2><div class="flows">__FLOWS__</div></main>
<script>
const DATA=__DATA__;
const colors={maroon:'var(--maroon)',saffron:'var(--saffron)',gold:'var(--gold)',green:'var(--green)',blue:'var(--blue)',grey:'var(--grey)'};
function build(nodes,depth){const ul=document.createElement('ul');ul.className='tree';
 for(const d of nodes){const li=document.createElement('li');if(depth===1){li.className='l1';li.style.setProperty('--k',colors[d.k]||'var(--maroon)')}
  const s=document.createElement('span');s.className='node'+(d.c?' has':'');s.textContent=d.t;li.appendChild(s);
  if(d.c){li.appendChild(build(d.c,depth+1));s.addEventListener('click',()=>li.classList.toggle('open'))}
  ul.appendChild(li)}return ul}
const tree=document.getElementById('tree');tree.appendChild(build(DATA.c,1));
const all=()=>tree.querySelectorAll('li');
document.getElementById('ex').onclick=()=>all().forEach(l=>l.classList.add('open'));
document.getElementById('co').onclick=()=>all().forEach(l=>l.classList.remove('open'));
document.getElementById('l1').onclick=()=>all().forEach(l=>l.classList.toggle('open',false));
document.getElementById('q').addEventListener('input',e=>{const q=e.target.value.trim().toLowerCase();
 all().forEach(l=>{l.classList.remove('hit');if(!q)return;});if(!q)return;
 all().forEach(l=>l.classList.remove('open'));
 all().forEach(l=>{const t=l.firstChild.textContent.toLowerCase();if(t.includes(q)){l.classList.add('hit');let p=l.parentElement.closest('li');while(p){p.classList.add('open');p=p.parentElement.closest('li')}}})});
document.getElementById('th').onclick=()=>{const r=document.documentElement;const dark=r.dataset.theme?r.dataset.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;r.dataset.theme=dark?'light':'dark';try{localStorage.setItem('theme',r.dataset.theme)}catch(e){}};
try{const t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t}catch(e){}
all().forEach(l=>{if(l.classList.contains('l1'))l.classList.add('open')});
</script>
</body></html>"""
page = (page.replace("__DATA__", json.dumps(TREE, ensure_ascii=False)).replace("__FLOWS__", flows_html).replace("__OVERVIEW__", overview_html)
        .replace("__ORG__", html.escape(C.ORG)).replace("__VER__", html.escape(C.VERSION)))
(ROOT / "03_Mind_Map.html").write_text(page, encoding="utf-8")
print("mind map + flowcharts written")
