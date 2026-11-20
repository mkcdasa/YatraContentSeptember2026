"""
Day-by-day route maps for the London & Europe Yatra.

For each day it draws an OpenStreetMap base map with every stop numbered in visiting order and every leg
drawn by mode (coach legs follow the real road via OSRM; walks, boats, the ferry, trains and cable cars are
dashed lines in their own colour). It writes:
    maps/out/day_NN.png   the map (1600 × 1000)
    maps/out/day_NN.json  stops and legs (from → to, mode, km, time) taken from itinerary_data.py,
                          so the numbers match the minute-by-minute plan
Flights to and from India are not drawn (only the European airport is shown).

    python3 maps/build_day_maps.py            (needs internet for tiles/routes the first time; cached after)
Map data © OpenStreetMap contributors (ODbL) — the attribution printed on each map is required by the licence.
"""
import io, json, math, os, sys, time, urllib.request
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import itinerary_data as D  # noqa: E402

UA = {"User-Agent": "YatraItineraryMaps/1.0 (Punya Kshetras tour planning; one-off print maps)"}
OUT = os.path.join(HERE, "out"); CACHE = os.path.join(HERE, "cache")
os.makedirs(OUT, exist_ok=True); os.makedirs(os.path.join(CACHE, "tiles"), exist_ok=True)
W, H, PAD = 1600, 1000, 90
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# coordinates: geocoded (coords_raw.json) + manual fixes where the geocoder missed or matched the wrong place
FIX = {"W_REST": (51.5445, -0.2985), "AKSHAYA": (51.6395, -0.3870), "MANOR": (51.6696, -0.3357), "TOWER_LUNCH": (51.5100, -0.0790),
       "EYE": (51.5033, -0.1195), "BUCKINGHAM": (51.5018, -0.1406), "CALAIS": (50.9660, 1.8640), "ISKCON_PAR": (48.9364, 2.5286),
       "ATOMIUM": (50.8949, 4.3415), "ISKCON_CGN": (50.9450, 6.9200), "CHAPEL": (47.0517, 8.3077), "LUZ_PIER": (47.0510, 8.3100),
       "COMO_LUNCH": (45.8100, 9.0850), "VAT_LUNCH": (41.9065, 12.4590), "H_MXP": (45.6450, 8.7150), "VE_MESTRE": (45.4828, 12.2320),
       "SARAVANAA_PAR": (48.8798, 2.3579), "RF_LUNCH": (47.6960, 8.6350),
       "BRITISH_MUSEUM": (51.5194, -0.1270), "BM_COACH": (51.5218, -0.1260), "TRAFALGAR": (51.5080, -0.1281), "WEST_DIN": (51.5003, -0.1140),
       "ST_PANCRAS": (51.5308, -0.1260), "GARE_NORD": (48.8809, 2.3553), "TROCADERO": (48.8616, 2.2893), "BRU_REST": (50.8460, 4.3540),
       "LUZ_DIN": (47.0505, 8.3060), "MIL_DIN": (45.4700, 9.1980), "VIC_LUNCH": (45.5455, 11.5354), "VEN_DIN": (45.4390, 12.3290),
       "H_ROM": (41.9000, 12.5010), "ROM_DIN": (41.9015, 12.4995), "H_PIS": (43.7085, 10.4036), "PIS_DIN": (43.7150, 10.4010)}
SKIP = {"HYD", "BLR", "AUH", "DXB"}

def coords():
    raw = json.load(open(os.path.join(HERE, "coords_raw.json")))
    c = {k: (v["lat"], v["lon"]) for k, v in raw.items() if v["lat"] is not None}
    c.update(FIX)
    json.dump({k: list(v) for k, v in sorted(c.items())}, open(os.path.join(HERE, "coords.json"), "w"), indent=1)
    return c

def get(url, path=None):
    if path and os.path.exists(path): return open(path, "rb").read()
    for a in range(4):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
            if path: open(path, "wb").write(data)
            time.sleep(0.15); return data
        except Exception:
            time.sleep(2 * (a + 1))
    raise RuntimeError(url)

def mx(lon, z): return (lon + 180) / 360 * 256 * 2 ** z
def my(lat, z):
    s = math.sin(math.radians(lat)); return (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * 256 * 2 ** z

def osrm(a, b):
    key = f"{a[1]:.5f},{a[0]:.5f};{b[1]:.5f},{b[0]:.5f}"
    p = os.path.join(CACHE, "route_" + key.replace(",", "_").replace(";", "__") + ".json")
    try:
        r = json.loads(get(f"https://router.project-osrm.org/route/v1/driving/{key}?overview=full&geometries=geojson", p))
        return [(lat, lon) for lon, lat in r["routes"][0]["geometry"]["coordinates"]]
    except Exception:
        return [a, b]

STYLE = {"Coach": ("#2A0D3D", 7, None), "Local coach": ("#2A0D3D", 7, None), "Walk": ("#16A34A", 5, (10, 8)),
         "Boat": ("#0E7490", 6, (16, 10)), "Ferry": ("#1C7FC4", 7, (22, 12)), "Train": ("#E8445A", 6, (4, 10)),
         "Cable car": ("#B45309", 6, (12, 6)), "Flight": ("#7C3AED", 4, (6, 10))}
LABEL = {"Coach": "Coach", "Local coach": "Local coach", "Walk": "Walk", "Boat": "Boat", "Ferry": "Ferry", "Train": "Train",
         "Cable car": "Cable car", "Flight": "Flight"}

def short(k):
    n = D.PLACES[k][0]
    for sep in (" – ", " (", ", ISKCON", " & Hohenzollern"):
        if sep in n and not n.startswith("Hotel"): n = n.split(sep)[0]
    return n.replace(" (TBC)", "")

def mins(r):
    from build_workbook import real_minutes
    if "→" in (r["tz"] or "") and r["mode"] in ("Flight", "Ferry"): return real_minutes(r)
    sh, sm = map(int, r["start"].split(":")); eh, em = map(int, r["end"].split(":"))
    return (eh * 60 + em - sh * 60 - sm) % 1440
def fmt(m): return f"{m // 60} h {m % 60:02d} min" if m >= 60 else f"{m} min"

def dashed(dr, pts, col, w, dash):
    if not dash:
        dr.line(pts, fill=col, width=w, joint="curve"); return
    on, off = dash; draw = True; left = on
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        seg = math.hypot(x2 - x1, y2 - y1); pos = 0
        while pos < seg:
            step = min(left, seg - pos)
            if draw:
                t0, t1 = pos / seg, (pos + step) / seg
                dr.line([(x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0), (x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1)], fill=col, width=w)
            pos += step; left -= step
            if left <= 0: draw = not draw; left = on if draw else off

def day_data(d, C):
    legs, stops = [], []
    def add_stop(k):
        if k in SKIP or k not in C: return
        if not stops or stops[-1] != k: stops.append(k)
    def hav(a, b):
        la1, lo1, la2, lo2 = map(math.radians, (*C[a], *C[b]))
        h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
        return 6371 * 2 * math.asin(math.sqrt(h))
    jump = [False]
    PAIR = {("TRONCHETTO", "SANMARCO"): ("Boat", 25), ("SANMARCO", "TRONCHETTO"): ("Boat", 25)}
    def implicit(k0, k, est_mode=None, est_min=None):
        if jump[0]: return
        dist = hav(k0, k)
        if (k0, k) in PAIR:
            m, t = PAIR[(k0, k)]; legs.append(dict(frm=k0, to=k, mode=m, km=round(dist * 1.2, 1), min=t, time="vaporetto", est=True)); return
        if est_mode == "Cable car":
            legs.append(dict(frm=k0, to=k, mode="Cable car", km=round(dist, 1), min=est_min or 30, time="cable car", est=True)); return
        if dist < 1.5:
            km = round(dist * 1.3, 1); legs.append(dict(frm=k0, to=k, mode="Walk", km=km, min=max(5, round(km / 4 * 60 / 5) * 5), time="on foot", est=True))
        elif dist < 15:
            km = max(1, round(dist * 1.3)); legs.append(dict(frm=k0, to=k, mode="Coach", km=km, min=max(10, round(km / 25 * 60 / 5) * 5 + 5), time="short hop", est=True))
    for r in d["rows"]:
        det = r["detail"].lower()
        if r["kind"] == "Transfer":
            if r["mode"] == "Coach" and ("empty" in det or "no passengers" in det):
                jump[0] = True; continue
            if r["mode"] == "Flight":
                add_stop(r["to"]); jump[0] = True; continue
            if stops and r["frm"] in C and stops[-1] != r["frm"] and stops[-1] in C and 0.05 < hav(stops[-1], r["frm"]) < 15:
                implicit(stops[-1], r["frm"])
            jump[0] = False
            add_stop(r["frm"]); add_stop(r["to"])
            if r["frm"] in C and r["to"] in C:
                legs.append(dict(frm=r["frm"], to=r["to"], mode=r["mode"], km=r["km"], min=mins(r), time=f'{r["start"]}–{r["end"]}'))
        elif r["to"]:
            k = r["to"]
            if stops and k in C and stops[-1] != k and stops[-1] in C and 0.05 < hav(stops[-1], k) < 15:
                k0 = stops[-1]
                if r["mode"] == "Cable car" or "TITLIS" in (k0, k):
                    implicit(k0, k, "Cable car", mins(r) if r["mode"] == "Cable car" else 30)
                else:
                    implicit(k0, k)
            jump[0] = False
            add_stop(k)
    # number stops; repeated places keep their first number
    num = {}
    for k in stops:
        if k not in num: num[k] = len(num) + 1
    return legs, num

def tiles(z, ox, oy, w, h):
    img = Image.new("RGB", (w, h), "#eee")
    for tx in range(int(ox // 256), int((ox + w) // 256) + 1):
        for ty in range(int(oy // 256), int((oy + h) // 256) + 1):
            p = os.path.join(CACHE, "tiles", f"{z}_{tx}_{ty}.png")
            t = Image.open(io.BytesIO(get(f"https://tile.openstreetmap.org/{z}/{tx}/{ty}.png", p))).convert("RGB")
            img.paste(t, (int(tx * 256 - ox), int(ty * 256 - oy)))
    return Image.blend(img, Image.new("RGB", (w, h), "#ffffff"), 0.18)

def fit(keys, C, w, h, pad, zmax):
    lats = [C[k][0] for k in keys]; lons = [C[k][1] for k in keys]
    for z in range(zmax, 3, -1):
        if mx(max(lons), z) - mx(min(lons), z) <= w - 2 * pad and my(min(lats), z) - my(max(lats), z) <= h - 2 * pad: break
    cx, cy = (mx(min(lons), z) + mx(max(lons), z)) / 2, (my(max(lats), z) + my(min(lats), z)) / 2
    return z, cx - w / 2, cy - h / 2

def paint(img, z, ox, oy, legs, num, C, r=19, f=22, only=None):
    dr = ImageDraw.Draw(img)
    P = lambda lat, lon: (mx(lon, z) - ox, my(lat, z) - oy)
    for L in legs:
        if only and not (L["frm"] in only and L["to"] in only): continue
        a, b = C[L["frm"]], C[L["to"]]
        path = osrm(a, b) if L["mode"] in ("Coach", "Local coach") and L["km"] >= 1 else [a, b]
        col, w, dash = STYLE.get(L["mode"], ("#333", 5, None))
        xy = [P(*q) for q in path]
        if not dash: dr.line(xy, fill="white", width=w + 6, joint="curve")
        dashed(dr, xy, col, w, dash)
    fb = ImageFont.truetype(FB, f)
    placed = []
    for k, n in num.items():
        if only and k not in only: continue
        x, y = P(*C[k]); dx = 0
        for (px, py) in placed:
            if abs(px - x) < r * 1.6 and abs(py - y) < r * 1.6: dx += r * 1.6
        x += dx; placed.append((x, y))
        col = "#E8445A" if k.startswith("H_") or k.startswith("LHR") or k == "MXP" else "#F28C28"
        dr.ellipse([x - r, y - r, x + r, y + r], fill=col, outline="white", width=4 if r > 15 else 3)
        tw = dr.textlength(str(n), font=fb); dr.text((x - tw / 2, y - f * .6), str(n), font=fb, fill="white")
    return P

def render(d, C):
    legs, num = day_data(d, C)
    z, ox, oy = fit(list(num), C, W, H - 60, PAD, 15); oy -= 40
    img = tiles(z, ox, oy, W, H)
    P = paint(img, z, ox, oy, legs, num, C)
    dr = ImageDraw.Draw(img)
    # close-up insets (up to two) for crowded clusters of stops
    pix = {k: P(*C[k]) for k in num}
    IW, IH = 620, 420
    corners = [(20, 72), (W - IW - 20, 72), (W - IW - 20, H - IH - 40)]
    used_c, done = [], set()
    for _ in range(2):
        rest = [k for k in num if k not in done]
        crowd = [k for k in rest if any(j != k and math.dist(pix[k], pix[j]) < 55 for j in rest)]
        if len(crowd) < 2: break
        best = max(crowd, key=lambda k: sum(1 for j in rest if math.dist(pix[k], pix[j]) < 90))
        cl = None
        for R in (90, 140, 200, 280):
            c2 = [j for j in rest if math.dist(pix[best], pix[j]) < R]
            if len(c2) >= 3 and len(c2) < len(num) and fit(c2, C, IW, IH, 55, 16)[0] >= z + 2:
                cl = c2
        if not cl:
            for R in (90, 140, 200):
                c2 = [j for j in rest if math.dist(pix[best], pix[j]) < R]
                if len(c2) >= 2 and fit(c2, C, IW, IH, 55, 16)[0] >= z + 1: cl = c2; break
        if not cl: break
        done |= set(cl)
        zi, oxi, oyi = fit(cl, C, IW, IH, 55, 16)
        cx = sum(pix[k][0] for k in cl) / len(cl); cy = sum(pix[k][1] for k in cl) / len(cl)
        def score(c):
            x0, y0 = c
            if c in used_c: return -1e9
            inside = sum(1 for k in num if x0 - 30 < pix[k][0] < x0 + IW + 30 and y0 - 30 < pix[k][1] < y0 + IH + 30)
            return -inside * 1000 + math.dist((x0 + IW / 2, y0 + IH / 2), (cx, cy)) * 0.01
        ix, iy = max(corners, key=score); used_c.append((ix, iy))
        ins = tiles(zi, oxi, oyi, IW, IH)
        paint(ins, zi, oxi, oyi, legs, num, C, r=17, f=19, only=set(cl))
        xs = [pix[k][0] for k in cl]; ys = [pix[k][1] for k in cl]
        dr.rectangle([min(xs) - 28, min(ys) - 28, max(xs) + 28, max(ys) + 28], outline="#2A0D3D", width=3)
        dr.rectangle([ix - 6, iy - 6, ix + IW + 6, iy + IH + 6], fill="#2A0D3D")
        img.paste(ins, (ix, iy))
        dr.rectangle([ix, iy, ix + 150, iy + 32], fill="#2A0D3D")
        dr.text((ix + 10, iy + 6), "Close-up", font=ImageFont.truetype(FB, 18), fill="#F6D58B")
    fb = ImageFont.truetype(FB, 22); fs = ImageFont.truetype(FB, 17); fr = ImageFont.truetype(FR, 15)
    # title bar + attribution
    dr.rectangle([0, 0, W, 56], fill="#2A0D3D")
    dr.text((24, 14), f"Day {d['day']} · {d['dow']} {int(d['date'][8:])} {'April' if d['date'][5:7]=='04' else 'May'} 2027 · Route map", font=fb, fill="#F6D58B")
    # legend of modes used
    used = []
    for L in legs:
        if L["mode"] not in used: used.append(L["mode"])
    lx, ly = 20, H - 34 - 26 * len(used) - 52
    dr.rounded_rectangle([lx, ly, lx + 210, H - 34], 10, fill="white", outline="#cbb")
    yy = ly + 10
    for m in used:
        col, w, dash = STYLE.get(m, ("#333", 5, None))
        dashed(dr, [(lx + 14, yy + 9), (lx + 64, yy + 9)], col, max(w - 1, 3), dash)
        dr.text((lx + 74, yy), LABEL.get(m, m), font=fs, fill="#2A0D3D"); yy += 26
    dr.ellipse([lx + 26, yy + 2, lx + 44, yy + 20], fill="#E8445A", outline="white", width=2); dr.text((lx + 74, yy), "Hotel / airport", font=fs, fill="#2A0D3D"); yy += 26
    dr.ellipse([lx + 26, yy + 2, lx + 44, yy + 20], fill="#F28C28", outline="white", width=2); dr.text((lx + 74, yy), "Visit / stop", font=fs, fill="#2A0D3D")
    att = "Map data © OpenStreetMap contributors"
    dr.rectangle([W - dr.textlength(att, font=fr) - 16, H - 24, W, H], fill="white"); dr.text((W - dr.textlength(att, font=fr) - 8, H - 21), att, font=fr, fill="#555")
    img.save(os.path.join(OUT, f"day_{d['day']:02d}.png"), optimize=True)
    out = dict(day=d["day"], stops=[dict(n=n, key=k, name=short(k)) for k, n in num.items()],
               legs=[dict(n=i + 1, frm=num.get(L["frm"]), to=num.get(L["to"]), from_name=short(L["frm"]), to_name=short(L["to"]), mode=L["mode"],
                          km=L["km"], minutes=L["min"], duration=fmt(L["min"]), time=L["time"], estimate=L.get("est", False)) for i, L in enumerate(legs)])
    out["coach_km"] = sum(L["km"] for L in legs if L["mode"] in ("Coach", "Local coach"))
    out["walk_km"] = round(sum(L["km"] for L in legs if L["mode"] == "Walk"), 1)
    json.dump(out, open(os.path.join(OUT, f"day_{d['day']:02d}.json"), "w"), indent=1, ensure_ascii=False)
    return out

if __name__ == "__main__":
    C = coords()
    for d in D.DAYS:
        o = render(d, C)
        print(f"day {d['day']:2d}: {len(o['stops'])} stops, {len(o['legs'])} legs, coach {o['coach_km']} km")
