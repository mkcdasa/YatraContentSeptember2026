"""
Six more poster designs in non-brand colour palettes (logos, price, dates, contacts unchanged), 1080 × 1350:
  postcard (teal/mustard) · scrapbook (sky blue) · magazine (red/white) · neon (navy/magenta/cyan)
  arches (teal/coral/sand) · offer (red/yellow, limited seats)

    python3 kh/build_posters3.py && node kh/render_posters3.cjs
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_kh as K  # noqa: E402
from build_posters import TOTAL  # noqa: E402

PK, C, E, ic, I, IMG = K.PK, K.C, K.E, K.ic, K.I, K.IMG
PRICE = E(PK["price"])
BASE = """
@import url('%s');
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Poppins,sans-serif;background:#000}
img{display:block}
.po{width:1080px;height:1350px;position:relative;overflow:hidden}
.lgw{background:#fff;border-radius:14px;padding:8px 14px;box-shadow:0 4px 14px rgba(0,0,0,.2)}.lgw img{height:54px}
.lgs{position:absolute;top:24px;left:28px;right:28px;display:flex;justify-content:space-between;align-items:center;z-index:5}
.seal{height:74px;border-radius:50%%;box-shadow:0 0 0 4px #fff,0 4px 12px rgba(0,0,0,.3)}
.ft{position:absolute;left:0;right:0;bottom:0;height:118px;display:flex;align-items:center;justify-content:space-between;padding:0 36px;z-index:5}
.ft .bk{border-radius:40px;padding:12px 26px;font-family:Montserrat;font-weight:800;font-size:25px;white-space:nowrap}
.ft .ph{font-family:Montserrat;font-weight:800;font-size:52px;display:flex;align-items:center;gap:10px}
.ft .ph svg{width:44px;height:44px}
.ft .web{text-align:right;font-family:Montserrat;font-weight:600;font-size:18px;line-height:1.45}
"""

def footer(bg, fg, btn_bg, btn_fg, ph):
    return (f'<div class="ft" style="background:{bg};color:{fg}"><span class="bk" style="background:{btn_bg};color:{btn_fg}">Book Now →</span>'
            f'<span class="ph" style="color:{ph}">{ic(I["phone"], ph, 2)}{C["phone"]}</span>'
            f'<span class="web">{C["web1"]}<br>{C["web2"]}<br>{C["social"]}</span></div>')

def logos(seal=True):
    return (f'<div class="lgs"><div class="lgw"><img src="{K.LOGO_HK}"></div>'
            + (f'<img class="seal" src="{K.SEAL}">' if seal else "") + f'<div class="lgw"><img src="{K.LOGO_PK}"></div></div>')

def doc(css, body, name):
    open(os.path.join(HERE, name), "w").write(
        f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE % K.FONTS}{css}</style></head>'
        f'<body><div class="po">{body}</div></body></html>')

# 1 ---------- vintage postcard (teal / mustard / cream) ----------
def postcard():
    css = """
.po{background:#F3E9D2}
.paper{position:absolute;inset:0;background:radial-gradient(circle at 20% 20%,rgba(255,255,255,.6),transparent 40%),repeating-linear-gradient(0deg,rgba(0,0,0,.015) 0 2px,transparent 2px 4px)}
.bd{position:absolute;inset:18px;border:10px solid transparent;border-image:repeating-linear-gradient(45deg,#C0392B 0 22px,#F3E9D2 22px 34px,#1F6F78 34px 56px,#F3E9D2 56px 68px) 10}
.gr{position:absolute;top:150px;left:0;right:0;text-align:center}
.gr .a{font-family:'Great Vibes';font-size:72px;color:#1F6F78;line-height:1}
.big{font-family:'Playfair Display';font-weight:800;font-size:236px;line-height:.86;letter-spacing:4px;
 background:url(%s) center/cover;-webkit-background-clip:text;background-clip:text;color:transparent;
 -webkit-text-stroke:5px #1F6F78;filter:drop-shadow(8px 8px 0 #E0A526)}
.gr .c{display:inline-block;margin-top:14px;background:#1F6F78;color:#F3E9D2;font-family:Montserrat;font-weight:800;font-size:28px;letter-spacing:6px;padding:10px 30px;border-radius:6px}
.lond{font-family:'Playfair Display';font-style:italic;font-weight:700;font-size:58px;color:#C0392B;margin-top:4px}
.ph3{position:absolute;top:735px;left:42px;display:flex;gap:12px}
.pc{background:#fff;padding:12px 12px 40px;box-shadow:0 8px 18px rgba(0,0,0,.25);position:relative}
.pc img{width:215px;height:175px;object-fit:cover}
.pc span{position:absolute;left:0;right:0;bottom:8px;text-align:center;font-family:'Great Vibes';font-size:30px;color:#333}
.pc:nth-child(1){transform:rotate(-5deg)}.pc:nth-child(2){transform:rotate(3deg) translateY(-14px)}.pc:nth-child(3){transform:rotate(-2deg)}
.stamp{position:absolute;top:690px;right:56px;width:240px;height:280px;background:#fff;padding:10px;box-shadow:0 6px 16px rgba(0,0,0,.25);transform:rotate(6deg);border:6px dotted #F3E9D2;outline:3px solid #fff}
.stin{width:100%%;height:100%%;background:#C0392B;color:#fff;text-align:center;display:flex;flex-direction:column;justify-content:center;border:3px solid #fff;outline:2px solid #C0392B}
.stin small{font-family:Montserrat;font-weight:700;font-size:15px;letter-spacing:2px}
.stin b{font-family:Montserrat;font-weight:800;font-size:35px;line-height:1.1}
.stin span{font-family:Montserrat;font-size:14px;line-height:1.3;padding:0 8px}
.pm{position:absolute;top:610px;right:250px;width:150px;height:150px;border:4px solid rgba(31,111,120,.65);border-radius:50%%;display:flex;align-items:center;justify-content:center;text-align:center;transform:rotate(-14deg);font-family:Montserrat;font-weight:800;color:rgba(31,111,120,.75);font-size:18px;line-height:1.2}
.lines{position:absolute;top:1000px;left:70px;right:70px;display:grid;grid-template-columns:1fr 1fr;gap:10px 40px}
.lines div{font-family:Montserrat;font-weight:700;font-size:21px;color:#1F3F44;border-bottom:2px dotted #1F6F78;padding-bottom:6px}
.lines div b{color:#C0392B}
"""
    pcs = "".join(f'<div class="pc"><img src="{IMG(k)}"><span>{t}</span></div>' for k, t in (("eiffel", "Paris"), ("venice", "Venice"), ("titlis", "Swiss Alps")))
    lines = "".join(f"<div><b>✓</b> {t}</div>" for t in ["International flights & visas", "15 nights in good hotels", "Indian veg meals, every meal",
                                                         f"{TOTAL} attractions, all tickets", "Coach, Eurostar & trains", "Indian tour manager"])
    body = (f'<div class="paper"></div><div class="bd"></div>{logos()}'
            f'<div class="gr"><div class="a">Greetings from</div><div class="lond">London &amp;</div><div class="big">EUROPE</div>'
            f'<div class="c">17 APR – 2 MAY 2027 · 16 DAYS</div></div>'
            f'<div class="ph3">{pcs}</div><div class="pm">GRAND<br>TOUR<br>2027</div>'
            f'<div class="stamp"><div class="stin"><small>ALL-INCLUSIVE</small><b>{PRICE}</b><span>per person<br>+ 5% GST + 2% TCS<br>flights &amp; visas incl.</span></div></div>'
            f'<div class="lines">{lines}</div>'
            + footer("#1F6F78", "#F3E9D2", "#E0A526", "#1F3F44", "#F3E9D2"))
    doc(css % (K.FONTS, IMG("colosseum")) if False else css.replace("%s", IMG("colosseum")).replace("%%", "%"), body, "p3_postcard.html")

# 2 ---------- polaroid scrapbook (sky blue) ----------
def scrapbook():
    css = """
.po{background:linear-gradient(180deg,#BFE6FF 0%,#E8F6FF 55%,#FFFFFF 100%)}
.cl{position:absolute;background:#fff;border-radius:50%;opacity:.8}
.tt{position:absolute;top:130px;left:0;right:0;text-align:center}
.tt .a{font-family:'Great Vibes';font-size:84px;color:#0B5394;line-height:.9}
.tt .b{font-family:Montserrat;font-weight:800;font-size:96px;color:#0B3D63;letter-spacing:6px;line-height:1}
.tt .c{display:inline-block;margin-top:10px;background:#FF6B6B;color:#fff;font-family:Montserrat;font-weight:800;font-size:26px;padding:8px 26px;border-radius:40px;transform:rotate(-2deg)}
.pl{position:absolute;background:#fff;padding:14px 14px 56px;box-shadow:0 10px 24px rgba(11,61,99,.28)}
.pl img{width:100%;height:100%;object-fit:cover}
.pl span{position:absolute;left:0;right:0;bottom:10px;text-align:center;font-family:'Great Vibes';font-size:36px;color:#0B3D63}
.pl:after{content:"";position:absolute;top:-16px;left:50%;width:110px;height:34px;margin-left:-55px;background:rgba(255,214,102,.75);transform:rotate(-4deg)}
.tag{position:absolute;right:70px;top:985px;width:330px;background:#FFD166;border-radius:20px 20px 20px 20px;padding:22px 24px;text-align:center;transform:rotate(-4deg);box-shadow:0 10px 24px rgba(0,0,0,.2)}
.tag:before{content:"";position:absolute;left:22px;top:22px;width:22px;height:22px;border-radius:50%;background:#E8F6FF;box-shadow:inset 0 2px 4px rgba(0,0,0,.2)}
.tag small{font-family:Montserrat;font-weight:800;font-size:17px;letter-spacing:2px;color:#0B3D63}
.tag b{display:block;font-family:Montserrat;font-weight:800;font-size:58px;color:#0B3D63;line-height:1.05}
.tag span{font-family:Montserrat;font-weight:600;font-size:16px;color:#0B3D63}
.chk{position:absolute;left:60px;top:975px;width:560px}
.chk div{font-family:Montserrat;font-weight:700;font-size:21px;color:#0B3D63;padding:4px 0;display:flex;gap:10px;align-items:center}
.chk div i{font-style:normal;width:30px;height:30px;border-radius:8px;background:#06D6A0;color:#fff;display:flex;align-items:center;justify-content:center;font-size:20px}
"""
    pls = [("towerbridge", "London", 60, 395, 300, 205, -6), ("eiffel", "Paris", 390, 380, 300, 220, 3), ("colosseum", "Rome", 720, 400, 300, 205, -3),
           ("keukenhof", "Keukenhof", 110, 690, 290, 180, 4), ("titlis", "Swiss Alps", 420, 700, 280, 180, -4), ("venice", "Venice", 730, 685, 290, 185, 5)]
    p = "".join(f'<div class="pl" style="left:{x}px;top:{y}px;width:{w}px;height:{h + 70}px;transform:rotate({r}deg)"><img src="{IMG(k)}" style="height:{h}px"><span>{t}</span></div>'
                for k, t, x, y, w, h, r in pls)
    clouds = "".join(f'<div class="cl" style="left:{x}px;top:{y}px;width:{w}px;height:{w*.45:.0f}px"></div>' for x, y, w in [(-40, 60, 260), (820, 90, 300), (380, 20, 200)])
    chk = "".join(f"<div><i>✓</i>{t}</div>" for t in ["Flights & visas included", "8 countries · 16 days", f"{TOTAL} attractions · all tickets",
                                                       "Indian veg meals every day", "Indian tour manager"])
    body = (f'{clouds}{logos()}<div class="tt"><div class="a">Pack your bags for</div><div class="b">EUROPE</div>'
            f'<div class="c">17 April – 2 May 2027</div></div>{p}<div class="chk">{chk}</div>'
            f'<div class="tag"><small>ALL-INCLUSIVE</small><b>{PRICE}</b><span>per person + 5% GST + 2% TCS</span></div>'
            + footer("#0B3D63", "#fff", "#FF6B6B", "#fff", "#FFD166"))
    doc(css, body, "p3_scrapbook.html")

# 3 ---------- magazine cover (red / white / black) ----------
def magazine():
    css = """
.bg{position:absolute;inset:0}.bg img{width:100%;height:100%;object-fit:cover;object-position:50% 50%}
.sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.35) 0%,rgba(0,0,0,0) 30%,rgba(0,0,0,0) 55%,rgba(0,0,0,.75) 85%)}
.mast{position:absolute;top:118px;left:36px;right:36px;font-family:'Playfair Display';font-weight:800;font-size:178px;line-height:.85;color:#fff;letter-spacing:-2px;text-shadow:0 4px 18px rgba(0,0,0,.35)}
.mast span{color:#E50914}
.iss{position:absolute;top:478px;left:42px;font-family:Montserrat;font-weight:700;color:#fff;font-size:20px;letter-spacing:4px}
.cl{position:absolute;left:40px;width:420px;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.6)}
.cl b{display:block;font-family:Montserrat;font-weight:800;font-size:34px;line-height:1.05}
.cl span{font-family:Montserrat;font-weight:600;font-size:19px}
.cl i{font-style:normal;color:#FFD400}
.cr{position:absolute;right:40px;width:360px;text-align:right;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.6)}
.cr b{display:block;font-family:Montserrat;font-weight:800;font-size:32px;line-height:1.05}
.cr span{font-family:Montserrat;font-weight:600;font-size:19px}
.burst{position:absolute;right:50px;top:330px;width:250px;height:250px;background:#FFD400;color:#111;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;
 clip-path:polygon(50% 0,61% 12%,75% 6%,79% 21%,94% 21%,91% 36%,100% 46%,90% 57%,96% 71%,81% 75%,79% 90%,64% 87%,54% 100%,43% 89%,28% 95%,23% 80%,8% 78%,11% 63%,0 52%,9% 41%,4% 26%,19% 23%,22% 8%,37% 12%);transform:rotate(8deg)}
.burst small{font-family:Montserrat;font-weight:800;font-size:16px}
.burst b{font-family:Montserrat;font-weight:800;font-size:42px;line-height:1}
.burst span{font-family:Montserrat;font-weight:700;font-size:13px;width:150px}
.bar{position:absolute;left:0;right:0;bottom:118px;background:#E50914;color:#fff;font-family:Montserrat;font-weight:800;font-size:25px;letter-spacing:2px;padding:14px 36px;display:flex;justify-content:space-between}
.lgs .lgw{background:rgba(255,255,255,.95)}
"""
    body = (f'<div class="bg"><img src="{IMG("venice")}"></div><div class="sh"></div>{logos(False)}'
            f'<div class="mast">GRAND<br><span>TOUR</span></div><div class="iss">LONDON &amp; EUROPE · SPRING 2027 ISSUE</div>'
            f'<div class="burst"><small>ALL-INCLUSIVE</small><b>{PRICE}</b><span>per person · flights &amp; visas included</span></div>'
            f'<div class="cl" style="top:640px"><b>8 COUNTRIES<br>16 DAYS</b><span>From Tower Bridge to the <i>Leaning Tower</i></span></div>'
            f'<div class="cl" style="top:800px"><b>{TOTAL} ATTRACTIONS</b><span>Eiffel Tower · Louvre · <i>Colosseum</i> · Vatican</span></div>'
            f'<div class="cr" style="top:640px"><b>SNOW ON<br>MOUNT TITLIS</b><span>Rotair cable car &amp; Glacier Cave</span></div>'
            f'<div class="cr" style="top:810px"><b>GONDOLAS<br>IN VENICE</b><span>St Mark\'s Square &amp; Rialto</span></div>'
            f'<div class="cl" style="top:960px;width:900px"><b style="font-size:28px">INDIAN FOOD EVERY MEAL · INDIAN TOUR MANAGER</b><span>+ 5% GST + 2% TCS · Emirates &amp; Etihad flights from Hyderabad &amp; Bangalore</span></div>'
            f'<div class="bar"><span>17 APRIL – 2 MAY 2027</span><span>LIMITED SEATS</span></div>'
            + footer("#111", "#fff", "#E50914", "#fff", "#FFD400"))
    doc(css, body, "p3_magazine.html")

# 4 ---------- neon night (navy / magenta / cyan) ----------
def neon():
    css = """
.po{background:linear-gradient(160deg,#0B1026 0%,#1B1046 45%,#3A0B4A 100%)}
.bg{position:absolute;left:0;right:0;top:0;height:780px;opacity:.55;-webkit-mask-image:linear-gradient(#000 40%,transparent);mask-image:linear-gradient(#000 40%,transparent)}
.bg img{width:100%;height:100%;object-fit:cover}
.glow{position:absolute;border-radius:50%;filter:blur(80px);opacity:.55}
.tt{position:absolute;top:170px;left:0;right:0;text-align:center}
.tt .a{font-family:Montserrat;font-weight:800;font-size:28px;letter-spacing:12px;color:#22D3EE;text-shadow:0 0 16px #22D3EE}
.tt .b{font-family:Montserrat;font-weight:800;font-size:150px;line-height:.95;color:#fff;text-shadow:0 0 18px #FF2E9A,0 0 46px #FF2E9A}
.tt .c{font-family:'Great Vibes';font-size:76px;color:#FF7AC6;text-shadow:0 0 14px #FF2E9A;line-height:1}
.dt{position:absolute;top:560px;left:0;right:0;text-align:center}
.dt span{display:inline-block;border:2px solid #22D3EE;color:#fff;font-family:Montserrat;font-weight:700;font-size:28px;letter-spacing:3px;padding:10px 30px;border-radius:50px;box-shadow:0 0 18px rgba(34,211,238,.6),inset 0 0 12px rgba(34,211,238,.4)}
.gl{position:absolute;left:48px;right:48px;display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.g{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.22);border-radius:22px;padding:18px;color:#fff;backdrop-filter:blur(6px)}
.g img{width:100%;height:150px;object-fit:cover;border-radius:14px}
.g b{display:block;font-family:Montserrat;font-weight:800;font-size:22px;margin-top:10px}
.g span{font-size:16px;color:#d4d8ff}
.pr{position:absolute;top:1040px;left:48px;right:48px;display:flex;align-items:center;justify-content:space-between;background:linear-gradient(90deg,#FF2E9A,#7C3AED);border-radius:24px;padding:20px 30px;color:#fff;box-shadow:0 0 30px rgba(255,46,154,.45)}
.pr b{font-family:Montserrat;font-weight:800;font-size:62px;line-height:1}
.pr small{display:block;font-family:Montserrat;font-weight:700;font-size:17px;letter-spacing:2px}
.pr span{font-family:Montserrat;font-weight:600;font-size:19px;text-align:right;line-height:1.4}
"""
    gl = "".join(f'<div class="g"><img src="{IMG(k)}"><b>{t}</b><span>{s}</span></div>' for k, t, s in
                 [("eiffelnight", "Paris by night", "Seine cruise & Eiffel"), ("londoneye", "London lights", "London Eye at sunset"), ("colosseum", "Roman nights", "Colosseum & Trevi")])
    body = (f'<div class="bg"><img src="{IMG("eiffelnight")}"></div><div class="glow" style="left:-120px;top:600px;width:420px;height:420px;background:#FF2E9A"></div>'
            f'<div class="glow" style="right:-140px;top:200px;width:460px;height:460px;background:#22D3EE"></div>{logos()}'
            f'<div class="tt"><div class="a">LONDON · PARIS · ROME</div><div class="b">EUROPE</div><div class="c">Grand Tour 2027</div></div>'
            f'<div class="dt"><span>17 APR – 2 MAY · 16 DAYS · 8 COUNTRIES</span></div>'
            f'<div class="gl" style="top:660px">{gl}</div>'
            f'<div class="pr"><div><small>ALL-INCLUSIVE · PER PERSON</small><b>{PRICE}</b></div><span>+ 5% GST + 2% TCS<br>flights, visas, hotels &amp; meals<br>{TOTAL} attractions included</span></div>'
            + footer("#0B1026", "#fff", "linear-gradient(90deg,#FF2E9A,#7C3AED)", "#fff", "#22D3EE"))
    doc(css, body, "p3_neon.html")

# 5 ---------- arches (teal / coral / sand, modern minimal) ----------
def arches():
    css = """
.po{background:#F6EFE6}
.lp{position:absolute;left:0;top:0;bottom:118px;width:440px;background:#0F766E}
.lp .in{position:absolute;top:150px;left:44px;right:30px;color:#fff}
.lp .a{font-family:'Great Vibes';font-size:62px;color:#FDBA74;line-height:1}
.lp .b{font-family:'Playfair Display';font-weight:800;font-size:84px;line-height:.95}
.lp .c{margin-top:18px;font-family:Montserrat;font-weight:700;font-size:22px;line-height:1.5}
.lp .c b{color:#FDBA74}
.lp ul{list-style:none;margin-top:22px}
.lp li{font-family:Montserrat;font-weight:600;font-size:19px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.25);display:flex;gap:10px;align-items:center}
.lp li svg{width:26px;height:26px;flex:none}
.pr{position:absolute;left:44px;right:30px;bottom:30px;background:#F97366;border-radius:20px;padding:18px 20px;color:#fff}
.pr small{font-family:Montserrat;font-weight:800;font-size:15px;letter-spacing:2px}
.pr b{display:block;font-family:Montserrat;font-weight:800;font-size:56px;line-height:1.05}
.pr span{font-family:Montserrat;font-weight:600;font-size:15px}
.ar{position:absolute;overflow:hidden;border-radius:200px 200px 16px 16px;border:8px solid #fff;box-shadow:0 12px 28px rgba(15,118,110,.25)}
.ar img{width:100%;height:100%;object-fit:cover}
.ar span{position:absolute;left:0;right:0;bottom:0;padding:26px 10px 12px;text-align:center;color:#fff;font-family:Montserrat;font-weight:800;font-size:21px;background:linear-gradient(transparent,rgba(15,118,110,.9))}
.lgs{left:470px}
.dot{position:absolute;border-radius:50%}
"""
    li = "".join(f'<li>{ic(I[k], "#FDBA74")}{t}</li>' for k, t in [("plane", "International flights & visas"), ("bed", "15 nights hotels"),
                                                                   ("food", "Indian veg meals"), ("ticket", f"{TOTAL} attractions"), ("user", "Indian tour manager")])
    ars = [("eiffel", "Paris", 480, 160, 270, 470), ("venice", "Venice", 770, 230, 270, 420), ("titlis", "Swiss Alps", 480, 660, 270, 360),
           ("colosseum", "Rome", 770, 680, 270, 410)]
    a = "".join(f'<div class="ar" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><img src="{IMG(k)}"><span>{t}</span></div>' for k, t, x, y, w, h in ars)
    body = (f'<div class="lp"><div class="in"><div class="a">Discover</div><div class="b">London &amp; Europe</div>'
            f'<div class="c">17 April – 2 May 2027<br><b>16 days · 8 countries</b></div><ul>{li}</ul></div>'
            f'<div class="pr"><small>ALL-INCLUSIVE · PER PERSON</small><b>{PRICE}</b><span>+ 5% GST + 2% TCS</span></div></div>'
            f'<div class="dot" style="right:40px;top:150px;width:60px;height:60px;background:#FDBA74"></div>'
            f'<div class="lgs" style="left:470px"><div class="lgw"><img src="{K.LOGO_HK}"></div><div class="lgw"><img src="{K.LOGO_PK}"></div></div>{a}'
            + footer("#134E4A", "#fff", "#F97366", "#fff", "#FDBA74"))
    doc(css, body, "p3_arches.html")

# 6 ---------- offer (red / yellow, urgency) ----------
def offer():
    css = """
.po{background:#C8102E}
.rays{position:absolute;left:50%;top:430px;width:1800px;height:1800px;margin-left:-900px;margin-top:-900px;background:repeating-conic-gradient(rgba(255,255,255,.07) 0 6deg,transparent 6deg 12deg)}
.tt{position:absolute;top:140px;left:0;right:0;text-align:center;color:#fff}
.tt .a{display:inline-block;background:#FFD400;color:#C8102E;font-family:Montserrat;font-weight:800;font-size:30px;letter-spacing:4px;padding:8px 28px;transform:rotate(-2deg)}
.tt .b{font-family:Montserrat;font-weight:800;font-size:98px;line-height:1;margin-top:14px;text-shadow:0 6px 0 rgba(0,0,0,.2)}
.tt .c{font-family:Montserrat;font-weight:700;font-size:30px;margin-top:6px}
.cal{position:absolute;top:470px;left:70px;width:300px;background:#fff;border-radius:22px;overflow:hidden;box-shadow:0 12px 24px rgba(0,0,0,.3);text-align:center}
.cal .m{background:#111;color:#FFD400;font-family:Montserrat;font-weight:800;font-size:26px;padding:10px;letter-spacing:4px}
.cal b{display:block;font-family:Montserrat;font-weight:800;font-size:120px;color:#C8102E;line-height:1.1}
.cal span{display:block;font-family:Montserrat;font-weight:700;font-size:22px;color:#111;padding-bottom:14px}
.ph2{position:absolute;top:460px;left:400px;right:60px;height:330px;border-radius:22px;overflow:hidden;border:8px solid #FFD400;box-shadow:0 12px 24px rgba(0,0,0,.3)}
.ph2 img{width:100%;height:100%;object-fit:cover}
.prb{position:absolute;top:830px;left:60px;right:60px;background:#FFD400;border-radius:24px;padding:20px 30px;display:flex;align-items:center;justify-content:space-between;box-shadow:0 12px 24px rgba(0,0,0,.3)}
.prb b{font-family:Montserrat;font-weight:800;font-size:84px;color:#C8102E;line-height:1}
.prb small{display:block;font-family:Montserrat;font-weight:800;font-size:19px;letter-spacing:2px;color:#111}
.prb span{text-align:right;font-family:Montserrat;font-weight:700;font-size:21px;color:#111;line-height:1.4}
.seats{position:absolute;top:1035px;left:60px;right:60px;display:flex;gap:16px}
.seats div{flex:1;background:rgba(0,0,0,.18);border:2px dashed rgba(255,255,255,.6);border-radius:16px;padding:12px;color:#fff;text-align:center;font-family:Montserrat;font-weight:700;font-size:19px}
.seats div b{display:block;font-size:34px;color:#FFD400}
"""
    body = (f'<div class="rays"></div>{logos()}<div class="tt"><div class="a">LIMITED SEATS · ONE COACH ONLY</div>'
            f'<div class="b">LONDON &amp; EUROPE</div><div class="c">8 countries · 16 days · {TOTAL} attractions</div></div>'
            f'<div class="cal"><div class="m">APRIL 2027</div><b>17</b><span>Departure · Saturday<br>Back 2 May</span></div>'
            f'<div class="ph2"><img src="{IMG("towerbridge")}"></div>'
            f'<div class="prb"><div><small>ALL-INCLUSIVE · PER PERSON</small><b>{PRICE}</b></div><span>+ 5% GST + 2% TCS<br>Flights &amp; visas included<br>Hotels, meals &amp; tickets included</span></div>'
            f'<div class="seats"><div><b>15</b>nights</div><div><b>8</b>countries</div><div><b>{TOTAL}</b>attractions</div><div><b>3</b>meals a day</div></div>'
            + footer("#111", "#fff", "#FFD400", "#C8102E", "#FFD400"))
    doc(css, body, "p3_offer.html")

if __name__ == "__main__":
    postcard(); scrapbook(); magazine(); neon(); arches(); offer()
    print("wrote 6 designs")
