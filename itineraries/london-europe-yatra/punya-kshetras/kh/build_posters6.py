"""
Two more headline posters (1080 x 1350), each in brand colours and a non-brand (Teal-Amber) theme:
  p6_countries_*  : LONDON & EUROPE GRAND TOUR · 8 COUNTRIES · 75 ATTRACTIONS · IN JUST 16 DAYS + same body as poster 5
  p6_unesco_*     : ... + 10 UNESCO WORLD HERITAGE SITES with a photo of each site
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
          ("stpeters", "Vatican City", "Vatican City"),
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
.uc{grid-column:span 2;border-radius:14px;background:linear-gradient(135deg,var(--n),var(--n3));color:#fff;padding:14px 16px;display:flex;flex-direction:column;justify-content:center}
.uc b{font:800 22px Montserrat;color:var(--g2);margin-bottom:6px;line-height:1.1}
.uc span{font:600 14px/1.55 Montserrat}
.A .big{font-size:72px}.A .w3{top:380px}.A .wc .ph{height:116px}.A .wc b{font-size:21px;margin-top:4px}
.A .mid{top:540px;bottom:226px}.A .cy p{font-size:12px;line-height:1.28}.A .cys{gap:7px 14px}
.B .ug{bottom:226px}
.fb{position:absolute;left:28px;right:28px;bottom:130px;height:86px;border-radius:14px;background:#fff;box-shadow:0 4px 14px rgba(0,0,0,.15);display:flex;align-items:center;overflow:hidden;border:2px solid var(--o)}
.fx{display:flex;align-items:center;gap:10px;padding:0 16px;height:100%%;border-right:1px dashed rgba(0,0,0,.2)}
.fic{width:40px;height:40px;border-radius:50%%;background:var(--n2);display:flex;align-items:center;justify-content:center;flex:none}
.fic svg{width:22px;height:22px}
.fx small{display:block;font:800 12px Montserrat;letter-spacing:2px;color:var(--c)}
.fx b{display:block;font:800 18px/1.15 Montserrat;color:var(--n)}
.fx span{font:600 13.5px Montserrat;color:#3a3040}
.fj{flex:1;height:100%%;background:linear-gradient(135deg,var(--n),var(--n3));color:#fff;display:flex;flex-direction:column;justify-content:center;padding:0 16px}
.fj b{display:flex;align-items:center;gap:8px;font:800 19px/1.1 Montserrat;color:var(--g2)}
.fj b svg{width:24px;height:24px;flex:none}
.fj span{font:600 13px Montserrat;margin-top:4px;white-space:nowrap}.fj span.fn{margin-top:2px;font-size:12.5px;color:var(--g2)}.fj b{font-size:18px}
.lg.dk{background:#2A0F38}.lg.nb{background:none;box-shadow:none;padding:0}.lg.nb img{height:62px}
.ft .ph2{font-size:27px;line-height:1.15}.ft .ph2 svg{width:30px;height:30px}.ft .web b{color:var(--g2)}
.uc em{font-style:normal;font:700 12px Montserrat;margin-top:8px;color:var(--g2)}
"""

PRICE = "₹4,60,000"

def flights():
    pl = ic(I["plane"], "#fff")
    return (f'<div class="fb"><div class="fx"><span class="fic">{pl}</span><div><small>ARRIVE</small><b>London Heathrow</b><span>before 6:30 PM · 17 Apr 2027</span></div></div>'
            f'<div class="fx"><span class="fic dep">{pl}</span><div><small>DEPART</small><b>Milan Malpensa</b><span>after 11 AM · 2 May 2027</span></div></div>'
            f'<div class="fj"><b>{ic(I["globe"], "#F6D58B")}JOIN FROM ANYWHERE IN THE WORLD</b><span>Need flights? We book at the actual fare on your booking day.</span><span class="fn">Return fare approx. ₹80,000 as of Nov 2026 · fares change daily</span></div></div>')

def page(pal, body, cls=""):
    css = (P.CSS + EXTRA).replace("%(vars)s", PALETTES[pal].replace("%", "%%")) % K.FONTS
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><div class="po {cls}">{body}</div></body></html>'

MK = os.path.relpath(os.path.join(HERE, "..", "..", "marketing", "brand"), HERE).replace(os.sep, "/")
BRANDS = {
    "hkgt": dict(prefix="p6", pals=["Brand", "Teal-Amber"]),
    # Bhakti Yatra (Hare Krishna Movement Indore): ISKCON Indore logo (white art, needs a dark box) + Bhakti Yatra logo
    "bhakti": dict(prefix="p6b", pals=["Bhakti-Purple", "Teal-Amber"]),
}
PALETTES["Bhakti-Purple"] = ("--n:#2A0F38;--n2:#4A1E66;--n3:#6A2C8C;--o:#7A3398;--c:#E07A1F;--g:#E7B24A;--g2:#F6D58B;"
                             "--bg:linear-gradient(180deg,#F3EAFB 0%,#FFFFFF 22%,#FBF6FF 100%)")
BR = "hkgt"

def logos():
    if BR == "bhakti":
        return (f'<div class="lg l dk"><img src="{MK}/iskcon_indore.png"></div>'
                f'<div class="lg r nb"><img src="{MK}/bhakti_yatra.png"></div>')
    return f'<div class="lg l"><img src="{K.LOGO_HK}"></div><div class="lg r"><img src="{K.LOGO_PK}"></div>'

def footer():
    if BR == "bhakti":
        return (f'<div class="ft"><div class="pr"><small>TOUR COST · PER PERSON</small><b>{PRICE}</b><span>Incl. UK &amp; Schengen visas</span><span>+ GST &amp; TCS · flights extra</span></div>'
                f'<span class="bk">Book Now →</span><span class="ph ph2">{ic(I["phone"], "#F6D58B", 2)}<span>+91 72248 64316<br>+91 92570 45200</span></span>'
                f'<span class="web">Bhakti Yatra · HKM Indore<br>FB · Instagram · YouTube: <b>Bhaktiyatra</b><br>17 Apr – 2 May 2027</span></div>')
    return (f'<div class="ft"><div class="pr"><small>TOUR COST · PER PERSON</small><b>{PRICE}</b><span>Incl. UK &amp; Schengen visas</span><span>+ GST &amp; TCS · flights extra</span></div>'
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
            f'<div class="un"><b>{len(A["unesco"])} UNESCO World Heritage Sites on this tour</b><div>{un}</div></div></div>' + flights() + footer())
    open(os.path.join(HERE, f"{BRANDS[BR]['prefix']}_countries_{pal}.html"), "w").write(page(pal, body, "A"))

def unesco(pal):
    tiles = "".join(f'<div class="ut"><img src="{IMG(k)}"><i>{n}</i><div><b>{E(t)}</b><small>{E(c)}</small></div></div>'
                    for n, (k, t, c) in enumerate(UNESCO, 1))
    names = " · ".join(E(c) for c, _ in A["countries"])
    tiles += f'<div class="uc"><b>8 Countries<br>{TOTAL} Attractions</b><span>{names}</span><em>16 days · 17 Apr – 2 May 2027</em></div>'
    body = (logos() + f'<div class="hd u"><div class="sc">London &amp; Europe Grand Tour</div>'
            f'<div class="big"><span class="n">8</span> COUNTRIES · <span class="n">{TOTAL}</span> ATTRACTIONS</div>'
            f'<div class="big"><span class="n">{len(UNESCO)}</span> UNESCO WORLD HERITAGE SITES</div>'
            f'<div class="rib">IN JUST <b>16 DAYS</b></div></div><div class="ug">{tiles}</div>' + flights() + footer())
    open(os.path.join(HERE, f"{BRANDS[BR]['prefix']}_unesco_{pal}.html"), "w").write(page(pal, body, "B"))

if __name__ == "__main__":
    assert len(A["unesco"]) == len(UNESCO) == 10
    for BR, cfg in BRANDS.items():
        for pal in cfg["pals"]:
            countries(pal); unesco(pal); print("wrote", BR, pal)
