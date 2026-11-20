"""
Four two-part poster sets (1080 × 1350 each), built to attract Indian travellers:
  bollywood – Bollywood-famous places (Swiss snow, Keukenhof tulips, Eiffel, Venice, Madame Tussauds)
  unesco    – 2 wonders of the world + 10 UNESCO World Heritage Sites
  top10     – top 10 must-see attractions countdown
  passport  – country-by-country passport stamps
Part 1 = the hook; Part 2 = every detail (16 days, inclusions, flights, price, contacts), styled per set.

    python3 kh/build_posters4.py && node kh/render_posters4.cjs
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_kh as K  # noqa: E402
from build_posters import TOTAL, DAYLINE  # noqa: E402
from build_posters3 import BASE, footer, logos  # noqa: E402

PK, C, E, ic, I, IMG = K.PK, K.C, K.E, K.ic, K.I, K.IMG
PRICE = E(PK["price"])

def doc(css, body, name, cls="p1"):
    open(os.path.join(HERE, name), "w").write(
        f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE % K.FONTS}{PART2_CSS}{css}</style></head>'
        f'<body><div class="po {cls}">{body}</div></body></html>')

# ---------- shared part 2 (all details), themed by CSS variables ----------
PART2_CSS = """
.p2{position:absolute;inset:0;background:var(--bg)}
.p2h{position:absolute;top:0;left:0;right:0;height:210px;background:var(--hd);color:#fff}
.p2h .lg{position:absolute;top:20px;left:28px;display:flex;gap:10px}.p2h .lgw img{height:42px}
.p2h .t{position:absolute;left:30px;bottom:22px}
.p2h .t small{font-family:Montserrat;font-weight:800;font-size:18px;letter-spacing:3px;color:var(--ac)}
.p2h .t b{display:block;font-family:'Playfair Display';font-weight:800;font-size:46px;line-height:1.05}
.p2h .p{position:absolute;right:30px;top:24px;text-align:right}
.p2h .p small{font-family:Montserrat;font-weight:700;font-size:15px;letter-spacing:2px;color:var(--ac)}
.p2h .p b{display:block;font-family:Montserrat;font-weight:800;font-size:58px;line-height:1}
.p2h .p span{font-family:Montserrat;font-weight:600;font-size:16px}
.p2h .pg{position:absolute;right:30px;bottom:22px;background:var(--ac);color:var(--hd2);font-family:Montserrat;font-weight:800;font-size:18px;border-radius:20px;padding:4px 14px}
.dl{position:absolute;top:226px;left:28px;right:28px;display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:87px;gap:8px 14px}
.dd{display:flex;gap:10px;align-items:flex-start;background:#fff;border-radius:12px;padding:9px 12px;box-shadow:0 2px 8px rgba(0,0,0,.08);border-left:5px solid var(--ac2)}
.dd i{flex:none;font-style:normal;width:50px;text-align:center;background:var(--hd);color:#fff;border-radius:8px;font-family:Montserrat;font-weight:800;font-size:24px;line-height:1;padding:6px 0}
.dd i small{display:block;font-size:9px;letter-spacing:1px}
.dd b{font-family:Montserrat;font-weight:800;font-size:18px;color:var(--tx);display:block;line-height:1.15}
.dd span{font-size:15px;line-height:1.3;margin-top:2px;color:#444;display:block}
.inl{position:absolute;top:1000px;left:28px;right:28px;display:grid;grid-template-columns:repeat(8,1fr);gap:6px}
.inl div{background:#fff;border-radius:12px;padding:7px 3px;text-align:center;font-family:Montserrat;font-weight:700;font-size:12.5px;color:var(--tx);box-shadow:0 2px 8px rgba(0,0,0,.08);line-height:1.2}
.inl svg{width:32px;height:32px;display:block;margin:0 auto 3px;background:var(--soft);border-radius:50%;padding:6px}
.fls{position:absolute;top:1092px;left:28px;right:28px;display:grid;grid-template-columns:1fr 1fr;gap:10px}
.fls>div{background:#fff;border-radius:12px;padding:9px 12px;box-shadow:0 2px 8px rgba(0,0,0,.08);font-size:14px;color:#333;display:flex;gap:10px;align-items:center}
.fls svg{flex:none;width:34px;height:34px;background:var(--hd);border-radius:50%;padding:7px}
.fls b{display:block;font-family:Montserrat;font-weight:800;font-size:16px;color:var(--tx)}
.why4{position:absolute;top:1166px;left:28px;right:28px;text-align:center;font-family:Montserrat;font-weight:700;font-size:15px;color:var(--tx);line-height:1.4}
.why4 b{color:var(--ac2)}
"""
INC = [("plane", "International flights"), ("passport", "UK & Schengen visas"), ("bed", "15 nights hotels"), ("food", "Indian veg, all meals"),
       ("bus", "Coach, Eurostar & trains"), ("ticket", f"{TOTAL} attractions"), ("user", "Indian tour manager"), ("senior", "Senior-friendly pace")]
def part2(title_small, title, foot):
    days = "".join(f'<div class="dd"><i><small>DAY</small>{n:02d}</i><div><b>{E(t)} · {E(dt)}</b><span>{E(p)}</span></div></div>'
                   for n, (dt, t, p) in enumerate(DAYLINE, 1))
    inc = "".join(f'<div>{ic(I[k], "var(--ac2)")}{E(t)}</div>' for k, t in INC)
    fl = (f'<div>{ic(I["plane"], "#fff")}<div><b>From Hyderabad · Emirates via Dubai</b>Sat 17 Apr 10:15 → London 18:40 · home Mon 3 May 03:05</div></div>'
          f'<div>{ic(I["plane"], "#fff")}<div><b>From Bangalore · Etihad via Abu Dhabi</b>Sat 17 Apr 04:35 → London 12:45 · home Mon 3 May 03:15</div></div>')
    return (f'<div class="p2"><div class="p2h"><div class="lg"><div class="lgw"><img src="{K.LOGO_HK}"></div><div class="lgw"><img src="{K.LOGO_PK}"></div></div>'
            f'<div class="t"><small>{title_small}</small><b>{title}</b></div>'
            f'<div class="p"><small>ALL-INCLUSIVE · PER PERSON</small><b>{PRICE}</b><span>+ 5% GST + 2% TCS · flights &amp; visas incl.</span></div>'
            f'<div class="pg">2 / 2</div></div><div class="dl">{days}</div><div class="inl">{inc}</div><div class="fls">{fl}</div>'
            f'<div class="why4"><b>Why us:</b> home-style Indian vegetarian food every day · one tour manager who speaks your language · visa help step by step · relaxed pace for seniors · run by Hare Krishna Golden Temple, Hyderabad</div></div>'
            + foot)

# ================= 1. Bollywood dreams (magenta / gold / film) =================
def bollywood():
    vars_ = ":root{--bg:#FFF4FA;--hd:#7A0B4C;--hd2:#4A0530;--ac:#FFC93C;--ac2:#D6147A;--tx:#4A0530;--soft:#FFE3F1}"
    css = vars_ + """
.po.p1{background:#14020D}
.film{position:absolute;left:0;right:0;height:46px;background:#000;display:flex;gap:18px;padding:10px 12px;overflow:hidden}
.film i{flex:none;width:30px;height:26px;background:#2b2b2b;border-radius:4px}
.ttl{position:absolute;top:150px;left:0;right:0;text-align:center}
.ttl small{font-family:Montserrat;font-weight:800;letter-spacing:8px;font-size:22px;color:#FFC93C}
.ttl .a{font-family:'Great Vibes';font-size:92px;color:#FF5FB0;line-height:1;text-shadow:0 0 20px rgba(255,95,176,.6)}
.ttl .b{font-family:Montserrat;font-weight:800;font-size:68px;color:#fff;line-height:1;letter-spacing:2px}
.sc{position:absolute;overflow:hidden;border-radius:16px;border:5px solid #FFC93C;box-shadow:0 10px 24px rgba(0,0,0,.5)}
.sc img{width:100%;height:100%;object-fit:cover}
.sc span{position:absolute;left:0;right:0;bottom:0;padding:26px 12px 10px;background:linear-gradient(transparent,rgba(20,2,13,.92));color:#fff}
.sc span b{display:block;font-family:Montserrat;font-weight:800;font-size:22px;color:#FFC93C}
.sc span em{font-style:normal;font-size:15px;line-height:1.25;display:block}
.pp{position:absolute;left:40px;right:40px;top:1090px;display:flex;align-items:center;justify-content:space-between;background:linear-gradient(90deg,#D6147A,#7A0B4C);border-radius:20px;padding:14px 26px;color:#fff}
.pp b{font-family:Montserrat;font-weight:800;font-size:54px;line-height:1}
.pp small{display:block;font-family:Montserrat;font-weight:700;font-size:15px;letter-spacing:2px;color:#FFC93C}
.pp span{text-align:right;font-family:Montserrat;font-weight:700;font-size:18px;line-height:1.4}
.pg1{position:absolute;top:110px;right:30px;background:#FFC93C;color:#4A0530;font-family:Montserrat;font-weight:800;font-size:18px;border-radius:20px;padding:4px 14px}
"""
    sc = [("titlis", "Snow in Switzerland", "Mount Titlis – with the famous DDLJ cut-out at the top", 40, 400, 490, 330),
          ("keukenhof", "Keukenhof tulips", "Where Silsila's 'Dekha Ek Khwab' was filmed", 550, 400, 490, 330),
          ("eiffel", "Eiffel Tower", "Up to the 2nd floor + Seine cruise", 40, 750, 320, 320),
          ("venice", "Venice gondola", "The most romantic ride in Europe", 380, 750, 320, 320),
          ("londoneye", "London Eye", "& Madame Tussauds Bollywood stars", 720, 750, 320, 320)]
    s = "".join(f'<div class="sc" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><img src="{IMG(k)}"><span><b>{t}</b><em>{d}</em></span></div>' for k, t, d, x, y, w, h in sc)
    holes = "".join("<i></i>" for _ in range(30))
    ft = footer("#000", "#fff", "linear-gradient(90deg,#D6147A,#FF5FB0)", "#fff", "#FFC93C")
    p1 = (f'<div class="film" style="top:0">{holes}</div>{logos()}<div class="pg1">1 / 2</div>'
          f'<div class="ttl"><small>LONDON &amp; EUROPE · 17 APR – 2 MAY 2027</small><div class="a">Live your</div><div class="b">BOLLYWOOD DREAM</div></div>{s}'
          f'<div class="pp"><div><small>ALL-INCLUSIVE · PER PERSON</small><b>{PRICE}</b></div><span>+ 5% GST + 2% TCS<br>Flights, visas, hotels &amp; Indian meals included</span></div>{ft}')
    doc(css, p1, "p4_bollywood_1.html")
    doc(css, part2("16 DAYS · 8 COUNTRIES · " + str(TOTAL) + " ATTRACTIONS", "Your Bollywood-style Europe", ft), "p4_bollywood_2.html", "")

# ================= 2. Wonders & UNESCO (forest green / gold) =================
def unesco():
    vars_ = ":root{--bg:#F4F1E6;--hd:#14532D;--hd2:#0B2E19;--ac:#E9C46A;--ac2:#B7791F;--tx:#14321F;--soft:#FBF3DC}"
    css = vars_ + """
.po.p1{background:#0F3D24}
.pat{position:absolute;inset:0;opacity:.07;background:repeating-linear-gradient(45deg,#E9C46A 0 2px,transparent 2px 22px)}
.ttl{position:absolute;top:140px;left:0;right:0;text-align:center;color:#fff}
.ttl small{font-family:Montserrat;font-weight:800;letter-spacing:6px;font-size:20px;color:#E9C46A}
.ttl b{display:block;font-family:'Playfair Display';font-weight:800;font-size:58px;line-height:1.05}
.ttl span{font-family:'Great Vibes';font-size:54px;color:#E9C46A}
.w2{position:absolute;top:330px;left:40px;right:40px;display:grid;grid-template-columns:1fr 1fr;gap:20px}
.wx{position:relative;height:300px;border-radius:18px;overflow:hidden;border:5px solid #E9C46A}
.wx img{width:100%;height:100%;object-fit:cover}
.wx .bd{position:absolute;top:12px;left:12px;background:#E9C46A;color:#0B2E19;font-family:Montserrat;font-weight:800;font-size:16px;padding:6px 14px;border-radius:30px}
.wx span{position:absolute;left:0;right:0;bottom:0;padding:24px 14px 10px;background:linear-gradient(transparent,rgba(11,46,25,.95));color:#fff;font-family:'Playfair Display';font-weight:800;font-size:30px}
.uh{position:absolute;top:660px;left:40px;right:40px;display:flex;align-items:center;gap:14px;color:#fff}
.uh b{font-family:Montserrat;font-weight:800;font-size:28px}
.uh i{font-style:normal;width:62px;height:62px;border-radius:50%;background:#E9C46A;color:#0B2E19;display:flex;align-items:center;justify-content:center;font-family:Montserrat;font-weight:800;font-size:28px}
.uh:after{content:"";flex:1;height:2px;background:linear-gradient(90deg,#E9C46A,transparent)}
.ug{position:absolute;top:740px;left:40px;right:40px;display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.u{position:relative;height:108px;border-radius:12px;overflow:hidden;border:2px solid rgba(233,196,106,.7)}
.u img{width:100%;height:100%;object-fit:cover}
.u span{position:absolute;left:0;right:0;bottom:0;padding:16px 8px 6px;background:linear-gradient(transparent,rgba(11,46,25,.95));color:#fff;font-family:Montserrat;font-weight:700;font-size:13.5px;line-height:1.15}
.pp{position:absolute;left:40px;right:40px;top:1110px;display:flex;align-items:center;justify-content:space-between;background:#E9C46A;border-radius:18px;padding:12px 24px;color:#0B2E19}
.pp b{font-family:Montserrat;font-weight:800;font-size:52px;line-height:1}
.pp small{display:block;font-family:Montserrat;font-weight:800;font-size:14px;letter-spacing:2px}
.pp span{text-align:right;font-family:Montserrat;font-weight:700;font-size:17px;line-height:1.4}
.pg1{position:absolute;top:110px;right:30px;background:#E9C46A;color:#0B2E19;font-family:Montserrat;font-weight:800;font-size:18px;border-radius:20px;padding:4px 14px}
"""
    un = [("tower", "Tower of London"), ("bigben", "Westminster"), ("notredame", "Paris, Seine banks"), ("grandplace", "Grand Place, Brussels"),
          ("amsterdam", "Amsterdam canals"), ("cologne", "Cologne Cathedral"), ("venice", "Venice & lagoon"), ("colosseum2", "Historic Rome"),
          ("stpeters", "Vatican City"), ("pisa", "Piazza del Duomo, Pisa"), ("eiffelnight", "+ Eiffel Tower"), ("trevi", "+ Trevi Fountain")]
    ug = "".join(f'<div class="u"><img src="{IMG(k)}"><span>{t}</span></div>' for k, t in un)
    ft = footer("#0B2E19", "#fff", "#E9C46A", "#0B2E19", "#E9C46A")
    p1 = (f'<div class="pat"></div>{logos()}<div class="pg1">1 / 2</div>'
          f'<div class="ttl"><small>LONDON &amp; EUROPE GRAND TOUR · 2027</small><b>See the Wonders of the World</b><span>in 16 days</span></div>'
          f'<div class="w2"><div class="wx"><img src="{IMG("colosseum")}"><div class="bd">NEW 7 WONDERS OF THE WORLD</div><span>Colosseum, Rome</span></div>'
          f'<div class="wx"><img src="{IMG("pisa")}"><div class="bd">WONDER OF THE MEDIEVAL WORLD</div><span>Leaning Tower of Pisa</span></div></div>'
          f'<div class="uh"><i>10</i><b>UNESCO World Heritage Sites</b></div><div class="ug">{ug}</div>'
          f'<div class="pp"><div><small>ALL-INCLUSIVE · PER PERSON</small><b>{PRICE}</b></div><span>+ 5% GST + 2% TCS · 17 Apr – 2 May 2027<br>Flights, visas, hotels &amp; Indian meals included</span></div>{ft}')
    doc(css, p1, "p4_unesco_1.html")
    doc(css, part2("2 WONDERS · 10 UNESCO SITES · 8 COUNTRIES", "Your 16-day heritage journey", ft), "p4_unesco_2.html", "")

# ================= 3. Top 10 must-see (sunset orange / white) =================
def top10():
    vars_ = ":root{--bg:#FFF7EF;--hd:#EA580C;--hd2:#7C2D12;--ac:#FFE08A;--ac2:#EA580C;--tx:#431407;--soft:#FFEDD5}"
    css = vars_ + """
.po.p1{background:linear-gradient(180deg,#FFF7EF,#FFE4CC)}
.ttl{position:absolute;top:120px;left:40px;right:40px;display:flex;align-items:flex-end;gap:18px}
.ttl .n{font-family:Montserrat;font-weight:800;font-size:200px;line-height:.8;background:linear-gradient(180deg,#F97316,#B91C1C);-webkit-background-clip:text;background-clip:text;color:transparent}
.ttl .t small{font-family:Montserrat;font-weight:800;font-size:22px;letter-spacing:4px;color:#B91C1C}
.ttl .t b{display:block;font-family:'Playfair Display';font-weight:800;font-size:58px;line-height:1;color:#431407}
.ttl .t span{font-family:Montserrat;font-weight:700;font-size:22px;color:#7C2D12}
.tg{position:absolute;top:320px;left:40px;right:40px;display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
.tt{position:relative;height:138px;border-radius:16px;overflow:hidden;display:flex;background:#fff;box-shadow:0 4px 12px rgba(124,45,18,.15)}
.tt img{width:170px;height:100%;object-fit:cover;flex:none}
.tt .r{padding:10px 12px;display:flex;flex-direction:column;justify-content:center}
.tt .r b{font-family:Montserrat;font-weight:800;font-size:20px;color:#431407;line-height:1.15}
.tt .r span{font-size:14.5px;color:#7C2D12;line-height:1.3;margin-top:3px}
.tt i{position:absolute;left:8px;top:8px;font-style:normal;width:46px;height:46px;border-radius:50%;background:linear-gradient(135deg,#F97316,#B91C1C);color:#fff;font-family:Montserrat;font-weight:800;font-size:22px;display:flex;align-items:center;justify-content:center;border:3px solid #fff}
.pp{position:absolute;left:40px;right:40px;top:1080px;display:flex;align-items:center;justify-content:space-between;background:linear-gradient(90deg,#B91C1C,#F97316);border-radius:18px;padding:14px 24px;color:#fff}
.pp b{font-family:Montserrat;font-weight:800;font-size:54px;line-height:1}
.pp small{display:block;font-family:Montserrat;font-weight:800;font-size:14px;letter-spacing:2px;color:#FFE08A}
.pp span{text-align:right;font-family:Montserrat;font-weight:700;font-size:17px;line-height:1.4}
.pg1{position:absolute;top:110px;right:30px;background:#B91C1C;color:#fff;font-family:Montserrat;font-weight:800;font-size:18px;border-radius:20px;padding:4px 14px}
"""
    t = [("eiffel", "Eiffel Tower, Paris", "Lift to the 2nd floor · Seine night cruise"),
         ("titlis", "Snow on Mount Titlis", "Rotair cable car · Glacier Cave · Cliff Walk"),
         ("colosseum", "Colosseum, Rome", "A New 7 Wonder of the World"),
         ("venice", "Venice gondola ride", "St Mark's Square · Rialto · Bridge of Sighs"),
         ("pisa", "Leaning Tower of Pisa", "The famous 'holding the tower' photo"),
         ("bigben", "London Eye & Big Ben", "British Museum · Westminster by night"),
         ("sistine", "Vatican & Sistine Chapel", "Michelangelo · St Peter's Basilica"),
         ("crownjewels", "The Koh-i-Noor", "Crown Jewels at the Tower of London"),
         ("keukenhof", "Keukenhof tulips", "Millions of flowers in full bloom"),
         ("lucerne", "Lucerne & the lake", "Chapel Bridge · Lake Lucerne cruise")]
    tg = "".join(f'<div class="tt"><img src="{IMG(k)}"><i>{n}</i><div class="r"><b>{a}</b><span>{b}</span></div></div>' for n, (k, a, b) in enumerate(t, 1))
    ft = footer("#431407", "#fff", "linear-gradient(90deg,#F97316,#B91C1C)", "#fff", "#FFE08A")
    p1 = (f'{logos()}<div class="pg1">1 / 2</div><div class="ttl"><div class="n">10</div><div class="t"><small>MUST-SEE IN EUROPE</small><b>All in one tour</b>'
          f'<span>London &amp; Europe · 17 Apr – 2 May 2027 · 16 days</span></div></div><div class="tg">{tg}</div>'
          f'<div class="pp"><div><small>ALL-INCLUSIVE · PER PERSON</small><b>{PRICE}</b></div><span>+ 5% GST + 2% TCS<br>+ {TOTAL - 10} more attractions included</span></div>{ft}')
    doc(css, p1, "p4_top10_1.html")
    doc(css, part2("TOP 10 + " + str(TOTAL - 10) + " MORE ATTRACTIONS", "Day by day, all 16 days", ft), "p4_top10_2.html", "")

# ================= 4. Passport stamps (navy / red / cream) =================
def passport():
    vars_ = ":root{--bg:#F5F0E1;--hd:#1E3A5F;--hd2:#0F2238;--ac:#F2C14E;--ac2:#C0392B;--tx:#0F2238;--soft:#FBEFD5}"
    css = vars_ + """
.po.p1{background:#F5F0E1}
.pg0{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(30,58,95,.05) 0 1px,transparent 1px 34px)}
.cv{position:absolute;top:110px;left:40px;width:300px;height:400px;background:#1E3A5F;border-radius:18px;color:#F2C14E;text-align:center;padding-top:40px;box-shadow:0 12px 24px rgba(0,0,0,.3);transform:rotate(-4deg)}
.cv small{font-family:Montserrat;font-weight:700;font-size:16px;letter-spacing:4px}
.cv b{display:block;font-family:'Playfair Display';font-weight:800;font-size:38px;margin-top:20px;line-height:1.1}
.cv .gl{width:120px;height:120px;margin:22px auto;border:4px solid #F2C14E;border-radius:50%}
.cv .gl svg{width:100%;height:100%;padding:16px}
.cv span{font-family:Montserrat;font-weight:700;font-size:15px;letter-spacing:2px}
.tt2{position:absolute;top:130px;left:380px;right:40px}
.tt2 small{font-family:Montserrat;font-weight:800;font-size:20px;letter-spacing:4px;color:#C0392B}
.tt2 b{display:block;font-family:'Playfair Display';font-weight:800;font-size:64px;line-height:1;color:#0F2238}
.tt2 span{display:block;margin-top:10px;font-family:Montserrat;font-weight:700;font-size:22px;color:#1E3A5F}
.tt2 em{display:inline-block;margin-top:14px;font-style:normal;background:#C0392B;color:#fff;font-family:Montserrat;font-weight:800;font-size:20px;padding:6px 18px;border-radius:30px}
.stg{position:absolute;top:540px;left:30px;right:30px;display:grid;grid-template-columns:repeat(4,1fr);gap:14px 12px}
.st{height:250px;border:4px double var(--c);border-radius:18px;padding:10px;text-align:center;color:var(--c);background:rgba(255,255,255,.55);position:relative}
.st:nth-child(odd){transform:rotate(-3deg)}.st:nth-child(even){transform:rotate(2.5deg)}
.st img{width:100%;height:118px;object-fit:cover;border-radius:10px;filter:saturate(1.1)}
.st b{display:block;font-family:Montserrat;font-weight:800;font-size:19px;letter-spacing:2px;margin-top:6px}
.st span{display:block;font-family:Montserrat;font-weight:600;font-size:13px;color:#333;line-height:1.3;margin-top:3px}
.st i{position:absolute;top:-14px;right:-10px;font-style:normal;background:var(--c);color:#fff;font-family:Montserrat;font-weight:800;font-size:13px;padding:4px 9px;border-radius:12px}
.pp{position:absolute;left:40px;right:40px;top:1105px;display:flex;align-items:center;justify-content:space-between;background:#1E3A5F;border-radius:18px;padding:12px 24px;color:#fff}
.pp b{font-family:Montserrat;font-weight:800;font-size:52px;line-height:1;color:#F2C14E}
.pp small{display:block;font-family:Montserrat;font-weight:800;font-size:14px;letter-spacing:2px}
.pp span{text-align:right;font-family:Montserrat;font-weight:700;font-size:17px;line-height:1.4}
.pg1{position:absolute;top:118px;right:30px;background:#C0392B;color:#fff;font-family:Montserrat;font-weight:800;font-size:18px;border-radius:20px;padding:4px 14px}
"""
    stp = [("UNITED KINGDOM", "Tower of London · London Eye · Koh-i-Noor", "towerbridge", "#1E3A5F", "3 NIGHTS"),
           ("FRANCE", "Eiffel Tower · Louvre · Seine cruise", "eiffel", "#C0392B", "2 NIGHTS"),
           ("BELGIUM", "Atomium · Grand Place", "atomium", "#B7791F", "1 NIGHT"),
           ("NETHERLANDS", "Keukenhof · windmills · canals", "keukenhof", "#D9480F", "1 NIGHT"),
           ("GERMANY", "Cologne Cathedral · Black Forest", "cologne", "#2F3E46", "2 NIGHTS"),
           ("SWITZERLAND", "Titlis snow · Lucerne · Rhine Falls", "titlis", "#C0392B", "2 NIGHTS"),
           ("ITALY", "Venice · Colosseum · Pisa · Milan", "venice", "#1F6F3F", "4 NIGHTS"),
           ("VATICAN", "Sistine Chapel · St Peter's", "stpeters", "#6B21A8", "DAY 14")]
    st = "".join(f'<div class="st" style="--c:{c}"><i>{n}</i><img src="{IMG(k)}"><b>{t}</b><span>{d}</span></div>' for t, d, k, c, n in stp)
    ft = footer("#0F2238", "#fff", "#C0392B", "#fff", "#F2C14E")
    p1 = (f'<div class="pg0"></div><div class="lgs" style="left:380px">'
          f'<div class="lgw"><img src="{K.LOGO_HK}"></div><div class="lgw"><img src="{K.LOGO_PK}"></div></div><div class="pg1" style="top:118px">1 / 2</div>'
          f'<div class="cv"><small>GRAND TOUR</small><b>London &amp;<br>Europe</b><div class="gl">{ic(I["globe"], "#F2C14E", 1.4)}</div><span>PASSPORT · 2027</span></div>'
          f'<div class="tt2" style="top:200px"><small>8 STAMPS IN 16 DAYS</small><b>Collect them all</b>'
          f'<span>17 April – 2 May 2027 · {TOTAL} attractions · 10 UNESCO sites</span><em>Flights &amp; visas included</em></div>'
          f'<div class="stg">{st}</div>'
          f'<div class="pp"><div><small>ALL-INCLUSIVE · PER PERSON</small><b>{PRICE}</b></div><span>+ 5% GST + 2% TCS<br>Hotels, Indian meals, coach &amp; tickets included</span></div>{ft}')
    doc(css, p1, "p4_passport_1.html")
    doc(css, part2("8 COUNTRIES · 16 DAYS", "Your passport to Europe", ft), "p4_passport_2.html", "")

if __name__ == "__main__":
    bollywood(); unesco(); top10(); passport()
    print("wrote 8 posters (4 sets × 2)")
