# Helpers for writing a yatra's minute-by-minute schedule (rows.json) as a small Python script.
#
#   import sys; sys.path.insert(0, "<skill>/engine")
#   from new_rows import m, d, save
#   HJ = "Residency Road, Jammu"; AP = "Jammu Airport, Satwari, Jammu"
#   R = [
#     (1,"14:00","14:30","Arrival","Jammu Airport (IXJ)","—",0,"Meet our representative, garland welcome",m(AP)),
#     (1,"14:30","14:50","Car","Jammu Airport","Hotel, Jammu",7,"Transfer to the hotel",d(AP,HJ)),
#     (1,"15:15","15:50","Lunch","Hotel restaurant, Jammu","—",0,"Lunch",m(HJ)),
#   ]
#   save(R, "rows.json")      # writes the file and prints km per day + total
#
# Row tuple: (day, start "HH:MM", end "HH:MM", mode, from_place, to_place or "—", km (int, road km only),
#             activity text, Google Maps URL). Meal rows use mode Breakfast / Lunch / Dinner.
import json
from urllib.parse import quote_plus

def m(q):
    "Google Maps search link for one place."
    return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(q)

def d(a, b, mode="driving"):
    "Google Maps directions link from a to b (mode: driving, walking, transit)."
    return ("https://www.google.com/maps/dir/?api=1&origin=" + quote_plus(a) +
            "&destination=" + quote_plus(b) + "&travelmode=" + mode)

def mins(a, b):
    h1, m1 = map(int, a.split(":")); h2, m2 = map(int, b.split(":"))
    return h2 * 60 + m2 - h1 * 60 - m1

def check(rows):
    "Warn about gaps, overlaps and negative durations within each day."
    prob = []
    for i, r in enumerate(rows):
        if mins(r[1], r[2]) < 0: prob.append(f"Day {r[0]} {r[1]}–{r[2]}: ends before it starts")
        if i and rows[i - 1][0] == r[0] and rows[i - 1][2] != r[1]:
            prob.append(f"Day {r[0]}: {rows[i-1][2]} → {r[1]} is not continuous")
    return prob

def summary(rows):
    days = sorted(set(r[0] for r in rows))
    per = {k: sum(r[6] for r in rows if r[0] == k) for k in days}
    print("km per day:", per, "total:", sum(per.values()))
    for p in check(rows): print("CHECK:", p)
    return per

def save(rows, path="rows.json"):
    json.dump([list(r) for r in rows], open(path, "w"), ensure_ascii=False)
    return summary(rows)
