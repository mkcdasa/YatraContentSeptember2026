"""
Brand settings for the marketing builders.

The same yatra is sold under two brands. Set YATRA_BRAND=bhakti to build the
Bhakti Yatra (Hare Krishna Movement Indore) versions; the default builds the
Hare Krishna Golden Temple, Hyderabad versions. Bhakti Yatra details come from
the Bhakti Yatra Vaishno Devi brochures (docs/brochures/Bhakti-Yatra-Indore/).
"""
import os

HKGT = dict(
    key="hkgt", out="out", prefix="London_Europe_Yatra_2027", html_prefix="",
    presenter="Hare Krishna Golden Temple · Hyderabad",
    org="Hare Krishna Golden Temple, Banjara Hills, Hyderabad",
    footer_org="Hare Krishna Golden Temple, Hyderabad",
    phone="+91 95053 88886", web="www.punyakshetras.com · www.hkmhyderabad.org",
    langs="Telugu, Hindi and English", logos=None,
)

BHAKTI = dict(
    key="bhakti", out="out/bhakti-yatra", prefix="Bhakti_Yatra_London_Europe_Yatra_2027", html_prefix="bhakti_",
    presenter="Hare Krishna Movement Indore",
    org="Bhakti Yatra by Hare Krishna Movement Indore · ISKCON Vijay Nagar, Indore, Madhya Pradesh",
    footer_org="Bhakti Yatra by Hare Krishna Movement Indore",
    phone="+91 72248 64316 · +91 92570 45200", web="Facebook · Instagram · YouTube: Bhaktiyatra",
    langs="Hindi and English", logos=("brand/iskcon_indore.png", "brand/bhakti_yatra.png"),
)

# HKGT maroon → Bhakti Yatra purple, applied to the generated HTML
COLOURS = {
    "#6B1414": "#3A1650", "#7A1616": "#3A1650", "#8E1F1A": "#5A2378", "#3E0B0B": "#1E0B2C",
    "#9C2A1E": "#6A2C8C", "#A8321D": "#7A3398", "#7A1F1F": "#4A1E66", "#3B1307": "#2A0F38",
    "rgba(62,11,11": "rgba(30,11,44", "#6B2A0B": "#4A1E66",
}


def current():
    return BHAKTI if os.environ.get("YATRA_BRAND") == "bhakti" else HKGT


def brand_row(rel, size="lg"):
    """ISKCON Indore logo · 'Hare Krishna Movement Indore presents' · Bhakti Yatra logo."""
    h = {"lg": (64, 46, 13), "sm": (42, 30, 10)}[size]
    return (f'<div style="display:flex;align-items:center;justify-content:space-between;gap:16px;width:100%">'
            f'<img src="{rel}brand/iskcon_indore.png" style="height:{h[0]}px">'
            f'<div style="text-align:center;font:700 {h[2]}pt Inter,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#fff;line-height:1.35;text-shadow:0 1px 3px rgba(0,0,0,.5)">Hare Krishna Movement<br>Indore presents</div>'
            f'<img src="{rel}brand/bhakti_yatra.png" style="height:{h[1]}px"></div>')


def apply(html, rel="../"):
    """Rewrite a page built for HKGT into the current brand."""
    b = current()
    if b["key"] == "hkgt":
        return html
    # two phone numbers and the social handle need a tighter footer and itinerary list
    for old, new in [(".contact{display:flex;justify-content:center;gap:28px;font-size:21px",
                      ".contact{display:flex;justify-content:center;gap:22px;font-size:17.5px;white-space:nowrap"),
                     (".day{display:grid;grid-template-columns:80px 108px 1fr;gap:8px;padding:10px 0;",
                      ".day{display:grid;grid-template-columns:80px 108px 1fr;gap:8px;padding:6px 0;"),
                     (".steps{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:20px}",
                      ".steps{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:12px}"),
                     (".flights{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px}",
                      ".flights{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:12px;margin-bottom:12px}"),
                     (".cover .map{margin:6mm auto 0;width:118mm}.cover .map svg{width:118mm;height:auto}",
                      ".cover .map{margin:4mm auto 0;width:96mm}.cover .map svg{width:96mm;height:auto}")]:
        html = html.replace(old, new)
    for old, new in COLOURS.items():
        html = html.replace(old, new).replace(old.lower(), new)
    for old, new in [
        ('<div class="org">Hare Krishna Golden Temple · Hyderabad</div>', '<div class="org">' + brand_row(rel) + '</div>'),
        ('<div class="org">London Europe Yatra 2027 · 17 April – 2 May</div>',
         '<div class="org" style="margin-bottom:10px">' + brand_row(rel, "sm") + '</div><div class="org">London Europe Yatra 2027 · 17 April – 2 May</div>'),
        ("presents a pilgrimage with Hare Krishna devotees", "a pilgrimage with ISKCON Hare Krishna devotees"),
        (HKGT["org"], b["org"]), (HKGT["footer_org"], b["footer_org"]), (HKGT["phone"], b["phone"]),
        ("+91 95053 88886", b["phone"]), (HKGT["web"], b["web"]),
        ("www.punyakshetras.com", "Bhaktiyatra"), ("www.hkmhyderabad.org", "Bhaktiyatra"),
        ("Hare Krishna Golden Temple", "Hare Krishna Movement Indore"), (HKGT["langs"], b["langs"]),
    ]:
        html = html.replace(old, new)
    return html
