#!/usr/bin/env python3
"""Turn a Google Maps Timeline export into travel statistics.

Reads any of the export formats Google has used:
  * Android on-device export  (Timeline.json, {"semanticSegments": [...]})
  * iPhone on-device export   (location-history.json, a top-level list)
  * Old Takeout export        (Semantic Location History/<year>/<YEAR>_<MONTH>.json)

Everything runs offline on your own computer; nothing is uploaded.

Usage:
    pip install reverse-geocode
    python3 timeline_travel_stats.py Timeline.json [more files or folders...] -o out/

Outputs (in the -o folder):
    visits.csv     one row per place visit with country / state / city
    countries.csv  countries with days, separate trips, first and last visit
    cities.csv     cities with country, state, days, separate trips, first and last visit
    by_year.csv    countries and cities seen per year
    summary.txt    plain-text overview (paste it, plus the CSVs, into an AI chat)
"""

import argparse
import csv
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date, datetime

# A new "trip" to the same city/country starts after this many days away.
TRIP_GAP_DAYS = 2

NUM = re.compile(r"-?\d+(?:\.\d+)?")


def parse_latlng(value):
    """Accepts '17.38°, 78.48°', 'geo:17.38,78.48' or {'latitudeE7':..., 'longitudeE7':...}."""
    if isinstance(value, dict):
        if "latitudeE7" in value:
            return value["latitudeE7"] / 1e7, value["longitudeE7"] / 1e7
        if "latLng" in value:
            return parse_latlng(value["latLng"])
        return None
    if isinstance(value, str):
        nums = NUM.findall(value)
        if len(nums) >= 2:
            lat, lng = float(nums[0]), float(nums[1])
            if -90 <= lat <= 90 and -180 <= lng <= 180:
                return lat, lng
    return None


def parse_time(value):
    if not value:
        return None
    if isinstance(value, (int, float)) or str(value).isdigit():
        return datetime.utcfromtimestamp(int(value) / 1000)
    text = str(value).replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        # Trim fractional seconds Python < 3.11 cannot read.
        return datetime.fromisoformat(re.sub(r"\.\d+", "", text))


def visits_from_file(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)

    if isinstance(data, dict) and "semanticSegments" in data:  # Android export
        for seg in data["semanticSegments"]:
            visit = seg.get("visit")
            if not visit:
                continue
            cand = visit.get("topCandidate", {})
            point = parse_latlng(cand.get("placeLocation", {}))
            if point:
                yield {
                    "start": parse_time(seg.get("startTime")),
                    "end": parse_time(seg.get("endTime")),
                    "lat": point[0],
                    "lng": point[1],
                    "place_id": cand.get("placeId", ""),
                    "semantic_type": cand.get("semanticType", ""),
                    "name": "",
                    "address": "",
                }

    elif isinstance(data, list):  # iPhone export
        for seg in data:
            visit = seg.get("visit")
            if not visit:
                continue
            cand = visit.get("topCandidate", {})
            point = parse_latlng(cand.get("placeLocation", ""))
            if point:
                yield {
                    "start": parse_time(seg.get("startTime")),
                    "end": parse_time(seg.get("endTime")),
                    "lat": point[0],
                    "lng": point[1],
                    "place_id": cand.get("placeID", ""),
                    "semantic_type": cand.get("semanticType", ""),
                    "name": "",
                    "address": "",
                }

    elif isinstance(data, dict) and "timelineObjects" in data:  # old Takeout
        for obj in data["timelineObjects"]:
            pv = obj.get("placeVisit")
            if not pv:
                continue
            loc = pv.get("location", {})
            point = parse_latlng(loc)
            dur = pv.get("duration", {})
            if point:
                yield {
                    "start": parse_time(dur.get("startTimestamp") or dur.get("startTimestampMs")),
                    "end": parse_time(dur.get("endTimestamp") or dur.get("endTimestampMs")),
                    "lat": point[0],
                    "lng": point[1],
                    "place_id": loc.get("placeId", ""),
                    "semantic_type": loc.get("semanticType", ""),
                    "name": loc.get("name", ""),
                    "address": loc.get("address", ""),
                }
    else:
        print(f"  skipped {path}: not a recognised Timeline format", file=sys.stderr)


def collect_files(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                for f in sorted(files):
                    if f.lower().endswith(".json"):
                        yield os.path.join(root, f)
        else:
            yield p


def local_dates(start, end):
    """Calendar dates a visit covers, in the visit's own recorded offset (capped at 31 days)."""
    if not start:
        return []
    first = start.date()
    last = end.date() if end and end >= start else first
    days = min((last - first).days, 31)
    return [date.fromordinal(first.toordinal() + i) for i in range(days + 1)]


def count_trips(days):
    days = sorted(days)
    trips = 1 if days else 0
    for a, b in zip(days, days[1:]):
        if (b - a).days > TRIP_GAP_DAYS:
            trips += 1
    return trips


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="Timeline export file(s) or folder(s)")
    ap.add_argument("-o", "--out", default="timeline_stats", help="output folder")
    ap.add_argument("--home-city", default="", help="exclude this city from the trip ranking (e.g. Hyderabad)")
    ap.add_argument("--min-population", type=int, default=15000,
                    help="snap each visit to the nearest town of at least this size (default 15000; "
                         "lower it to see small villages and pilgrimage towns separately)")
    args = ap.parse_args()

    try:
        import reverse_geocode
    except ImportError:
        sys.exit("Please install the offline geocoder first:  pip install reverse-geocode")

    visits = []
    for path in collect_files(args.inputs):
        print(f"reading {path}")
        visits.extend(visits_from_file(path))
    visits = [v for v in visits if v["start"]]
    visits.sort(key=lambda v: v["start"].timestamp())
    if not visits:
        sys.exit("No place visits found in the input.")
    print(f"{len(visits)} place visits; looking up cities offline...")

    # Round to ~100 m so repeated visits to the same spot are geocoded once.
    keys = sorted({(round(v["lat"], 3), round(v["lng"], 3)) for v in visits})
    geo = dict(zip(keys, reverse_geocode.search(keys, min_population=args.min_population)))

    os.makedirs(args.out, exist_ok=True)
    country_days = defaultdict(set)
    city_days = defaultdict(set)
    year_countries = defaultdict(set)
    year_cities = defaultdict(set)
    rows = []
    for v in visits:
        g = geo[(round(v["lat"], 3), round(v["lng"], 3))]
        country, state, city = g["country"], g.get("state", ""), g["city"]
        days = local_dates(v["start"], v["end"])
        country_days[country].update(days)
        city_days[(city, state, country)].update(days)
        year_countries[v["start"].year].add(country)
        year_cities[v["start"].year].add(f"{city}, {country}")
        rows.append([v["start"].isoformat(), v["end"].isoformat() if v["end"] else "",
                     f"{v['lat']:.5f}", f"{v['lng']:.5f}", city, state, country,
                     v["semantic_type"], v["name"], v["address"], v["place_id"]])

    write_csv(os.path.join(args.out, "visits.csv"),
              ["start", "end", "lat", "lng", "city", "state", "country",
               "semantic_type", "name", "address", "place_id"], rows)

    country_rows = sorted(
        ([c, len(d), count_trips(d), min(d), max(d)] for c, d in country_days.items()),
        key=lambda r: -r[1])
    write_csv(os.path.join(args.out, "countries.csv"),
              ["country", "days", "trips", "first_visit", "last_visit"], country_rows)

    city_rows = sorted(
        ([c, s, k, len(d), count_trips(d), min(d), max(d)] for (c, s, k), d in city_days.items()),
        key=lambda r: (-r[4], -r[3]))
    write_csv(os.path.join(args.out, "cities.csv"),
              ["city", "state", "country", "days", "trips", "first_visit", "last_visit"], city_rows)

    write_csv(os.path.join(args.out, "by_year.csv"),
              ["year", "countries", "cities", "country_list"],
              [[y, len(year_countries[y]), len(year_cities[y]), "; ".join(sorted(year_countries[y]))]
               for y in sorted(year_countries)])

    home = args.home_city.lower()
    lines = [
        f"Period: {visits[0]['start'].date()} to {visits[-1]['start'].date()}",
        f"Place visits: {len(visits)}",
        f"Countries: {len(country_days)}",
        f"Cities/towns: {len(city_days)}",
        "",
        "Countries (days, trips):",
    ]
    lines += [f"  {r[0]}: {r[1]} days, {r[2]} trips (first {r[3]}, last {r[4]})" for r in country_rows]
    lines += ["", "Most-visited cities (trips, days):"]
    lines += [f"  {r[0]}, {r[1]}, {r[2]}: {r[4]} trips, {r[3]} days"
              for r in city_rows if r[0].lower() != home][:40]
    lines += ["", "Per year:"]
    lines += [f"  {y}: {len(year_countries[y])} countries, {len(year_cities[y])} cities"
              for y in sorted(year_countries)]
    summary = "\n".join(lines)
    with open(os.path.join(args.out, "summary.txt"), "w", encoding="utf-8") as fh:
        fh.write(summary + "\n")
    print("\n" + summary)
    print(f"\nWrote CSVs and summary to {args.out}/")


if __name__ == "__main__":
    main()
