"""
Exports the shareable parts of itinerary_data.py to JSON for build_word.cjs.

Internal figures (budget, hotel rates, fares, ticket costs) stay out: this file
feeds a document that is sent to people outside the team.

    python3 marketing/export_word_data.py && node marketing/build_word.cjs
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import itinerary_data as D  # noqa: E402
from build_marketing import DAY_TEXT, TEMPLES, GST, SUBTOTAL, TCS, inr  # noqa: E402
import brand  # noqa: E402


def place(key):
    return D.PLACES[key][0] if key else ""


def row_out(r):
    if r["kind"] == "Transfer":
        what = {"Coach": "Coach", "Walk": "Walk", "Boat": "Boat", "Ferry": "Ferry", "Train": "Train",
                "Flight": "Flight", "Cable car": "Cable car"}.get(r["mode"], r["mode"])
        where = f"{place(r['frm'])} → {place(r['to'])}"
        if r["km"]:
            km = r["km"]
            what += f" · {km:g} km"
    else:
        what = r["kind"]
        where = place(r["to"])
    detail = r["detail"]
    if r["meal_by"]:
        detail = (r["meal_by"] + ". " + detail).strip()
    note = r["note"] or ""
    if "₹" in note:  # internal fare notes
        note = ""
    return {"time": f"{r['start']}–{r['end']}", "what": what, "where": where, "link": r["link"],
            "detail": detail.strip(), "note": note, "meal": r["kind"] in ("Breakfast", "Lunch", "Dinner"),
            "move": r["kind"] == "Transfer"}


def meals(day):
    out = {"Breakfast": [], "Lunch": [], "Dinner": []}
    for r in day["rows"]:
        if r["kind"] in out:
            out[r["kind"]].append(f"{r['start']} · {place(r['to'])} · {r['meal_by']}")
    return {k: "; ".join(v) or "On the flight" for k, v in out.items()}


def no_city_days(days):
    """Bhakti Yatra: one generic flight in and out, no departure cities or airlines."""
    d1, d16 = days[0], days[-1]
    keep = [r for r in d1["rows"] if r["what"] in ("Briefing",)]
    d1["rows"] = [
        {"time": "As per flight", "what": "Reporting", "where": "Departure airport in India", "link": "", "meal": False, "move": False, "note": "",
         "detail": "Report 3 hours before the flight. Group check-in; the tour manager hands over the kit (cap, bag, ID card, name badge). Today is Kamada Ekadasi: fruit meals are pre-ordered on the flight."},
        {"time": "Sat 17 April", "what": "Flight", "where": "International flight to London Heathrow (included)", "link": D.maps_place("LHR"), "meal": False, "move": True, "note": "",
         "detail": "Economy group fare; flight details are shared at booking. Arrive at Heathrow in the afternoon or evening. Ekadasi: fruit meals on board; carry dry fruits and nuts."},
        {"time": "On arrival", "what": "Arrival", "where": "London Heathrow", "link": D.maps_place("LHR"), "meal": False, "move": False, "note": "",
         "detail": "UK Border (eVisa linked to the passport), baggage claim, meet the tour manager. Headcount."},
        {"time": "After arrival", "what": "Coach · 25 km", "where": "London Heathrow → Hotel, Wembley area (TBC)", "link": D.maps_route("LHR", "H_LON"), "meal": False, "move": True, "note": "",
         "detail": "Coach to the hotel. Welcome talk, group rules, WhatsApp group, SIM/eSIM help. Check-in and rest."},
        {"time": "Evening", "what": "Dinner", "where": D.PLACES["H_LON"][0], "link": D.maps_place("H_LON"), "meal": True, "move": False, "note": "",
         "detail": "Hotel / Indian caterer – Ekadasi (grain-free) menu: fruit, potato, sabudana, paneer, nuts, milk."},
    ] + keep
    d1["coach_km"] = 25  # one coach run instead of two
    d1["meals"] = {"Breakfast": "On the flight", "Lunch": "On the flight", "Dinner": "Evening · Hotel, Wembley · Ekadasi (grain-free) menu"}
    rows = []
    for r in d16["rows"]:
        if r["what"].startswith("Flight"):
            continue
        rows.append(r)
    rows.append({"time": "11:40", "what": "Flight", "where": "Milan Malpensa → India (included)", "link": D.maps_place("MXP"), "meal": False, "move": True, "note": "",
                 "detail": "International flight home (economy group fare). Arrive in India early on Monday 3 May. Varuthini Ekadasi: fruit meals on board; break fast on 3 May after landing."})
    d16["rows"] = rows
    for r in d16["rows"]:
        for k in ("detail", "note"):
            r[k] = r[k].replace("Group check-in on Etihad", "Group check-in")


def main():
    days = []
    for d in D.DAYS:
        coach = sum(r["km"] for r in d["rows"] if r["kind"] == "Transfer" and r["mode"] == "Coach")
        walk = sum(r["km"] for r in d["rows"] if r["kind"] == "Transfer" and r["mode"] == "Walk")
        days.append({"day": d["day"], "date": d["date"], "dow": d["dow"], "title": d["title"],
                     "overnight": d["overnight"], "tz": d["tz"], "summary": DAY_TEXT[d["day"] - 1][2],
                     "short": DAY_TEXT[d["day"] - 1][1], "coach_km": coach, "walk_km": round(walk, 1),
                     "rows": [row_out(r) for r in d["rows"]], "meals": meals(d)})
    data = {
        "yatra": D.YATRA,
        "price": {"base": inr(D.PRICE_PP), "gst": inr(GST), "subtotal": inr(SUBTOTAL), "tcs": inr(TCS),
                  "total": inr(SUBTOTAL + TCS)},
        "days": days,
        "temples": TEMPLES,
        "hotels": [(c, n) for c, n, *_ in D.HOTELS],
        "inclusions": D.INCLUSIONS, "exclusions": D.EXCLUSIONS,
        "visa": D.VISA_DOCS, "dos": D.DOS, "donts": D.DONTS, "practical": D.PRACTICAL,
        "challenges": [c for c in D.CHALLENGES if "margin" not in c[0].lower() and "budget" not in c[0].lower()
                       and "driver hours" not in c[0].lower()],
        "tickets": [(d, p, planned) for d, p, planned, *_ in D.ENTRY_TICKETS],
        "booking": D.BOOKING,
    }
    b = brand.current()
    if b["key"] != "hkgt":
        no_city_days(days)
    data["brand"] = {k: b[k] for k in ("key", "out", "prefix", "presenter", "org", "footer_org", "phone", "web", "logos")}
    if b["key"] != "hkgt":
        data["yatra"] = dict(data["yatra"], organiser=b["org"], contact=f'{b["phone"]} · {b["web"]}')
    text = json.dumps(data, ensure_ascii=False, indent=1)
    if b["key"] != "hkgt":
        text = text.replace(brand.HKGT["langs"], b["langs"])
        for old, new in brand.FLIGHT_TEXT:
            text = text.replace(json.dumps(old, ensure_ascii=False)[1:-1], json.dumps(new, ensure_ascii=False)[1:-1])
    out = os.path.join(HERE, "word_data.json")
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", out)


if __name__ == "__main__":
    main()
