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
    out = os.path.join(HERE, "word_data.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("wrote", out)


if __name__ == "__main__":
    main()
