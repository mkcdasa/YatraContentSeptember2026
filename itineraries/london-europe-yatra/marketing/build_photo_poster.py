"""
Two-page photo poster (front and back) for the London Europe Yatra 2027.

Photos are freely licensed images from Wikimedia Commons, kept in
marketing/photos/ with their credits in photos/credits.json for our records (written by
fetch_photos.py). No photo credits are printed on the poster:
the team does not want them on any creative. Render with: node marketing/render_photo_poster.cjs
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(HERE, "photos")
OUT = os.path.join(HERE, "html", "photo_poster.html")

CREDITS = json.load(open(os.path.join(PHOTOS, "credits.json"), encoding="utf-8"))


def img(key):
    return "../photos/" + CREDITS[key]["file"]


FOCUS = {"pisa": "92% center", "radhadesh": "center 40%"}  # keep the leaning tower in the crop


def tile(key, caption, cls=""):
    pos = f' style="object-position:{FOCUS[key]}"' if key in FOCUS else ""
    return (f'<figure class="tile {cls}"><img src="{img(key)}" alt="{caption}"{pos}>'
            f'<figcaption>{caption}</figcaption></figure>')


FRONT_TILES = [("manor", "Bhaktivedanta Manor, London"), ("eiffel", "Eiffel Tower, Paris"),
               ("keukenhof", "Keukenhof tulips, Holland"), ("titlis", "Mount Titlis snow, Switzerland"),
               ("venice", "Gondola ride, Venice"), ("colosseum", "Colosseum, Rome")]
BACK_TILES = [("westminster", "Big Ben & Parliament"), ("radhadesh", "Radhadesh temple, Belgium"), ("windmills", "Zaanse Schans windmills"), ("amsterdam", "Amsterdam canals"),
              ("rhinefalls", "Rhine Falls"), ("lucerne", "Chapel Bridge, Lucerne"),
              ("vatican", "St Peter's, Vatican"), ("pisa", "Leaning Tower of Pisa")]

ROUTE = ["London", "Paris", "Brussels", "Amsterdam", "Cologne", "Black Forest", "Zurich", "Lucerne",
         "Interlaken", "Lake Como", "Milan", "Venice", "Rome", "Florence", "Pisa"]
COUNTRIES = ["UK", "France", "Belgium", "Netherlands", "Germany", "Switzerland", "Italy", "Vatican"]
TEMPLES = ["Bhaktivedanta Manor", "ISKCON Soho", "ISKCON Paris", "Radhadesh", "ISKCON Cologne", "Goloka Dham",
           "ISKCON Zurich", "Villaggio Hare Krishna", "Prabhupada Desh", "Villa Vrindavan"]
INCLUDED = [("✈", "Flights from Hyderabad & Bangalore"), ("🛂", "UK & Schengen visa"), ("🏨", "15 nights hotels"),
            ("🍛", "All Satvik meals"), ("🚌", "Private coach"), ("🎟", "Sightseeing & entry tickets"),
            ("🙏", "Tour manager")]

CSS = """
@page{size:A4;margin:0}
:root{--maroon:#7A1616;--deep:#3E0B0B;--saffron:#F28C1B;--gold:#F4C542;--cream:#FFF8EC;--teal:#0E7C86;--pink:#E0457B;--sky:#2A7DE1;--leaf:#2E9E5B}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,sans-serif;color:#2B1A12}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;background:var(--cream)}
.page:last-child{page-break-after:auto}
.serif{font-family:'Playfair Display',serif}
/* front */
.hero{position:relative;height:118mm;background:#222 center/cover no-repeat}
.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(62,11,11,.55) 0%,rgba(62,11,11,.05) 38%,rgba(62,11,11,.15) 60%,rgba(62,11,11,.92) 100%)}
.hero .in{position:absolute;inset:0;z-index:2;display:flex;flex-direction:column;align-items:center;padding:9mm 10mm 0;color:#fff;text-align:center}
.org{font-size:10.5pt;letter-spacing:.22em;text-transform:uppercase;font-weight:700;color:var(--gold);text-shadow:0 1px 3px rgba(0,0,0,.6)}
.pres{font-family:'Playfair Display',serif;font-style:italic;font-size:12pt;margin-top:1.5mm;text-shadow:0 1px 3px rgba(0,0,0,.6)}
.title{margin-top:auto;margin-bottom:7mm}
.title h1{font-family:'Playfair Display',serif;font-weight:800;font-size:46pt;line-height:.95;text-shadow:0 3px 12px rgba(0,0,0,.55)}
.title h2{font-family:'Playfair Display',serif;font-style:italic;font-weight:600;font-size:24pt;color:var(--gold);margin-top:1mm}
.band{background:linear-gradient(90deg,var(--saffron),#F7B733);color:#3B1307;text-align:center;padding:3.2mm 6mm;font-weight:800;font-size:17pt}
.band span{font-weight:600}
.chips{display:flex;flex-wrap:wrap;justify-content:center;gap:2mm;padding:4mm 10mm 0}
.chips div{background:#fff;border:1.5px solid var(--maroon);color:var(--maroon);border-radius:99px;padding:1mm 3.6mm;font-size:9.5pt;font-weight:700}
.grid{display:grid;gap:2.6mm;padding:4mm 10mm 0}
.g3{grid-template-columns:repeat(3,1fr)}
.g4{grid-template-columns:repeat(4,1fr)}
.tile{position:relative;border-radius:3.5mm;overflow:hidden;box-shadow:0 2px 6px rgba(0,0,0,.18)}
.tile img{display:block;width:100%;height:38mm;object-fit:cover}
.g4 .tile img{height:40mm}
.tile figcaption{position:absolute;left:0;right:0;bottom:0;padding:5mm 2.5mm 1.8mm;color:#fff;font-size:8.6pt;font-weight:700;background:linear-gradient(180deg,transparent,rgba(0,0,0,.78))}
.row{display:grid;grid-template-columns:78mm 1fr;gap:4mm;padding:4.5mm 10mm 0;align-items:stretch}
.price{background:var(--maroon);color:#fff;border-radius:4mm;padding:4mm 4mm;text-align:center;position:relative}
.price .l{font-size:8.5pt;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);font-weight:700}
.price .v{font-family:'Playfair Display',serif;font-weight:800;font-size:31pt;line-height:1.05}
.price .s{font-size:10pt;font-weight:700}
.price .t{font-size:9pt;color:#F6DFC0;margin-top:.8mm}
.hl{background:#fff;border-radius:4mm;padding:3.5mm 4.5mm;border:1.5px solid #EAD7B7}
.hl h3{font-family:'Playfair Display',serif;color:var(--maroon);font-size:13pt;margin-bottom:1.5mm}
.hl ul{list-style:none;columns:2;column-gap:4mm}
.hl li{font-size:9.3pt;line-height:1.5;padding-left:4mm;position:relative;break-inside:avoid}
.hl li:before{content:"✦";position:absolute;left:0;color:var(--saffron);font-size:7.5pt;top:.6mm}
.foot{position:absolute;left:0;right:0;bottom:0;background:var(--deep);color:#fff;text-align:center;padding:3.6mm 6mm 3.2mm}
.foot .c{font-size:13.5pt;font-weight:700}
.foot .c b{color:var(--gold)}
.foot .w{font-size:9.5pt;margin-top:.6mm;color:#F3E2C5}
.foot .n{font-size:7.2pt;margin-top:1mm;color:#CDB79A}
/* back */
.top{background:linear-gradient(120deg,var(--deep),var(--maroon) 60%,#A8321D);color:#fff;padding:8mm 10mm 6mm;text-align:center}
.top h2{font-family:'Playfair Display',serif;font-size:27pt;font-weight:800}
.top p{font-size:11pt;color:#F6DFC0;margin-top:1mm}
.route{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:1.4mm 1mm;margin-top:4mm}
.route span{background:rgba(255,255,255,.12);border:1px solid rgba(244,197,66,.6);border-radius:99px;padding:.8mm 2.8mm;font-size:9pt;font-weight:600}
.route i{color:var(--gold);font-style:normal;font-size:9pt}
.sec{padding:4.5mm 10mm 0}
.sec h3{font-family:'Playfair Display',serif;color:var(--maroon);font-size:15pt;margin-bottom:2mm;display:flex;align-items:center;gap:3mm}
.sec h3:after{content:"";flex:1;height:1.5px;background:linear-gradient(90deg,var(--saffron),transparent)}
.temples{display:flex;flex-wrap:wrap;gap:1.8mm}
.temples div{background:linear-gradient(90deg,#FFE7C2,#FFF3DE);border:1px solid #F2C98A;color:#6B2A0B;border-radius:2.5mm;padding:1.3mm 3mm;font-size:9.4pt;font-weight:700}
.inc{display:grid;grid-template-columns:repeat(4,1fr);gap:2.2mm}
.inc div{background:#fff;border-radius:3mm;border:1.5px solid #EAD7B7;padding:2.5mm 2mm;text-align:center;font-size:8.8pt;font-weight:700;color:#3B1D12;line-height:1.25}
.inc div b{display:block;font-size:15pt;margin-bottom:.8mm}
.inc .pr{background:var(--maroon);color:#fff;border-color:var(--maroon)}
.inc .pr b{font-family:'Playfair Display',serif;font-size:15pt;color:var(--gold)}
"""


def front():
    tiles = "".join(tile(k, c) for k, c in FRONT_TILES)
    highlights = ["10 ISKCON temples", "Koh-i-Noor & London Eye", "Eiffel Tower & Louvre",
                  "Tulips & windmills", "Mount Titlis snow", "Venice gondola ride",
                  "Vatican & Colosseum", "Satvik prasadam daily"]
    return f"""<section class="page">
<div class="hero" style="background-image:url('{img("towerbridge")}')"><div class="in">
 <div class="org">Hare Krishna Golden Temple · Hyderabad</div>
 <div class="pres">presents a pilgrimage with Hare Krishna devotees</div>
 <div class="title"><h1>London Europe</h1><h2>Yatra 2027</h2></div></div></div>
<div class="band">17 April – 2 May 2027 <span>· 15 Nights / 16 Days · 8 Countries</span></div>
<div class="chips">{''.join(f'<div>{c}</div>' for c in COUNTRIES)}</div>
<div class="grid g3">{tiles}</div>
<div class="row">
 <div class="price"><div class="l">Yatra amount per person</div><div class="v">₹5,49,000</div>
  <div class="s">including international flights</div><div class="t">+ 5% GST + 2% TCS*</div></div>
 <div class="hl"><h3>Highlights</h3><ul>{''.join(f'<li>{h}</li>' for h in highlights)}</ul></div>
</div>
<div class="foot"><div class="c"><b>Call / WhatsApp</b> +91 95053 88886</div>
 <div class="w">www.punyakshetras.com · www.hkmhyderabad.org</div>
 <div class="n">*TCS is refunded or credited through your income-tax return. Limited seats – one coach.</div></div>
</section>"""


def back():
    route = '<i>→</i>'.join(f'<span>{c}</span>' for c in ROUTE)
    tiles = "".join(tile(k, c) for k, c in BACK_TILES)
    inc = "".join(f'<div><b>{i}</b>{t}</div>' for i, t in INCLUDED)
    return f"""<section class="page">
<div class="top"><h2>16 days · 8 countries · 10 temples</h2><p>Flights from Hyderabad &amp; Bangalore · one coach, one family of devotees</p>
<div class="route">{route}</div></div>
<div class="sec"><h3>Places we visit</h3></div>
<div class="grid g4" style="padding-top:0">{tiles}</div>
<div class="sec"><h3>Holy places</h3><div class="temples">{''.join(f'<div>🪷 {t}</div>' for t in TEMPLES)}<div>🍲 Akshaya Patra kitchen, Watford</div></div></div>
<div class="sec"><h3>Included</h3><div class="inc">{inc}<div class="pr"><b>₹5,49,000</b>per person incl. flights<br>+ 5% GST + 2% TCS</div></div></div>
<div class="foot"><div class="c"><b>Reserve your seat · Call / WhatsApp</b> +91 95053 88886</div>
 <div class="w">Hare Krishna Golden Temple, Banjara Hills, Hyderabad · www.punyakshetras.com · www.hkmhyderabad.org</div>
 <div class="n">Itinerary may change slightly for operational reasons. Payment schedule and cancellation terms on the booking form.</div></div>
</section>"""


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    html = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>London Europe Yatra 2027 – Poster</title>'
            '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">'
            f'<style>{CSS}</style></head><body>{front()}{back()}</body></html>')
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
