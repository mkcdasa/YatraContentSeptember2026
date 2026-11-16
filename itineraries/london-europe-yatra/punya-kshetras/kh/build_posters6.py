"""
Two more headline posters (1080 x 1350), each in brand colours and a non-brand (Teal-Amber) theme:
  p6_countries_*  : LONDON & EUROPE GRAND TOUR · 8 COUNTRIES · 75 ATTRACTIONS · IN JUST 16 DAYS + same body as poster 5
  p6_unesco_*     : ... + 11 UNESCO WORLD HERITAGE SITES with a photo of each site
    python3 kh/build_posters6.py && node kh/render_posters6.cjs
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_posters5 as P  # noqa: E402

K, E, ic, I, IMG, C, PK, A, TOTAL = P.K, P.E, P.ic, P.I, P.IMG, P.C, P.PK, P.A, P.TOTAL
PALETTES = {
    "Brand": "--n:#2A0D3D;--n2:#3A1452;--n3:#5B1F7E;--o:#F28C28;--c:#E8445A;--g:#E7B24A;--g2:#F6D58B;--bg:linear-gradient(180deg,#FFEFE0 0%,#FFFFFF 22%,#FFF8EE 100%)",
    "Teal-Amber": P.PALETTES["Teal-Amber"],
}
ICONS3 = [("colosseum", "Colosseum, Rome", "Rome · Italy"), ("pisa", "Leaning Tower of Pisa", "Pisa · Italy"),
          ("eiffel", "Eiffel Tower, Paris", "Paris · France")]
UNESCO = [("tower", "Tower of London", "United Kingdom"), ("westminster", "Westminster & Big Ben", "United Kingdom"),
          ("eiffel", "Paris, Banks of the Seine", "France"), ("grandplace", "Grand Place, Brussels", "Belgium"),
          ("amsterdam", "Amsterdam Canal Ring", "Netherlands"), ("cologne", "Cologne Cathedral", "Germany"),
          ("venice", "Venice & its Lagoon", "Italy"), ("colosseumair", "Historic Centre of Rome", "Italy"),
          ("stpeters", "Vatican City", "Vatican City"), ("florence", "Historic Centre of Florence", "Italy"),
          ("pisa", "Piazza del Duomo, Pisa", "Italy")]

EXTRA = """
.big{font-size:80px;line-height:1.04}
.u .big{font-size:53px;line-height:1.06;white-space:nowrap}
.ug{position:absolute;top:374px;left:28px;right:28px;bottom:134px;display:grid;grid-template-columns:repeat(4,1fr);grid-template-rows:repeat(3,1fr);gap:12px}
.ut{position:relative;border-radius:14px;overflow:hidden;border:4px solid #fff;box-shadow:0 4px 14px rgba(0,0,0,.2)}
.ut img{width:100%%;height:100%%;object-fit:cover}
.ut i{position:absolute;top:8px;left:8px;width:30px;height:30px;border-radius:50%%;background:var(--c);color:#fff;font:800 15px Montserrat;font-style:normal;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,.3)}
.ut div{position:absolute;left:0;right:0;bottom:0;padding:26px 10px 8px;background:linear-gradient(transparent,rgba(0,0,0,.82));color:#fff}
.ut b{display:block;font:700 16.5px/1.15 Montserrat}
.ut small{font:600 12px Montserrat;color:var(--g2);letter-spacing:.5px;text-transform:uppercase}
.uc{border-radius:14px;background:linear-gradient(135deg,var(--n),var(--n3));color:#fff;padding:14px 16px;display:flex;flex-direction:column;justify-content:center}
.uc b{font:800 22px Montserrat;color:var(--g2);margin-bottom:6px;line-height:1.1}
.uc span{font:600 14px/1.55 Montserrat}
.uc em{font-style:normal;font:700 12px Montserrat;margin-top:8px;color:var(--g2)}
"""

def page(pal, body):
    css = (P.CSS + EXTRA).replace("%(vars)s", PALETTES[pal].replace("%", "%%")) % K.FONTS
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><div class="po">{body}</div></body></html>'

def logos():
    return f'<div class="lg l"><img src="{K.LOGO_HK}"></div><div class="lg r"><img src="{K.LOGO_PK}"></div>'

def footer():
    return (f'<div class="ft"><div class="pr"><small>ALL-INCLUSIVE · PER PERSON</small><b>{E(PK["price"])}</b><span>+ 5% GST + 2% TCS · flights &amp; visas incl.</span></div>'
            f'<span class="bk">Book Now →</span><span class="ph">{ic(I["phone"], "#F6D58B", 2)}{C["phone"]}</span>'
            f'<span class="web">{C["web1"]}<br>{C["web2"]}<br>17 Apr – 2 May 2027</span></div>')

def countries(pal):
    w3 = "".join(f'<div class="wc"><div class="ph"><img src="{IMG(k)}"><span>{E(b)}</span></div><b>{E(t)}</b></div>' for k, t, b in ICONS3)
    cys = "".join(f'<div class="cy"><div class="cyh"><span class="cyi">{ic(I[P.CICON[c]], "#fff")}</span><b>{E(c)}</b><em>{len(it)}</em></div>'
                  f'<p>{" · ".join(E(x) for x in it)}</p></div>' for c, it in A["countries"])
    un = "".join(f"<span>{E(x)}</span>" for x in A["unesco"])
    body = (logos() + f'<div class="hd"><div class="sc">London &amp; Europe Grand Tour</div>'
            f'<div class="big"><span class="n">8</span> COUNTRIES</div>'
            f'<div class="big"><span class="n">{TOTAL}</span> ATTRACTIONS</div>'
            f'<div class="rib">IN JUST <b>16 DAYS</b></div></div>'
            f'<div class="w3">{w3}</div><div class="mid"><div class="cys">{cys}</div>'
            f'<div class="un"><b>{len(A["unesco"])} UNESCO World Heritage Sites on this tour</b><div>{un}</div></div></div>' + footer())
    open(os.path.join(HERE, f"p6_countries_{pal}.html"), "w").write(page(pal, body))

def unesco(pal):
    tiles = "".join(f'<div class="ut"><img src="{IMG(k)}"><i>{n}</i><div><b>{E(t)}</b><small>{E(c)}</small></div></div>'
                    for n, (k, t, c) in enumerate(UNESCO, 1))
    names = " · ".join(E(c) for c, _ in A["countries"])
    tiles += f'<div class="uc"><b>8 Countries<br>{TOTAL} Attractions</b><span>{names}</span><em>16 days · 17 Apr – 2 May 2027</em></div>'
    body = (logos() + f'<div class="hd u"><div class="sc">London &amp; Europe Grand Tour</div>'
            f'<div class="big"><span class="n">8</span> COUNTRIES · <span class="n">{TOTAL}</span> ATTRACTIONS</div>'
            f'<div class="big"><span class="n">11</span> UNESCO WORLD HERITAGE SITES</div>'
            f'<div class="rib">IN JUST <b>16 DAYS</b></div></div><div class="ug">{tiles}</div>' + footer())
    open(os.path.join(HERE, f"p6_unesco_{pal}.html"), "w").write(page(pal, body))

if __name__ == "__main__":
    assert len(A["unesco"]) == 11
    for pal in PALETTES:
        countries(pal); unesco(pal); print("wrote", pal)
