"""Builds punya-kshetras/rows.json (brand-skill schedule format) from itinerary_data.py.
Short walking hops are dropped and activity text is trimmed so each day fits one A4 page.
    python3 punya-kshetras/make_rows.py
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import itinerary_data as D

def name(key):
    if not key: return ""
    p = D.PLACES.get(key)
    if not p: return key
    nm, _, city, _ = p
    if key.startswith("H_"): return f"Hotel, {city}" if "Malpensa" not in nm else "Hotel near Malpensa airport"
    return re.sub(r"\s*\((TBC|[A-Z]{3}|[^)]*confirm[^)]*)\)", "", nm)

def short(t, n=95):
    t = re.sub(r"^(HYDERABAD|BANGALORE) GROUP:\s*", lambda m: m.group(1).title() + " group: ", t)
    t = re.split(r"(?<=[.;!])\s", t.strip())[0].rstrip(".;")
    t = re.sub(r"\s*\((?:TBC|timed[^)]*|free[^)]*|[^)]*[€£][^)]*)\)", "", t)
    t = re.sub(r"\s*[€£]\s?\d[\d.,]*\s*(?:\w+\s?){0,2}", " ", t).replace(" ,", ",").strip()
    t = re.sub(r"\s*\([^)]*optional[^)]*\)", "", t, flags=re.I)
    t = re.sub(r",\s*optional[^,;]*", "", t, flags=re.I)
    t = re.sub(r"^Optional walk", "Evening walk", t)
    if t.count("(") > t.count(")"): t = t[:t.rfind("(")].rstrip(" ,;:–-")
    if len(t) > n: t = t[:n].rsplit(" ", 1)[0].rstrip(",;:–-") + "…"
    return t

MODE = {"Breakfast": "Breakfast", "Lunch": "Lunch", "Dinner": "Dinner", "Temple darshan": "Darshan",
        "Spiritual programme": "Darshan", "Seva visit": "Darshan", "Morning programme": "Kirtan",
        "Briefing": "Kirtan", "Ceremony": "Sightseeing", "Boat cruise": "Boat", "Cable car & snow": "Cable car"}
SKIP = ("Coach run 2 (empty)",)
def ov(a, b): return a[1] < b[2] and b[1] < a[2]
rows = []
for day in D.DAYS:
    for r in day["rows"]:
        k, m, det = r["kind"], r["mode"], r["detail"]
        if any(det.startswith(s) for s in SKIP): continue
        if k == "Transfer" and m == "Walk": continue          # short walks are folded into the next stop
        if k in ("Hotel check-in", "Check-out", "Packing"): continue
        to = name(r["to"]); frm = name(r["frm"])
        if k == "Transfer":
            mode = {"Coach": "Coach", "Local coach": "Coach", "Flight": "Flight", "Train": "Train",
                    "Boat": "Boat", "Ferry": "Ferry", "Cable car": "Cable car"}.get(m, m)
            act = {"Coach": "By coach · bhajans, japa and sthala purana on board",
                   "Train": "High-speed train", "Boat": "Boat ride", "Ferry": "Ferry across the English Channel"}.get(mode, short(det))
            if mode == "Flight": act = short(det, 120)
            row = [day["day"], r["start"], r["end"], mode, frm, to, int(r["km"] or 0), act]
        else:
            mode = MODE.get(k, "Sightseeing" if k in ("Sightseeing", "Photo stop", "Viewpoint", "Evening walk", "Descent") else k)
            if mode in ("Breakfast", "Lunch", "Dinner"):
                act = {"Breakfast": "Breakfast", "Lunch": "Pure-vegetarian lunch", "Dinner": "Pure-vegetarian dinner"}[mode]
                if det.startswith("EXCEPTION") and day["day"] == 14: act = "Early breakfast before the Rome train"
                elif det.startswith("EXCEPTION"): act = "Early breakfast before the airport"
                elif "train" in det.lower() and mode == "Dinner": act = "Packed dinner, eaten on the train"
                elif "Ekadasi" in det or "Dvadasi" in det or "fast" in det.lower(): act = short(det, 70)
                elif mode == "Lunch" and det and len(det) < 60 and not det.startswith("Backup"): act = short(det, 60)
            elif mode == "Kirtan" and k == "Morning programme":
                act = "Japa, kirtan and Bhagavatam reading"
            elif k == "Briefing":
                act = "Evening kirtan and briefing for tomorrow" if "welcome" not in det.lower() else short(det)
            else:
                act = short(det)
            row = [day["day"], r["start"], r["end"], mode, to or frm, "—", 0, act]
        row.append(r.get("link") or "")
        rows.append(row)
# a luggage coach that runs while the group is on a train is not part of the yatri's day
rows = [r for r in rows if not (r[3] == "Coach" and any(t[0] == r[0] and t[3] == "Train" and ov(r, t) for t in rows))]
json.dump(rows, open(os.path.join(HERE, "rows.json"), "w"), ensure_ascii=False)
per = {}
for r in rows: per[r[0]] = per.get(r[0], 0) + 1
print("rows per day:", per, "total", len(rows))
