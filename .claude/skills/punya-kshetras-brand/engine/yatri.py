# Yatri itinerary (A4, flowing): places and activities only, no timings; meal plan with restaurants and map links.
# Usage (cwd = <workdir>/build): python3 yatri.py <package.py>
import json, sys, html, os
from urllib.parse import quote_plus
from common import *
PK=load_pkg(sys.argv[1] if len(sys.argv)>1 else None)
IMG=load_img(PK)
def m(q): return q if q.startswith("http") else "https://www.google.com/maps/search/?api=1&query="+quote_plus(q)

def meals_table(pk):
    rows=load_rows(pk)
    R=json.load(open(pk["restaurants_path"])) if os.path.exists(pk["restaurants_path"]) else {}
    out=[]; days=sorted(set(r[0] for r in rows))
    for d in days:
        cells=[]
        for meal in ("Breakfast","Lunch","Dinner"):
            r=[x for x in rows if x[0]==d and x[3]==meal]
            if not r: cells.append('<td class="na">—</td>'); continue
            place=r[0][4]; info=R.get(place)
            if info:
                opts="".join(f'<div><a href="{o["map"]}">{PIN}{E(o["name"])}</a><small>{E(o["note"])}</small></div>' for o in info)
            else:
                opts=f'<div><a href="{r[0][8]}">{PIN}{E(place)}</a></div>'
            extra=" · Ekadashi prasadam" if "Ekadashi" in r[0][7] and "parana" not in r[0][7] else (" · Ekadashi parana" if "parana" in r[0][7] else "")
            cells.append(f'<td>{opts}{f"<em>{E(extra[3:])}</em>" if extra else ""}</td>')
        out.append(f'<tr><th>Day {d}</th>{"".join(cells)}</tr>')
    return "".join(out)

CSS="""@import url('fonts/local.css');
:root{--plum:#3A1452;--plum2:#5B1F7E;--plum3:#2A0D3D;--coral:#E8445A;--orange:#F28C28;--gold:#E7B24A;--gold2:#F6D58B;--cream:#FFF7EA;--ink:#2A2131;--muted:#6E6077;--line:#EADFCB}
@page{size:A4;margin:14mm 13mm 16mm}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Poppins,sans-serif;color:var(--ink);font-size:9.6pt;background:#fff;-webkit-print-color-adjust:exact;print-color-adjust:exact}
a{color:inherit;text-decoration:none}
.top{background:linear-gradient(135deg,var(--plum3),var(--plum2));color:#fff;border-radius:5mm;overflow:hidden;position:relative;padding:7mm 8mm 7mm}
.top .bg{position:absolute;inset:0;opacity:.28}.top .bg img{width:100%;height:100%;object-fit:cover}
.top>*{position:relative}
.logos{display:flex;justify-content:space-between;align-items:center}
.logos div{background:#fff;border-radius:3mm;padding:1.5mm 3mm}.logos img{height:13mm;display:block}
.kick{display:inline-flex;align-items:center;gap:2.5mm;margin-top:5mm;font-family:Montserrat;font-weight:800;font-size:9.5pt;letter-spacing:.7mm;text-transform:uppercase;background:linear-gradient(90deg,var(--coral),var(--orange));border-radius:10mm;padding:1.6mm 4.5mm}
.kick .hico{width:8.5mm;height:5.3mm;fill:#fff}
h1{font-family:'Playfair Display';font-size:28pt;line-height:1.05;margin-top:3mm}
h1 span{display:block;font-family:'Great Vibes';font-weight:400;color:var(--gold2);font-size:30pt;margin-top:-1mm}
.meta{margin-top:3mm;display:flex;flex-wrap:wrap;gap:2mm 3mm;font-family:Montserrat;font-weight:700;font-size:9pt}
.meta span{background:rgba(255,255,255,.14);border:.3mm solid rgba(246,213,139,.6);border-radius:8mm;padding:1mm 3.5mm}
.route{font-family:'Playfair Display';color:var(--gold2);font-size:11pt;margin-top:2.5mm}
h2{font-family:'Playfair Display';color:var(--plum);font-size:17pt;margin:6mm 0 3mm}
h2 i{font-family:'Great Vibes';font-style:normal;color:var(--coral);font-size:21pt;margin-left:2mm}
.spec{display:grid;grid-template-columns:1fr 1fr;gap:2.6mm}
.spec div{background:var(--cream);border-radius:3mm;padding:2.6mm 3.4mm;border-left:1.2mm solid var(--gold)}
.spec div:nth-child(-n+2){border-left-color:var(--coral);background:#fff3f0}
.spec b{display:block;font-family:Montserrat;font-size:9pt;color:var(--plum)}
.spec span{font-size:8.6pt;line-height:1.4}
.memo{margin-top:3mm;text-align:center;font-family:'Playfair Display';font-style:italic;color:var(--plum2);font-size:11pt}
.day{background:var(--cream);border-radius:4mm;padding:4mm 5mm;margin-bottom:4mm;break-inside:avoid;box-shadow:0 .6mm 2mm rgba(58,20,82,.08)}
.dh{display:flex;align-items:center;gap:3mm;margin-bottom:2.5mm}
.dn{background:linear-gradient(135deg,var(--coral),var(--orange));color:#fff;font-family:Montserrat;font-weight:800;border-radius:2.5mm;padding:1.6mm 3mm;font-size:9pt;white-space:nowrap}
.dh h3{font-family:'Playfair Display';color:var(--plum);font-size:13pt;line-height:1.15;flex:1}
.st{background:var(--plum);color:#fff;border-radius:8mm;padding:1mm 3.5mm;font-family:Montserrat;font-size:7.6pt;font-weight:600;white-space:nowrap}.st b{color:var(--gold2)}
.pl{list-style:none}
.pl li{display:grid;grid-template-columns:52mm 1fr;gap:3mm;padding:1.4mm 0;border-bottom:.25mm dashed var(--line)}
.pl li:last-child{border-bottom:0}
.pl a{font-family:Montserrat;font-weight:700;color:var(--plum);font-size:8.8pt;display:flex;gap:1.2mm;align-items:flex-start}
.pin{width:3.6mm;height:3.6mm;fill:var(--coral);flex:none;margin-top:.4mm}
.pl a u{text-decoration:none;font-weight:600;color:var(--coral);font-size:7pt;margin-left:1mm}
.pl span{font-size:8.8pt;line-height:1.4}
.acts{margin-top:2mm;display:flex;flex-wrap:wrap;gap:1.6mm}
.acts span{background:#f6effb;color:var(--plum2);border-radius:6mm;padding:.9mm 3mm;font-size:7.9pt;font-weight:500}
.acts span:before{content:"♪ ";color:var(--coral)}
.pb{break-before:page}
table.meals{width:100%;border-collapse:separate;border-spacing:0;background:var(--cream);border-radius:3mm;overflow:hidden;font-size:8.2pt}
table.meals th,table.meals td{padding:2mm 2.4mm;vertical-align:top;border-bottom:.25mm solid var(--line);text-align:left}
table.meals thead th{background:var(--plum);color:#fff;font-family:Montserrat;font-size:8.4pt}
table.meals tbody th{font-family:Montserrat;color:var(--plum);white-space:nowrap;width:15mm}
table.meals tr{break-inside:avoid}
table.meals td div{margin-bottom:1.2mm}
table.meals a{font-weight:600;color:var(--plum);display:flex;gap:1mm;align-items:flex-start}
table.meals small{display:block;color:var(--muted);font-size:7.2pt;margin-left:4.6mm;line-height:1.3}
table.meals em{display:block;color:var(--coral);font-style:normal;font-size:7.4pt;font-weight:600}
.note{font-size:8pt;color:var(--muted);margin-top:2.5mm;line-height:1.45}
.foot{margin-top:6mm;background:linear-gradient(135deg,var(--plum3),var(--plum2));color:#fff;border-radius:4mm;padding:5mm 6mm;text-align:center;break-inside:avoid}
.foot .ph{font-family:Montserrat;font-weight:800;font-size:20pt;color:var(--gold2)}
.foot .s{font-family:'Great Vibes';font-size:22pt;color:var(--gold2)}
"""
def build(pk):
    it=pk["itinerary"]; hero=it["hero"]
    days="".join(f'''<div class="day"><div class="dh"><span class="dn">DAY {i+1}</span><h3>{E(d["title"])}</h3>{f'<span class="st">Overnight: <b>{E(d["stay"])}</b></span>' if d["stay"] else ""}</div>
<ul class="pl">{"".join(f'<li><a href="{m(q)}">{PIN}<span>{E(p)}<u>Map ↗</u></span></a><span>{E(w)}</span></li>' for p,q,w in d["places"])}</ul>
<div class="acts">{"".join(f"<span>{E(a)}</span>" for a in d["acts"])}</div></div>''' for i,d in enumerate(it["days"]))
    spec="".join(f"<div><b>{E(a)}</b><span>{E(b)}</span></div>" for a,b in it["special"]+SPECIAL)
    return f'''<!doctype html><html><head><meta charset="utf-8"><title>{E(pk["title"])} {E(pk["title2"])} – Yatri Itinerary</title><style>{CSS}</style></head><body>
<div class="top"><div class="bg"><img src="{IMG[hero]["src"]}"></div>
<div class="logos"><div><img src="brand/hkgt_logo.png"></div><div><img src="brand/pk_logo.png"></div></div>
<div class="kick">{HELI if pk["show_heli_icon"] else ""}{E(it["kicker"])}</div>
<h1>{E(pk["title"])}<span>{E(pk["title2"])}</span></h1>
<div class="meta"><span>{E(pk["dates"])}</span><span>{E(pk["duration"])}</span><span>{E(WITH_LINE)}</span></div>
<div class="route">{E(pk["tagline"])}</div></div>
<h2>A spiritually enriching<i>yatra</i></h2>
<div class="spec">{spec}</div>
<div class="memo">{E(it["memo"])}</div>
<h2>Day by day<i>itinerary</i></h2>
{days}
<h2 class="pb">Meal plan<i>pure vegetarian</i></h2>
<table class="meals"><thead><tr><th></th><th>Breakfast</th><th>Lunch</th><th>Dinner</th></tr></thead><tbody>{meals_table(pk)}</tbody></table>
<p class="note">{E(it["meal_note"])}</p>
<div class="foot"><div>For any help during the yatra, call</div><div class="ph">{CONTACT["phone"]}</div><div>{CONTACT["web1"]} · {CONTACT["web2"]}</div><div class="s">{E(it["footer_closing"])}</div></div>
</body></html>'''
if __name__=="__main__":
    open("itinerary.html","w").write(build(PK)); print("wrote itinerary.html")
