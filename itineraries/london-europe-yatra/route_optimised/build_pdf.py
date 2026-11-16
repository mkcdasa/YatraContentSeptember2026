"""Builds the route-optimised itinerary PDF: python3 route_optimised/build_pdf.py && node route_optimised/render.cjs"""
import os, sys, html, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plan as P  # noqa: E402
D = P.D
E = html.escape

START = datetime.date(2027, 4, 17)
def date(n): d = START + datetime.timedelta(days=n - 1); return d.strftime("%a %d %b")

EXCL_OLD = {(11, "H_INT"), (14, "H_FLR")}   # luggage-only / empty coach runs in the old plan
def old_day(i):
    t = km = 0
    for r in D.DAYS[i - 1]["rows"]:
        if not (r["frm"] and r["km"]) or r["mode"] == "Flight": continue
        if r["mode"] in ("Coach", "Local coach"): km += r["km"]
        if (i, r["to"]) in EXCL_OLD or i == 1: continue
        t += P.mins(r["start"], r["end"])
    return t, km
def new_day(d):
    t = km = 0
    for l in P.legs(d):
        if l["mode"] in ("Coach", "Local coach"): km += l["km"]
        t += l["m"]
    if d["n"] == 13: km += 260          # empty coach Venice-Mestre → Florence with the luggage
    if d["n"] == 1: t = 0
    return t, km
def first(d):
    return min(r[0] for r in d["rows"] if r[2] not in ("Morning programme",))
def last(d):
    return max(r[1] for r in d["rows"] if r[1] > "05:00")

old = [old_day(i) for i in range(1, 17)]
new = [new_day(d) for d in P.DAYS]
OT, NT = sum(x[0] for x in old[1:15]), sum(x[0] for x in new[1:15])
OK, NK = sum(x[1] for x in old), sum(x[1] for x in new)
H = lambda m: f"{m // 60} h {m % 60:02d} m"

CHANGES = [
 ("London → Paris by Eurostar", "The coach-and-ferry crossing (Wembley → Dover → ferry → Calais → Paris) took a full day, 09:00–20:30. Eurostar from St Pancras takes 2 h 16 m and puts us in Paris by lunchtime, so Paris needs only 1½ days. The Channel Tunnel replaces the ferry as the 'crossing' experience."),
 ("ISKCON Paris on the way out", "The temple is in Sevran, north-east of Paris, right on the motorway to Brussels. Visiting it on departure day saves a separate 40 km round trip."),
 ("Belgium → Netherlands in one straight line", "Brussels → Keukenhof → Amsterdam the same day, then Zaanse Schans (just north of Amsterdam) on the way out towards Cologne. No back-tracking."),
 ("Radhadesh dropped", "Radhadesh (Château de Petite Somme and the Museum of Sacred Art) is deep in the Belgian Ardennes. Brussels → Radhadesh → Amsterdam was 425 km against 210 km direct: a 215 km, 2¾-hour detour plus a 3-hour visit, for two attractions few non-devotee customers know."),
 ("Milan by evening, Villaggio on the Venice road", "Milan Duomo, the Galleria and La Scala move to the evening of the Como day (Como is 50 km from Milan). Villaggio Hare Krishna (near Bergamo) is on the A4 motorway to Venice, so it is visited next morning instead of as a separate evening detour."),
 ("Rome gets a night; no more 05:00 start", "The current Day 14 starts at 05:00, goes Venice → Rome → Florence by train in one day and ends at 22:30. Now we take the Frecciarossa from Venice-Mestre at 07:30, see the Vatican, St Peter's and the Colosseum that afternoon, sleep in Rome, see the Trevi Fountain, Pantheon, Piazza Navona and Spanish Steps next morning, and take the 1 h 35 m train to Florence after lunch. The coach carries the big luggage to Florence while we are in Rome."),
 ("Pisa on the way to the airport", "Pisa lies between Florence and Malpensa, so the last day is just Pisa and a 4½-hour drive, arriving at the hotel by 17:30 for a relaxed final evening before the flight."),
]
SKIP = [
 ("Château de Petite Somme (Radhadesh)", "Skipped", "Not well known outside ISKCON circles; costs a 215 km detour. If Radhadesh must stay (for example for the Bhakti Yatra group), it can be added back on Day 6 or 7 at the cost of about 5½ hours (detour plus visit)."),
 ("Museum of Sacred Art (Radhadesh)", "Skipped", "Same place as above."),
 ("English Channel ferry", "Replaced", "By the Eurostar ride through the Channel Tunnel, a more remarkable 'wonder' and 9 hours quicker."),
 ("Eurostar through the Channel Tunnel", "Added", "50 km under the sea; the Channel Tunnel is one of the ASCE 'Seven Wonders of the Modern World'."),
 ("Piazza Navona", "Added", "Rome's most beautiful square, possible thanks to the morning in Rome."),
 ("Spanish Steps", "Added", "Hugely popular with Indian travellers (film locations); also thanks to the morning in Rome."),
]
WHERE = {
 "United Kingdom": {"Buckingham Palace": 3, "Changing of the Guard": 3, "The King's Gallery": 3, "Tower of London": 3, "Crown Jewels & Koh-i-Noor": 3,
                    "Tower Bridge": 3, "Thames boat ride": 3, "London Eye": 3, "Big Ben & Houses of Parliament": 3, "Westminster Bridge": 3,
                    "Madame Tussauds": 2, "Covent Garden & Royal Opera House": 2, "English Channel ferry": "→ Eurostar, Day 4"},
 "France": {"Eiffel Tower (2nd floor)": 4, "Arc de Triomphe": 4, "Champs-Élysées": 4, "Place de la Concorde": 4, "Trocadéro": 4,
            "Notre-Dame": 5, "Île de la Cité": 5, "Louvre & Mona Lisa": 5, "Seine river cruise": 4},
 "Belgium": {"Atomium": 6, "Grand Place": 5, "Manneken Pis": 5, "Galeries Royales Saint-Hubert": 5, "Château de Petite Somme": "skipped", "Museum of Sacred Art": "skipped"},
 "Netherlands": {"Amsterdam canal cruise": 6, "Zaanse Schans windmills": 7, "Clog & cheese workshops": 7, "Keukenhof tulip gardens": 6},
 "Germany": {"Cologne Cathedral": 7, "Hohenzollern Bridge": 7, "Black Forest drive": 8, "Lake Titisee": 9, "Cuckoo-clock shops": 9},
 "Switzerland": {"Rhine Falls": 9, "Zurich old town": 9, "Bahnhofstrasse": 9, "Lake Zurich": 9, "Grossmünster & Fraumünster": 9,
                 "Mount Titlis snow & Rotair": 10, "Glacier Cave & Cliff Walk": 10, "Lion Monument": 10, "Chapel Bridge": 10, "Lucerne Old Town": 10,
                 "Lake Lucerne cruise": 10, "Luzern–Interlaken Express": 10, "Jungfrau view": 11},
 "Italy": {"Lake Como boat ride": 11, "Como Cathedral": 11, "Milan Duomo": 11, "Galleria Vittorio Emanuele II": 11, "La Scala": 11,
           "Basilica of St Anthony, Padova": 12, "Prato della Valle": 12, "St Mark's Square & Basilica": 12, "Doge's Palace & Bridge of Sighs": 12,
           "Rialto Bridge": 12, "Venice gondola ride": 12, "Colosseum (inside)": 13, "Roman Forum": 13, "Trevi Fountain": 14, "Pantheon": 14,
           "Florence Duomo": 14, "Piazza della Signoria": 14, "Ponte Vecchio": 14, "Piazzale Michelangelo": 14,
           "Leaning Tower, Cathedral & Baptistery of Pisa": 15, "Frecciarossa high-speed train": "13, 14"},
 "Vatican City": {"Vatican Museums": 13, "Sistine Chapel": 13, "St Peter's Basilica": 13, "St Peter's Square": 13},
}
ADDED = {"France": [("Eurostar through the Channel Tunnel", 4)], "Italy": [("Piazza Navona", 14), ("Spanish Steps", 14)]}
CONFIRM = [
 "Eurostar group fare (40 seats, 09:01 St Pancras → Paris) against the old Dover ferry + coach day; book as soon as sales open (about 11 months ahead).",
 "Two coaches instead of one: a UK coach for Days 1–4 morning, and a continental coach from Paris Gare du Nord (Day 4) to Malpensa (Day 16). This often costs less, as the coach no longer crosses the Channel.",
 "Hotels: Paris now 1 night (was 2); add 1 night in Rome near Termini (Day 13); Florence stays 1 night (Day 14).",
 "Frecciarossa group tickets: Venice-Mestre → Rome (Day 13, 07:30) and Rome → Florence (Day 14, 13:20); the old plan already had Venice → Rome → Florence, now spread over two days.",
 "Rome sights are on 29–30 April (Vatican Museums and the Colosseum are closed on 1 May). 1 May (Pisa day) is an Italian holiday: the Square of Miracles stays open but is crowded.",
 "Goloka Dham is now on Saturday 24 April (was Sunday): no Sunday feast, so book prasadam lunch with the temple in advance.",
 "Keukenhof is now Thursday 22 April (was Saturday 24 April): fewer crowds on a weekday.",
]

def legrow(l):
    return (f'<tr class="go"><td>{l[0]}–{l[1]}</td><td>{E(l[5])}</td><td>{E(P.NAME.get(l[3], l[3]))} → {E(P.NAME.get(l[4], l[4]))}'
            + (f'<div class="nt">{l[6]}</div>' if l[6] else "") + "</td></tr>")
def dayhtml(d):
    t, km = new_day(d)
    rows = []
    for r in d["rows"]:
        if r[2] == "GO":
            rows.append(legrow(r))
        else:
            rows.append(f'<tr><td>{r[0]}–{r[1]}</td><td>{E(r[2])}</td><td>{r[3]}</td></tr>')
    tag = (f'<span class="same">Same as the current Day {d["same"]}</span>' if d.get("same") else '<span class="chg">Re-organised</span>')
    stats = f'Coach {km:.0f} km · group travel {H(t)}' if d["n"] != 1 else 'Arrival day: two flights (Bangalore 12:45, Hyderabad 18:40)'
    return (f'<section class="day"><div class="dhb"><div class="dh"><b>Day {d["n"]}</b><span>{date(d["n"])}</span>{tag}</div>'
            f'<h3>{E(d["title"])}</h3><div class="ds">Overnight: <b>{E(d["on"])}</b> · {stats}</div>'
            f'<table class="t">{"".join(rows[:3])}</table></div><table class="t">{"".join(rows[3:])}</table></section>')

def glance():
    rows = []
    for d, o, n, od in zip(P.DAYS, old, new, D.DAYS):
        rows.append(f'<tr><td><b>{d["n"]}</b><br><small>{date(d["n"])}</small></td><td>{E(d["title"])}<br><small>Overnight: {E(d["on"])}</small></td>'
                    f'<td class="r">{n[1]:.0f}</td><td class="r">{H(n[0]) if d["n"] > 1 else "–"}</td>'
                    f'<td class="old">{E(od["title"])}<br><small>{o[1]:.0f} km · {H(o[0]) if d["n"] > 1 else "–"}</small></td></tr>')
    return ('<table class="g"><tr><th>Day</th><th>New route</th><th>Coach km</th><th>Travel</th><th>Current plan (for comparison)</th></tr>'
            + "".join(rows) + "</table>")

def checklist():
    out, n = [], 0
    for c, items in WHERE.items():
        lis = []
        for a, w in items.items():
            cls = "sk" if w == "skipped" else ("sw" if isinstance(w, str) and w.startswith("→") else "")
            if not cls: n += 1
            lis.append(f'<li class="{cls}">{E(a)}<em>{"Day " + str(w) if not isinstance(w, str) or w[0].isdigit() else E(w)}</em></li>')
        for a, w in ADDED.get(c, []):
            n += 1
            lis.append(f'<li class="ad">{E(a)}<em>Day {w} · new</em></li>')
        out.append(f'<div class="cc"><b>{E(c)}</b><ul>{"".join(lis)}</ul></div>')
    return n, "".join(out)

N, CHK = checklist()
CSS = """
@page{size:A4;margin:12mm 12mm 14mm}
*{box-sizing:border-box}body{font-family:Poppins,Arial,sans-serif;color:#2A2131;font-size:10.5px;margin:0}
h1{font-family:'Playfair Display',serif;color:#2A0D3D;font-size:28px;margin:0}h2{color:#2A0D3D;font-size:17px;border-bottom:3px solid #F28C28;padding-bottom:4px;margin:18px 0 8px}
h3{font-size:13px;color:#2A0D3D;margin:4px 0;break-after:avoid}.ds{break-after:avoid}.dhb{break-inside:avoid}
.top{background:linear-gradient(135deg,#2A0D3D,#5B1F7E);color:#fff;border-radius:10px;padding:16px 18px;margin-bottom:12px}
.top h1{color:#fff}.top p{margin:6px 0 0;color:#F6D58B;font-size:12px}
.kp{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:10px 0}
.k{background:#FFF8EE;border:1px solid #F3D9B5;border-radius:8px;padding:8px 10px}.k b{display:block;font-size:17px;color:#E8445A}.k span{font-size:10px}.k s{color:#8a7f90}
ol.ch li{margin-bottom:4px}ol.ch b{color:#2A0D3D}
table{border-collapse:collapse;width:100%}
.g td,.g th{border-bottom:1px solid #e5dde9;padding:4px 5px;vertical-align:top;text-align:left}.g th{background:#2A0D3D;color:#fff;font-size:10px}
.g .r{text-align:right;white-space:nowrap}.g .old{color:#7a6f80;font-size:9.5px;width:34%}
.sk td{font-size:10px}
.s{width:100%}.s td,.s th{border:1px solid #e5dde9;padding:5px 6px;text-align:left;vertical-align:top}.s th{background:#FFF1E2}
.st{font-weight:700}.st.Skipped{color:#B91C1C}.st.Added{color:#15803D}.st.Replaced{color:#B45309}
.day{break-inside:auto;margin-bottom:14px}
.dh{display:flex;gap:10px;align-items:center;background:#2A0D3D;color:#fff;border-radius:6px;padding:5px 10px;break-after:avoid}
.dh b{font-size:13px}.dh .same,.dh .chg{margin-left:auto;font-size:9.5px;border-radius:10px;padding:1px 8px}.dh .same{background:#6E6077}.dh .chg{background:#F28C28}
.ds{font-size:10px;color:#6E6077;margin-bottom:4px}
.t td{border-bottom:1px solid #eee;padding:3px 5px;vertical-align:top}.t td:first-child{white-space:nowrap;width:74px;color:#5B1F7E;font-weight:600}
.t td:nth-child(2){width:92px;font-weight:600}.t tr{break-inside:avoid}
.t tr.go td{background:#F4F0F7;color:#3a3040}.t tr.go td:nth-child(2){color:#0E7490}.nt{font-size:9.5px;color:#6E6077}
.ccs{columns:2;column-gap:14px}.cc{break-inside:avoid;margin-bottom:8px}.cc b{color:#2A0D3D}
.cc ul{margin:3px 0 0;padding-left:16px}.cc li em{font-style:normal;color:#6E6077;margin-left:6px;font-size:9.5px}
.cc li.sk{color:#B91C1C;text-decoration:line-through}.cc li.sw{color:#B45309}.cc li.ad{color:#15803D;font-weight:600}
.cf li{margin-bottom:4px}.pb{break-before:page}
"""
body = f"""
<div class="top"><h1>London &amp; Europe Grand Tour 2027 — Route-Optimised Itinerary</h1>
<p>17 April – 2 May 2027 · 15 nights / 16 days · 8 countries · arrive London Heathrow, depart Milan Malpensa (unchanged) · proposal for approval</p></div>
<div class="kp">
<div class="k"><b>{H(NT)}</b><span>group travel time, Days 2–15<br><s>{H(OT)} in the current plan</s></span></div>
<div class="k"><b>{H(OT - NT)}</b><span>less time on the road and on trains</span></div>
<div class="k"><b>{NK:,.0f} km</b><span>coach distance<br><s>{OK:,.0f} km in the current plan</s></span></div>
<div class="k"><b>{N}</b><span>attractions still covered<br>(2 skipped, 3 added)</span></div>
</div>
<p>Every promised attraction is kept except the two at Radhadesh. The 05:00 start on the Rome day is gone, and Rome now gets a full day and a night. The arrival flights (17 April, London Heathrow) and the departure flights (2 May, Milan Malpensa) are unchanged.</p>
<h2>What changed and why</h2><ol class="ch">{"".join(f"<li><b>{E(a)}.</b> {E(b)}</li>" for a, b in CHANGES)}</ol>
<h2>Skipped, replaced and added attractions</h2>
<table class="s"><tr><th>Attraction</th><th>Status</th><th>Comment</th></tr>{"".join(f'<tr><td>{E(a)}</td><td class="st {s}">{s}</td><td>{E(c)}</td></tr>' for a, s, c in SKIP)}</table>
<p>Net result: 75 − 2 skipped − 1 replaced + 3 added = <b>{N} attractions</b>, so the posters' "75 attractions" still holds.</p>
<h2>The route at a glance</h2>{glance()}
<p style="font-size:9.5px;color:#6E6077">Coach km include empty and luggage-only runs (they still cost money). Travel time is the group's time on coaches, trains, boats used as transport and the ferry, from the timed plan; road times were checked against OSRM driving times plus 15% for a coach and a break on long legs.</p>
<h2>Things to confirm before we switch</h2><ul class="cf">{"".join(f"<li>{E(x)}</li>" for x in CONFIRM)}</ul>
<h2 class="pb">Day-by-day plan</h2>{"".join(dayhtml(d) for d in P.DAYS)}
<h2 class="pb">Attraction checklist — where each promise is kept</h2><div class="ccs">{CHK}</div>
"""
FONTS = "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Poppins:wght@400;600;700&display=swap"
open(os.path.join(HERE, "route_optimised.html"), "w").write(
    f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}"><style>{CSS}</style></head><body>{body}</body></html>')
print("old", H(OT), OK, "new", H(NT), NK, "attractions", N)
