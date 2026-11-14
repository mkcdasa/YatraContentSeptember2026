"""
Travel-catalogue style brochure for the London & Europe Grand Tour, following the page flow of the outside
brochure the team supplied as a design reference (photo pages fading to cream, brush-stroke footer, two day
cards per page, route map, price cards, inclusions/exclusions, tips, things to carry, why us, payments,
cancellation, terms). Content, prices and branding come from ../package.py, ../rows.json, kh_days.py and the
punya-kshetras-brand skill (logos, contacts, terms).

    python3 kh/build_kh.py            (writes kh/brochure_kh.html)
    node kh/render_kh.cjs             (writes kh/out/*.pdf and kh/build/page-NN.png previews)
"""
import html, importlib.util, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WD = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(WD, "..", "..", ".."))
SKILL = os.path.join(ROOT, ".claude", "skills", "punya-kshetras-brand")
sys.path.insert(0, os.path.join(SKILL, "engine"))
import brand as B  # noqa: E402
sys.path.insert(0, HERE)
from kh_days import DAYS  # noqa: E402

spec = importlib.util.spec_from_file_location("package", os.path.join(WD, "package.py"))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
PK = mod.PKG
ROWS = json.load(open(os.path.join(WD, "rows.json")))
E = html.escape
C = B.CONTACT

def rel(p): return os.path.relpath(p, HERE).replace(os.sep, "/")
IMG = lambda k: rel(os.path.join(WD, "img", k + ".jpg"))
LOGO_HK = rel(os.path.join(SKILL, "assets", "brand", "hkgt_logo.png"))
LOGO_PK = rel(os.path.join(SKILL, "assets", "brand", "pk_logo.png"))
SEAL = rel(os.path.join(SKILL, "assets", "brand", "seal.png"))
FONTS = rel(os.path.join(SKILL, "assets", "fonts", "local.css"))
MAP = "map_base.svg"

# ---------- icons (simple line icons) ----------
def ic(p, c="currentColor", w=1.9):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{p}</svg>'
I = {
 "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>', "x": '<path d="M6 6l12 12M18 6L6 18"/>',
 "plane": '<path d="M2.5 13.5l19-7-5 15-3.5-6.5z"/><path d="M13 15l3-3"/>',
 "bed": '<path d="M3 18V7M3 13h18v5M21 13a3 3 0 0 0-3-3h-7v3"/><circle cx="7" cy="10.5" r="1.6"/>',
 "bus": '<rect x="4" y="3.5" width="16" height="14" rx="2.5"/><path d="M4 11h16M7.5 20.5v-3M16.5 20.5v-3"/><circle cx="8" cy="14.5" r=".6"/><circle cx="16" cy="14.5" r=".6"/>',
 "food": '<path d="M4 3v8a2 2 0 0 0 2 2v8M8 3v8M6 3v5"/><path d="M15 21V3c3 1 4.5 4 4.5 8h-4.5"/>',
 "ticket": '<path d="M3 8a2 2 0 0 0 0 4v0a2 2 0 0 0 0 4v2h18v-2a2 2 0 0 1 0-4 2 2 0 0 1 0-4V6H3z"/><path d="M14 6v12" stroke-dasharray="2 2"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
 "passport": '<rect x="5" y="2.5" width="14" height="19" rx="2"/><circle cx="12" cy="10" r="3.2"/><path d="M9 17h6"/>',
 "train": '<rect x="5" y="3" width="14" height="14" rx="3"/><path d="M5 10h14M8.5 21l2-4M15.5 21l-2-4"/><circle cx="9" cy="13.5" r=".6"/><circle cx="15" cy="13.5" r=".6"/>',
 "boat": '<path d="M3 15l2 5h14l2-5z"/><path d="M12 3v12M12 4l6 9h-6"/>',
 "rupee": '<path d="M7 4h10M7 8.5h10M7 4c6 0 6 9 0 9l8 7"/>',
 "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
 "phone": '<path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
 "pin": '<path d="M12 21s-7-7.2-7-12a7 7 0 0 1 14 0c0 4.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
 "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
 "cash": '<rect x="2.5" y="6" width="19" height="12" rx="2"/><circle cx="12" cy="12" r="2.6"/><path d="M6 9v.01M18 15v.01"/>',
 "plug": '<path d="M9 2v6M15 2v6M6 8h12v4a6 6 0 0 1-12 0zM12 18v4"/>',
 "wifi": '<path d="M2 9a15 15 0 0 1 20 0M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0"/><circle cx="12" cy="19.5" r=".8"/>',
 "heart": '<path d="M12 20s-7.5-4.6-9-9.5C2 6.9 4.3 4.5 7 4.5c2 0 3.4 1.2 5 3 1.6-1.8 3-3 5-3 2.7 0 5 2.4 4 6-1.5 4.9-9 9.5-9 9.5z"/>',
 "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
 "camera": '<path d="M3 8a2 2 0 0 1 2-2h2.5L9 4h6l1.5 2H19a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><circle cx="12" cy="13" r="3.8"/>',
 "jacket": '<path d="M8 3l4 3 4-3 4 3v15h-5v-8h-6v8H4V6z"/>',
 "shoe": '<path d="M3 16v-5c2 0 3-1 4-3l5 3 4 1c3 .6 5 2 5 4v1z"/><path d="M3 19h18"/>',
 "umbrella": '<path d="M3 12a9 9 0 0 1 18 0z"/><path d="M12 12v7a2 2 0 0 0 4 0"/>',
 "pill": '<rect x="3" y="8" width="18" height="8" rx="4" transform="rotate(-35 12 12)"/><path d="M9.5 8.5l5 7"/>',
 "glasses": '<circle cx="6.5" cy="14" r="3.5"/><circle cx="17.5" cy="14" r="3.5"/><path d="M10 14h4M3 13l2-6M21 13l-2-6"/>',
 "bag": '<path d="M5 8h14l-1 13H6z"/><path d="M9 8a3 3 0 0 1 6 0"/>',
 "doc": '<path d="M6 2.5h8l4 4V21H6z"/><path d="M14 2.5v4h4M9 12h6M9 16h6"/>',
 "bank": '<path d="M3 9.5L12 4l9 5.5M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 20.5h18"/>',
 "card": '<rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="M2.5 10h19M6 15h4"/>',
 "calendar": '<rect x="3" y="4.5" width="18" height="16" rx="2"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/>',
 "refresh": '<path d="M20 11a8 8 0 0 0-14.9-3.5M4 4v4h4M4 13a8 8 0 0 0 14.9 3.5M20 20v-4h-4"/>',
 "cloud": '<path d="M7 18a4.5 4.5 0 0 1-.5-9 6 6 0 0 1 11.5 1.5A3.8 3.8 0 0 1 17.5 18z"/><path d="M9 21l1-2M13 21l1-2"/>',
 "percent": '<path d="M19 5L5 19"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/>',
 "group": '<circle cx="8" cy="9" r="3"/><circle cx="16.5" cy="9.5" r="2.5"/><path d="M2.5 20a5.5 5.5 0 0 1 11 0M13.5 20a4.5 4.5 0 0 1 8 0"/>',
 "flag": '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
 "music": '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
 "senior": '<circle cx="10" cy="5" r="2.5"/><path d="M10 8v6l-3 7M10 14l3 7M7 11h6M16 10v11"/>',
}
SPARK = ('<svg class="spark" viewBox="0 0 40 40"><g stroke="#F28C28" stroke-width="2" stroke-linecap="round">'
         + "".join(f'<line x1="20" y1="20" x2="{20+15*math.cos(a):.1f}" y2="{20+15*math.sin(a):.1f}"/>' for a in [i*math.pi/6 for i in range(12)])
         + '</g><circle cx="20" cy="20" r="3" fill="#E8445A"/></svg>')
STAR4 = '<svg class="st4" viewBox="0 0 20 20"><path d="M10 0C11 7 13 9 20 10 13 11 11 13 10 20 9 13 7 11 0 10 7 9 9 7 10 0z" fill="#F28C28"/></svg>'

def footer(dark=False):
    return (f'<div class="foot"><svg viewBox="0 0 800 70" preserveAspectRatio="none">'
            '<path fill="#F28C28" d="M0,34 C120,18 210,40 330,26 C470,8 600,38 800,16 L800,70 L0,70Z"/>'
            '<path fill="#2A0D3D" d="M30,44 C170,26 300,50 430,34 C560,18 680,44 790,30 L800,70 L0,70Z"/></svg>'
            f'<span>{C["web1"]} &nbsp;·&nbsp; {C["phone"]}</span></div>')

def logos():
    return f'<div class="lg"><img src="{LOGO_HK}"><img src="{LOGO_PK}"></div>'

def page(body, cls="", bg=None, bgh="45%", pos="50% 50%"):
    bgp = f'<div class="bgph" style="height:{bgh}"><img src="{IMG(bg)}" style="object-position:{pos}"></div>' if bg else ""
    return f'<section class="page {cls}">{bgp}{logos() if "cover" not in cls and "back" not in cls else ""}{body}{footer()}</section>'

def title(main, sub=None, script=None, align="center"):
    s = f'<div class="script">{E(script)}</div>' if script else ""
    sb = f'<div class="ribbon">{E(sub)}</div>' if sub else ""
    return f'<div class="ttl" style="text-align:{align}">{s}<h1>{main}</h1>{sb}</div>'

# ---------- 1 cover ----------
def cover():
    circ = "".join(f'<div class="cc"><img src="{IMG(k)}"><span>{E(t)}</span></div>' for k, t in
                   [("towerbridge", "London"), ("colosseum", "Rome"), ("titlis", "Swiss Alps"), ("venice", "Venice")])
    return f'''<section class="page cover">
<div class="cv"><img src="{IMG("eiffel")}"></div><div class="cvshade"></div>
<div class="cvtop"><div class="lgw"><img src="{LOGO_HK}"></div><img class="seal" src="{SEAL}"><div class="lgw"><img src="{LOGO_PK}"></div></div>
<div class="cvt"><div class="cvs">London &amp;</div><div class="cvb">EUROPE</div>
<div class="cvr">Grand Tour 2027</div></div>
<div class="cvbot"><div class="cvd"><span>{E(PK["dates"])}</span><b>{E(PK["duration"])}</b></div>
<div class="cvc">8 Countries · 60+ Attractions · 11 UNESCO Sites</div>
<div class="ccs">{circ}</div>
<div class="cvp"><small>All-inclusive, per person</small><b>{E(PK["price"])}</b><em>incl. international flights &amp; visas · {E(PK["gst_note"])}</em></div></div>
{footer()}</section>'''

# ---------- 2 departure ----------
def departure():
    fl = "".join(f'<div class="frow"><div class="fi">{ic(I["plane"],"#fff")}</div><div>{E(x)}</div></div>' for x in PK["flights"])
    why = [w for w in PK["why"]]
    wl = "".join(f'<li><span class="bul">{ic(I["check"],"#fff",2.4)}</span><b>{E(a)}</b> – {E(b)}</li>' for a, b in why)
    return page(f'''{STAR4.replace('class="st4"','class="st4" style="left:30mm;top:52mm"')}
<div class="planeimg">{ic(I["plane"],"#3A1452",1.2)}</div>
{title("DEPARTURE DATE", "FROM HYDERABAD & BANGALORE")}
<div class="sub2">London &amp; Europe Grand Tour · Group Departure</div>
<div class="card datebox"><div class="mon">APRIL – MAY 2027</div>
<div class="dates2"><div><small>Departure</small><b>Sat 17 April</b></div><div class="arrow">→</div><div><small>Return</small><b>Sun 2 May</b><em>landing Mon 3 May</em></div></div>
<div class="dur">{E(PK["duration"])} · 8 Countries</div></div>
<div class="card flights"><div class="ch">{ic(I["plane"],"#F28C28")} Flights · booked by us</div>{fl}</div>
<div class="pillh">Why travel with us?</div>
<div class="card whycard"><ul class="why2">{wl}</ul></div>''', bg="lucerne2", bgh="40%")

# ---------- 3 route map ----------
CITIES = [("London", -0.13, 51.51, "stay", "3N"), ("Dover", 1.31, 51.13, "stop", ""), ("Calais", 1.86, 50.95, "stop", ""),
          ("Paris", 2.35, 48.86, "stay", "2N"), ("Brussels", 4.35, 50.85, "stay", "1N"), ("Ardennes", 5.46, 50.35, "stop", ""),
          ("Amsterdam", 4.90, 52.37, "stay", "1N"), ("Keukenhof", 4.55, 52.27, "stop", ""), ("Cologne", 6.96, 50.94, "stay", "1N"),
          ("Black Forest", 8.15, 47.90, "stay", "1N"), ("Rhine Falls", 8.61, 47.68, "stop", ""), ("Zurich", 8.54, 47.37, "stay", "1N"),
          ("Lucerne", 8.31, 47.05, "stop", ""), ("Titlis", 8.40, 46.78, "stop", ""), ("Interlaken", 7.86, 46.69, "stay", "1N"),
          ("Lake Como", 9.08, 45.85, "stop", ""), ("Milan", 9.19, 45.46, "stay", "1N"), ("Padova", 11.88, 45.41, "stop", ""),
          ("Venice", 12.33, 45.44, "stay", "1N"), ("Rome & Vatican", 12.48, 41.90, "stop", ""), ("Florence", 11.26, 43.77, "stay", "1N"),
          ("Pisa", 10.40, 43.72, "stop", ""), ("Milan Malpensa", 8.72, 45.63, "stay", "1N")]
ROUTE = [("London", "Dover", "c"), ("Dover", "Calais", "f"), ("Calais", "Paris", "c"), ("Paris", "Brussels", "c"),
         ("Brussels", "Ardennes", "c"), ("Ardennes", "Amsterdam", "c"), ("Amsterdam", "Keukenhof", "c"), ("Keukenhof", "Cologne", "c"),
         ("Cologne", "Black Forest", "c"), ("Black Forest", "Rhine Falls", "c"), ("Rhine Falls", "Zurich", "c"), ("Zurich", "Titlis", "c"),
         ("Titlis", "Lucerne", "c"), ("Lucerne", "Interlaken", "t"), ("Interlaken", "Lake Como", "c"), ("Lake Como", "Milan", "c"),
         ("Milan", "Padova", "c"), ("Padova", "Venice", "c"), ("Venice", "Rome & Vatican", "t"), ("Rome & Vatican", "Florence", "t"),
         ("Florence", "Pisa", "c"), ("Pisa", "Milan Malpensa", "c")]
LBL = {"London": (-12, -14, "end"), "Dover": (-8, 26, "end"), "Calais": (10, 26, "start"), "Paris": (-12, 6, "end"),
       "Brussels": (-10, -12, "end"), "Ardennes": (12, 14, "start"), "Amsterdam": (12, -10, "start"), "Keukenhof": (-12, -2, "end"),
       "Cologne": (14, 4, "start"), "Black Forest": (-12, 6, "end"), "Rhine Falls": (14, -6, "start"), "Zurich": (14, 8, "start"),
       "Lucerne": (-12, -4, "end"), "Titlis": (14, 10, "start"), "Interlaken": (-12, 6, "end"), "Lake Como": (14, -8, "start"),
       "Milan": (-6, 30, "end"), "Padova": (4, 32, "middle"), "Venice": (-4, -18, "middle"), "Rome & Vatican": (-14, 8, "end"),
       "Florence": (14, 2, "start"), "Pisa": (-12, 6, "end"), "Milan Malpensa": (-14, 8, "end")}
def routemap():
    P = json.load(open(os.path.join(HERE, "map_proj.json")))
    K = math.cos(math.radians(48))
    def xy(lon, lat): return ((lon - P["LON0"]) / (P["LON1"] - P["LON0"]) * P["W"], (P["LAT1"] - lat) / (P["LAT1"] - P["LAT0"]) * P["H"])
    pos = {n: xy(lo, la) for n, lo, la, _, _ in CITIES}
    seg = ""
    for a, b, m in ROUTE:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        mx, my = (x1 + x2) / 2 + (y2 - y1) * .12, (y1 + y2) / 2 - (x2 - x1) * .12
        st = {"c": 'stroke="#2A0D3D" stroke-width="5"', "f": 'stroke="#1C7FC4" stroke-width="5" stroke-dasharray="10 8"',
              "t": 'stroke="#E8445A" stroke-width="5" stroke-dasharray="3 9" stroke-linecap="round"'}[m]
        seg += f'<path d="M{x1:.0f},{y1:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}" fill="none" {st}/>'
    pins = ""
    for n, lo, la, kind, nt in CITIES:
        x, y = pos[n]; dx, dy, an = LBL[n]
        if kind == "stay":
            pins += (f'<g transform="translate({x:.0f},{y:.0f})"><path d="M0,0 C-14,-18 -14,-34 0,-34 C14,-34 14,-18 0,0Z" fill="#E8445A" stroke="#fff" stroke-width="3"/>'
                     f'<circle cx="0" cy="-23" r="5.5" fill="#fff"/></g>')
        else:
            pins += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="8" fill="#F28C28" stroke="#fff" stroke-width="3"/>'
        lab = E(n) + (f" · {nt}" if nt else "")
        pins += (f'<text x="{x+dx:.0f}" y="{y+dy:.0f}" text-anchor="{an}" class="mapml {"mapmls" if kind=="stay" else ""}" '
                 f'paint-order="stroke" stroke="#fff" stroke-width="7" stroke-linejoin="round">{lab}</text>')
    cn = [("UNITED KINGDOM", -2.6, 53.2), ("FRANCE", 1.2, 46.9), ("BELGIUM", 4.4, 49.85), ("NETHERLANDS", 6.6, 53.45),
          ("GERMANY", 10.2, 51.2), ("SWITZERLAND", 9.9, 46.55), ("ITALY", 12.6, 43.1), ("VATICAN", 11.4, 41.2)]
    cl = "".join(f'<text x="{xy(lo,la)[0]:.0f}" y="{xy(lo,la)[1]:.0f}" class="mapcn">{t}</text>' for t, lo, la in cn)
    svg = (f'<svg viewBox="0 0 {P["W"]} {P["H"]}" class="ov" preserveAspectRatio="xMidYMid slice"><style>.mapml{{font:700 22px Montserrat;fill:#2A0D3D}}.mapmls{{font-size:25px;fill:#3A1452}}'
           f'.mapcn{{font:800 20px Montserrat;fill:#E8445A;opacity:.55;letter-spacing:3px;text-anchor:middle}}</style>{cl}{seg}{pins}</svg>')
    leg = "".join(f'<div class="li"><span class="lk {k}"></span>{t}</div>' for k, t in
                  [("pin", "Overnight stay"), ("dot", "Sightseeing stop"), ("coach", "Private coach"), ("ferry", "Channel ferry"), ("train", "Train")])
    return page(f'''{title("ROUTE MAP", "8 COUNTRIES · ONE SMOOTH JOURNEY", script="Your journey")}
<div class="map"><img src="{MAP}">{svg}</div>
<div class="legend card">{leg}</div>
<div class="mapnote card"><b>Start:</b> London (flights from Hyderabad &amp; Bangalore) &nbsp;→&nbsp; <b>End:</b> Milan Malpensa (flights home) &nbsp;·&nbsp; about 4,000 km by coach</div>''')

# ---------- 4 wonders & attractions ----------
def wonders():
    a = PK["attractions"]
    w = "".join(f'<div class="wc"><img src="{IMG(k)}"><div class="wcb">{E(b)}</div><b>{E(t)}</b></div>' for k, t, b in a["wonders"])
    cicons = {"United Kingdom": "flag", "France": "star", "Belgium": "camera", "Netherlands": "heart", "Germany": "pin",
              "Switzerland": "sun", "Italy": "globe", "Vatican City": "ticket"}
    cs = "".join(f'<div class="cy"><div class="cyh"><span class="cyi">{ic(I[cicons.get(c,"star")],"#fff")}</span><b>{E(c)}</b><em>{len(it)}</em></div>'
                 f'<p>{" · ".join(E(x) for x in it)}</p></div>' for c, it in a["countries"])
    total = sum(len(i) for _, i in a["countries"])
    un = "".join(f"<span>{E(x)}</span>" for x in a["unesco"])
    return page(f'''{title(f"{total} ATTRACTIONS", "IN 8 COUNTRIES · ALL INCLUDED", script="Wonders of the world")}
<div class="wons">{w}</div><div class="cys">{cs}</div>
<div class="unesco"><b>{len(a["unesco"])} UNESCO World Heritage Sites on this tour</b><div>{un}</div></div>''')

# ---------- day pages ----------
STAYS = {d["n"]: d["stay"] for d in PK["daypages"]}
def meals(n):
    ms = []
    for r in ROWS:
        if r[0] == n and r[3] in ("Breakfast", "Lunch", "Dinner") and r[3] not in ms: ms.append(r[3])
    return ms
def daycard(n, side):
    t, k, bl = DAYS[n - 1]
    stay = STAYS.get(n)
    items = "".join(f"<li>{E(x)}</li>" for x in bl) + (f'<li class="ov">Overnight stay: <b>{E(stay)}</b></li>' if stay else "")
    ml = "".join(f'<span class="meal">{ic(I["food"],"#E8445A")}{m}</span>' for m in meals(n))
    from datetime import date, timedelta
    d = date(2027, 4, 17) + timedelta(n - 1)
    return (f'<div class="dc {side}"><div class="dtab"><small>DAY</small><b>{n:02d}</b></div>'
            f'<div class="dhd"><h2>{E(t)}</h2><div class="ddt">{d.strftime("%a %d %b %Y")}</div></div><ul>{items}</ul>'
            f'<div class="meals">{ml}</div></div>')
def daypage(a, b):
    ka, kb = DAYS[a - 1][1], DAYS[b - 1][1]
    return page(f'''<div class="drow r1">{daycard(a,"l")}<div class="dph"><img src="{IMG(ka)}"><span>{E(cap(ka))}</span></div></div>
<div class="drow r2"><div class="dph"><img src="{IMG(kb)}"><span>{E(cap(kb))}</span></div>{daycard(b,"r")}</div>
{SPARK.replace('class="spark"','class="spark" style="right:14mm;top:150mm"')}''', cls="dpage", bg=DAYBG[a], bgh="32%")
DAYBG = {1: "westminster2", 3: "towerbridge", 5: "eiffelnight", 7: "zaanse", 9: "lucerne", 11: "como2", 13: "trevi", 15: "pontevecchio"}
CAPS = json.load(open(os.path.join(WD, "imgmap.json")))
def cap(k): return CAPS.get(k, {}).get("cap", k.title())

# ---------- stays ----------
STAYIMG = [("London", "Wembley", "3 Nights", "towerbridge"), ("Paris", "", "2 Nights", "eiffelnight"), ("Brussels", "", "1 Night", "atomium"),
           ("Amsterdam", "", "1 Night", "amsterdam"), ("Cologne", "", "1 Night", "cologne2"), ("Black Forest", "Titisee", "1 Night", "rhinefalls2"),
           ("Zurich", "", "1 Night", "zurich"), ("Interlaken", "", "1 Night", "interlaken"), ("Milan", "", "1 Night", "milan2"),
           ("Venice", "Mestre", "1 Night", "venice2"), ("Florence", "", "1 Night", "florence"), ("Milan Malpensa", "Airport area", "1 Night", "como2")]
def stays():
    cards = "".join(f'<div class="sc"><div class="sci"><img src="{IMG(k)}"><span class="scn">{E(n)}</span></div>'
                    f'<div class="scb"><b>{E(c)}</b>{f"<small>{E(s)}</small>" if s else ""}</div></div>' for c, s, n, k in STAYIMG)
    return page(f'''{title("YOUR STAY", "15 NIGHTS · 12 HANDPICKED HOTELS", script="Rest well, travel far")}
<div class="card stnote">{ic(I["bed"],"#E8445A")}<div>Comfortable hotels checked and approved by our team, <b>twin sharing</b>, with hot Indian vegetarian breakfast and dinner. Hotels are chosen close to the sights so you spend less time on the road.</div></div>
<div class="scs">{cards}</div>''', bg="como", bgh="22%")

# ---------- price ----------
def price():
    rows = "".join(f'<tr><td>{ic(I["pin"],"#E8445A")} {E(c)}{f" <small>({E(s)})</small>" if s else ""}</td><td>{E(n)}</td></tr>' for c, s, n, _ in STAYIMG)
    return page(f'''{title("YOUR PACKAGE PRICE", "ONE PRICE · EVERYTHING INCLUDED")}
<div class="pgrid"><div class="card ptab"><div class="pth">{ic(I["bed"],"#fff")} Hotels &amp; nights</div>
<table><tr><th>Destination</th><th>Stay</th></tr>{rows}</table></div>
<div><div class="pc"><div class="pcl">All-inclusive<br><small>per person · twin sharing</small></div><div class="pcv">{E(PK["price"])}</div></div>
<div class="pc2"><div>{ic(I["percent"],"#fff")}<span>+ 5% GST</span></div><div>{ic(I["rupee"],"#fff")}<span>+ 2% TCS</span></div></div>
<div class="card pin">{ic(I["shield"],"#1F6B4F")}<div><b>Includes international flights &amp; visas.</b> The 2% TCS is credited back to you through your income-tax return.</div></div>
<div class="card pin">{ic(I["calendar"],"#E8445A")}<div><b>{E(PK["dates_long"])}</b><br>{E(PK["seats_note"])}</div></div>
<div class="card pin">{ic(I["phone"],"#3A1452")}<div>Call <b>{C["phone"]}</b> to book your seat</div></div></div></div>''', bg="titlis", bgh="30%")

# ---------- inclusions ----------
def incl():
    iic = ["plane", "passport", "bed", "food", "bus", "ticket", "user", "boat"]
    inc = "".join(f'<li><span>{ic(I[iic[i % len(iic)]],"#1F6B4F")}</span>{E(x)}</li>' for i, x in enumerate(PK["incl"]))
    eic = ["rupee", "bag", "x"]
    exc = "".join(f'<li><span>{ic(I[eic[i % len(eic)]],"#E8445A")}</span>{E(x)}</li>' for i, x in enumerate(PK["excl"]))
    return page(f'''<div class="ietitle"><h1>Inclusions <em>&amp;</em><br>Exclusions</h1><div class="ftr">FOR YOUR TRIP</div></div>
<div class="iegrid"><div class="iec inc"><div class="ieh">{ic(I["check"],"#fff",2.6)} INCLUSIONS</div><ul>{inc}</ul></div>
<div class="iec exc"><div class="ieh">{ic(I["x"],"#fff",2.6)} EXCLUSIONS</div><ul>{exc}</ul>
<div class="meal2">{ic(I["food"],"#E8445A")}<p>{E(PK["meal_note"])}</p></div></div></div>
<div class="script big2">Explore with Confidence</div>''', bg="venice", bgh="30%")

# ---------- tips ----------
PRACT = [("sun", "Weather in late April", "15–21 °C by day and 6–11 °C at night, with some rain. Titisee mornings are near freezing and the Titlis summit is below zero with snow. Sunset is after 8 pm."),
         ("cash", "Currency", "UK: pound (£). France, Belgium, Netherlands, Germany, Italy and the Vatican: euro (€). Switzerland: Swiss franc. Carry a multi-currency forex card and a little cash."),
         ("plug", "Power plugs", "UK: 3-pin (Type G). Europe: 2 round pins (Type C/F). Switzerland: Type J (Type C fits). Carry a universal adapter and a power bank."),
         ("wifi", "Mobile & data", "Take an international roaming pack or a Europe + UK eSIM, and check that Switzerland is covered. WhatsApp is our group channel."),
         ("clock", "Time zones", "UK is 4 h 30 m behind India; France to Italy are 3 h 30 m behind."),
         ("senior", "Senior citizens", "Seats near the front, wheelchairs booked at the Louvre, Vatican and airports, extra rest stops and lifts wherever available."),
         ("cash", "Water & toilets", "Tap water is drinkable in most places. Public toilets often charge €0.50–€1; use restaurant and museum toilets."),
         ("bag", "Shopping", "Paris perfumes, Swiss chocolates and watches, cuckoo clocks in Titisee, leather in Florence, Murano glass in Venice. Ask for tax-free forms.")]
def tips():
    pr = "".join(f'<div class="tp"><span>{ic(I[i],"#fff")}</span><div><b>{E(t)}</b><p>{E(x)}</p></div></div>' for i, t, x in PRACT)
    dos = "".join(f'<li>{E(x)}</li>' for x in PK["dos"]); dn = "".join(f'<li>{E(x)}</li>' for x in PK["donts"])
    return page(f'''{title("IMPORTANT TIPS", "GOOD TO KNOW BEFORE YOU GO")}
<div class="tps">{pr}</div>
<div class="dd"><div class="card do"><h3>{ic(I["check"],"#1F6B4F",2.6)} Do's</h3><ul>{dos}</ul></div>
<div class="card dont"><h3>{ic(I["x"],"#E8445A",2.6)} Don'ts</h3><ul>{dn}</ul></div></div>''', bg="lucerne", bgh="18%")

# ---------- carry ----------
CARRY = [("passport", "Passport, visa copies & photo ID"), ("jacket", "Warm jacket, gloves & woollen cap (for Titlis)"),
         ("shoe", "Comfortable walking shoes, already broken in"), ("umbrella", "Raincoat or umbrella"),
         ("pill", "Personal medicines with prescriptions"), ("plug", "Universal plug adapter & power bank"),
         ("glasses", "Sunglasses, cap & sunscreen"), ("bag", "Small day-bag for sightseeing"),
         ("cash", "Forex card & a little cash"), ("camera", "Camera or phone with free storage")]
def carry():
    ls = "".join(f'<div class="cr"><span>{ic(I[i],"#E8445A")}</span>{E(t)}</div>' for i, t in CARRY)
    return page(f'''<div class="carryl"><img src="{IMG("titlis")}"></div>
<div class="carryr">{title("Things to", None, None, "left").replace("<h1>","<h1 class=thg>")}<div class="script carrys">Carry</div>
<div class="crs">{ls}</div>
<div class="card crn">{ic(I["star"],"#F28C28")}<div><b>Dress code:</b> shoulders and knees covered for churches and the Vatican; no caps inside.</div></div></div>''', cls="carry")

# ---------- why ----------
WHYI = ["ticket", "food", "user", "senior", "passport", "group", "shield"]
def why():
    ws = "".join(f'<div class="wy"><span>{ic(I[WHYI[i]],"#fff")}</span><div><b>{E(a)}</b><p>{E(b)}</p></div></div>' for i, (a, b) in enumerate(PK["why"]))
    ex = "".join(f'<div class="ex"><span>{ic(I[k],"#E8445A")}</span>{E(x)}</div>' for k, x in zip(["music", "doc", "bed", "clock", "senior", "food"], PK["experiences"]))
    mo = os.path.join(SKILL, "assets", "img")
    return page(f'''<div class="whyt"><div class="script">Why</div><h1>CHOOSE US</h1><div class="wsub">TRUSTED BY FAMILIES · CHOSEN FOR MEMORIES</div></div>
<div class="wys">{ws}</div><div class="exs">{ex}</div>
<div class="mos"><div><img src="{rel(os.path.join(mo,"moments1.jpg"))}"><span>Moments from our past tours</span></div>
<div><img src="{rel(os.path.join(mo,"moments2.jpg"))}"><span>Travellers with Punya Kshetras</span></div></div>''', cls="whyp")

# ---------- payments ----------
VISA = [("Passport", "valid 3+ months after 3 May 2027, 2 blank pages, plus old passports"),
        ("Photos", "35 × 45 mm, white background, 2 copies (Schengen size)"),
        ("Income-tax returns", "ITR-V for the last 3 financial years"),
        ("Bank statement", "last 3 months, sealed and signed by the bank"),
        ("If employed", "3 months' salary slips and a leave letter"),
        ("Covering letter", "from you or your company")]
def payments():
    vs = "".join(f'<li><b>{E(a)}</b> – {E(b)}</li>' for a, b in VISA)
    return page(f'''<div class="ept"><h1>Easy Booking</h1><div class="eps">Hassle-free travel</div></div>
<div class="pillh" style="margin-top:4mm">Payment terms</div>
<div class="pts"><div class="card pt">{ic(I["rupee"],"#E8445A")}<div><b>Advance payment</b><p>Your seat is confirmed when the advance is received.</p></div></div>
<div class="card pt">{ic(I["calendar"],"#E8445A")}<div><b>Balance payment</b><p>Full and final payment before departure.</p></div></div></div>
<div class="pmgrid"><div class="card pm"><div class="pmh">{ic(I["bank"],"#fff")} Payment methods</div>
<div class="pmr">{ic(I["bank"],"#3A1452")} Bank transfer</div><div class="pmr">{ic(I["phone"],"#3A1452")} UPI</div>
<div class="pmr">{ic(I["doc"],"#3A1452")} Cheque</div><div class="pmr">{ic(I["cash"],"#3A1452")} Cash</div>
<div class="pmr note">{ic(I["card"],"#E8445A")} Card payments carry 2% extra</div></div>
<div class="card pm"><div class="pmh">{ic(I["phone"],"#fff")} Book your seat</div>
<div class="pmr big">{ic(I["phone"],"#E8445A")} {C["phone"]}</div><div class="pmr">{ic(I["mail"],"#3A1452")} {C["email"]}</div>
<div class="pmr">{ic(I["globe"],"#3A1452")} {C["web1"]}</div><div class="pmr">{ic(I["globe"],"#3A1452")} {C["web2"]}</div>
<div class="pmr note">Bank details are shared on confirmation by our team.</div></div></div>
<div class="pillh">Documents for your visa</div>
<div class="card visa"><ul>{vs}</ul><p>We guide you through the UK and Schengen visa paperwork step by step. Visa fees are included.</p></div>''', bg="florence2", bgh="22%")

# ---------- cancellation ----------
def cancel():
    em = C["cancel_email"]
    cs = [("doc", "Cancellation requests must be sent in writing to " + em + "."),
          ("calendar", "More than 45 days before travel: 30% of the tour cost is retained, 70% refunded."),
          ("clock", "45 to 30 days before travel: 50% of the tour cost is retained."),
          ("x", "Less than 30 days, no-show, or after the tour starts: no refund."),
          ("refresh", "Rescheduling is allowed once, subject to availability, on payment of 10% of the tour cost, if requested at least 7 days before travel."),
          ("rupee", "Refunds are paid after 30 days of cancellation. If we cancel the tour, the amount paid is refunded in full.")]
    cc = "".join(f'<div class="cn"><span class="cni">{ic(I[i],"#fff",2.1)}</span><span class="cnn">{n+1:02d}</span><p>{E(t)}</p></div>' for n, (i, t) in enumerate(cs))
    return page(f'''<div class="cpt"><h1>Cancellation</h1><div class="script">Policy</div></div><div class="cns">{cc}</div>''', bg="pontevecchio", bgh="24%")

# ---------- terms ----------
def terms():
    skip = {"Cancellation by yatri", "Rescheduling"}
    ts = [(a, b.format(**C)) for a, b in B.TERMS if a not in skip] + list(PK["extra_terms"])
    ts = [(a, b.replace("yatris", "travellers").replace("yatri", "traveller").replace("yatra", "tour")) for a, b in ts]
    tl = "".join(f'<div class="tc"><span>{n+1:02d}</span><p><b>{E(a)}.</b> {E(b)}</p></div>' for n, (a, b) in enumerate(ts))
    return page(f'''<div class="tct"><h1>Terms &amp;</h1><div class="tcc">Conditions</div></div><div class="tcs">{tl}</div>''', bg="stpeters2", bgh="18%")

# ---------- back ----------
def back():
    return f'''<section class="page back"><div class="cv"><img src="{IMG("towerbridge")}"></div><div class="bkshade"></div>
<div class="bk"><div class="bklg"><div class="lgw"><img src="{LOGO_HK}"></div><div class="lgw"><img src="{LOGO_PK}"></div></div>
<div class="script bks">Explore with Confidence</div>
<div class="bkl">For details &amp; registration</div>
<div class="bkp">{ic(I["phone"],"#F6D58B")} {C["phone"]}</div>
<div class="bki">{C["email"]}</div><div class="bki">{C["web1"]} · {C["web2"]}</div><div class="bki gold">{E(C["social_line"])}</div>
<div class="bka">{E(C["address"])}</div>
<div class="bkf">{E(PK["title"])} {E(PK["title2"])} · {E(PK["dates"])} · {E(PK["price"])} per person, all-inclusive</div></div>
{footer()}</section>'''

CSS = open(os.path.join(HERE, "kh.css")).read()
def build():
    pages = [cover(), departure(), routemap(), wonders()]
    for a in range(1, 17, 2): pages.append(daypage(a, a + 1))
    pages += [stays(), price(), incl(), tips(), carry(), why(), payments(), cancel(), terms(), back()]
    doc = (f'<!doctype html><html><head><meta charset="utf-8"><title>{E(PK["title"])} {E(PK["title2"])}</title>'
           f'<link rel="stylesheet" href="{FONTS}"><style>{CSS}</style></head><body>{"".join(pages)}</body></html>')
    open(os.path.join(HERE, "brochure_kh.html"), "w").write(doc)
    print("wrote brochure_kh.html,", len(pages), "pages")

if __name__ == "__main__":
    build()
