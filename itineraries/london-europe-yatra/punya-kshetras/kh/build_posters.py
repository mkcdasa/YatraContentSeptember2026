"""
Marketing posters in the catalogue style (same look as brochure_kh):
  A. one tall image with every detail          → poster_single.html  (1080 × 2280)
  B. the same details split over two images     → poster_part1.html / poster_part2.html (1080 × 1350 each)
Content: ../package.py (price, flights, attractions), kh_days.py (final places), brand skill (logos, contacts).

    python3 kh/build_posters.py && node kh/render_posters.cjs
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_kh as K  # noqa: E402  (reuses images, icons, logos, package and contacts)

PK, C, E, ic, I, IMG = K.PK, K.C, K.E, K.ic, K.I, K.IMG
TOTAL = sum(len(i) for _, i in PK["attractions"]["countries"])
DAYLINE = [
    ("Sat 17 Apr", "Fly to London", "Hyderabad & Bangalore groups land at Heathrow · welcome dinner"),
    ("Sun 18 Apr", "London", "Madame Tussauds · ISKCON Soho · British Museum · Bhaktivedanta Manor"),
    ("Mon 19 Apr", "Royal London", "Buckingham Palace · Tower of London & Koh-i-Noor · Trafalgar Square · London Eye"),
    ("Tue 20 Apr", "London → Paris", "Eurostar under the Channel · Arc de Triomphe · Notre-Dame · Seine cruise"),
    ("Wed 21 Apr", "Paris", "Louvre & Mona Lisa · Eiffel Tower 2nd floor · Trocadéro"),
    ("Thu 22 Apr", "Paris → Brussels", "Atomium · Grand Place · Manneken Pis · Belgian waffles"),
    ("Fri 23 Apr", "Belgium → Amsterdam", "Radhadesh château in the Ardennes · Amsterdam canal cruise"),
    ("Sat 24 Apr", "Holland → Cologne", "Zaanse Schans windmills · Keukenhof tulips · Cologne Cathedral"),
    ("Sun 25 Apr", "Germany", "ISKCON Cologne · Goloka Dham · through the Black Forest"),
    ("Mon 26 Apr", "Black Forest → Zurich", "Lake Titisee & cuckoo clocks · Rhine Falls · Zurich old town"),
    ("Tue 27 Apr", "Swiss Alps", "Snow on Mount Titlis · Ice Flyer · Lucerne · train to Interlaken"),
    ("Wed 28 Apr", "Alps → Italy", "Gotthard · Hare Krishna village, Bergamo · Milan Duomo"),
    ("Thu 29 Apr", "Milan → Venice", "Prabhupada Desh · Padova · St Mark's Square · gondola ride"),
    ("Fri 30 Apr", "Rome & Vatican", "High-speed train · Vatican Museums · Sistine Chapel · St Peter's"),
    ("Sat 1 May", "Rome → Pisa", "Colosseum · Trevi Fountain · Pantheon · Leaning Tower of Pisa"),
    ("Sun 2 May", "Fly home", "Pisa → Milan → Dubai / Abu Dhabi → Hyderabad / Bangalore (land 3 May)"),
]
INCL = [("plane", "International flights"), ("passport", "UK & Schengen visas"), ("bed", "15 nights hotels"),
        ("food", "All Indian veg meals"), ("bus", "Coach, Eurostar & trains"), ("ticket", "All entry tickets"),
        ("user", "Indian tour manager")]
WONDERS = [("colosseum", "Colosseum", "New 7 Wonders"), ("pisa", "Leaning Tower", "Medieval Wonder"),
           ("eiffel", "Eiffel Tower", "330 m icon"), ("sistine", "Sistine Chapel", "Michelangelo")]
COUNTRIES = ["UK", "France", "Belgium", "Netherlands", "Germany", "Switzerland", "Italy", "Vatican"]
FLIGHTS = [("Hyderabad", "Emirates via Dubai", "dep 17 Apr 10:15 · home 3 May 03:05"),
           ("Bangalore", "Etihad via Abu Dhabi", "dep 17 Apr 04:35 · home 3 May 03:15")]

CSS = """
@import url('%s');
*{box-sizing:border-box;margin:0;padding:0}
:root{--n:#2A0D3D;--n2:#3A1452;--n3:#5B1F7E;--o:#F28C28;--c:#E8445A;--g:#E7B24A;--g2:#F6D58B;--cr:#FFF8EE}
body{font-family:Poppins,sans-serif;color:#2A2131;background:#000}
img{display:block}
.po{width:1080px;position:relative;overflow:hidden;background:linear-gradient(180deg,#FFF8EE,#FFEFDC)}
.hero{position:relative;height:var(--hh);overflow:hidden}
.hero>img{width:100%%;height:100%%;object-fit:cover;object-position:50%% 42%%}
.hero .sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(255,248,238,.92) 0%%,rgba(255,248,238,.45) 20%%,rgba(255,248,238,0) 34%%,rgba(42,13,61,0) 52%%,rgba(42,13,61,.85) 82%%,#2A0D3D 100%%)}
.top{position:absolute;top:26px;left:30px;right:30px;display:flex;justify-content:space-between;align-items:center}
.lgw{background:#fff;border-radius:14px;padding:8px 14px;box-shadow:0 4px 14px rgba(0,0,0,.25)}.lgw img{height:62px}
.seal{height:86px;border-radius:50%%;box-shadow:0 0 0 5px #fff,0 4px 14px rgba(0,0,0,.35)}
.tt{position:absolute;top:128px;left:0;right:0;text-align:center}
.s1{font-family:'Great Vibes';font-size:96px;line-height:.9;color:#D8263E;text-shadow:0 3px 0 #fff,0 6px 0 rgba(122,30,43,.5),0 0 24px rgba(255,255,255,.95)}
.s2{font-family:'Playfair Display';font-weight:800;font-size:132px;line-height:.95;letter-spacing:6px;background:linear-gradient(180deg,#FFE7A3,#F6C24A 45%%,#C9851C);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 4px 0 #7A3E0A) drop-shadow(0 8px 12px rgba(0,0,0,.35))}
.s3{display:inline-block;margin-top:8px;background:var(--n);color:#fff;font-family:Montserrat;font-weight:800;font-size:28px;letter-spacing:5px;padding:9px 32px;border-radius:8px}
.hb{position:absolute;left:0;right:0;bottom:24px;text-align:center;color:#fff}
.dt{display:inline-flex;align-items:center;gap:14px;background:#fff;border-radius:50px;padding:7px 7px 7px 28px;box-shadow:0 4px 14px rgba(0,0,0,.3)}
.dt span{font-family:Montserrat;font-weight:800;color:var(--n);font-size:34px}
.dt b{background:linear-gradient(90deg,var(--c),var(--o));color:#fff;font-family:Montserrat;font-weight:800;font-size:27px;border-radius:50px;padding:9px 24px}
.stat{margin-top:14px;font-family:Montserrat;font-weight:700;font-size:25px;color:var(--g2);letter-spacing:1px}
.cty{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin-top:12px;padding:0 40px}
.cty span{border:1.5px solid rgba(246,213,139,.75);border-radius:40px;padding:4px 16px;font-family:Montserrat;font-weight:600;font-size:19px}
.band{background:var(--n);color:#fff;display:flex;align-items:center;justify-content:center;gap:34px;padding:22px 36px}
.pr{text-align:center}
.pr small{display:block;font-family:Montserrat;font-weight:700;font-size:18px;letter-spacing:2px;color:var(--g2);text-transform:uppercase}
.pr b{font-family:Montserrat;font-weight:800;font-size:72px;line-height:1;background:linear-gradient(180deg,#FFE7A3,#F6C24A);-webkit-background-clip:text;background-clip:text;color:transparent}
.pr em{display:block;font-style:normal;font-family:Montserrat;font-weight:600;font-size:19px}
.pr2{display:flex;flex-direction:column;gap:10px}
.pr2 div{background:linear-gradient(90deg,var(--c),var(--o));border-radius:12px;padding:9px 20px;font-family:Montserrat;font-weight:800;font-size:24px;text-align:center}
.pr2 .w{background:#fff;color:var(--n);font-size:19px}
.sec{padding:26px 36px 0}
.h{display:flex;align-items:center;gap:14px;margin-bottom:14px}
.h b{font-family:'Playfair Display';font-weight:800;font-size:40px;color:var(--n)}
.h i{font-family:'Great Vibes';font-style:normal;font-size:44px;color:var(--o)}
.h:after{content:"";flex:1;height:3px;background:linear-gradient(90deg,var(--o),transparent)}
.wons{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.wn{position:relative;text-align:center}
.wn img{width:100%%;height:176px;object-fit:cover;border-radius:14px;border:4px solid #fff;box-shadow:0 4px 14px rgba(0,0,0,.2)}
.wn span{position:absolute;left:8px;right:8px;top:138px;background:linear-gradient(90deg,var(--c),var(--o));color:#fff;border-radius:30px;font-family:Montserrat;font-weight:700;font-size:15px;padding:4px 6px}
.wn b{display:block;font-family:'Playfair Display';color:var(--n);font-size:22px;margin-top:6px}
.days{display:grid;grid-template-columns:1fr 1fr;gap:10px 16px}
.dy{display:flex;gap:12px;align-items:flex-start;background:#fff;border-radius:14px;padding:10px 14px;box-shadow:0 3px 10px rgba(42,13,61,.1);border-left:5px solid var(--o)}
.dn{flex:none;width:58px;text-align:center;background:var(--n);color:#fff;border-radius:10px;padding:5px 0}
.dn small{display:block;font-family:Montserrat;font-weight:700;font-size:11px;letter-spacing:1px}
.dn b{display:block;font-family:Montserrat;font-weight:800;font-size:27px;line-height:1}
.dy h4{font-family:Montserrat;font-weight:800;font-size:19px;color:var(--n);line-height:1.15}
.dy h4 em{font-style:normal;font-weight:600;font-size:14px;color:var(--c);margin-left:6px}
.dy p{font-size:15.5px;line-height:1.3;margin-top:2px;color:#3a3040}
.inc{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.ic{background:#fff;border-radius:14px;padding:12px 8px;text-align:center;box-shadow:0 3px 10px rgba(42,13,61,.1);font-family:Montserrat;font-weight:700;font-size:17px;color:var(--n);line-height:1.2}
.ic svg{width:46px;height:46px;margin:0 auto 6px;background:#FFF0E0;border-radius:50%%;padding:9px}
.ic.big{grid-column:span 1;background:linear-gradient(135deg,var(--n2),var(--c));color:#fff}.ic.big svg{background:rgba(255,255,255,.22)}
.fl{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.f{display:flex;gap:12px;align-items:center;background:#fff;border-radius:14px;padding:12px 16px;box-shadow:0 3px 10px rgba(42,13,61,.1)}
.f svg{flex:none;width:46px;height:46px;background:linear-gradient(135deg,var(--c),var(--o));border-radius:50%%;padding:10px}
.f b{display:block;font-family:Montserrat;font-weight:800;font-size:20px;color:var(--n)}
.f span{font-size:16px}
.why{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.wy{background:#fff;border-radius:14px;padding:12px;text-align:center;box-shadow:0 3px 10px rgba(42,13,61,.1)}
.wy svg{width:44px;height:44px;margin:0 auto 6px;background:linear-gradient(135deg,var(--n2),var(--c));border-radius:50%%;padding:9px}
.wy b{display:block;font-family:Montserrat;font-weight:800;font-size:17px;color:var(--n)}
.wy span{font-size:14px;line-height:1.25;display:block;margin-top:2px}
.cta{position:absolute;left:0;right:0;bottom:0;height:150px}
.cta svg.brush{position:absolute;inset:0;width:100%%;height:100%%}
.ctab{position:absolute;left:36px;right:36px;bottom:20px;display:flex;align-items:center;justify-content:space-between;color:#fff}
.bk{background:linear-gradient(90deg,var(--c),var(--o));border-radius:40px;padding:12px 26px;font-family:Montserrat;font-weight:800;font-size:26px;white-space:nowrap}
.ph{font-family:Montserrat;font-weight:800;font-size:54px;color:var(--g2);display:flex;align-items:center;gap:10px}
.ph svg{width:46px;height:46px}
.web{text-align:right;font-family:Montserrat;font-weight:600;font-size:18px;line-height:1.45}
.pg{position:absolute;top:118px;right:30px;background:var(--c);color:#fff;font-family:Montserrat;font-weight:800;font-size:20px;border-radius:30px;padding:6px 16px}
.p2top{position:relative;height:250px;overflow:hidden}
.p2top>img{width:100%%;height:100%%;object-fit:cover;object-position:50%% 55%%}
.p2top .sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(42,13,61,.25),rgba(42,13,61,.9))}
.p2t{position:absolute;left:36px;right:36px;bottom:22px;color:#fff;display:flex;justify-content:space-between;align-items:flex-end}
.p2t .a{font-family:'Great Vibes';font-size:54px;color:var(--g2);line-height:.9}
.p2t .b{font-family:'Playfair Display';font-weight:800;font-size:54px;line-height:1}
.p2t .c{text-align:right;font-family:Montserrat;font-weight:700;font-size:22px}
.p2t .c b{display:block;font-size:40px;color:var(--g2)}
.p2lg{position:absolute;top:22px;left:30px;display:flex;gap:10px}
.p2lg .lgw img{height:46px}
"""

def brush():
    return ('<div class="cta"><svg class="brush" viewBox="0 0 1080 150" preserveAspectRatio="none">'
            '<path fill="#F28C28" d="M0,40 C180,14 330,52 520,30 C720,6 880,46 1080,20 L1080,150 L0,150Z"/>'
            '<path fill="#2A0D3D" d="M0,58 C200,34 360,70 560,50 C760,28 900,62 1080,42 L1080,150 L0,150Z"/></svg>'
            f'<div class="ctab"><span class="bk">Book Now →</span><span class="ph">{ic(I["phone"], "#F6D58B", 2)}{C["phone"]}</span>'
            f'<span class="web">{C["web1"]}<br>{C["web2"]}<br>{C["social"]}</span></div></div>')

def hero(h, img="towerbridge"):
    circ = "".join(f"<span>{c}</span>" for c in COUNTRIES)
    return f'''<div class="hero" style="--hh:{h}px"><img src="{IMG(img)}"><div class="sh"></div>
<div class="top"><div class="lgw"><img src="{K.LOGO_HK}"></div><img class="seal" src="{K.SEAL}"><div class="lgw"><img src="{K.LOGO_PK}"></div></div>
<div class="tt"><div class="s1">London &amp;</div><div class="s2">EUROPE</div><div class="s3">GRAND TOUR 2027</div></div>
<div class="hb"><div class="dt"><span>17 April – 2 May 2027</span><b>15 Nights / 16 Days</b></div>
<div class="stat">8 Countries · {TOTAL} Attractions · {len(PK["attractions"]["unesco"])} UNESCO World Heritage Sites</div><div class="cty">{circ}</div></div></div>'''

def band():
    return f'''<div class="band"><div class="pr"><small>All-inclusive · per person</small><b>{E(PK["price"])}</b><em>+ 5% GST + 2% TCS (TCS credited back in your ITR)</em></div>
<div class="pr2"><div>International flights &amp; visas included</div><div class="w">Limited seats · one coach only</div></div></div>'''

def wonders():
    w = "".join(f'<div class="wn"><img src="{IMG(k)}"><span>{E(b)}</span><b>{E(t)}</b></div>' for k, t, b in WONDERS)
    return f'<div class="sec"><div class="h"><i>Wonders</i><b>of the world</b></div><div class="wons">{w}</div></div>'

def days(title=True):
    d = "".join(f'<div class="dy"><div class="dn"><small>DAY</small><b>{n:02d}</b></div><div><h4>{E(t)}<em>{E(dt)}</em></h4><p>{E(p)}</p></div></div>'
                for n, (dt, t, p) in enumerate(DAYLINE, 1))
    h = '<div class="h"><i>Your</i><b>16-day journey</b></div>' if title else ""
    return f'<div class="sec">{h}<div class="days">{d}</div></div>'

def incl():
    i = "".join(f'<div class="ic">{ic(I[k], "#E8445A")}{E(t)}</div>' for k, t in INCL)
    i += f'<div class="ic big">{ic(I["star"], "#fff")}{TOTAL} attractions<br>all included</div>'
    return f'<div class="sec"><div class="h"><i>All</i><b>inclusive</b></div><div class="inc">{i}</div></div>'

def flights():
    f = "".join(f'<div class="f">{ic(I["plane"], "#fff")}<div><b>From {E(a)} · {E(b)}</b><span>{E(c)}</span></div></div>' for a, b, c in FLIGHTS)
    return f'<div class="sec"><div class="h"><i>Flights</i><b>booked by us</b></div><div class="fl">{f}</div></div>'

WHY = [("food", "Indian food", "Veg breakfast, lunch & dinner daily"), ("user", "Tour manager", "Speaks your language, start to end"),
       ("senior", "Senior care", "Relaxed pace, lifts & wheelchairs"), ("passport", "Visa help", "UK & Schengen, step by step")]
def why():
    w = "".join(f'<div class="wy">{ic(I[k], "#fff")}<b>{E(t)}</b><span>{E(s)}</span></div>' for k, t, s in WHY)
    return f'<div class="sec"><div class="h"><i>Why</i><b>travel with us</b></div><div class="why">{w}</div></div>'

def page(body, h, name):
    html = (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS % K.FONTS}</style></head>'
            f'<body><div class="po" style="height:{h}px">{body}{brush()}</div></body></html>')
    open(os.path.join(HERE, name), "w").write(html)

def build():
    page(hero(720) + band() + wonders() + days() + incl() + flights() + why(), 2560, "poster_single.html")
    page(hero(760) + band() + wonders() + incl().replace('class="sec"', 'class="sec" style="padding-top:20px"')
         + '<div class="pg">1 / 2</div>', 1350 + 520, "poster_part1.html")
    p2 = (f'<div class="p2top"><img src="{IMG("colosseum")}"><div class="sh"></div>'
          f'<div class="p2lg"><div class="lgw"><img src="{K.LOGO_HK}"></div><div class="lgw"><img src="{K.LOGO_PK}"></div></div>'
          f'<div class="p2t"><div><div class="a">Your 16-day</div><div class="b">Journey</div></div>'
          f'<div class="c">17 Apr – 2 May 2027<b>{E(PK["price"])}</b>+ 5% GST + 2% TCS · incl. flights &amp; visas</div></div></div>'
          + days(False) + flights() + why() + '<div class="pg">2 / 2</div>')
    page(p2, 1350 + 520, "poster_part2.html")
    print("wrote poster_single.html, poster_part1.html, poster_part2.html")

if __name__ == "__main__":
    build()
