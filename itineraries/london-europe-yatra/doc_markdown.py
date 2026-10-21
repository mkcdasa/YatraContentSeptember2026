"""Render the living document's sections as markdown from itinerary_data.py.

    python3 doc_markdown.py OUTDIR      # writes one .md per doc section
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import itinerary_data as D  # noqa: E402
from build_workbook import TZ_OFFSET  # noqa: E402,F401


def cell(s):
    return str(s).replace("|", "/").replace("\n", " ")


def mins(row, tz):
    if "→" in tz and row["mode"] in ("Flight", "Ferry"):
        from build_workbook import real_minutes
        return real_minutes(dict(row, tz=tz))
    sh, sm = map(int, row["start"].split(":"))
    eh, em = map(int, row["end"].split(":"))
    return (eh * 60 + em - sh * 60 - sm) % 1440


def fmt_m(m):
    return f"{m // 60} h {m % 60:02d} m" if m >= 60 else f"{m} m"


def coach_totals(d):
    km = sum(r["km"] for r in d["rows"] if r["kind"] == "Transfer" and r["mode"] == "Coach")
    t = sum(mins(r, r["tz"] or d["tz"]) for r in d["rows"] if r["kind"] == "Transfer" and r["mode"] == "Coach")
    return km, t


def day_md(d):
    km, t = coach_totals(d)
    out = [f"### Day {d['day']} · {d['dow']} {d['date'][8:]} July · {d['title']}", "",
           f"Overnight: {d['overnight']}. By coach: {km:,} km, {fmt_m(t)} including breaks.", "",
           "| Time | What | Where (map) | Mode · km · duration | Details | Meal by / notes |",
           "| --- | --- | --- | --- | --- | --- |"]
    for r in d["rows"]:
        tz = r["tz"] or d["tz"]
        if r["kind"] == "Transfer":
            what = f"{r['mode']} transfer"
            where = f"[{cell(D.PLACES[r['frm']][0])} → {cell(D.PLACES[r['to']][0])}]({r['link']})"
            mode = f"{r['mode']} · {r['km']:,} km · {fmt_m(mins(r, tz))}"
        else:
            what = r["kind"]
            where = f"[{cell(D.PLACES[r['to']][0])}]({r['link']})"
            mode = f"{r['mode']} · {fmt_m(mins(r, tz))}"
        extra = " ".join(x for x in (r["meal_by"], r["note"]) if x)
        tzs = f" {tz}" if tz != "CEST" else ""
        detail = r["detail"]
        if detail.endswith("Bhajans, japa and sthala-purana narration on board.") and detail.startswith(r["mode"] + " "):
            detail = "On board: bhajans, japa, sthala-purana narration."
        out.append(f"| {r['start']}–{r['end']}{tzs} | {what} | {where} | {mode} | {cell(detail)} | {cell(extra)} |")
    return "\n".join(out)


def sections():
    s = {}
    s["summary"] = "\n".join(
        ["## Day summary", "",
         f"The coach covers about {sum(coach_totals(d)[0] for d in D.DAYS):,} km over 16 days. No day goes past the EU limit of 9 hours' driving. Days 6 and 10 are the longest, at about 7.5 hours on the coach including breaks.", "",
         "| Day | Date | Route | Overnight | Coach km | Coach time incl. breaks |", "| --- | --- | --- | --- | --- | --- |"]
        + [f"| {d['day']} | {d['dow']} {d['date'][8:]} Jul | {cell(d['title'])} | {d['overnight']} | {coach_totals(d)[0]:,} | {fmt_m(coach_totals(d)[1])} |" for d in D.DAYS]
        + ["", "Flights, the Dover–Calais ferry, boats, cable cars and the Lucerne–Interlaken train are not counted in coach km."])
    for name, rng, head in (("d1", range(0, 4), "Days 1–4: Hyderabad → London → Paris"),
                            ("d2", range(4, 8), "Days 5–8: Paris, New Mayapur, Brussels, Radhadesh, Amsterdam"),
                            ("d3", range(8, 12), "Days 9–12: Netherlands, Cologne, Goloka Dham, Black Forest, Zurich, Titlis, Lucerne"),
                            ("d4", range(12, 16), "Days 13–16: Lake Como, Milan, Venice, Pisa, Florence, Rome, Vatican")):
        s[name] = f"## {head}\n\n" + "\n\n".join(day_md(D.DAYS[i]) for i in rng)
    meals = ["## Meal plan", "",
             "Breakfast is at the hotel on all 15 hotel mornings. Lunch is at a temple on 6 days and at an Indian restaurant (or packed) on the rest. Dinner is at the hotel except on Day 2 (Govinda's, Soho) and Day 16 (packed, before the flight).", "",
             "| Day | Breakfast | Lunch | Dinner |", "| --- | --- | --- | --- |"]
    for d in D.DAYS:
        by = {}
        for r in d["rows"]:
            if r["kind"] in ("Breakfast", "Lunch", "Dinner"):
                by[r["kind"]] = f"{r['start']}–{r['end']} · [{cell(D.PLACES[r['to']][0])}]({r['link']}) · {cell(r['meal_by'])}"
        meals.append(f"| {d['day']} | {by.get('Breakfast', 'In flight / airport')} | {by.get('Lunch', '')} | {by.get('Dinner', '')} |")
    meals += ["", "All meals are Satvik: no onion, garlic, eggs, meat or fish. Confirm each menu in writing 2 weeks ahead and reconfirm 48 hours ahead. Restaurants marked TBC still need to be shortlisted and booked."]
    s["meals"] = "\n".join(meals)
    s["pros"] = "\n".join(["## Pros and cons by day", "", "Every day has one clear highlight. The cost is early starts and long coach legs on Days 4, 6, 10 and 16.", "",
                           "| Day | Pros | Cons / watch-outs |", "| --- | --- | --- |"]
                          + [f"| {a} | {cell(b)} | {cell(c)} |" for a, b, c in D.PROS_CONS])
    s["challenges"] = "\n".join(["## Challenges and risks", "", "The biggest risks are driver-hour limits, July traffic at borders and tunnels, and pickpockets in Paris and Rome. Each one has a mitigation below.", "",
                                 "| Challenge | What happens | Mitigation |", "| --- | --- | --- |"]
                                + [f"| {cell(a)} | {cell(b)} | {cell(c)} |" for a, b, c in D.CHALLENGES])
    s["dos"] = "\n".join(["## Do's and don'ts", "", "Share this section with yatris at the pre-departure orientation.", "", "**Do**", ""]
                         + [f"- {x}" for x in D.DOS] + ["", "**Don't**", ""] + [f"- {x}" for x in D.DONTS])
    s["visa"] = "\n".join(["## Visa, documents, inclusions and exclusions", "",
                           "The Schengen biometric appointment takes 10–12 minutes per person when every document is ready. Tick each item off below.", ""]
                          + [f"- [ ] **{a}:** {b}" for a, b in D.VISA_DOCS]
                          + ["", "| Inclusions | Exclusions |", "| --- | --- |"]
                          + [f"| {D.INCLUSIONS[i] if i < len(D.INCLUSIONS) else ''} | {D.EXCLUSIONS[i] if i < len(D.EXCLUSIONS) else ''} |" for i in range(max(len(D.INCLUSIONS), len(D.EXCLUSIONS)))]
                          + ["", f"Price: {D.YATRA['price']}."])
    s["practical"] = "\n".join(["## Practical information", "", "Pack for both heat and cold: Rome can reach 35 °C and the Titlis summit 0 °C within the same week.", "",
                                "| Topic | Details |", "| --- | --- |"] + [f"| {a} | {cell(b)} |" for a, b in D.PRACTICAL])
    return s


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for k, v in sections().items():
        open(os.path.join(out, k + ".md"), "w").write(v)
        print(k, len(v))
