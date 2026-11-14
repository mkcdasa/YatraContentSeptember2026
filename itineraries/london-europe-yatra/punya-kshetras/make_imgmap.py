"""Writes imgmap.json from the photos in img/. Credits come from ../marketing/photos/credits.json and
imgcredits.json; they are kept for our records only and are never printed (team decision).
A missing photo falls back to a related one so the build never breaks.
    python3 make_imgmap.py
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
old = json.load(open(os.path.join(HERE, "..", "marketing", "photos", "credits.json")))
new = json.load(open(os.path.join(HERE, "imgcredits.json")))
CAP = {"towerbridge": "Tower Bridge, London", "manor": "Bhaktivedanta Manor", "eiffel": "Eiffel Tower, Paris",
       "keukenhof": "Keukenhof tulip gardens", "titlis": "Mount Titlis", "venice": "Venice", "colosseum": "Colosseum, Rome",
       "windmills": "Zaanse Schans windmills", "amsterdam": "Amsterdam", "rhinefalls": "Rhine Falls", "lucerne": "Lucerne",
       "pisa": "Pisa", "westminster": "Westminster", "radhadesh": "Radhadesh, Belgium", "vatican": "St Peter's, Vatican"}
FALLBACK = {"bigben": "westminster", "grandplace": "atomium", "cologne": "amsterdam", "titisee": "rhinefalls",
            "zurich": "lucerne", "interlaken": "titlis", "como": "lucerne", "milan": "venice", "padova": "venice",
            "florence": "pisa", "pontevecchio": "pisa", "trevi": "colosseum", "stpeters": "vatican", "seine": "eiffel",
            "alps": "titlis", "louvre": "eiffel", "notredame": "eiffel", "arc": "eiffel", "atomium": "amsterdam"}
m = {}
for f in sorted(os.listdir(os.path.join(HERE, "img"))):
    k = f[:-4]
    c = new.get(k) or {}
    o = old.get(k) or {}
    credit = f'{c.get("title", o.get("title", ""))} – {c.get("artist", o.get("artist", ""))}, {c.get("license", o.get("license", ""))}'
    m[k] = {"src": f"img/{f}", "credit": credit, "cap": c.get("cap") or CAP.get(k, k.title())}
for k, fb in FALLBACK.items():
    if k not in m and fb in m: m[k] = dict(m[fb])
json.dump(m, open(os.path.join(HERE, "imgmap.json"), "w"), indent=1, ensure_ascii=False)
print(len(m), "images; real:", len(os.listdir(os.path.join(HERE, "img"))))
