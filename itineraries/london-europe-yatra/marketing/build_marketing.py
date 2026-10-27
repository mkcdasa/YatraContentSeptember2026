"""
Posters and brochure for the London Europe Yatra 2027 (English).

Writes HTML into marketing/html/, then render.js turns it into JPG posters and
PDFs in marketing/out/. Facts come from itinerary_data.py so the marketing never
drifts from the plan: edit the data, re-run both scripts.

    python3 marketing/build_marketing.py && node marketing/render.cjs
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import itinerary_data as D  # noqa: E402

HTML_DIR = os.path.join(HERE, "html")

PRICE = "₹5,49,000"
GST = round(D.PRICE_PP * 0.05)
SUBTOTAL = D.PRICE_PP + GST
TCS = round(SUBTOTAL * 0.02)
PHONE = "+91 95053 88886"
WEB = "www.punyakshetras.com · www.hkmhyderabad.org"
ORG = "Hare Krishna Golden Temple, Banjara Hills, Hyderabad"


def inr(n):
    s = str(int(n))
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return "₹" + ",".join(parts + [tail]) if parts else "₹" + tail


COUNTRIES = ["United Kingdom", "France", "Belgium", "Netherlands", "Germany", "Switzerland", "Italy", "Vatican City"]

TEMPLES = ["Bhaktivedanta Manor, Watford", "ISKCON Soho, London", "ISKCON Paris", "Radhadesh, Belgium",
           "ISKCON Cologne", "Goloka Dham, Germany", "ISKCON Zurich", "Villaggio Hare Krishna, Italy",
           "Prabhupada Desh, Italy", "Villa Vrindavan, Florence"]

WONDERS = ["Changing of the Guard & Tower of London (Koh-i-Noor)", "London Eye & Thames cruise",
           "Eiffel Tower, Louvre & Seine cruise", "Keukenhof tulips & Dutch windmills",
           "Mount Titlis snow & Lake Lucerne", "Rhine Falls & the Black Forest",
           "Venice gondola ride", "Vatican, Sistine Chapel & Colosseum", "Florence & Leaning Tower of Pisa"]

# day, short route for the at-a-glance list, brochure description
DAY_TEXT = [
    (1, "Fly to London", "Hyderabad group flies Emirates via Dubai (dep 04:40, arrive Heathrow 16:10); Bangalore group flies Etihad via Abu Dhabi (dep 10:00, arrive 18:45). Kamada Ekadasi: fruit meals on board. Welcome kirtan and dinner at the hotel."),
    (2, "Akshaya Patra · Bhaktivedanta Manor · Madame Tussauds · ISKCON Soho", "Visit the Akshaya Patra kitchen in Watford, then Bhaktivedanta Manor for darshan of Sri Sri Radha-Gokulananda, the Sunday programme and feast prasadam. Afternoon at Madame Tussauds; evening arati at ISKCON Soho, where Srila Prabhupada installed Radha-Londonishvara in 1969; stroll through Covent Garden."),
    (3, "Royal London: Guard · Tower & Koh-i-Noor · Thames · London Eye", "Changing of the Guard at Buckingham Palace and The King's Gallery; the Tower of London with the Crown Jewels and the Koh-i-Noor; a walk on Tower Bridge; a Thames boat ride; the London Eye at sunset; Big Ben and the Houses of Parliament."),
    (4, "Dover ferry → Calais → Paris", "Coach to Dover and the ferry across the English Channel past the White Cliffs, then on through France to Paris. Balarama Rasayatra kirtan on the way."),
    (5, "Paris: Eiffel Tower · Notre-Dame · ISKCON Paris · Seine", "Arc de Triomphe and the Champs-Élysées, the Eiffel Tower (2nd floor), Notre-Dame, darshan at ISKCON Paris and an evening cruise on the Seine."),
    (6, "Louvre → Brussels", "Morning at the Louvre (Mona Lisa), then Brussels: the Atomium, the Grand Place and Manneken Pis."),
    (7, "Radhadesh → Amsterdam canal cruise", "Darshan and prasadam at ISKCON Radhadesh, a castle temple in the Ardennes hills; on to Amsterdam for an evening canal cruise."),
    (8, "Windmills · Keukenhof tulips → Cologne", "The windmills of Zaanse Schans and the Keukenhof tulip gardens at peak bloom; drive to Cologne."),
    (9, "Cologne · Goloka Dham → Black Forest", "Cologne Cathedral and ISKCON Cologne, then the Sunday programme and feast at Goloka Dham; evening in the Black Forest."),
    (10, "Titisee · Rhine Falls → Zurich", "Lake Titisee and the cuckoo-clock shops, the thundering Rhine Falls, Zurich and darshan at ISKCON Zurich."),
    (11, "Mount Titlis · Lucerne → Interlaken", "Snow on Mount Titlis by the rotating cable car; Lucerne's Lion Monument and Chapel Bridge; a lake cruise; scenic train to Interlaken."),
    (12, "Gotthard → Lake Como → Villaggio Hare Krishna", "Through the Swiss Alps and the Gotthard to Italy: a boat ride on Lake Como and darshan at Villaggio Hare Krishna; overnight Milan."),
    (13, "Milan · Prabhupada Desh · Padova · Venice", "Milan Cathedral, prasadam at ISKCON Prabhupada Desh, the Basilica of St Anthony in Padova and an evening in Venice: St Mark's Square and a gondola ride."),
    (14, "Rome by high-speed train: Vatican · Colosseum", "High-speed train to Rome: the Vatican Museums and Sistine Chapel, St Peter's Basilica, the Colosseum and the Trevi Fountain; train to Florence."),
    (15, "Florence · Villa Vrindavan · Pisa", "Florence (Duomo, Ponte Vecchio, Piazzale Michelangelo), prasadam at ISKCON Villa Vrindavan, the Leaning Tower of Pisa; farewell dinner near Milan Malpensa."),
    (16, "Fly home via Abu Dhabi", "Etihad from Milan Malpensa via Abu Dhabi; land in Hyderabad (02:45) and Bangalore (03:15) on Monday 3 May. Varuthini Ekadasi: fruit meals on board."),
]

# route map: (label, lat, lon, label side, label dy, minor) - minor labels are hidden on small maps
CITIES = [("London", 51.51, -0.13, "l", 0, False), ("Dover", 51.13, 1.31, "r", 0, True), ("Paris", 48.86, 2.35, "l", 0, False),
          ("Brussels", 50.85, 4.35, "r", 17, True), ("Radhadesh", 50.31, 5.45, "r", 12, True), ("Amsterdam", 52.37, 4.90, "r", 0, False),
          ("Cologne", 50.94, 6.96, "r", -4, False), ("Black Forest", 47.90, 8.15, "l", 0, True), ("Zurich", 47.37, 8.54, "r", -6, False),
          ("Lucerne", 47.05, 8.31, "r", 12, True), ("Interlaken", 46.69, 7.86, "l", 2, False), ("Lake Como", 45.81, 9.08, "r", -6, True),
          ("Milan", 45.46, 9.19, "r", 14, False), ("Venice", 45.44, 12.33, "r", 0, False), ("Rome", 41.90, 12.50, "r", 0, False),
          ("Florence", 43.77, 11.25, "r", 0, False), ("Pisa", 43.72, 10.40, "l", 0, False), ("Malpensa", 45.63, 8.72, "l", 0, None)]
ROUTE = ["London", "Dover", "Paris", "Brussels", "Radhadesh", "Amsterdam", "Cologne", "Black Forest", "Zurich",
         "Lucerne", "Interlaken", "Lake Como", "Milan", "Venice", "Rome", "Florence", "Pisa", "Malpensa"]
TRAIN_LEGS = {("Venice", "Rome"), ("Rome", "Florence")}
FERRY_LEGS = {("Dover", "Paris")}


def route_svg(w, h, dark=False):
    small = w < 420
    lat0, lat1, lon0, lon1 = 52.6, 41.7, -0.3, 12.7
    k = math.cos(math.radians(47))
    padl, padr, padt, padb = (62, 70, 26, 70) if small else (90, 100, 30, 70)
    s = min((w - padl - padr) / ((lon1 - lon0) * k), (h - padt - padb) / (lat0 - lat1))
    ox = padl + ((w - padl - padr) - (lon1 - lon0) * k * s) / 2
    oy = padt + ((h - padt - padb) - (lat0 - lat1) * s) / 2

    def xy(lat, lon):
        return ox + (lon - lon0) * k * s, oy + (lat0 - lat) * s

    pos = {c[0]: xy(c[1], c[2]) for c in CITIES}
    ink = "#F5E6C8" if dark else "#7A1F1F"
    soft = "rgba(245,230,200,.35)" if dark else "rgba(122,31,31,.25)"
    text = "#FFF8EC" if dark else "#3B1D12"
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg" font-family="Inter, sans-serif">']
    for a, b in zip(ROUTE, ROUTE[1:]):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        dash = ' stroke-dasharray="7 6"' if (a, b) in TRAIN_LEGS else ' stroke-dasharray="2 6"' if (a, b) in FERRY_LEGS else ""
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{ink}" stroke-width="3" stroke-linecap="round"{dash}/>')
    for name, lat, lon, side, dy, minor in CITIES:
        x, y = pos[name]
        big = name in ("London", "Paris", "Amsterdam", "Zurich", "Venice", "Rome", "Florence")
        r = 7 if big else 5
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#E8891D" stroke="{text}" stroke-width="2"/>')
        if minor is None or (minor and small):
            continue
        anchor = "end" if side == "l" else "start"
        dx = -11 if side == "l" else 11
        weight = 700 if big else 500
        size = (15 if small else 17) if big else (12.5 if small else 14)
        out.append(f'<text x="{x + dx:.1f}" y="{y + 5 + dy:.1f}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{text}">{name}</text>')
    out.append(f'<g font-size="13" fill="{text}"><line x1="16" y1="{h-46}" x2="46" y2="{h-46}" stroke="{ink}" stroke-width="3"/>'
               f'<text x="54" y="{h-41}">Coach</text>'
               f'<line x1="16" y1="{h-26}" x2="46" y2="{h-26}" stroke="{ink}" stroke-width="3" stroke-dasharray="7 6"/>'
               f'<text x="54" y="{h-21}">Train</text>'
               f'<line x1="110" y1="{h-26}" x2="140" y2="{h-26}" stroke="{ink}" stroke-width="3" stroke-dasharray="2 6"/>'
               f'<text x="148" y="{h-21}">Ferry</text></g>')
    out.append(f'<rect x="1" y="1" width="{w-2}" height="{h-2}" fill="none" stroke="{soft}" rx="14"/>')
    out.append("</svg>")
    return "".join(out)


LOTUS = ('<svg viewBox="0 0 120 60" width="{w}" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="{c}" stroke-width="2.2">'
         '<path d="M60 8 C48 22 48 40 60 54 C72 40 72 22 60 8Z"/>'
         '<path d="M60 54 C44 50 32 38 30 22 C44 26 54 36 60 54Z"/>'
         '<path d="M60 54 C76 50 88 38 90 22 C76 26 66 36 60 54Z"/>'
         '<path d="M60 54 C40 56 20 50 8 38 C26 34 46 42 60 54Z"/>'
         '<path d="M60 54 C80 56 100 50 112 38 C94 34 74 42 60 54Z"/></g></svg>')


def lotus(w=90, c="#C9A227"):
    return LOTUS.format(w=w, c=c)


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">')

BASE_CSS = """
:root{--maroon:#6B1414;--maroon2:#8E1F1A;--saffron:#E8891D;--gold:#C9A227;--gold2:#E9C86A;--cream:#FFF8EC;--ink:#2B1A12;--muted:#6E5A4B;}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,sans-serif;color:var(--ink);-webkit-font-smoothing:antialiased}
.serif{font-family:'Playfair Display',serif}
"""


def page(title, css, body):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>{FONTS}<style>{BASE_CSS}{css}</style></head><body>{body}</body></html>'


def contact_bar(dark=True):
    return (f'<div class="contact"><div><b>Call / WhatsApp</b> {PHONE}</div><div>{WEB}</div></div>')


def price_box():
    return (f'<div class="pricebox"><div class="pl">Yatra amount per person</div>'
            f'<div class="pv serif">{PRICE}</div>'
            f'<div class="pi">including international flights</div>'
            f'<div class="pt">+ 5% GST + 2% TCS*</div></div>')


# --------------------------------------------------------------------------- posters

POSTER_CSS = """
body{width:1080px;height:1350px;overflow:hidden}
.p{position:relative;width:1080px;height:1350px;background:radial-gradient(1200px 700px at 50% -10%,#9C2A1E 0%,#6B1414 45%,#3E0B0B 100%);color:var(--cream);padding:56px 64px;display:flex;flex-direction:column}
.p:before{content:"";position:absolute;inset:22px;border:2px solid rgba(233,200,106,.55);border-radius:22px;pointer-events:none}
.p:after{content:"";position:absolute;inset:32px;border:1px solid rgba(233,200,106,.25);border-radius:16px;pointer-events:none}
.org{text-align:center;font-size:20px;letter-spacing:.18em;text-transform:uppercase;color:var(--gold2);font-weight:600}
.presents{text-align:center;font-size:18px;color:#F1DDB8;margin-top:6px;font-style:italic;font-family:'Playfair Display',serif}
.lotus{display:flex;justify-content:center;margin:10px 0 2px}
h1{font-family:'Playfair Display',serif;font-weight:800;text-align:center;line-height:.95;color:#fff}
h1 .a{display:block;font-size:104px;letter-spacing:-.01em}
h1 .b{display:block;font-size:46px;font-weight:600;font-style:italic;color:var(--gold2);margin-top:10px}
.sub{text-align:center;font-size:23px;color:#F6E7CC;margin-top:14px}
.dates{margin:22px auto 0;background:linear-gradient(90deg,#E8891D,#F2B544);color:#3B1307;border-radius:999px;padding:14px 34px;font-weight:800;font-size:28px;text-align:center;box-shadow:0 8px 24px rgba(0,0,0,.25)}
.dates span{font-weight:600;opacity:.85}
.countries{display:flex;flex-wrap:wrap;justify-content:center;gap:8px 10px;margin-top:20px}
.countries div{border:1px solid rgba(233,200,106,.6);color:#FBEBCB;border-radius:999px;padding:6px 14px;font-size:17px;font-weight:600}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:26px}
.card{background:rgba(255,248,236,.07);border:1px solid rgba(233,200,106,.35);border-radius:18px;padding:18px 22px}
.card h3{font-family:'Playfair Display',serif;color:var(--gold2);font-size:27px;margin-bottom:8px}
.card li{list-style:none;font-size:18px;line-height:1.33;padding-left:22px;position:relative;color:#FFF3DD}
.card li:before{content:"✦";position:absolute;left:0;color:var(--saffron);font-size:14px;top:3px}
.bottom{display:grid;grid-template-columns:400px 1fr;gap:22px;margin-top:22px;align-items:stretch}
.pricebox{background:var(--cream);color:var(--ink);border-radius:20px;padding:18px 22px;text-align:center;box-shadow:0 10px 30px rgba(0,0,0,.3)}
.pl{font-size:16px;letter-spacing:.12em;text-transform:uppercase;color:var(--maroon2);font-weight:700}
.pv{font-size:66px;font-weight:800;color:var(--maroon);line-height:1.05;margin-top:2px}
.pi{font-size:18px;font-weight:700;color:var(--ink)}
.pt{font-size:18px;color:var(--muted);margin-top:4px;font-weight:600}
.inc{background:rgba(255,248,236,.07);border:1px solid rgba(233,200,106,.35);border-radius:18px;padding:16px 20px}
.inc h4{color:var(--gold2);font-size:17px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chips div{background:rgba(232,137,29,.18);border:1px solid rgba(232,137,29,.6);border-radius:10px;padding:6px 11px;font-size:16.5px;font-weight:600;color:#FFF1D6}
.foot{margin-top:auto;text-align:center}
.contact{display:flex;justify-content:center;gap:28px;font-size:21px;color:#fff;font-weight:500}
.contact b{color:var(--gold2)}
.note{font-size:14.5px;color:#E7D2B0;margin-top:8px}
"""


def poster_main(story=False):
    body = f"""<div class="p">
<div class="org">{ORG.split(',')[0]} · Hyderabad</div>
<div class="presents">presents a pilgrimage with Hare Krishna devotees</div>
<div class="lotus">{lotus(84)}</div>
<h1><span class="a">London Europe</span><span class="b">Yatra 2027</span></h1>
<div class="sub">15 nights / 16 days · 10 ISKCON temples · Europe's great sights · Satvik meals</div>
<div class="dates">17 April – 2 May 2027 <span>· 8 countries</span></div>
<div class="countries">{''.join(f'<div>{c}</div>' for c in COUNTRIES)}</div>
<div class="cols">
 <div class="card"><h3>Holy places</h3><ul>{''.join(f'<li>{t}</li>' for t in TEMPLES)}<li>Akshaya Patra kitchen, Watford</li></ul></div>
 <div class="card"><h3>Wonders of Europe</h3><ul>{''.join(f'<li>{t}</li>' for t in WONDERS)}</ul></div>
</div>
<div class="bottom">{price_box()}
 <div class="inc"><h4>Included</h4><div class="chips">
 <div>✈ International flights from Hyderabad &amp; Bangalore</div><div>Visa charges</div><div>Hotels (15 nights)</div>
 <div>All meals – Satvik prasadam</div><div>Private coach</div><div>All sightseeing &amp; entry tickets</div><div>Tour manager</div></div></div>
</div>
<div class="foot">{contact_bar()}<div class="note">*TCS is refunded or credited through your income-tax return. Limited seats – one coach. Itinerary may change slightly for operational reasons.</div></div>
</div>"""
    if not story:
        return page("London Europe Yatra 2027 – Poster", POSTER_CSS, body)
    css = POSTER_CSS.replace("height:1350px", "height:1920px") + """
.p{padding:120px 64px 110px}
h1 .a{font-size:118px} h1 .b{font-size:54px} .sub{font-size:25px} .org{font-size:22px} .presents{font-size:21px}
.card{padding:24px 26px} .card h3{font-size:34px;margin-bottom:12px} .card li{font-size:22px;line-height:1.55} .chips div{font-size:20px;padding:8px 13px}
.cols{margin-top:44px} .bottom{grid-template-columns:1fr;margin-top:36px;gap:28px} .pv{font-size:96px} .pl{font-size:19px} .pi,.pt{font-size:22px}
.pricebox{padding:26px} .inc{padding:22px 24px} .foot{margin-top:40px} .inc h4{font-size:19px} .contact{font-size:23px;flex-direction:column;gap:6px;align-items:center} .note{font-size:16px}
.dates{font-size:32px;margin-top:34px} .countries{margin-top:28px} .countries div{font-size:20px}
"""
    return page("London Europe Yatra 2027 – Story", css, body)


GLANCE_CSS = POSTER_CSS + """
.p{padding:54px 60px}
h1 .a{font-size:70px} h1 .b{font-size:34px;margin-top:4px}
.glance{display:grid;grid-template-columns:1fr 360px;gap:22px;margin-top:20px;flex:1;min-height:0}
.days{background:rgba(255,248,236,.06);border:1px solid rgba(233,200,106,.35);border-radius:18px;padding:12px 18px}
.day{display:grid;grid-template-columns:80px 108px 1fr;gap:8px;padding:10px 0;border-bottom:1px dashed rgba(233,200,106,.25);align-items:baseline}
.day:last-child{border-bottom:0}
.dn{font-family:'Playfair Display',serif;color:var(--saffron);font-weight:800;font-size:22px}
.dd{color:var(--gold2);font-size:16px;font-weight:600}
.dr{color:#FFF3DD;font-size:18px;line-height:1.3;font-weight:500}
.side{display:flex;flex-direction:column;gap:16px}
.mapbox{background:rgba(255,248,236,.04);border-radius:16px}
.side .pricebox .pv{font-size:54px}
"""


def poster_glance():
    rows = []
    for d in D.DAYS:
        n = d["day"]
        short = DAY_TEXT[n - 1][1]
        rows.append(f'<div class="day"><div class="dn">Day {n}</div><div class="dd">{d["dow"]} {int(d["date"][8:])} {"Apr" if d["date"][5:7]=="04" else "May"}</div><div class="dr">{short}</div></div>')
    body = f"""<div class="p">
<div class="org">London Europe Yatra 2027 · 17 April – 2 May</div>
<h1 style="margin-top:6px"><span class="a">Itinerary at a glance</span><span class="b">16 days · 8 countries · one coach, one family</span></h1>
<div class="glance"><div class="days">{''.join(rows)}</div>
<div class="side"><div class="mapbox">{route_svg(360, 640, dark=True)}</div>{price_box()}</div></div>
<div class="foot" style="margin-top:16px">{contact_bar()}<div class="note">*TCS is refunded or credited through your income-tax return. Flights from Hyderabad and Bangalore; return to both cities on 3 May.</div></div>
</div>"""
    return page("London Europe Yatra 2027 – Itinerary", GLANCE_CSS, body)


PRICE_CSS = POSTER_CSS + """
h1 .a{font-size:76px} h1 .b{font-size:36px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:22px}
table.calc{width:100%;border-collapse:collapse;font-size:20px;color:var(--ink)}
table.calc td{padding:7px 4px;border-bottom:1px solid #E9DCC4}
table.calc td:last-child{text-align:right;font-weight:700}
table.calc tr.tot td{border-top:2px solid var(--maroon);border-bottom:0;font-size:22px;color:var(--maroon)}
.white{background:var(--cream);color:var(--ink);border-radius:18px;padding:20px 24px}
.white h3{font-family:'Playfair Display',serif;color:var(--maroon);font-size:28px;margin-bottom:8px}
.white .small{font-size:15.5px;color:var(--muted);margin-top:8px;line-height:1.4}
.card li{font-size:18px}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:20px}
.step{background:rgba(255,248,236,.07);border:1px solid rgba(233,200,106,.35);border-radius:16px;padding:14px}
.step b{display:block;font-family:'Playfair Display',serif;color:var(--saffron);font-size:30px}
.step span{font-size:16.5px;color:#FFF3DD;line-height:1.35;display:block;margin-top:4px}
.flights{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px}
.flight{background:var(--cream);color:var(--ink);border-radius:16px;padding:14px 18px}
.flight b{display:block;font-family:'Playfair Display',serif;color:var(--maroon);font-size:24px}
.flight span{display:block;font-size:16.5px;line-height:1.4;margin-top:2px}
"""


def poster_price():
    body = f"""<div class="p">
<div class="org">London Europe Yatra 2027 · 17 April – 2 May</div>
<div class="lotus">{lotus(70)}</div>
<h1><span class="a">Yatra amount</span><span class="b">{PRICE} per person, including international flights</span></h1>
<div class="grid2">
 <div class="white"><h3>What you pay</h3><table class="calc">
  <tr><td>Yatra amount</td><td>{inr(D.PRICE_PP)}</td></tr>
  <tr><td>GST 5%</td><td>{inr(GST)}</td></tr>
  <tr><td>Sub-total</td><td>{inr(SUBTOTAL)}</td></tr>
  <tr><td>TCS 2% (comes back to you*)</td><td>{inr(TCS)}</td></tr>
  <tr class="tot"><td>Total paid</td><td>{inr(SUBTOTAL + TCS)}</td></tr></table>
  <div class="small">*TCS (Tax Collected at Source) is deposited against your PAN. You get it back as a refund or as credit against your tax when you file your income-tax return. Per person, twin sharing.</div></div>
 <div class="card"><h3>Included</h3><ul>
  <li>International flights from Hyderabad or Bangalore (economy, group fares)</li><li>UK and Schengen visa charges</li>
  <li>15 nights in hotels</li><li>All meals: Satvik prasadam, no onion or garlic</li><li>Private coach throughout, ferry, boats and trains in the plan</li>
  <li>All sightseeing and entry tickets in the itinerary</li><li>Experienced tour manager and licensed local guides</li></ul></div>
</div>
<div class="grid2" style="margin-top:18px">
 <div class="card"><h3>Not included</h3><ul><li>GST 5% and TCS 2%</li><li>Personal expenses and shopping</li><li>Driver tips (€3 per person per day)</li><li>Optional extras (e.g. Pisa tower climb, Doge's Palace)</li></ul></div>
 <div class="card"><h3>Who can join</h3><ul><li>Devotees, families and friends</li><li>Passport valid 3+ months after 3 May 2027</li><li>Fit to walk 6–8 km on city days</li><li>Seniors welcome: we plan rests and a slower group</li></ul></div>
</div>
<div class="steps">
 <div class="step"><b>1</b><span>Call or WhatsApp to register and reserve your seat</span></div>
 <div class="step"><b>2</b><span>Share passport and visa documents (ITR, bank statement)</span></div>
 <div class="step"><b>3</b><span>UK visa from mid-January 2027; Schengen visa by early March</span></div>
 <div class="step"><b>4</b><span>Pre-departure meeting and kit; fly on 17 April 2027</span></div>
</div>
<div class="flights">
 <div class="flight"><b>✈ From Hyderabad</b><span>Out Sat 17 Apr: Emirates via Dubai, dep 04:40 → London 16:10</span><span>Back Sun 2 May: Etihad via Abu Dhabi → Hyderabad 02:45 (3 May)</span></div>
 <div class="flight"><b>✈ From Bangalore</b><span>Out Sat 17 Apr: Etihad via Abu Dhabi, dep 10:00 → London 18:45</span><span>Back Sun 2 May: Etihad via Abu Dhabi → Bangalore 03:15 (3 May)</span></div>
</div>
<div class="foot">{contact_bar()}<div class="note">Limited seats – one coach. Prices are per person; payment schedule and cancellation terms on the booking form.</div></div>
</div>"""
    return page("London Europe Yatra 2027 – Price", PRICE_CSS, body)


# --------------------------------------------------------------------------- brochure

BRO_CSS = """
@page{size:A4;margin:0}
body{background:#fff}
.pg{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;padding:16mm 16mm 18mm;background:var(--cream)}
.pg:last-child{page-break-after:auto}
.pg .hdr{display:flex;justify-content:space-between;font-size:9pt;color:var(--maroon2);letter-spacing:.12em;text-transform:uppercase;font-weight:600;border-bottom:1px solid #E3CFA8;padding-bottom:5mm;margin-bottom:7mm}
.pg .ftr{position:absolute;left:16mm;right:16mm;bottom:9mm;display:flex;justify-content:space-between;font-size:8.5pt;color:var(--muted);border-top:1px solid #E3CFA8;padding-top:3mm}
h2{font-family:'Playfair Display',serif;color:var(--maroon);font-size:26pt;line-height:1.1;margin-bottom:5mm}
h3{font-family:'Playfair Display',serif;color:var(--maroon2);font-size:14pt;margin:5mm 0 2mm}
p,li{font-size:10.5pt;line-height:1.5}
ul{padding-left:5mm}
.cover{background:radial-gradient(900px 600px at 50% 0%,#9C2A1E 0%,#6B1414 50%,#3E0B0B 100%);color:var(--cream);text-align:center;padding:22mm 18mm}
.cover:before{content:"";position:absolute;inset:8mm;border:1.5px solid rgba(233,200,106,.6);border-radius:6mm}
.cover .org{font-size:11pt;letter-spacing:.2em;text-transform:uppercase;color:var(--gold2);font-weight:600}
.cover h1{font-family:'Playfair Display',serif;font-size:46pt;line-height:1;margin-top:4mm;color:#fff}
.cover h1 i{display:block;font-size:26pt;color:var(--gold2);margin-top:3mm}
.cover .dates{display:inline-block;margin-top:9mm;background:linear-gradient(90deg,#E8891D,#F2B544);color:#3B1307;border-radius:99px;padding:3mm 9mm;font-weight:800;font-size:15pt}
.cover .cty{margin-top:7mm;font-size:11.5pt;color:#F6E7CC;line-height:1.6}
.cover .map{margin:6mm auto 0;width:118mm}.cover .map svg{width:118mm;height:auto}
.cover .pb{margin:5mm auto 0;width:110mm;background:var(--cream);color:var(--ink);border-radius:5mm;padding:5mm}
.cover .pb .v{font-family:'Playfair Display',serif;font-size:32pt;color:var(--maroon);font-weight:800}
.cover .pb .s{font-size:11pt;font-weight:600}
.cover .ct{position:absolute;bottom:16mm;left:0;right:0;font-size:11pt}
.cover .ct b{color:var(--gold2)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:7mm}
.box{background:#fff;border:1px solid #E3CFA8;border-radius:4mm;padding:5mm 6mm}
.box h3{margin-top:0}
.facts{display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;margin:2mm 0 6mm}
.fact{background:var(--maroon);color:var(--cream);border-radius:4mm;padding:4mm;text-align:center}
.fact b{display:block;font-family:'Playfair Display',serif;font-size:20pt;color:var(--gold2)}
.fact span{font-size:9pt}
table.fl{width:100%;border-collapse:collapse;font-size:9.5pt}
table.fl th{background:var(--maroon);color:var(--cream);text-align:left;padding:2mm 3mm;font-weight:600}
table.fl td{padding:2mm 3mm;border-bottom:1px solid #E9DCC4;vertical-align:top}
.dayc{display:grid;grid-template-columns:24mm 1fr;gap:4mm;padding:2.6mm 0;border-bottom:1px dashed #DCC59A}
.dayc .n{font-family:'Playfair Display',serif;color:var(--saffron);font-size:17pt;font-weight:800;line-height:1}
.dayc .d{font-size:9pt;color:var(--maroon2);font-weight:600;margin-top:1mm}
.dayc .t{font-weight:700;font-size:11pt;color:var(--maroon)}
.dayc p{font-size:10pt;margin-top:1mm}
.dayc .o{font-size:8.8pt;color:var(--muted);margin-top:1mm}
.chipl{display:flex;flex-wrap:wrap;gap:2.5mm}
.chipl span{background:#fff;border:1px solid #E3CFA8;border-radius:99px;padding:1.5mm 4mm;font-size:9.5pt}
table.calc{width:100%;border-collapse:collapse;font-size:11pt}
table.calc td{padding:2mm 1mm;border-bottom:1px solid #E9DCC4}
table.calc td:last-child{text-align:right;font-weight:700}
table.calc tr.tot td{border-top:2px solid var(--maroon);font-size:12.5pt;color:var(--maroon);border-bottom:0}
.small{font-size:9pt;color:var(--muted);line-height:1.45}
.callout{background:var(--maroon);color:var(--cream);border-radius:5mm;padding:5mm;text-align:center;margin-top:5mm}
.callout .big{font-family:'Playfair Display',serif;font-size:24pt;color:var(--gold2)}
"""


def bro_page(inner, n, cls="pg"):
    return (f'<section class="{cls}"><div class="hdr"><span>London Europe Yatra 2027</span><span>17 April – 2 May 2027</span></div>'
            f'{inner}<div class="ftr"><span>{ORG}</span><span>{PHONE} · page {n}</span></div></section>')


def brochure():
    pages = []
    cover = f"""<section class="pg cover">
<div class="org">{ORG.split(',')[0]} · Hyderabad</div>
<div style="margin-top:6mm">{lotus(70)}</div>
<h1>London Europe Yatra<i>2027 · with Hare Krishna devotees</i></h1>
<div class="dates">17 April – 2 May 2027 · 15 nights / 16 days</div>
<div class="cty">{' · '.join(COUNTRIES)}</div>
<div class="map">{route_svg(560, 470, dark=True)}</div>
<div class="pb"><div class="v">{PRICE}</div><div class="s">per person, including international flights</div><div class="small">+ 5% GST + 2% TCS (TCS refunded or credited through your income-tax return)</div></div>
<div class="ct"><b>Call / WhatsApp</b> {PHONE} &nbsp;·&nbsp; {WEB}</div></section>"""
    pages.append(cover)

    overview = f"""<h2>A pilgrimage across Europe</h2>
<p>Travel with Hare Krishna devotees through eight countries in sixteen days. Take darshan at ten ISKCON temples, including Srila Prabhupada's Bhaktivedanta Manor and the castle temple of Radhadesh. See Europe's great sights, from the Tower of London and the Eiffel Tower to Mount Titlis, Venice and the Vatican. Every meal is Satvik prasadam, and the group travels together in one private coach with an experienced tour manager.</p>
<div class="facts"><div class="fact"><b>16</b><span>days / 15 nights</span></div><div class="fact"><b>8</b><span>countries</span></div><div class="fact"><b>10</b><span>ISKCON temples</span></div><div class="fact"><b>2</b><span>departure cities</span></div></div>
<div class="two"><div class="box"><h3>Holy places</h3><ul>{''.join(f'<li>{t}</li>' for t in TEMPLES)}<li>Akshaya Patra kitchen, Watford (seva visit)</li></ul></div>
<div class="box"><h3>Wonders of Europe</h3><ul>{''.join(f'<li>{t}</li>' for t in WONDERS)}<li>Brussels, Amsterdam canals and Lake Como</li></ul></div></div>
<h3>Flights</h3>
<table class="fl"><tr><th>Group</th><th>Outbound – Sat 17 April 2027</th><th>Return – Sun 2 May 2027</th></tr>
<tr><td><b>Hyderabad</b></td><td>Emirates EK 525 / EK 31 via Dubai. Dep 04:40, arrive London Heathrow 16:10.</td><td>Etihad EY 82 / EY 352 via Abu Dhabi. Dep Milan Malpensa 11:40, arrive Hyderabad 02:45 on Mon 3 May.</td></tr>
<tr><td><b>Bangalore</b></td><td>Etihad EY 1013 / EY 67 via Abu Dhabi. Dep 10:00, arrive London Heathrow 18:45.</td><td>Etihad EY 82 / EY 232 via Abu Dhabi. Dep Milan Malpensa 11:40, arrive Bangalore 03:15 on Mon 3 May.</td></tr></table>
<p class="small" style="margin-top:2mm">Flight numbers and times are the shortlisted 2027 schedules and may change before ticketing.</p>
<h3>A typical day</h3>
<p>07:30 morning programme (japa, kirtan, Bhagavatam) · 08:00–09:00 breakfast at the hotel · 09:00 coach departs · lunch near the sights or at a temple · evening arati where possible · dinner at the hotel. Early starts only on the Rome day (Day 14) and the flight home (Day 16).</p>"""
    pages.append(bro_page(overview, 2))

    def day_block(n):
        d = D.DAYS[n - 1]
        mon = "April" if d["date"][5:7] == "04" else "May"
        return (f'<div class="dayc"><div><div class="n">Day {n}</div><div class="d">{d["dow"]} {int(d["date"][8:])} {mon}</div></div>'
                f'<div><div class="t">{DAY_TEXT[n-1][1]}</div><p>{DAY_TEXT[n-1][2]}</p><div class="o">Overnight: {d["overnight"]}</div></div></div>')

    pages.append(bro_page('<h2>Day by day</h2>' + ''.join(day_block(n) for n in range(1, 9)), 3))
    pages.append(bro_page('<h2>Day by day <span style="font-size:14pt;color:#8E1F1A">continued</span></h2>' + ''.join(day_block(n) for n in range(9, 17)), 4))

    price = f"""<h2>Yatra amount and inclusions</h2>
<div class="two"><div class="box"><h3>{PRICE} per person</h3><p><b>Including international flights</b>, per person on twin sharing, plus 5% GST and 2% TCS.</p>
<table class="calc" style="margin-top:3mm"><tr><td>Yatra amount</td><td>{inr(D.PRICE_PP)}</td></tr><tr><td>GST 5%</td><td>{inr(GST)}</td></tr>
<tr><td>Sub-total</td><td>{inr(SUBTOTAL)}</td></tr><tr><td>TCS 2%*</td><td>{inr(TCS)}</td></tr><tr class="tot"><td>Total paid</td><td>{inr(SUBTOTAL + TCS)}</td></tr></table>
<p class="small" style="margin-top:3mm">*TCS (Tax Collected at Source) is deposited against your PAN. You get it back as a refund, or as credit against your tax, when you file your income-tax return. A PAN is needed for the booking.</p></div>
<div class="box"><h3>Included</h3><ul><li>International flights from Hyderabad or Bangalore (economy, group fares)</li><li>UK and Schengen visa charges</li><li>15 nights in hotels</li><li>All meals: Satvik prasadam, no onion or garlic; Ekadasi meals</li><li>Private coach throughout, Dover–Calais ferry, Thames, Seine, Amsterdam and lake boats, Swiss and Italian trains in the plan</li><li>All sightseeing and entry tickets in the itinerary</li><li>Tour manager and licensed local guides</li></ul>
<h3>Not included</h3><ul><li>GST 5% and TCS 2%</li><li>Personal expenses and shopping</li><li>Driver tips (€3 per person per day)</li><li>Optional extras: Pisa tower climb, Doge's Palace, Florence dome climb and similar</li></ul></div></div>
<h3>Visa documents (start collecting now)</h3>
<div class="two"><div class="box"><ul>
<li><b>Passport</b> valid 3+ months after 3 May 2027 with 2 blank pages, plus old passports</li>
<li><b>Photos</b> 35 × 45 mm, white background, 2 copies (Schengen size)</li>
<li><b>ITR-V</b> for the last 3 financial years</li><li><b>Bank statement</b> for 3 months, sealed and signed by the bank</li></ul></div>
<div class="box"><ul><li><b>Salary slips</b> (3 months) and a leave letter, if employed</li><li><b>Covering letter</b> from you or your company</li>
<li><b>UK visa</b>: apply from mid-January 2027 (eVisa)</li><li><b>Schengen visa</b> through Italy, by early March 2027; biometrics in person</li></ul></div></div>"""
    pages.append(bro_page(price, 5))

    dos = ''.join(f'<li>{x}</li>' for x in D.DOS[:6])
    donts = ''.join(f'<li>{x}</li>' for x in D.DONTS[:6])
    good = f"""<h2>Good to know</h2>
<div class="two"><div class="box" style="padding:4mm 5mm"><h3>Weather in late April</h3><p>London 7–15 °C with showers; Paris to Cologne 8–17 °C; the Black Forest close to 0 °C at night; Mount Titlis about −5 °C in snow; Italy 10–21 °C. Pack layers, a warm jacket, gloves and cap for Titlis, an umbrella and comfortable walking shoes.</p>
<h3>Walking</h3><p>City days involve 6–8 km of walking and some standing. The tour manager plans rests, and a slower group with an assistant for seniors.</p>
<h3>Ekadasi</h3><p>Kamada Ekadasi (17 April) and Varuthini Ekadasi (2 May) fall on flight days. Fruit meals are ordered on all flights, and a grain-free dinner is served in London on 17 April.</p></div>
<div class="box"><h3>Do</h3><ul>{dos}</ul></div></div>
<div class="box" style="margin-top:4mm;padding:4mm 6mm"><h3>Don't</h3><ul>{donts}</ul></div>
<div class="callout"><div class="big">Reserve your seat</div><p style="font-size:11pt;margin-top:1mm"><b>Call / WhatsApp {PHONE}</b><br>{WEB}<br>{ORG}</p>
<p style="font-size:9pt;color:#F1DDB8;margin-top:1.5mm">Limited seats – one coach · payment and cancellation terms on the booking form</p></div>"""
    pages.append(bro_page(good, 6))
    return page("London Europe Yatra 2027 – Brochure", BRO_CSS, ''.join(pages))


def main():
    os.makedirs(HTML_DIR, exist_ok=True)
    files = {
        "poster_1_main.html": poster_main(),
        "poster_2_itinerary.html": poster_glance(),
        "poster_3_price.html": poster_price(),
        "poster_4_story.html": poster_main(story=True),
        "brochure.html": brochure(),
    }
    for name, html in files.items():
        with open(os.path.join(HTML_DIR, name), "w", encoding="utf-8") as f:
            f.write(html)
    print("wrote", len(files), "HTML files to", HTML_DIR)


if __name__ == "__main__":
    main()
