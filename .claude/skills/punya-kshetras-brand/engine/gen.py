# Brochure (A4, multi-page) generator. Usage (cwd = <workdir>/build): python3 gen.py <package.py>
import json, sys, html, os, datetime
from common import *
PK=load_pkg(sys.argv[1] if len(sys.argv)>1 else None)
IMG=load_img(PK)  # key -> {"src":..., "credit":..., "cap":...}
def img(k,cls="ph",style=""):
    i=IMG[k]; return f'<img class="{cls}" style="{style}" src="{i["src"]}">'
def photo(k,h,cap=None,radius="3mm"):
    i=IMG[k]
    c=f'<div class="cap">{E(cap)}</div>' if cap else ""
    return f'<div class="phbox" style="height:{h};border-radius:{radius}">{img(k)}{c}</div>'
def mins(a,b):
    h1,m1=map(int,a.split(':'));h2,m2=map(int,b.split(':'));return h2*60+m2-h1*60-m1
CSS_EXTRA="""
.phbox{position:relative;overflow:hidden;box-shadow:0 1mm 3mm rgba(0,0,0,.18)}
.phbox .cap{position:absolute;left:0;right:0;bottom:0;padding:5mm 3mm 2mm;color:#fff;font-family:Montserrat;font-weight:700;font-size:8.5pt;background:linear-gradient(transparent,rgba(30,8,45,.85))}
.phbox .cap small{display:block;font-weight:400;font-size:7pt;opacity:.9}
.daybadge{display:inline-flex;align-items:center;gap:3mm}
.daybadge .n{background:linear-gradient(135deg,var(--coral),var(--orange));color:#fff;font-family:Montserrat;font-weight:800;border-radius:3mm;padding:2mm 3.5mm;font-size:10pt;letter-spacing:.4mm}
.daybadge h2{font-size:17pt;color:var(--plum)}
.stay{display:inline-block;margin-left:auto;background:var(--plum);color:#fff;border-radius:10mm;padding:1.3mm 4mm;font-family:Montserrat;font-size:8pt;font-weight:600}
.stay b{color:var(--gold2)}
.sig{border-left:1.2mm solid var(--gold);background:#fff;border-radius:0 3mm 3mm 0;padding:2.6mm 4mm;margin:3mm 0}
.sig h4{font-family:Montserrat;font-size:8.3pt;color:var(--coral);text-transform:uppercase;letter-spacing:.4mm;margin-bottom:1mm}
.sig p{font-size:8.8pt;line-height:1.45}
.stat{background:#fff;border-radius:4mm;text-align:center;padding:4mm 2mm;box-shadow:0 1mm 3mm rgba(58,20,82,.1)}
.stat b{display:block;font-family:'Playfair Display';font-size:24pt;color:var(--coral);line-height:1}
.stat span{font-family:Montserrat;font-size:7.6pt;font-weight:600;color:var(--plum);text-transform:uppercase;letter-spacing:.3mm}
h3.sub{font-family:Montserrat;font-size:10pt;color:var(--plum);text-transform:uppercase;letter-spacing:.5mm;margin-bottom:2.5mm}
.qbox{background:linear-gradient(135deg,var(--plum3),var(--plum2));color:#fff;border-radius:4mm;padding:6mm 7mm;position:relative}
.qbox p{font-family:'Playfair Display';font-style:italic;font-size:11pt;line-height:1.55}
.qbox .src{font-family:Montserrat;font-style:normal;font-size:8pt;color:var(--gold2);margin-top:2mm;text-align:right}
.qbox:before{content:"\\201C";position:absolute;left:3mm;top:-4mm;font-family:'Playfair Display';font-size:48pt;color:var(--gold)}
"""
def chrome(pk,title,sub,n,total):
    return (f'<div class="hdr"><div class="logo"><img src="brand/hkgt_logo.png"></div>'
            f'<div class="ttl">{E(title)}<small>{E(sub)}</small></div>'
            f'<div class="logo"><img src="brand/pk_logo.png"></div></div>'
            f'<div class="ftr"><span><b>Punya Kshetras</b> by Hare Krishna Golden Temple · {E(pk["title"])} {E(pk["title2"])}</span>'
            f'<span>Call <b>{CONTACT["phone"]}</b> · {CONTACT["web1"]}</span><span>{n} / {total}</span></div>')

def cover(pk):
    circles="".join(f'<div class="circ" style="{pos}">{img(k)}</div>' for k,pos in pk["cover_circles"])
    return f'''<div class="page cover">
<div class="cv-bg">{img(pk["hero"],"ph",f"object-position:{pk.get('hero_pos','50% 50%')}")}</div><div class="cv-shade"></div>
<div class="cv-top"><div class="logo"><img src="brand/hkgt_logo.png"></div><img class="seal" src="brand/seal.png"><div class="logo"><img src="brand/pk_logo.png"></div></div>
<div class="cv-title"><div class="kick mont">{HELI if pk["show_heli_icon"] else ""}{E(pk["kicker"])}</div>
<h1>{E(pk["title"])}</h1><div class="script t2">{E(pk["title2"])}</div>
<div class="pill with">{E(WITH_LINE)}</div></div>
{circles}
<div class="cv-band"><div class="dates mont">{E(pk["dates"])}</div><div class="dur mont">{E(pk["duration"])}</div><div class="route">{E(pk["tagline"])}</div>
{f'<div class="regclose mont">{E(pk["cover_note"])}</div>' if pk["cover_note"] else ""}
<div class="cv-feats">{"".join(f"<span>{E(x)}</span>" for x in pk["cover_feats"])}</div></div>
<div class="cv-foot"><span class="book mont" style="white-space:nowrap">{E(CTA)}</span><span class="ph mont" style="display:flex;align-items:center">{PHONE_SVG.format(w="18pt",c="#3A1452",s="vertical-align:-0.12em;margin-right:2mm")}{CONTACT["phone"]}</span><span class="web">{CONTACT["web1"]}<br>{CONTACT["web2"]}</span></div>
</div>'''
COVER_CSS="""
.cover{background:var(--plum3)}
.cv-bg{position:absolute;inset:0}
.cv-shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(42,13,61,.55) 0%,rgba(42,13,61,.05) 30%,rgba(42,13,61,.15) 52%,rgba(42,13,61,.92) 74%,var(--plum3) 86%)}
.cv-top{position:absolute;top:9mm;left:10mm;right:10mm;display:flex;justify-content:space-between;align-items:center}
.cv-top .logo{background:#fff;border-radius:4mm;padding:2mm 3.5mm;box-shadow:0 1mm 4mm rgba(0,0,0,.3)}
.cv-top .logo img{height:16mm;display:block}
.cv-top .seal{height:22mm;border-radius:50%;box-shadow:0 0 0 1mm #fff,0 1mm 4mm rgba(0,0,0,.4)}
.cv-title{position:absolute;top:38mm;left:0;right:0;text-align:center;color:#fff;text-shadow:0 1mm 4mm rgba(0,0,0,.55)}
.cv-title .kick{display:inline-flex;align-items:center;gap:2.5mm;font-size:10pt;letter-spacing:.8mm;text-transform:uppercase;color:#fff;font-weight:800;background:linear-gradient(90deg,var(--coral),var(--orange));border-radius:10mm;padding:1.8mm 5mm;text-shadow:none;box-shadow:0 1mm 4mm rgba(0,0,0,.4)}
.cv-title .kick .hico{width:9mm;height:5.6mm;fill:#fff}
.cv-title h1{font-size:46pt;line-height:1;margin-top:2mm;font-weight:800}
.cv-title .t2{font-size:40pt;color:var(--gold2);margin-top:-2mm}
.cv-title .with{background:linear-gradient(90deg,var(--gold),var(--gold2));color:var(--plum3);margin-top:2mm;text-shadow:none;font-size:9.5pt}
.circ{position:absolute;width:44mm;height:44mm;border-radius:50%;overflow:hidden;border:1.6mm solid #fff;box-shadow:0 1.5mm 5mm rgba(0,0,0,.45)}
.cv-band{position:absolute;left:0;right:0;bottom:24mm;text-align:center;color:#fff}
.cv-band .dates{display:block;width:max-content;margin:0 auto 3mm;background:#fff;color:var(--plum3);border-radius:3mm;padding:1.6mm 6mm;font-weight:800;font-size:13pt;letter-spacing:.4mm;box-shadow:0 1mm 4mm rgba(0,0,0,.35)}
.cv-band .dur{display:inline-block;background:linear-gradient(90deg,var(--coral),var(--orange));border-radius:12mm;padding:2.5mm 9mm;font-weight:800;font-size:15pt;letter-spacing:.5mm}
.cv-band .route{font-family:'Playfair Display';font-size:12.5pt;margin-top:3mm;color:var(--gold2);padding:0 12mm}
.cv-band .regclose{display:inline-block;margin-top:2.5mm;background:var(--coral);color:#fff;border-radius:2mm;padding:1mm 4mm;font-weight:700;font-size:8.6pt;letter-spacing:.2mm}
.cv-feats{display:flex;justify-content:center;flex-wrap:wrap;gap:2mm 3mm;margin-top:3.5mm;padding:0 10mm}
.cv-feats span{border:.3mm solid rgba(246,213,139,.7);border-radius:8mm;padding:1mm 3.5mm;font-size:7.8pt;font-family:Montserrat;font-weight:600}
.cv-foot{position:absolute;left:0;right:0;bottom:0;height:18mm;background:#fff;display:flex;align-items:center;line-height:1;justify-content:space-between;padding:0 10mm}
.cv-foot .book{background:linear-gradient(90deg,var(--coral),var(--orange));color:#fff;border-radius:10mm;padding:2.5mm 6mm;font-weight:800;font-size:11pt}
.cv-foot .ph{font-size:19pt;font-weight:800;color:var(--plum)}
.cv-foot .web{font-size:8pt;text-align:right;color:var(--plum);font-weight:600;line-height:1.4}
"""
def welcome(pk,n,T):
    hl="".join(f"<li>{E(h)}</li>" for h in pk["highlights"])
    stays="".join(f'<div class="stat"><b style="font-size:{"12pt" if len(pk["stays"])>4 else "16pt"};white-space:nowrap">{E(b)}</b><span>{E(a)}</span></div>' for a,b in pk["stays"])
    return f'''<div class="page">{chrome(pk,"Welcome",pk["greeting"],n,T)}<div class="body">
<div class="grid2" style="grid-template-columns:1.15fr .85fr;gap:6mm">
<div><h2 class="sec-title">Warm greetings<span class="script" style="display:block;margin:0">from Punya Kshetras</span></h2><div class="orn left"><span></span></div>
<p class="lead">{E(pk["intro"])}</p>
<p style="margin-top:3mm">{E(ORG_LINE)}</p></div>
<div>{photo("prabhupada","62mm" if len(pk["highlights"])>9 else "70mm",None)}<div style="font-size:7.5pt;color:var(--muted);text-align:center;margin-top:1.5mm">His Divine Grace A.C. Bhaktivedanta Swami Srila Prabhupada,<br>Founder-Acharya of ISKCON</div></div></div>
<div class="qbox" style="margin-top:6mm"><p>{E(PRABHUPADA_QUOTE[0])}</p><div class="src">Srila Prabhupada · {E(PRABHUPADA_QUOTE[1])}</div></div>
<div class="grid2" style="margin-top:6mm;grid-template-columns:1.2fr .8fr;gap:6mm">
<div class="card"><h3 class="sub">Yatra highlights</h3><ul class="tick star" style="{"columns:2;column-gap:4mm;font-size:8pt" if len(pk["highlights"])>9 else ""}">{hl}</ul></div>
<div><h3 class="sub">Overnight stays</h3><div style="display:grid;grid-template-columns:{"1fr 1fr 1fr" if len(pk["stays"])>4 else "1fr 1fr"};gap:3mm">{stays}</div>
<div class="card" style="margin-top:4mm;padding:4mm"><h3 class="sub" style="margin-bottom:1mm">Your departure</h3><p style="font-size:8.6pt">{E(pk["best"])}</p></div></div></div>
</div></div>'''
def journey(pk,n,T):
    st=pk["stops"]; N=len(st)
    # serpentine: 2 columns if many
    rows=[]
    for i,(name,sub,mode,dist) in enumerate(st):
        conn=f'<div class="conn"><span class="mode">{E(mode)}</span><span class="dist">{E(dist)}</span></div>' if mode else ""
        rows.append(f'<div class="stop"><div class="dot">{i+1}</div><div class="nm"><b>{E(name)}</b><small>{E(sub)}</small></div></div>{conn}')
    stats=pk["stats"]
    statsh="".join(f'<div class="stat"><b>{E(str(a))}</b><span>{E(b)}</span></div>' for a,b in stats)
    cols=2 if N>6 else 1
    half=(N+1)//2 if cols==2 else N
    def colhtml(items): return '<div class="jcol">'+"".join(items)+'</div>'
    parts=[]
    for i,(name,sub,mode,dist) in enumerate(st):
        last=(i==N-1) or (cols==2 and i==half-1)
        conn="" if (not mode or last) else f'<div class="conn"><span class="mode">{E(mode)}</span><span class="dist">{E(dist)}</span></div>'
        parts.append(f'<div class="stop"><div class="dot">{i+1}</div><div class="nm"><b>{E(name)}</b><small>{E(sub)}</small></div></div>{conn}')
    if cols==2:
        m=st[half-1]; bridge=f'<div class="bridge">continues → <b>{E(m[2])}</b> {E(m[3])}</div>'
        jh=colhtml(parts[:half]+[bridge])+colhtml(parts[half:])
    else: jh=colhtml(parts)
    return f'''<div class="page">{chrome(pk,pk["journey_title"],pk["tagline"],n,T)}<div class="body">
<h2 class="sec-title">The route<span class="script">step by step</span></h2><div class="orn left"><span></span></div>
<div style="display:grid;grid-template-columns:repeat({len(stats)},1fr);gap:3mm;margin-bottom:6mm">{statsh}</div>
<div class="journey" style="grid-template-columns:repeat({cols},1fr)">{jh}</div>
<div style="position:absolute;left:0;right:0;bottom:0;height:56mm;display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm">{"".join(photo(k,"56mm",c) for k,c in pk["journey_photos"])}</div>
</div></div>'''
JCSS="""
.journey{display:grid;gap:8mm}
.jcol{position:relative}
.stop{display:flex;align-items:center;gap:4mm;position:relative;z-index:1}
.dot{width:10mm;height:10mm;border-radius:50%;background:linear-gradient(135deg,var(--plum2),var(--plum3));color:#fff;font-family:Montserrat;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:10pt;box-shadow:0 0 0 1.2mm var(--gold2);flex:none}
.nm b{display:block;font-family:'Playfair Display';font-size:12pt;color:var(--plum)}
.nm small{font-size:8pt;color:var(--muted)}
.conn{margin-left:4.6mm;border-left:.9mm dashed var(--coral);padding:2mm 0 2mm 8mm;display:flex;gap:2mm;align-items:center;min-height:9mm}
.conn .mode{background:var(--coral);color:#fff;font-family:Montserrat;font-weight:700;font-size:7pt;border-radius:5mm;padding:.6mm 2.6mm;text-transform:uppercase}
.conn .dist{font-family:Montserrat;font-size:7.6pt;color:var(--plum);font-weight:600}
.bridge{margin:3mm 0 0 4mm;font-size:8pt;color:var(--coral);font-family:Montserrat}
"""
def daypage(pk,d,rows,n,T):
    tr=[]
    for r in rows:
        if r[0]!=d["n"]: continue
        dd,s,e,mode,fr,to,km,act,mp=r
        where=fr if to=="—" else f"{fr} → {to}"
        cls="meal" if mode in("Breakfast","Lunch","Dinner") else "air" if mode in("Helicopter","Flight","Gondola","Ropeway","Shikara") else ""
        tagc=mode.split()[0].replace("/","")
        tr.append(f'<tr class="{cls}"><td class="t">{s} – {e}</td><td class="m"><span class="tag {tagc}">{E(mode)}</span></td><td><b>{E(where)}</b> <span style="color:var(--muted)">· {E(act)}</span></td><td class="k">{str(km)+" km" if km else ""}</td></tr>')
    stay=f'<span class="stay">Overnight: <b>{E(d["stay"])}</b></span>' if d["stay"] else f'<span class="stay">Departure · <b>{E(pk["closing"])}</b></span>'
    a,b=d["imgs"]
    return f'''<div class="page">{chrome(pk,f"Day {d['n']:02d} · Detailed Itinerary",d["title"],n,T)}<div class="body">
<div class="dphotos" style="display:grid;grid-template-columns:1.25fr .75fr;gap:3mm;height:52mm">{photo(a,"52mm",IMG[a].get("cap"))}{photo(b,"52mm",IMG[b].get("cap"))}</div>
<div style="display:flex;align-items:center;margin-top:4mm"><div class="daybadge"><span class="n">DAY {d["n"]:02d}<small style="display:block;font-size:6.6pt;font-weight:600;letter-spacing:.2mm">{day_date(pk,d["n"],"%a %d %b")}</small></span><h2>{E(d["title"])}</h2></div>{stay}</div>
<p style="margin-top:2.5mm;font-size:9.4pt">{E(d["story"])}</p>
<div class="sig"><h4>{E(d["sig"][0])}</h4><p>{E(d["sig"][1])}</p></div>
<table class="tl">{"".join(tr)}</table>
<div style="font-size:6.8pt;color:var(--muted);margin-top:1.5mm">{E(day_date(pk,d["n"],"%A %d %B %Y"))}{" · " if pk.get("start_date") else ""}{E(pk["timing_note"])}</div>
</div></div>'''
def places(pk,n,T):
    ps=pk["places"]; cells="".join(f'<div class="phbox" style="height:{"74mm" if len(ps)<=6 else "60mm"};border-radius:3mm">{img(k)}<div class="cap">{E(t)}<small>{E(s)}</small></div></div>' for k,t,s in ps)
    return f'''<div class="page">{chrome(pk,"Holy Places You Will Visit","Darshan, history and natural beauty",n,T)}<div class="body">
<h2 class="sec-title">Sacred places<span class="script">on this yatra</span></h2><div class="orn left"><span></span></div>
<div class="grid3" style="gap:3.5mm">{cells}</div></div></div>'''
def flights_card(pk):
    if not pk["flights"]: return ""
    li="".join(f"<li>{E(x)}</li>" for x in pk["flights"])
    return f'<div class="card" style="margin-top:4mm;padding:4mm"><h3 class="sub" style="margin-bottom:1.5mm">{E(pk["flights_title"])}</h3><ul class="tick" style="font-size:8.4pt">{li}</ul></div>'
def incl(pk,rows,n,T):
    meals=[r for r in rows if r[3] in ("Breakfast","Lunch","Dinner")]
    rowsh=[f'<tr><td class="t">Day {r[0]}</td><td><span class="tag {r[3]}">{r[3]}</span></td><td style="white-space:nowrap">{r[1]}–{r[2]}</td><td>{E(r[4])}</td></tr>' for r in meals]
    if len(rowsh)>12:
        h=(len(rowsh)+1)//2
        mt=f'</table><div class="grid2" style="gap:4mm"><table class="tl ml" style="font-size:6.9pt">{"".join(rowsh[:h])}</table><table class="tl ml" style="font-size:6.9pt">{"".join(rowsh[h:])}</table></div><table>'
    else: mt="".join(rowsh)
    return f'''<div class="page">{chrome(pk,"Package Details","Inclusions · exclusions · meal plan",n,T)}<div class="body">
<div class="grid2" style="gap:5mm">
<div class="card"><h3 class="sub">Package includes</h3><ul class="tick" style="font-size:{"7.9pt" if len(pk["incl"])>9 or len(pk["flights"])>2 else "8.6pt"}">{"".join(f"<li>{E(x)}</li>" for x in pk["incl"])}</ul></div>
<div><div class="card"><h3 class="sub">Not included</h3><ul class="tick cross" style="font-size:{"7.9pt" if len(pk["flights"])>2 else "8.6pt"}">{"".join(f"<li>{E(x)}</li>" for x in pk["excl"])}</ul></div>
<div class="card" style="margin-top:4mm;background:linear-gradient(135deg,var(--plum3),var(--plum2));color:#fff;text-align:center">
<div class="mont" style="font-size:8pt;letter-spacing:.6mm;color:var(--gold2);font-weight:700">PACKAGE PRICE &amp; DATES</div>
<div style="font-family:'Playfair Display';font-size:14pt;margin:1mm 0">{E(pk["dates_long"])}</div>
<div style="font-family:Montserrat;font-weight:800;font-size:20pt;color:var(--gold2);line-height:1.1">{E(pk["price"])} <span style="font-size:10pt">{E(pk["gst_note"])}</span></div><div style="font-size:8.4pt">{E(pk["price_note"])}<br>{f'<b style="color:var(--gold2)">Registrations close {E(pk["reg_close"])}.</b> ' if pk.get("reg_close") else ""}{E(pk["seats_note"])}<br>Call <b style="color:var(--gold2)">{CONTACT["phone"]}</b> to book.</div></div>
{flights_card(pk)}</div></div>
{"" if len(meals)>12 else f'<h3 class="sub" style="margin-top:4mm">Meal plan · pure vegetarian</h3><table class="tl ml" style="font-size:8pt">{mt}</table>'}
</div></div>'''
def mealpage(pk,rows,n,T):
    meals=[r for r in rows if r[3] in ("Breakfast","Lunch","Dinner")]
    tr="".join(f'<tr class="meal"><td class="t">Day {r[0]}</td><td><span class="tag {r[3]}">{r[3]}</span></td><td style="white-space:nowrap">{r[1]}–{r[2]}</td><td><b>{E(r[4])}</b> <span style="color:var(--muted)">· {E(r[7])}</span></td></tr>' for r in meals)
    return f'''<div class="page">{chrome(pk,"Meal Plan",pk["meal_subtitle"],n,T)}<div class="body">
<h2 class="sec-title">Every meal<span class="script">planned with care</span></h2><div class="orn left"><span></span></div>
<p style="margin-bottom:4mm">{E(pk["meal_note"])}</p>
<table class="tl ml" style="font-size:8.2pt">{tr}</table></div></div>'''
def why(pk,n,T):
    w="".join(f'<div class="wrow"><div class="wnum">{i+1}</div><div><b>{E(a)}</b><span>{E(b)}</span></div></div>' for i,(a,b) in enumerate(pk["why"]))
    ex="".join(f'<div class="exp"><div class="ico">{ICONS[i]}</div><span>{E(x)}</span></div>' for i,x in enumerate(EXPERIENCES))
    return f'''<div class="page" style="background:linear-gradient(160deg,var(--plum3),var(--plum2) 70%,#7a2a8f)">{chrome(pk,"Why Punya Kshetras","Nourish your soul on sacred journeys",n,T)}<div class="body" style="color:#fff">
<h2 class="sec-title" style="color:#fff">How we are<span class="script" style="color:var(--gold2)">different</span></h2><div class="orn left"><span></span></div>
<div class="wgrid">{w}</div>
<h3 class="sub" style="color:var(--gold2);margin-top:7mm">Curated special experiences</h3>
<div class="exps">{ex}</div>
<div style="margin-top:7mm" class="grid2">{photo("moments1","70mm","Moments from our past yatras")}{photo("moments2","70mm","Devotees on yatra with Punya Kshetras")}</div>
</div></div>'''
WCSS="""
table.ml td.t{width:10mm}table.ml td:nth-child(2){width:17mm}table.ml td:nth-child(3){width:19mm}
ul.tick li{font-size:inherit}

.wgrid{display:grid;grid-template-columns:1fr 1fr;gap:3mm}
.wrow{display:flex;gap:3mm;align-items:flex-start;background:rgba(255,255,255,.08);border:.3mm solid rgba(246,213,139,.35);border-radius:3mm;padding:3mm}
.wnum{flex:none;width:7mm;height:7mm;border-radius:50%;background:var(--coral);display:flex;align-items:center;justify-content:center;font-family:Montserrat;font-weight:800;font-size:8.5pt}
.wrow b{display:block;font-family:Montserrat;font-size:9.4pt;color:var(--gold2)}
.wrow span{font-size:8.4pt;line-height:1.4;opacity:.95}
.exps{display:grid;grid-template-columns:repeat(6,1fr);gap:2.5mm}
.exp{background:#fff;color:var(--plum);border-radius:3mm;text-align:center;padding:3mm 1.5mm;font-family:Montserrat;font-weight:600;font-size:7.2pt;line-height:1.3}
.exp .ico{width:11mm;height:11mm;margin:0 auto 1.5mm;border-radius:50%;background:var(--cream);display:flex;align-items:center;justify-content:center}
.exp svg{width:7mm;height:7mm}
"""
def tips(pk,n,T):
    faq="".join(f'<div class="faq"><b>{E(q)}</b><p>{E(a)}</p></div>' for q,a in pk["faq_common"]+pk["faq"])
    pack=pk["pack"]; dos=pk["dos"]; donts=pk["donts"]
    return f'''<div class="page">{chrome(pk,"Know Before You Go","Packing · do's & don'ts · FAQs",n,T)}<div class="body">
<div class="grid3" style="gap:4mm">
<div class="card"><h3 class="sub">Pack these</h3><ul class="tick">{"".join(f"<li>{E(x)}</li>" for x in pack)}</ul></div>
<div class="card"><h3 class="sub">Do's</h3><ul class="tick">{"".join(f"<li>{E(x)}</li>" for x in dos)}</ul></div>
<div class="card"><h3 class="sub">Don'ts</h3><ul class="tick cross">{"".join(f"<li>{E(x)}</li>" for x in donts)}</ul></div></div>
<h3 class="sub" style="margin-top:6mm">Frequently asked questions</h3><div class="grid2" style="gap:3mm">{faq}</div>
</div></div>'''
FCSS=".faq{background:#fff;border-radius:3mm;padding:3mm 4mm;border-left:1mm solid var(--coral)}.faq b{font-family:Montserrat;font-size:8.8pt;color:var(--plum)}.faq p{font-size:8.4pt;line-height:1.45;margin-top:1mm}"
def terms(pk,n,T):
    k=[a for a,_ in TERMS].index("Rescheduling")+1
    t="".join(f'<div class="term"><b>{E(a)}</b><p>{E(b.format(**CONTACT))}</p></div>' for a,b in TERMS[:k]+pk["extra_terms"]+TERMS[k:])
    return f'''<div class="page">{chrome(pk,"Terms & Conditions","Please read before booking",n,T)}<div class="body">
<div class="tgrid">{t}</div>
<div style="position:absolute;bottom:0;left:0;right:0"><h3 class="sub">Who joined our yatras</h3><div style="height:62mm;background:#fff;border-radius:3mm;padding:2mm"><img src="{IMG["joined"]["src"]}" style="width:100%;height:100%;object-fit:contain"></div></div>
</div></div>'''
TCSS=".tgrid{columns:2;column-gap:6mm}.term{break-inside:avoid;margin-bottom:3mm}.term b{font-family:Montserrat;font-size:8.6pt;color:var(--coral);text-transform:uppercase;letter-spacing:.3mm}.term p{font-size:8.2pt;line-height:1.45;margin-top:.6mm}"
def back(pk,n,T,credits):
    return f'''<div class="page" style="background:var(--plum3)">
<div style="position:absolute;inset:0;opacity:.28">{img(pk["back"])}</div>
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(42,13,61,.6),rgba(42,13,61,.95) 60%)"></div>
<div style="position:absolute;top:24mm;left:0;right:0;text-align:center;color:#fff">
<div style="display:inline-flex;gap:6mm"><div class="cvlogo"><img src="brand/hkgt_logo.png"></div><div class="cvlogo"><img src="brand/pk_logo.png"></div></div>
<div class="script" style="font-size:34pt;color:var(--gold2);margin-top:9mm">{E(BACK_TAGLINE)}</div>
<div class="orn" style="width:120mm;margin:3mm auto"><span></span></div>
<div class="mont" style="font-size:13pt;font-weight:700;margin-top:4mm">For details &amp; registration</div>
<div style="font-size:9.5pt;opacity:.9;margin-top:1mm">Please contact any temple devotee you are in touch with, or</div>
<div class="mont" style="font-size:30pt;font-weight:800;color:var(--gold2);margin-top:5mm">{PHONE_SVG.format(w="26pt",c="#F6D58B",s="vertical-align:-0.12em;margin-right:2mm")}{CONTACT["phone"]}</div>
<div class="mont" style="font-size:12pt;margin-top:3mm">✉ {CONTACT["email"]}</div>
<div class="mont" style="font-size:11pt;margin-top:3mm">{CONTACT["web1"]} &nbsp;·&nbsp; {CONTACT["web2"]}</div>
<div class="mont" style="font-size:10pt;margin-top:2mm;color:var(--gold2)">{CONTACT["social_line"]}</div>
<div style="font-size:9.5pt;margin:8mm auto 0;width:150mm;line-height:1.55">{E(CONTACT["address"])}</div>
<div class="script" style="font-size:26pt;margin-top:8mm;color:#fff">{E(pk["closing"])}</div>
</div>
<div style="position:absolute;bottom:6mm;left:12mm;right:12mm;font-size:5.6pt;color:rgba(255,255,255,.6);line-height:1.4">Photo credits (Wikimedia Commons, used under their licences): {E(credits)}. Srila Prabhupada photographs and past-yatra photos © Hare Krishna Golden Temple / respective owners.</div>
</div>'''
BCSS=".cvlogo{background:#fff;border-radius:4mm;padding:2.5mm 4mm}.cvlogo img{height:20mm;display:block}"
FIT="<script>\nwindow.__fit=document.fonts.ready.then(()=>{document.querySelectorAll('.page .body').forEach(b=>{\n  const t=b.querySelector('table.tl'), ph=b.querySelector('.dphotos');\n  if(!t) return;\n  let fs=7.9,pad=1.05,h=52,guard=0;\n  const over=()=>b.scrollHeight>b.clientHeight+1;\n  while(over() && guard++<60){\n    if(fs>7.0){fs-=0.15;pad=Math.max(.55,pad-.05);}\n    else if(ph && h>34){h-=3;ph.style.height=h+'mm';ph.querySelectorAll('.phbox').forEach(x=>x.style.height=h+'mm');}\n    else if(fs>6.3){fs-=0.15;}\n    else break;\n    t.style.fontSize=fs+'pt'; t.querySelectorAll('td').forEach(td=>td.style.padding=pad+'mm 1.4mm');\n  }\n  if(over()) document.title+=' OVERFLOW';\n});});\n</script>"
def brochure(pk):
    rows=load_rows(pk)
    pages=[]
    meals_n=len([r for r in rows if r[3] in ('Breakfast','Lunch','Dinner')])
    T=6+len(pk["daypages"])+3+(1 if meals_n>12 else 0)
    pages.append(cover(pk))
    pages.append(welcome(pk,2,T)); pages.append(journey(pk,3,T))
    n=4
    for d in pk["daypages"]: pages.append(daypage(pk,d,rows,n,T)); n+=1
    pages.append(places(pk,n,T)); n+=1
    pages.append(incl(pk,rows,n,T)); n+=1
    if meals_n>12: pages.append(mealpage(pk,rows,n,T)); n+=1
    pages.append(why(pk,n,T)); n+=1
    pages.append(tips(pk,n,T)); n+=1
    pages.append(terms(pk,n,T)); n+=1
    html_so_far="".join(pages); used=set(k for k in IMG if IMG[k].get("credit") and IMG[k]["src"] in html_so_far)
    credits="; ".join(sorted(set(IMG[k]["credit"] for k in used)))
    pages.append(back(pk,n,T,credits))
    css=open("style.css").read()+CSS_EXTRA+COVER_CSS+JCSS+WCSS+FCSS+TCSS+BCSS
    return f'<!doctype html><html><head><meta charset="utf-8"><title>{E(pk["title"])} {E(pk["title2"])}</title><style>{css}</style></head><body>{"".join(pages)}{FIT}</body></html>'
if __name__=="__main__":
    open("brochure.html","w").write(brochure(PK)); print("wrote brochure.html")
