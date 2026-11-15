"""
Five more poster designs for the London & Europe Grand Tour (same content and branding, different looks):
  A mosaic   – 9-photo collage teaser                    1080 × 1350
  B luxury   – black & gold, elegant serif               1080 × 1350
  C ticket   – boarding-pass style                       1080 × 1350
  D map      – big route map with price                  1080 × 1350
  E story    – 8 country strips for WhatsApp/Insta story 1080 × 1920

    python3 kh/build_posters2.py && node kh/render_posters2.cjs
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_kh as K  # noqa: E402
from build_posters import TOTAL, brush  # noqa: E402

PK, C, E, ic, I, IMG = K.PK, K.C, K.E, K.ic, K.I, K.IMG
PRICE = E(PK["price"])
BASE = """
@import url('%s');
*{box-sizing:border-box;margin:0;padding:0}
:root{--n:#2A0D3D;--n2:#3A1452;--n3:#5B1F7E;--o:#F28C28;--c:#E8445A;--g:#E7B24A;--g2:#F6D58B}
body{font-family:Poppins,sans-serif;background:#000}
img{display:block}
.po{width:1080px;position:relative;overflow:hidden}
.lgw{background:#fff;border-radius:14px;padding:8px 14px;box-shadow:0 4px 14px rgba(0,0,0,.25)}.lgw img{height:58px}
.seal{height:80px;border-radius:50%%;box-shadow:0 0 0 5px #fff,0 4px 14px rgba(0,0,0,.35)}
.gold{background:linear-gradient(180deg,#FFE7A3,#F6C24A 45%%,#C9851C);-webkit-background-clip:text;background-clip:text;color:transparent}
.cta{position:absolute;left:0;right:0;bottom:0;height:150px}
.cta svg.brush{position:absolute;inset:0;width:100%%;height:100%%}
.ctab{position:absolute;left:36px;right:36px;bottom:20px;display:flex;align-items:center;justify-content:space-between;color:#fff}
.bk{background:linear-gradient(90deg,var(--c),var(--o));border-radius:40px;padding:12px 26px;font-family:Montserrat;font-weight:800;font-size:26px;white-space:nowrap}
.ph{font-family:Montserrat;font-weight:800;font-size:54px;color:var(--g2);display:flex;align-items:center;gap:10px}
.ph svg{width:46px;height:46px}
.web{text-align:right;font-family:Montserrat;font-weight:600;font-size:18px;line-height:1.45}
"""

def doc(css, body, h, name):
    html = (f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE % K.FONTS}{css}</style></head>'
            f'<body><div class="po" style="height:{h}px">{body}</div></body></html>')
    open(os.path.join(HERE, name), "w").write(html)

def logos(seal=True):
    return (f'<div class="lgs"><div class="lgw"><img src="{K.LOGO_HK}"></div>'
            + (f'<img class="seal" src="{K.SEAL}">' if seal else "") + f'<div class="lgw"><img src="{K.LOGO_PK}"></div></div>')

# ---------------- A. mosaic ----------------
def mosaic():
    tiles = ["towerbridge", "eiffel", "venice", "titlis", "colosseum", "keukenhof", "pisa", "lucerne", "stpeters"]
    caps = ["London", "Paris", "Venice", "Mount Titlis", "Rome", "Keukenhof", "Pisa", "Lucerne", "Vatican"]
    g = "".join(f'<div class="t"><img src="{IMG(k)}"><span>{c}</span></div>' for k, c in zip(tiles, caps))
    css = """
.mo{position:absolute;inset:0;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,1fr);gap:6px;background:#fff}
.t{position:relative;overflow:hidden}.t img{width:100%;height:100%;object-fit:cover}
.t span{position:absolute;left:10px;bottom:10px;background:rgba(42,13,61,.8);color:#fff;font-family:Montserrat;font-weight:700;font-size:20px;padding:4px 14px;border-radius:30px}
.lgs{position:absolute;top:22px;left:24px;right:24px;display:flex;justify-content:space-between;align-items:center}
.card{position:absolute;left:150px;right:150px;top:395px;background:rgba(255,248,238,.96);border-radius:28px;padding:26px 30px 30px;text-align:center;box-shadow:0 20px 50px rgba(0,0,0,.45);border:4px solid var(--g)}
.k{display:inline-block;background:linear-gradient(90deg,var(--c),var(--o));color:#fff;font-family:Montserrat;font-weight:800;font-size:22px;letter-spacing:3px;padding:7px 22px;border-radius:30px}
.a{font-family:'Great Vibes';font-size:84px;color:#D8263E;line-height:1;margin-top:6px}
.b{font-family:'Playfair Display';font-weight:800;font-size:96px;line-height:.95;letter-spacing:4px;color:var(--n)}
.d{font-family:Montserrat;font-weight:800;font-size:30px;color:var(--n2);margin-top:12px}
.p{margin-top:14px;font-family:Montserrat;font-weight:800;font-size:64px;color:var(--c);line-height:1}
.p small{display:block;font-size:20px;color:var(--n);font-weight:600;margin-top:6px}
"""
    body = (f'<div class="mo">{g}</div>{logos()}<div class="card"><div class="k">8 COUNTRIES · {TOTAL} ATTRACTIONS</div>'
            f'<div class="a">London &amp;</div><div class="b">EUROPE</div><div class="d">17 April – 2 May 2027 · 16 Days</div>'
            f'<div class="p">{PRICE}<small>per person · + 5% GST + 2% TCS · flights &amp; visas included</small></div></div>{brush()}')
    doc(css, body, 1350, "p2_mosaic.html")

# ---------------- B. luxury ----------------
def luxury():
    cs = [("United Kingdom", "Tower of London · London Eye"), ("France", "Eiffel Tower · Louvre"), ("Belgium", "Atomium · Grand Place"),
          ("Netherlands", "Keukenhof · canals"), ("Germany", "Cologne · Black Forest"), ("Switzerland", "Mount Titlis · Lucerne"),
          ("Italy", "Venice · Rome · Pisa"), ("Vatican City", "Sistine Chapel · St Peter's")]
    rows = "".join(f'<div class="r"><b>{i:02d}</b><div><h4>{E(c)}</h4><p>{E(s)}</p></div></div>' for i, (c, s) in enumerate(cs, 1))
    circ = "".join(f'<div class="cc"><img src="{IMG(k)}"></div>' for k in ("colosseum", "eiffelnight", "venice"))
    css = """
.po{background:radial-gradient(ellipse at 50% 0%,#3A1452 0%,#160620 55%,#0A0310 100%)}
.bgph{position:absolute;left:0;right:0;top:0;height:560px;opacity:.38;-webkit-mask-image:linear-gradient(#000,transparent);mask-image:linear-gradient(#000,transparent)}
.bgph img{width:100%;height:100%;object-fit:cover}
.fr{position:absolute;inset:22px;border:2px solid rgba(231,178,74,.6);border-radius:8px;pointer-events:none}
.fr2{position:absolute;inset:32px;border:1px solid rgba(231,178,74,.35);border-radius:6px}
.lgs{position:absolute;top:52px;left:56px;right:56px;display:flex;justify-content:space-between;align-items:center}
.tt{position:absolute;top:180px;left:0;right:0;text-align:center;color:#fff}
.tt small{font-family:Montserrat;font-weight:700;letter-spacing:10px;font-size:22px;color:var(--g2)}
.tt .a{font-family:'Playfair Display';font-style:italic;font-size:62px;margin-top:8px;color:#fff}
.tt .b{font-family:'Playfair Display';font-weight:800;font-size:128px;letter-spacing:12px;line-height:1}
.tt .d{font-family:Montserrat;font-weight:600;letter-spacing:6px;font-size:24px;margin-top:10px;color:#fff}
.orn{display:flex;align-items:center;justify-content:center;gap:16px;margin:16px auto 0;width:520px}
.orn:before,.orn:after{content:"";flex:1;height:1.5px;background:linear-gradient(90deg,transparent,var(--g))}
.orn:after{transform:scaleX(-1)}
.orn span{width:12px;height:12px;background:var(--g);transform:rotate(45deg)}
.ccs{position:absolute;top:530px;left:0;right:0;display:flex;justify-content:center;gap:28px}
.cc{width:170px;height:170px;border-radius:50%;overflow:hidden;border:4px solid var(--g);box-shadow:0 0 0 6px rgba(231,178,74,.2)}
.cc img{width:100%;height:100%;object-fit:cover}
.lst{position:absolute;top:735px;left:80px;right:80px;display:grid;grid-template-columns:1fr 1fr;gap:12px 40px}
.r{display:flex;gap:14px;align-items:center;border-bottom:1px solid rgba(231,178,74,.3);padding-bottom:9px}
.r b{font-family:'Playfair Display';font-size:34px;color:var(--g)}
.r h4{font-family:Montserrat;font-weight:700;color:#fff;font-size:21px;letter-spacing:1px}
.r p{color:#d9c9e6;font-size:16px}
.pr{position:absolute;top:1015px;left:0;right:0;text-align:center;color:#fff}
.pr small{font-family:Montserrat;font-weight:700;letter-spacing:6px;font-size:18px;color:var(--g2)}
.pr b{display:block;font-family:'Playfair Display';font-weight:800;font-size:84px;line-height:1.05}
.pr em{font-style:normal;font-family:Montserrat;font-size:19px}
"""
    body = (f'<div class="bgph"><img src="{IMG("eiffelnight")}"></div><div class="fr"></div><div class="fr2"></div>{logos()}'
            f'<div class="tt"><small>A GRAND JOURNEY · 2027</small><div class="a">London &amp;</div><div class="b gold">EUROPE</div>'
            f'<div class="orn"><span></span></div><div class="d">17 APRIL – 2 MAY · 16 DAYS · 8 COUNTRIES</div></div>'
            f'<div class="ccs">{circ}</div><div class="lst">{rows}</div>'
            f'<div class="pr"><small>ALL-INCLUSIVE · PER PERSON</small><b class="gold">{PRICE}</b>'
            f'<em>+ 5% GST + 2% TCS · international flights, visas, hotels &amp; all meals included</em></div>{brush()}')
    doc(css, body, 1350, "p2_luxury.html")

# ---------------- C. boarding pass ----------------
def ticket():
    stops = ["LONDON", "PARIS", "BRUSSELS", "AMSTERDAM", "COLOGNE", "BLACK FOREST", "ZURICH", "LUCERNE", "INTERLAKEN",
             "LAKE COMO", "MILAN", "VENICE", "ROME", "VATICAN", "FLORENCE", "PISA"]
    st = "".join(f"<span>{s}</span>" for s in stops)
    bars = "".join(f'<i style="width:{w}px"></i>' for w in [3, 1, 2, 4, 1, 1, 3, 2, 1, 4, 2, 1, 3, 1, 2, 2, 4, 1, 3, 1, 1, 2, 4, 2, 1, 3, 1, 2, 3, 1, 4, 1, 2] * 2)
    inc = "".join(f'<div>{ic(I[k], "#E8445A")}{t}</div>' for k, t in
                  [("plane", "Flights"), ("passport", "Visas"), ("bed", "15 nights hotels"), ("food", "All Indian veg meals"),
                   ("bus", "Private coach"), ("ticket", "All entry tickets")])
    css = """
.po{background:linear-gradient(160deg,#5B1F7E,#2A0D3D 60%,#160620)}
.bg{position:absolute;inset:0;opacity:.25}.bg img{width:100%;height:100%;object-fit:cover}
.lgs{position:absolute;top:26px;left:30px;right:30px;display:flex;justify-content:space-between;align-items:center}
.hd{position:absolute;top:150px;left:0;right:0;text-align:center;color:#fff}
.hd .a{font-family:'Great Vibes';font-size:70px;color:var(--g2);line-height:1}
.hd .b{font-family:Montserrat;font-weight:800;font-size:40px;letter-spacing:6px}
.tk{position:absolute;left:50px;right:50px;top:300px;height:640px;display:flex;filter:drop-shadow(0 18px 30px rgba(0,0,0,.5))}
.m{flex:1;background:#FFF8EE;border-radius:28px 0 0 28px;position:relative;padding:0}
.s{width:250px;background:#FFF0E0;border-radius:0 28px 28px 0;border-left:4px dashed #C9B8A0;padding:26px 22px;position:relative}
.m:before,.m:after{content:"";position:absolute;right:-22px;width:44px;height:44px;border-radius:50%;background:#2A0D3D;z-index:2}
.m:before{top:-22px}.m:after{bottom:-22px}
.tb{background:linear-gradient(90deg,var(--c),var(--o));border-radius:28px 0 0 0;padding:16px 30px;color:#fff;display:flex;justify-content:space-between;align-items:center;font-family:Montserrat;font-weight:800}
.tb span{font-size:24px;letter-spacing:3px}.tb b{font-size:20px;background:rgba(255,255,255,.2);padding:4px 14px;border-radius:20px}
.rt{display:flex;align-items:center;justify-content:space-between;padding:22px 34px 6px}
.ap b{display:block;font-family:Montserrat;font-weight:800;font-size:76px;color:var(--n);line-height:1}
.ap span{font-family:Montserrat;font-weight:600;font-size:18px;color:#6E6077}
.ap.r{text-align:right}
.pl{flex:1;display:flex;align-items:center;gap:10px;padding:0 20px}
.pl i{flex:1;border-top:3px dashed var(--o)}.pl svg{width:56px;height:56px}
.fl{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;padding:12px 34px;border-top:2px dashed #E3D2BC;border-bottom:2px dashed #E3D2BC;margin:10px 0}
.fl small{display:block;font-family:Montserrat;font-weight:700;font-size:13px;color:#8a7a92;letter-spacing:1px}
.fl b{font-family:Montserrat;font-weight:800;font-size:22px;color:var(--n)}
.via{padding:6px 34px}
.via small{font-family:Montserrat;font-weight:700;font-size:14px;color:#8a7a92;letter-spacing:2px}
.via div{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}
.via span{background:#fff;border:1.5px solid #EADFCB;border-radius:20px;padding:3px 11px;font-family:Montserrat;font-weight:700;font-size:15px;color:var(--n2)}
.inc{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;padding:14px 34px}
.inc div{display:flex;align-items:center;gap:8px;font-family:Montserrat;font-weight:700;font-size:17px;color:var(--n)}
.inc svg{width:34px;height:34px;background:#FFF0E0;border-radius:50%;padding:6px;flex:none}
.s small{display:block;font-family:Montserrat;font-weight:700;font-size:14px;color:#8a7a92;letter-spacing:2px;margin-top:10px}
.s b{display:block;font-family:Montserrat;font-weight:800;font-size:26px;color:var(--n)}
.s .pr{font-size:44px;color:var(--c);line-height:1.05}
.s .tx{font-size:15px;font-weight:600;color:var(--n2)}
.bc{position:absolute;left:22px;right:22px;bottom:26px;height:90px;display:flex;gap:2px;align-items:stretch;overflow:hidden}
.bc i{background:#2A0D3D;display:block;flex:none}
.ft{position:absolute;top:975px;left:0;right:0;text-align:center;color:#fff;font-family:Montserrat}
.ft b{font-size:34px;font-weight:800}.ft span{display:block;font-size:22px;color:var(--g2);margin-top:6px}
"""
    body = (f'<div class="bg"><img src="{IMG("towerbridge")}"></div>{logos()}'
            f'<div class="hd"><div class="a">Your boarding pass to</div><div class="b">LONDON &amp; EUROPE</div></div>'
            f'<div class="tk"><div class="m"><div class="tb"><span>GRAND TOUR 2027</span><b>GROUP · ONE COACH</b></div>'
            f'<div class="rt"><div class="ap"><b>HYD</b><span>Hyderabad / BLR</span></div><div class="pl"><i></i>{ic(I["plane"], "#E8445A", 1.6)}<i></i></div>'
            f'<div class="ap r"><b>LHR</b><span>London Heathrow</span></div></div>'
            f'<div class="fl"><div><small>DEPART</small><b>17 APR 2027</b></div><div><small>RETURN</small><b>2 MAY 2027</b></div>'
            f'<div><small>DURATION</small><b>16 DAYS</b></div><div><small>COUNTRIES</small><b>8</b></div></div>'
            f'<div class="via"><small>VIA · BY PRIVATE COACH, FERRY &amp; TRAIN</small><div>{st}</div></div>'
            f'<div class="inc">{inc}</div></div>'
            f'<div class="s"><small>PASSENGER</small><b>YOU &amp; FAMILY</b><small>CLASS</small><b>ALL-INCLUSIVE</b>'
            f'<small>FARE PER PERSON</small><b class="pr">{PRICE}</b><b class="tx">+ 5% GST + 2% TCS<br>incl. flights &amp; visas</b>'
            f'<small>ATTRACTIONS</small><b>{TOTAL}</b><div class="bc">{bars}</div></div></div>'
            f'<div class="ft"><b>Limited seats · one coach only</b><span>Flights: Emirates via Dubai (Hyderabad) · Etihad via Abu Dhabi (Bangalore)</span></div>{brush()}')
    doc(css, body, 1350, "p2_ticket.html")

# ---------------- D. route map ----------------
HL = ('<div class="hl"><b>Top highlights</b>' + ''.join(f'<div>{x}</div>' for x in ['Eiffel Tower & Louvre','Tower of London · London Eye','Keukenhof tulips','Snow on Mount Titlis','Venice gondola ride','Vatican & Colosseum','Leaning Tower of Pisa']) + '</div>')

def mapposter():
    m = re.search(r'<div class="map">.*?</svg></div>', K.routemap(), re.S).group(0)
    css = """
.po{background:linear-gradient(180deg,#FFF8EE,#FFEFDC)}
.lgs{position:absolute;top:22px;left:26px;right:26px;display:flex;justify-content:space-between;align-items:center;z-index:3}
.hd{position:absolute;top:118px;left:0;right:0;text-align:center}
.hd .a{font-family:'Great Vibes';font-size:60px;color:var(--o);line-height:1}
.hd .b{font-family:'Playfair Display';font-weight:800;font-size:58px;color:var(--n);line-height:1}
.hd .c{display:inline-block;margin-top:8px;background:linear-gradient(90deg,var(--c),var(--o));color:#fff;font-family:Montserrat;font-weight:800;font-size:22px;letter-spacing:2px;padding:6px 22px;border-radius:8px}
.map{position:absolute;left:36px;width:700px;top:300px;height:714px;border-radius:24px;overflow:hidden;border:6px solid #fff;box-shadow:0 10px 30px rgba(42,13,61,.25)}
.map img,.map .ov{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.pc{position:absolute;left:756px;right:36px;top:300px;background:var(--n);color:#fff;border-radius:20px;padding:16px 22px;text-align:center;box-shadow:0 8px 20px rgba(0,0,0,.35)}
.pc small{font-family:Montserrat;font-weight:700;font-size:15px;letter-spacing:2px;color:var(--g2)}
.pc b{display:block;font-family:Montserrat;font-weight:800;font-size:50px;line-height:1.05}
.pc span{font-family:Montserrat;font-size:15px}
.lg2{position:absolute;left:756px;right:36px;top:500px;background:#fff;border-radius:16px;padding:12px 16px;font-family:Montserrat;font-weight:600;font-size:16px;color:var(--n);box-shadow:0 4px 14px rgba(0,0,0,.15)}
.lg2 div{display:flex;align-items:center;gap:8px;padding:3px 0}
.k1{width:16px;height:16px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:var(--c)}
.k2{width:13px;height:13px;border-radius:50%;background:var(--o)}
.k3{width:30px;border-top:4px solid var(--n)}.k4{width:30px;border-top:4px dashed #1C7FC4}.k5{width:30px;border-top:4px dotted var(--c)}
.hl{position:absolute;left:756px;right:36px;top:700px;background:#fff;border-radius:16px;padding:12px 16px;box-shadow:0 4px 14px rgba(0,0,0,.15)}
.hl b{display:block;font-family:Montserrat;font-weight:800;font-size:17px;color:var(--c);margin-bottom:4px}
.hl div{font-family:Montserrat;font-weight:600;font-size:15.5px;color:var(--n);padding:3px 0;border-bottom:1px dashed #EADFCB}
.inr{position:absolute;top:1095px;left:36px;right:36px;display:grid;grid-template-columns:repeat(6,1fr);gap:10px}
.inr div{background:#fff;border-radius:14px;padding:10px 4px;text-align:center;font-family:Montserrat;font-weight:700;font-size:15px;color:var(--n);box-shadow:0 3px 10px rgba(42,13,61,.12)}
.inr svg{width:40px;height:40px;margin:0 auto 4px;display:block;background:#FFF0E0;border-radius:50%;padding:8px}
.nt{position:absolute;top:1040px;left:40px;right:40px;text-align:center;font-family:Montserrat;font-weight:700;font-size:21px;color:var(--n2)}
"""
    leg = ('<div class="lg2"><div><span class="k1"></span>Overnight stay</div><div><span class="k2"></span>Sightseeing</div>'
           '<div><span class="k3"></span>Private coach</div><div><span class="k4"></span>Channel ferry</div><div><span class="k5"></span>Train</div></div>')
    body = (f'{logos(False)}<div class="hd"><div class="a">One smooth journey</div><div class="b">London to Italy</div>'
            f'<div class="c">8 COUNTRIES · 16 DAYS · 17 APR – 2 MAY 2027</div></div>{m}'
            f'<div class="pc"><small>ALL-INCLUSIVE</small><b>{PRICE}</b><span>per person + 5% GST + 2% TCS<br>flights &amp; visas included</span></div>{leg}{HL}'
            f'<div class="nt">About 4,000 km by private coach · Channel ferry · Swiss &amp; Italian trains · {TOTAL} attractions</div>'
            + '<div class="inr">' + ''.join(f'<div>{ic(I[k], "#E8445A")}{t}</div>' for k, t in [("plane","Flights"),("passport","Visas"),("bed","Hotels"),("food","Indian meals"),("bus","Coach & trains"),("ticket","Entry tickets")]) + '</div>'
            + brush())
    doc(css, body, 1350, "p2_map.html")

# ---------------- E. story strips ----------------
def story():
    cs = [("UNITED KINGDOM", "Tower of London · London Eye · Buckingham Palace", "towerbridge"),
          ("FRANCE", "Eiffel Tower · Louvre · Seine cruise", "eiffel"),
          ("BELGIUM", "Atomium · Grand Place · Radhadesh château", "atomium"),
          ("NETHERLANDS", "Keukenhof tulips · windmills · canals", "keukenhof"),
          ("GERMANY", "Cologne Cathedral · Black Forest", "cologne"),
          ("SWITZERLAND", "Mount Titlis snow · Lucerne · Rhine Falls", "titlis"),
          ("ITALY", "Venice · Colosseum · Pisa · Lake Como", "venice"),
          ("VATICAN CITY", "Sistine Chapel · St Peter's Basilica", "stpeters")]
    strips = "".join(f'<div class="st"><img src="{IMG(k)}"><div class="sl"><b>{i:02d}</b><div><h3>{c}</h3><p>{E(s)}</p></div></div></div>'
                     for i, (c, s, k) in enumerate(cs, 1))
    css = """
.po{background:#2A0D3D}
.top{position:absolute;top:0;left:0;right:0;height:330px;background:linear-gradient(180deg,#FFF8EE,#FFEFDC);text-align:center}
.lgs{position:absolute;top:20px;left:24px;right:24px;display:flex;justify-content:space-between;align-items:center}
.lgs .lgw img{height:50px}.lgs .seal{height:70px}
.t1{position:absolute;top:118px;left:0;right:0}
.t1 .a{font-family:'Great Vibes';font-size:70px;color:#D8263E;line-height:1}
.t1 .b{font-family:'Playfair Display';font-weight:800;font-size:82px;color:var(--n);line-height:1;letter-spacing:4px}
.t1 .c{font-family:Montserrat;font-weight:800;font-size:26px;color:var(--c);margin-top:6px}
.sts{position:absolute;top:330px;left:0;right:0;height:1260px;display:flex;flex-direction:column}
.st{flex:1;position:relative;overflow:hidden;border-bottom:3px solid var(--g)}
.st img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.st:nth-child(even) .sl{left:auto;right:0;flex-direction:row-reverse;text-align:right;background:linear-gradient(270deg,rgba(42,13,61,.92),rgba(42,13,61,0))}
.sl{position:absolute;left:0;top:0;bottom:0;width:78%;display:flex;align-items:center;gap:18px;padding:0 34px;background:linear-gradient(90deg,rgba(42,13,61,.92),rgba(42,13,61,0));color:#fff}
.sl b{font-family:'Playfair Display';font-size:56px;color:var(--g2)}
.sl h3{font-family:Montserrat;font-weight:800;font-size:32px;letter-spacing:3px}
.sl p{font-size:20px;color:#f0e6f6}
.pr{position:absolute;top:1600px;left:0;right:0;text-align:center;color:#fff}
.pr b{font-family:Montserrat;font-weight:800;font-size:66px}
.pr span{display:block;font-family:Montserrat;font-weight:600;font-size:20px;color:var(--g2)}
"""
    body = (f'<div class="top">{logos()}<div class="t1"><div class="a">London &amp;</div><div class="b">EUROPE</div>'
            f'<div class="c">17 APRIL – 2 MAY 2027 · 16 DAYS · 8 COUNTRIES</div></div></div><div class="sts">{strips}</div>'
            f'<div class="pr"><b class="gold">{PRICE}</b><span>per person · + 5% GST + 2% TCS · flights, visas, hotels &amp; meals included</span></div>{brush()}')
    doc(css, body, 1920, "p2_story.html")

if __name__ == "__main__":
    mosaic(); luxury(); ticket(); mapposter(); story()
    print("wrote p2_mosaic, p2_luxury, p2_ticket, p2_map, p2_story")
