"""Writes map_base.svg: Western Europe outlines (Natural Earth low-res, via geopandas 0.14 bundled data)
with the 8 tour countries highlighted. Run once; the SVG is committed so the brochure build needs no geopandas.
    pip install geopandas==0.14.4 && python3 make_map.py
"""
import math, json, warnings
warnings.filterwarnings("ignore")
import geopandas as gpd
LON0, LON1, LAT0, LAT1 = -6.2, 15.2, 40.6, 55.2
K = math.cos(math.radians(48))
W = 1000; H = round(W * (LAT1 - LAT0) / ((LON1 - LON0) * K))
def xy(lon, lat): return ((lon - LON0) * K / ((LON1 - LON0) * K) * W, (LAT1 - lat) / (LAT1 - LAT0) * H)
TOUR = {"United Kingdom", "France", "Belgium", "Netherlands", "Germany", "Switzerland", "Italy"}
w = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
w = w[w.continent.isin(["Europe", "Africa"])]
paths = []
for _, r in w.iterrows():
    geoms = r.geometry.geoms if r.geometry.geom_type == "MultiPolygon" else [r.geometry]
    d = ""
    for g in geoms:
        pts = [xy(x, y) for x, y in g.exterior.coords]
        if all(px < -50 or px > W + 50 for px, _ in pts) or all(py < -50 or py > H + 50 for _, py in pts): continue
        d += "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts) + "Z"
    if d:
        cls = "tour" if r["name"] in TOUR else "other"
        paths.append(f'<path class="{cls}" d="{d}"/>')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">'
       '<style>.tour{fill:#FFE3C2;stroke:#E8445A;stroke-width:1.6}.other{fill:#F3EEE6;stroke:#CFC4B4;stroke-width:1}</style>'
       '<rect width="100%" height="100%" fill="#CFE6F2"/>' + "".join(paths) + "</svg>")
open("map_base.svg", "w").write(svg)
json.dump({"LON0": LON0, "LON1": LON1, "LAT0": LAT0, "LAT1": LAT1, "W": W, "H": H}, open("map_proj.json", "w"))
print("map", W, H, len(paths))
