"""
"Headline numbers" poster (1080 × 1350), same look as the brochure's Wonders & Attractions page:
8 COUNTRIES · 3 WONDERS OF THE WORLD · 75 ATTRACTIONS in equal big type, then IN JUST 16 DAYS,
the three wonders, country cards with counts, the 11 UNESCO sites, price and Book Now.

    python3 kh/build_posters5.py && node kh/render_posters5.cjs
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_kh as K  # noqa: E402

PK, C, E, ic, I, IMG = K.PK, K.C, K.E, K.ic, K.I, K.IMG
A = PK["attractions"]
TOTAL = sum(len(i) for _, i in A["countries"])
WONDERS3 = [("colosseum", "Colosseum, Rome", "New 7 Wonders of the World"),
            ("pisa", "Leaning Tower of Pisa", "Wonder of the Medieval World"),
            ("eiffel", "Eiffel Tower, Paris", "Modern wonder · 330 m")]
CICON = {"United Kingdom": "flag", "France": "star", "Belgium": "camera", "Netherlands": "heart", "Germany": "pin",
         "Switzerland": "sun", "Italy": "globe", "Vatican City": "ticket"}

CSS = """
@import url('%s');
*{box-sizing:border-box;margin:0;padding:0}
:root{--n:#2A0D3D;--n2:#3A1452;--n3:#5B1F7E;--o:#F28C28;--c:#E8445A;--g:#E7B24A;--g2:#F6D58B}
body{font-family:Poppins,sans-serif;background:#000}
img{display:block}
.po{width:1080px;height:1350px;position:relative;overflow:hidden;background:linear-gradient(180deg,#EAF5FB 0%%,#FFF8EE 18%%,#FFF3E4 80%%,#FFE9D2 100%%)}
.lg{position:absolute;top:16px;left:50%%;transform:translateX(-50%%);display:flex;gap:8px;background:#fff;border-radius:12px;padding:7px 12px;box-shadow:0 3px 12px rgba(42,13,61,.15)}
.lg img{height:40px}
.hd{position:absolute;top:76px;left:0;right:0;text-align:center}
.sc{font-family:'Great Vibes';font-size:46px;color:var(--o);line-height:1}
.big{font-family:'Playfair Display';font-weight:800;color:var(--n);font-size:64px;line-height:1.02;letter-spacing:1px}
.big .n{color:var(--c)}
.rib{display:inline-block;margin-top:10px;background:linear-gradient(90deg,var(--c),var(--o));color:#fff;font-family:Montserrat;font-weight:800;font-size:38px;letter-spacing:4px;padding:10px 40px;border-radius:10px;transform:rotate(-1.5deg);box-shadow:0 6px 16px rgba(232,68,90,.4)}
.rib b{font-size:46px;color:#FFF3B0}
.w3{position:absolute;top:420px;left:32px;right:32px;display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.wc{text-align:center}
.wc .ph{position:relative;height:160px;border-radius:14px;overflow:hidden;border:5px solid #fff;box-shadow:0 5px 16px rgba(0,0,0,.2)}
.wc img{width:100%%;height:100%%;object-fit:cover}
.wc span{position:absolute;left:10px;right:10px;bottom:10px;background:linear-gradient(90deg,var(--c),var(--o));color:#fff;border-radius:30px;font-family:Montserrat;font-weight:700;font-size:15px;padding:5px 8px}
.wc b{display:block;margin-top:6px;font-family:'Playfair Display';font-weight:800;font-size:23px;color:var(--n)}
.mid{position:absolute;top:622px;left:32px;right:32px;bottom:132px;display:flex;flex-direction:column;justify-content:space-between}
.cys{display:grid;grid-template-columns:1fr 1fr;gap:8px 14px}
.cy{background:#fff;border-radius:12px;padding:8px 12px;box-shadow:0 2px 8px rgba(42,13,61,.1);border-left:5px solid var(--o)}
.cyh{display:flex;align-items:center;gap:8px}
.cyi{width:26px;height:26px;border-radius:50%%;background:var(--n2);display:flex;align-items:center;justify-content:center;flex:none}
.cyi svg{width:15px;height:15px}
.cyh b{font-family:Montserrat;font-size:17px;color:var(--n);text-transform:uppercase;letter-spacing:1px;flex:1}
.cyh em{font-style:normal;background:var(--c);color:#fff;font-family:Montserrat;font-weight:800;font-size:16px;border-radius:14px;padding:1px 10px}
.cy p{font-size:12.5px;line-height:1.32;margin-top:3px;color:#3a3040}
.un{background:linear-gradient(135deg,var(--n),var(--n3));border-radius:14px;padding:10px 14px}
.un b{display:block;color:var(--g2);font-family:Montserrat;font-size:17px;margin-bottom:6px}
.un div{display:flex;flex-wrap:wrap;gap:5px}
.un span{border:1px solid rgba(246,213,139,.7);color:#fff;border-radius:14px;padding:2px 10px;font-size:12.5px;font-family:Montserrat;font-weight:600}
.ft{position:absolute;left:0;right:0;bottom:0;height:120px;background:var(--n);display:flex;align-items:center;justify-content:space-between;padding:0 30px;color:#fff}
.ft .pr small{display:block;font-family:Montserrat;font-weight:700;font-size:14px;letter-spacing:2px;color:var(--g2)}
.ft .pr b{font-family:Montserrat;font-weight:800;font-size:46px;color:var(--g2);line-height:1}
.ft .pr span{display:block;font-family:Montserrat;font-size:14px}
.ft .bk{background:linear-gradient(90deg,var(--c),var(--o));border-radius:40px;padding:10px 22px;font-family:Montserrat;font-weight:800;font-size:22px}
.ft .ph{font-family:Montserrat;font-weight:800;font-size:40px;color:var(--g2);display:flex;align-items:center;gap:8px}
.ft .ph svg{width:36px;height:36px}
.ft .web{text-align:right;font-family:Montserrat;font-weight:600;font-size:14px;line-height:1.45}
"""

def build():
    w3 = "".join(f'<div class="wc"><div class="ph"><img src="{IMG(k)}"><span>{E(b)}</span></div><b>{E(t)}</b></div>' for k, t, b in WONDERS3)
    cys = "".join(f'<div class="cy"><div class="cyh"><span class="cyi">{ic(I[CICON[c]], "#fff")}</span><b>{E(c)}</b><em>{len(it)}</em></div>'
                  f'<p>{" · ".join(E(x) for x in it)}</p></div>' for c, it in A["countries"])
    un = "".join(f"<span>{E(x)}</span>" for x in A["unesco"])
    body = (f'<div class="lg"><img src="{K.LOGO_HK}"><img src="{K.LOGO_PK}"></div>'
            f'<div class="hd"><div class="sc">London &amp; Europe Grand Tour</div>'
            f'<div class="big"><span class="n">8</span> COUNTRIES</div>'
            f'<div class="big"><span class="n">3</span> WONDERS OF THE WORLD</div>'
            f'<div class="big"><span class="n">{TOTAL}</span> ATTRACTIONS</div>'
            f'<div class="rib">IN JUST <b>16 DAYS</b></div></div>'
            f'<div class="w3">{w3}</div><div class="mid"><div class="cys">{cys}</div>'
            f'<div class="un"><b>{len(A["unesco"])} UNESCO World Heritage Sites on this tour</b><div>{un}</div></div></div>'
            f'<div class="ft"><div class="pr"><small>ALL-INCLUSIVE · PER PERSON</small><b>{E(PK["price"])}</b><span>+ 5% GST + 2% TCS · flights &amp; visas incl.</span></div>'
            f'<span class="bk">Book Now →</span><span class="ph">{ic(I["phone"], "#F6D58B", 2)}{C["phone"]}</span>'
            f'<span class="web">{C["web1"]}<br>{C["web2"]}<br>17 Apr – 2 May 2027</span></div>')
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS % K.FONTS}</style></head><body><div class="po">{body}</div></body></html>'
    open(os.path.join(HERE, "p5_headline.html"), "w").write(html)
    print("wrote p5_headline.html")

if __name__ == "__main__":
    build()
