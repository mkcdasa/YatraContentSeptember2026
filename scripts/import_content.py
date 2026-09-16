#!/usr/bin/env python3
"""
Turn the Yatra Department's spreadsheets and Word documents into seed SQL.

    python3 scripts/import_content.py --src ./source-content --out supabase/seed

Expected files in --src (names are matched loosely, case-insensitive):
    *Yatra_Calendar*.xlsx     the 22-sheet master workbook
    *Shakti_Peethas*.xlsx     holy places master
    *Itenararies*.docx        all itineraries
    *Evernote*.docx           department notes, packing lists, links

Everything is emitted as idempotent INSERT ... ON CONFLICT so the script can be
re-run after the team edits a sheet. Slugs are the natural keys.
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import os
import re
import sys
import unicodedata
from typing import Any, Iterable

try:
    import openpyxl
    import docx
except ImportError:
    sys.exit("pip install openpyxl python-docx")

# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

MONTHS = {
    "january": 1, "jan": 1, "february": 2, "feb": 2, "febraury": 2, "febuary": 2,
    "march": 3, "mar": 3, "april": 4, "apr": 4, "may": 5, "june": 6, "jun": 6,
    "july": 7, "jul": 7, "august": 8, "aug": 8, "september": 9, "sep": 9,
    "sept": 9, "spetember": 9, "sepember": 9, "october": 10, "oct": 10,
    "november": 11, "nov": 11, "december": 12, "dec": 12,
}


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return re.sub(r"-{2,}", "-", text)[:90] or "item"


def clean(v: Any) -> str:
    """Normalise a cell to a single-spaced string."""
    if v is None:
        return ""
    if isinstance(v, (dt.datetime, dt.date)):
        return v.strftime("%Y-%m-%d")
    return " ".join(str(v).split())


def q(v: Any) -> str:
    """SQL literal."""
    if v is None or v == "":
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return repr(v)
    return "'" + str(v).replace("'", "''") + "'"


def arr(values: Iterable[Any], cast: str = "text[]") -> str:
    vals = [v for v in values if v not in (None, "")]
    if not vals:
        return f"'{{}}'::{cast}"
    if cast.startswith("smallint"):
        return "array[" + ",".join(str(int(v)) for v in vals) + f"]::{cast}"
    inner = ",".join("'" + str(v).replace("'", "''") + "'" for v in vals)
    return f"array[{inner}]::{cast}"


def parse_months(text: str) -> list[int]:
    """'May, June, September' and 'Nov to Feb' and 'April to October' -> [..]."""
    text = (text or "").lower()
    if not text:
        return []
    found: set[int] = set()

    # ranges first: "april to october", "nov – feb", "september to october"
    for a, b in re.findall(r"([a-z]+)\s*(?:to|-|–|until|till)\s*([a-z]+)", text):
        if a in MONTHS and b in MONTHS:
            start, end = MONTHS[a], MONTHS[b]
            m = start
            while True:
                found.add(m)
                if m == end:
                    break
                m = m % 12 + 1
                if len(found) > 12:
                    break

    for word in re.findall(r"[a-z]+", text):
        if word in MONTHS:
            found.add(MONTHS[word])
    return sorted(found)


def parse_duration(text: str) -> tuple[int | None, int | None]:
    """'12N/13D' -> (12, 13)."""
    m = re.search(r"(\d+)\s*N\s*/\s*(\d+)\s*D", str(text or ""), re.I)
    return (int(m.group(1)), int(m.group(2))) if m else (None, None)


def as_num(v: Any) -> float | None:
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = re.sub(r"[^\d.\-]", "", str(v))
    try:
        return float(s) if s not in ("", "-", ".") else None
    except ValueError:
        return None


def as_date(v: Any) -> str | None:
    if isinstance(v, (dt.datetime, dt.date)):
        return v.strftime("%Y-%m-%d")
    s = clean(v)
    return s if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s) else None


def find(src: str, pattern: str) -> str | None:
    hits = [p for p in glob.glob(os.path.join(src, "**", "*"), recursive=True)
            if re.search(pattern, os.path.basename(p), re.I)]
    return hits[0] if hits else None


def rows(ws) -> list[list[Any]]:
    return [list(r) for r in ws.iter_rows(values_only=True)]


def cell(row: list[Any], i: int) -> str:
    return clean(row[i]) if i < len(row) else ""


# --------------------------------------------------------------------------
# scope / nature classification
# --------------------------------------------------------------------------

INTERNATIONAL_HINTS = ("kailas", "nepal", "muktinath", "srilanka", "sri lanka", "bali",
                       "europe", "cambodia", "thailand", "usa", "australia", "vietnam",
                       "malaysia", "russia", "mayapur" )
RISKY_HINTS = ("kailas", "amarnath", "chardham", "char dham", "kedarnath")
SPECIAL_HINTS = ("kumbh", "khumb", "pushkar", "ratha yatra", "rath yatra", "mela")
SEASONAL_HINTS = ("chardham", "char dham", "kailas", "amarnath", "muktinath", "nepal", "dodham", "do dham")


def classify(title: str, declared: str = "") -> tuple[str, str, int]:
    t = title.lower()
    d = (declared or "").lower()
    if "inernational" in d or "international" in d or any(h in t for h in INTERNATIONAL_HINTS):
        scope = "international"
    elif "national" in d:
        scope = "national"
    else:
        scope = "domestic"

    if any(h in t for h in SPECIAL_HINTS):
        nature = "special"
    elif any(h in t for h in RISKY_HINTS):
        nature = "risky"
    elif any(h in t for h in SEASONAL_HINTS):
        nature = "seasonal"
    else:
        nature = "evergreen"

    if "kailas" in t:
        difficulty = 5
    elif "amarnath" in t or ("chardham" in t and "helicopter" not in t):
        difficulty = 4
    elif "ahobilam" in t or "muktinath" in t or "badrinath" in t:
        difficulty = 3
    else:
        difficulty = 2
    return scope, nature, difficulty


THEME_MAP = [
    ("jyotirling", "Dwadasha Jyotirlingas"), ("shakti", "Ashtadasha Shakti Peethas"),
    ("divya", "106 Divya Desams"), ("narasimha", "Nava Narasimha Kshetras"),
    ("dwaraka", "Pancha Dwaraka"), ("ramayan", "Footsteps of Lord Rama"),
    ("chardham", "Char Dham"), ("char dham", "Char Dham"),
    ("pushkar", "Pushkaras"), ("kumbh", "Kumbh Mela"), ("khumb", "Kumbh Mela"),
    ("parikrama", "Parikrama"), ("mayapur", "Mayapur Nine Islands"),
]


STOPWORDS = {"yatra", "yatras", "pilgrimage", "by", "the", "and", "route", "special", "spl"}


def tokens(slug: str) -> set[str]:
    return {t for t in slug.split("-") if t and t not in STOPWORDS}


def best_match(slug: str, candidates: set[str]) -> str | None:
    """Pick the candidate sharing the most distinctive tokens, needing >=2 or a
    single rare token that is at least 5 characters long."""
    want = tokens(slug)
    if not want:
        return None
    scored = []
    for cand in candidates:
        have = tokens(cand)
        # treat kailas/kailasa, chardham/char-dham as the same stem
        overlap = {w for w in want if any(w[:6] == h[:6] for h in have)}
        if overlap:
            scored.append((len(overlap), -len(have), cand))
    if not scored:
        return None
    scored.sort(reverse=True)
    score, _, cand = scored[0]
    if score >= 2:
        return cand
    only = next(iter(tokens(slug) & {t for t in tokens(cand)} or tokens(slug)), "")
    return cand if len(only) >= 4 else None


def themes_for(title: str) -> list[str]:
    t = title.lower()
    return sorted({label for key, label in THEME_MAP if key in t})


# --------------------------------------------------------------------------
# extractors
# --------------------------------------------------------------------------

def extract_destinations(wb_main, wb_places) -> list[dict]:
    """State-wise temple list + the Shakti Peetha / Jyotirlinga / Divya Desam master."""
    out: dict[str, dict] = {}

    ws = wb_main["List of Temples State Wise & Ya"]
    state = None
    for row in rows(ws):
        vals = [clean(v) for v in row]
        filled = [v for v in vals if v]
        if not filled:
            continue
        if len(filled) == 1:                      # a state banner row
            state = filled[0]
            continue
        if vals[0].lower().startswith("s no") or cell(vals, 1).lower() == "name of the temple":
            continue
        name = cell(vals, 1)
        if not name:
            continue
        best = cell(vals, 4)
        rec = {
            "slug": slugify(f"{name}-{state or ''}"),
            "name": name,
            "kinds": ["temple"],
            "deity": cell(vals, 3) or None,
            "region": cell(vals, 2) or None,
            "city": cell(vals, 2) or None,
            "state": state,
            "country": "India",
            "best_months": parse_months(best),
            "avoid_months": [],
            "best_time_note": best or None,
            "sevas": [s.strip() for s in cell(vals, 5).split(",") if s.strip()],
            "speciality": cell(vals, 6) or None,
            "description": None,
            "map_url": None,
        }
        out.setdefault(rec["slug"], rec)

    # holy-places master: mixed types in one sheet, distinguished by column B
    ws2 = wb_places["Master "]
    kind_map = {
        "shakipeeth": "shakti_peetha", "shaktipeeth": "shakti_peetha",
        "jyotirlinga": "jyotirlinga", "divyadesham": "divya_desam",
        "unesco heritage sites": "unesco",
    }
    for row in rows(ws2):
        vals = [clean(v) for v in row]
        if not any(vals) or cell(vals, 0).lower().startswith("sr"):
            continue
        raw_kind = cell(vals, 1).lower()
        name = cell(vals, 2)
        if not name:
            continue
        kind = kind_map.get(raw_kind, "river" if not raw_kind else "other")
        state = cell(vals, 4) or None
        slug = slugify(f"{name}-{state or ''}")
        detail = cell(vals, 10)
        rec = out.get(slug)
        if rec:                                    # same place already seen — merge
            if kind not in rec["kinds"]:
                rec["kinds"].append(kind)
            rec["description"] = rec["description"] or (detail or None)
            continue
        out[slug] = {
            "slug": slug, "name": name, "kinds": [kind],
            "deity": cell(vals, 6) or None,
            "region": None, "city": cell(vals, 3) or None,
            "state": state,
            "country": "India" if "india" in (state or "India").lower() or state else "India",
            "best_months": [], "avoid_months": [], "best_time_note": None,
            "sevas": [], "speciality": None,
            "description": detail or None,
            "map_url": cell(vals, 9) or None,
        }
    return list(out.values())


def extract_yatras(wb) -> tuple[list[dict], list[dict], list[dict]]:
    """Yatras, their 2026 batches and the pricing attached to each batch."""
    yatras: dict[str, dict] = {}
    batches: list[dict] = []
    prices: list[dict] = []

    def ingest(sheet_name: str, general_at: int, premium_at: int | None):
        ws = wb[sheet_name]
        for row in rows(ws):
            vals = [clean(v) for v in row]
            raw = list(row)
            title = cell(vals, 1)
            if not title or title.lower() in ("yatra title", "s no", "s no.", "sno"):
                continue
            if not re.match(r"^\d", cell(vals, 0)):
                continue
            slug = slugify(title)
            nights, days = parse_duration(cell(vals, 5))
            scope, nature, difficulty = classify(title, cell(vals, 2))
            yatras.setdefault(slug, {
                "slug": slug, "title": title.title(), "scope": scope, "nature": nature,
                "themes": themes_for(title), "nights": nights, "days": days,
                "min_pax": int(as_num(raw[6]) or 30) if len(raw) > 6 else 30,
                "difficulty": difficulty,
                "visa_required": scope == "international",
                "summary": None,
                "senior_friendly": difficulty <= 3,
            })
            start, end = as_date(raw[7] if len(raw) > 7 else None), as_date(raw[8] if len(raw) > 8 else None)
            if not start:
                continue
            key = f"{slug}|{start}"
            batches.append({"key": key, "yatra_slug": slug, "start_date": start,
                            "end_date": end, "status": "planned"})
            for tier, base in (("general", general_at), ("premium", premium_at)):
                if base is None or len(raw) <= base:
                    continue
                amount = as_num(raw[base])
                if not amount:
                    continue
                prices.append({
                    "batch_key": key, "yatra_slug": slug, "tier": tier, "amount": amount,
                    "gst": as_num(raw[base + 1]) or 0 if len(raw) > base + 1 else 0,
                    "tcs": as_num(raw[base + 2]) or 0 if len(raw) > base + 2 else 0,
                })

    #                              general AMOUNT col, premium AMOUNT col
    ingest("ALL YATRAS WITH DATES & BUDGET ", 11, 15)
    ingest("International Yatras ", 13, None)
    return list(yatras.values()), batches, prices


def extract_economics(wb) -> list[dict]:
    ws = wb["Management Budget for VIPs"]
    out = []
    for row in rows(ws):
        vals = [clean(v) for v in row]
        raw = list(row)
        title = cell(vals, 1)
        if not title or not re.match(r"^\d", cell(vals, 0)):
            continue
        revenue = as_num(raw[11]) if len(raw) > 11 else None
        surplus = as_num(raw[12]) if len(raw) > 12 else None
        out.append({
            "yatra_slug": slugify(title),
            "expected_pax": int(as_num(raw[5]) or 0) or None if len(raw) > 5 else None,
            "ticket_avg": as_num(raw[7]) if len(raw) > 7 else None,
            "expected_revenue": revenue,
            "expected_surplus": surplus,
            "margin_pct": round(surplus / revenue * 100, 2) if revenue and surplus else None,
            "notes": cell(vals, 14) or None,
        })
    return out


def extract_travel_windows(wb) -> list[dict]:
    """Dashboard sheet: two stacked tables, domestic then international."""
    ws = wb["Dashboard"]
    out = []
    for row in rows(ws):
        vals = [clean(v) for v in row]
        name = cell(vals, 1)
        if not name or name.lower() in ("destination", "best season to travel"):
            continue
        best, shoulder, avoid = cell(vals, 3), cell(vals, 4), cell(vals, 5)
        if not (best or shoulder or avoid):
            continue
        total = cell(vals, 2)
        m = re.search(r"(\d+)", total)
        out.append({
            "yatra_slug": slugify(name),
            "label": name,
            "best_months": parse_months(best),
            "shoulder_months": parse_months(shoulder),
            "avoid_months": parse_months(avoid),
            "open_months": int(m.group(1)) if m and "month" in total.lower() else None,
            "weather_note": shoulder or None,
            "caution": avoid or None,
        })
    return out


def extract_calendar(wb) -> tuple[list[dict], list[dict]]:
    panchanga: dict[str, dict] = {}
    events: list[dict] = []

    ws = wb["PROMOTIONAL CALENDER 2026"]
    for row in rows(ws):
        raw = list(row)
        d = as_date(raw[0] if raw else None)
        if not d:
            continue
        vals = [clean(v) for v in row]
        panchanga[d] = {
            "on_date": d, "tithi": cell(vals, 4) or None, "masam": cell(vals, 5) or None,
            "paksha": cell(vals, 6) or None, "nakshatra": cell(vals, 7) or None,
            "yoga": cell(vals, 8) or None, "karana": cell(vals, 9) or None,
        }
        for idx, kind in ((1, "special_occasion"), (2, "iskcon_festival"), (3, "public_holiday")):
            for piece in re.split(r"[,;]\s*", cell(vals, idx)):
                piece = piece.strip()
                if piece:
                    events.append({"on_date": d, "kind": kind, "title": piece,
                                   "temple": None, "deity": None, "masam": None,
                                   "significance": None})

    ws2 = wb["Special festival Yatras"]
    for row in rows(ws2):
        raw = list(row)
        d = as_date(raw[1] if len(raw) > 1 else None)
        if not d:
            continue
        vals = [clean(v) for v in row]
        for idx, kind in ((2, "iskcon_festival"), (3, "hindu_festival")):
            for piece in re.split(r"[,;]\s*", cell(vals, idx)):
                piece = piece.strip()
                if piece:
                    events.append({
                        "on_date": d, "kind": kind, "title": piece,
                        "temple": cell(vals, 4) or None, "deity": cell(vals, 7) or None,
                        "masam": cell(vals, 8) or None,
                        "significance": cell(vals, 9) or None,
                    })
    # dedupe (a festival often appears in both sheets)
    seen, unique = set(), []
    for e in events:
        k = (e["on_date"], e["kind"], e["title"].lower())
        if k not in seen:
            seen.add(k)
            unique.append(e)
    return list(panchanga.values()), unique


DAY_RE = re.compile(r"^\**\s*day\s*0*(\d+)\b", re.I)


def extract_itineraries(path: str) -> list[dict]:
    """Heading 1 starts a yatra; 'Day N' lines start a day; text accrues to it."""
    doc = docx.Document(path)
    itineraries: list[dict] = []
    current: dict | None = None
    day: dict | None = None

    def close_day():
        nonlocal day
        if current and day and (day["body"] or day["title"]):
            current["days"].append(day)
        day = None

    for para in doc.paragraphs:
        text = " ".join(para.text.split())
        if not text:
            continue
        style = para.style.name
        if style.startswith("Heading"):
            close_day()
            title = re.sub(r"[*🌟]", "", text).strip()
            title = re.sub(r"\s*Yatra Highlights\s*$", "", title, flags=re.I).strip(" .")
            if not title:
                continue
            current = {"title": title, "slug": slugify(title), "intro": None, "days": []}
            itineraries.append(current)
            continue
        if current is None:
            continue
        m = DAY_RE.match(text)
        if m:
            close_day()
            rest = DAY_RE.sub("", text).strip(" -–:*")
            day = {"day_number": int(m.group(1)), "title": rest[:160] or None, "body": ""}
            continue
        if day is not None:
            day["body"] = (day["body"] + "\n" + text).strip()
        elif current["intro"] is None and len(text) > 20:
            current["intro"] = text[:600]
    close_day()

    # keep only sections that actually produced day-by-day content, and
    # collapse duplicate headings (the source doc repeats several yatras)
    best: dict[str, dict] = {}
    for it in itineraries:
        if not it["days"]:
            continue
        prev = best.get(it["slug"])
        if prev is None or len(it["days"]) > len(prev["days"]):
            best[it["slug"]] = it
    return list(best.values())


YT_RE = re.compile(r"https?://(?:www\.)?(?:youtu\.be/|youtube\.com/watch\?v=)([\w-]{6,})")


def extract_notes(path: str) -> tuple[list[dict], list[dict]]:
    """Evernote export -> knowledge articles + the YouTube links scattered in it."""
    doc = docx.Document(path)
    lines = [" ".join(p.text.split()) for p in doc.paragraphs]
    lines = [l for l in lines if l]

    videos = []
    for line in lines:
        for m in YT_RE.finditer(line):
            videos.append({"title": f"Reference video {m.group(1)}", "youtube_id": m.group(1),
                           "url": m.group(0), "kind": "expert"})
    seen, uniq = set(), []
    for v in videos:
        if v["youtube_id"] not in seen:
            seen.add(v["youtube_id"])
            uniq.append(v)

    # Section the note by its own signposts. Anything before the first marker is
    # dropped rather than guessed at.
    sections = [
        ("items-to-carry", "Items to Carry for a Yatra", "packing", "public", "Items to carry for the Yatra"),
        ("why-yatra-with-devotees", "Why Yatra With Hare Krishna Devotees", "orientation", "public", "Why yatras with Hare Krishna devotees?:"),
        ("yatra-themes", "Yatra Themes and Circuits", "planning", "public", "Highlights or themes for Yatras or trips"),
        ("innovations-in-yatras", "Innovations in Yatras", "hospitality", "staff", "INNOVATIONS IN YATRAS"),
        ("low-cost-enrolment", "Low Cost, Rapid Enrolment Channels", "marketing", "staff", "*LOW COST-RAPID ENROLLMENTS FOR YATRAS*"),
        ("knowledge-base-charter", "Knowledge Base Charter", "planning", "staff", "Create a Knowledge Base for Yatras"),
    ]
    articles = []
    for slug, title, category, visibility, marker in sections:
        try:
            start = next(i for i, l in enumerate(lines) if marker.lower() in l.lower())
        except StopIteration:
            continue
        body, blanks = [], 0
        for line in lines[start + 1:start + 90]:
            if any(m.lower() in line.lower() for _, _, _, _, m in sections if m != marker):
                break
            if len(line) < 3:
                blanks += 1
                if blanks > 2:
                    break
                continue
            body.append(f"- {line}" if not line.startswith(("-", "*", "♦")) else line)
        if body:
            articles.append({"slug": slug, "title": title, "category": category,
                             "visibility": visibility, "body_md": "\n".join(body)})
    return articles, uniq


# --------------------------------------------------------------------------
# SQL emission
# --------------------------------------------------------------------------

HEADER = (
    "-- Generated by scripts/import_content.py — do not edit by hand.\n"
    "-- Re-running the importer regenerates these files from the source workbooks.\n"
)


def emit(dest, yatras, batches, prices, econ, windows, panchanga, events, itins, articles, videos):
    """Return ordered (filename, sql) parts.

    Split by entity rather than emitted as one file: the whole seed is a few
    megabytes, and a reviewer or a partial re-run wants destinations without
    also re-reading a thousand panchanga rows. Numbering fixes the order, which
    matters because batches resolve yatras by slug.
    """
    parts: list[tuple[str, list[str]]] = []
    L: list[str] = []

    L.append("-- destinations ---------------------------------------------------------")
    for d in dest:
        L.append(
            "insert into destinations (slug,name,kinds,deity,region,city,state,country,"
            "best_months,avoid_months,best_time_note,sevas,speciality,description,map_url) values ("
            f"{q(d['slug'])},{q(d['name'])},{arr(d['kinds'],'place_kind[]')},{q(d['deity'])},"
            f"{q(d['region'])},{q(d['city'])},{q(d['state'])},{q(d['country'])},"
            f"{arr(d['best_months'],'smallint[]')},{arr(d['avoid_months'],'smallint[]')},"
            f"{q(d['best_time_note'])},{arr(d['sevas'])},{q(d['speciality'])},{q(d['description'])},"
            f"{q(d['map_url'])}) on conflict (slug) do update set "
            "name=excluded.name, kinds=excluded.kinds, deity=excluded.deity, "
            "best_months=excluded.best_months, sevas=excluded.sevas, "
            "speciality=excluded.speciality, description=coalesce(excluded.description, destinations.description);"
        )

    parts.append(("01_destinations.sql", L)); L = []
    L.append("-- yatras --------------------------------------------------------------")
    for y in yatras:
        L.append(
            "insert into yatras (slug,title,scope,nature,themes,nights,days,min_pax,difficulty,"
            "visa_required,senior_friendly,summary) values ("
            f"{q(y['slug'])},{q(y['title'])},{q(y['scope'])}::yatra_scope,{q(y['nature'])}::yatra_nature,"
            f"{arr(y['themes'])},{q(y['nights'])},{q(y['days'])},{q(y['min_pax'])},{q(y['difficulty'])},"
            f"{q(y['visa_required'])},{q(y['senior_friendly'])},{q(y['summary'])}) "
            "on conflict (slug) do update set title=excluded.title, scope=excluded.scope, "
            "nature=excluded.nature, themes=excluded.themes, nights=excluded.nights, days=excluded.days;"
        )

    # An itinerary heading may name a yatra the budget sheet never listed. Create
    # the shell here, before anything resolves a yatra by slug, so no itinerary
    # and no travel window is silently dropped.
    known_slugs = {y["slug"] for y in yatras}
    for it in itins:
        if it["slug"] in known_slugs:
            continue
        scope, nature, difficulty = classify(it["title"])
        L.append(
            "insert into yatras (slug,title,scope,nature,themes,difficulty,visa_required) values ("
            f"{q(it['slug'])},{q(it['title'])},{q(scope)}::yatra_scope,{q(nature)}::yatra_nature,"
            f"{arr(themes_for(it['title']))},{difficulty},{q(scope == 'international')}) "
            "on conflict (slug) do nothing;"
        )

    parts.append(("02_yatras.sql", L)); L = []
    L.append("-- batches -------------------------------------------------------------")
    for b in batches:
        L.append(
            "insert into yatra_batches (yatra_id,start_date,end_date,status) select y.id,"
            f"{q(b['start_date'])}::date,{q(b['end_date'])}::date,'planned'::batch_status "
            f"from yatras y where y.slug={q(b['yatra_slug'])} "
            "and not exists (select 1 from yatra_batches x where x.yatra_id=y.id "
            f"and x.start_date={q(b['start_date'])}::date);"
        )

    parts.append(("03_batches.sql", L)); L = []
    L.append("-- pricing (staff-tier) ------------------------------------------------")
    for p in prices:
        L.append(
            "insert into batch_pricing (batch_id,yatra_id,tier,amount,gst,tcs) "
            f"select b.id,y.id,{q(p['tier'])}::price_tier,{p['amount']},{p['gst']},{p['tcs']} "
            f"from yatras y join yatra_batches b on b.yatra_id=y.id "
            f"where y.slug={q(p['yatra_slug'])} and b.start_date={q(p['batch_key'].split('|')[1])}::date "
            "and not exists (select 1 from batch_pricing bp where bp.batch_id=b.id "
            f"and bp.tier={q(p['tier'])}::price_tier);"
        )

    parts.append(("04_pricing.sql", L)); L = []
    L.append("-- economics (staff-tier) ----------------------------------------------")
    for e in econ:
        L.append(
            "insert into batch_economics (yatra_id,expected_pax,ticket_avg,expected_revenue,"
            "expected_surplus,margin_pct,notes) select y.id,"
            f"{q(e['expected_pax'])},{q(e['ticket_avg'])},{q(e['expected_revenue'])},"
            f"{q(e['expected_surplus'])},{q(e['margin_pct'])},{q(e['notes'])} "
            f"from yatras y where y.slug={q(e['yatra_slug'])} "
            "and not exists (select 1 from batch_economics be where be.yatra_id=y.id);"
        )

    parts.append(("05_economics.sql", L)); L = []
    L.append("-- travel windows ------------------------------------------------------")
    for w in windows:
        L.append(
            "insert into travel_windows (yatra_id,best_months,shoulder_months,avoid_months,"
            "open_months,weather_note,caution) select y.id,"
            f"{arr(w['best_months'],'smallint[]')},{arr(w['shoulder_months'],'smallint[]')},"
            f"{arr(w['avoid_months'],'smallint[]')},{q(w['open_months'])},{q(w['weather_note'])},"
            f"{q(w['caution'])} from yatras y where y.slug={q(w['yatra_slug'])} "
            "on conflict (yatra_id) do update set best_months=excluded.best_months, "
            "shoulder_months=excluded.shoulder_months, avoid_months=excluded.avoid_months, "
            "open_months=excluded.open_months, caution=excluded.caution;"
        )

    parts.append(("06_travel_windows.sql", L)); L = []
    L.append("-- panchanga ----------------------------------------------------------")
    for p in panchanga:
        L.append(
            "insert into panchanga (on_date,tithi,masam,paksha,nakshatra,yoga,karana) values ("
            f"{q(p['on_date'])}::date,{q(p['tithi'])},{q(p['masam'])},{q(p['paksha'])},"
            f"{q(p['nakshatra'])},{q(p['yoga'])},{q(p['karana'])}) "
            "on conflict (on_date) do update set tithi=excluded.tithi, masam=excluded.masam, "
            "paksha=excluded.paksha, nakshatra=excluded.nakshatra;"
        )

    parts.append(("07_panchanga.sql", L)); L = []
    L.append("-- calendar events ----------------------------------------------------")
    for e in events:
        L.append(
            "insert into calendar_events (on_date,kind,title,temple,deity,masam,significance) "
            f"select {q(e['on_date'])}::date,{q(e['kind'])}::event_kind,{q(e['title'])},"
            f"{q(e['temple'])},{q(e['deity'])},{q(e['masam'])},{q(e['significance'])} "
            "where not exists (select 1 from calendar_events c where "
            f"c.on_date={q(e['on_date'])}::date and c.kind={q(e['kind'])}::event_kind "
            f"and c.title={q(e['title'])});"
        )

    parts.append(("08_calendar_events.sql", L)); L = []
    L.append("-- itineraries --------------------------------------------------------")
    for it in itins:
        L.append(
            "insert into itineraries (yatra_id,version,title,intro,is_current) "
            f"select y.id,1,{q(it['title'])},{q(it['intro'])},true from yatras y "
            f"where y.slug={q(it['slug'])} on conflict (yatra_id,version) do update set "
            "intro=excluded.intro;"
        )
        for d in it["days"]:
            L.append(
                "insert into itinerary_days (itinerary_id,day_number,title,body) "
                f"select i.id,{d['day_number']},{q(d['title'])},{q(d['body'])} "
                f"from itineraries i join yatras y on y.id=i.yatra_id "
                f"where y.slug={q(it['slug'])} and i.version=1 "
                "on conflict (itinerary_id,day_number) do update set "
                "title=excluded.title, body=excluded.body;"
            )

    parts.append(("09_itineraries.sql", L)); L = []
    L.append("-- knowledge articles -------------------------------------------------")
    for a in articles:
        L.append(
            "insert into knowledge_articles (slug,title,category,body_md,visibility) values ("
            f"{q(a['slug'])},{q(a['title'])},{q(a['category'])},{q(a['body_md'])},"
            f"{q(a['visibility'])}::audience) on conflict (slug) do update set "
            "title=excluded.title, body_md=excluded.body_md, visibility=excluded.visibility;"
        )

    parts.append(("10_articles.sql", L)); L = []
    L.append("-- videos -------------------------------------------------------------")
    for v in videos:
        L.append(
            "insert into videos (title,youtube_id,url,kind) "
            f"select {q(v['title'])},{q(v['youtube_id'])},{q(v['url'])},{q(v['kind'])}::video_kind "
            f"where not exists (select 1 from videos x where x.youtube_id={q(v['youtube_id'])});"
        )

    parts.append(("11_videos.sql", L))
    return _render(parts)


# Keep any one seed file comfortably reviewable, and small enough to move over
# an API that takes file content inline. Splitting happens on whole statements.
MAX_BYTES = 400_000


def _render(parts: list[tuple[str, list[str]]]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for name, body in parts:
        if not body:
            continue
        chunks: list[list[str]] = [[]]
        size = 0
        for stmt in body:
            if size + len(stmt) > MAX_BYTES and chunks[-1]:
                chunks.append([])
                size = 0
            chunks[-1].append(stmt)
            size += len(stmt) + 1
        stem, ext = name.rsplit(".", 1)
        for i, chunk in enumerate(chunks):
            suffix = "" if len(chunks) == 1 else f"_{chr(ord('a') + i)}"
            out.append((f"{stem}{suffix}.{ext}",
                        HEADER + "begin;\n\n" + "\n".join(chunk) + "\n\ncommit;\n"))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="source-content")
    ap.add_argument("--out", default="supabase/seed", help="directory for the numbered seed files")
    args = ap.parse_args()

    main_xlsx = find(args.src, r"yatra.*calendar.*\.xlsx$")
    places_xlsx = find(args.src, r"shakti.*\.xlsx$")
    itin_docx = find(args.src, r"iten|itiner.*\.docx$")
    notes_docx = find(args.src, r"evernote.*\.docx$")
    missing = [n for n, p in [("calendar xlsx", main_xlsx), ("places xlsx", places_xlsx),
                              ("itineraries docx", itin_docx), ("notes docx", notes_docx)] if not p]
    if missing:
        sys.exit(f"missing source files in {args.src}: {', '.join(missing)}")

    wb_main = openpyxl.load_workbook(main_xlsx, data_only=True)
    wb_places = openpyxl.load_workbook(places_xlsx, data_only=True)

    dest = extract_destinations(wb_main, wb_places)
    yatras, batches, prices = extract_yatras(wb_main)
    econ = extract_economics(wb_main)
    windows = extract_travel_windows(wb_main)
    panchanga, events = extract_calendar(wb_main)
    itins = extract_itineraries(itin_docx)
    articles, videos = extract_notes(notes_docx)

    # The Dashboard names destinations loosely ("Kailash - Land Route") while the
    # budget sheet names packages ("KAILASA MANASA SAROVAR YATRA"). Match on
    # shared significant tokens rather than exact slugs, and report what missed
    # so nobody assumes a window was applied when it was not.
    known = {y["slug"] for y in yatras} | {i["slug"] for i in itins}
    matched, unmatched, used = [], [], set()
    for w in windows:
        hit = w["yatra_slug"] if w["yatra_slug"] in known else best_match(w["yatra_slug"], known)
        if hit and hit not in used:
            used.add(hit)
            matched.append({**w, "yatra_slug": hit})
        else:
            unmatched.append(w)

    parts = emit(dest, yatras, batches, prices, econ, matched, panchanga, events,
                 itins, articles, videos)
    outdir = args.out
    os.makedirs(outdir, exist_ok=True)
    for name in sorted(os.listdir(outdir)):
        if re.fullmatch(r"\d\d_.*\.sql", name):
            os.remove(os.path.join(outdir, name))
    for name, sql in parts:
        with open(os.path.join(outdir, name), "w") as fh:
            fh.write(sql)

    print(f"wrote {len(parts)} files to {outdir}/")
    for label, n in [("destinations", len(dest)), ("yatras", len(yatras)),
                     ("batches", len(batches)), ("prices", len(prices)),
                     ("economics", len(econ)), ("travel windows", len(matched)),
                     ("panchanga days", len(panchanga)), ("calendar events", len(events)),
                     ("itineraries", len(itins)),
                     ("itinerary days", sum(len(i["days"]) for i in itins)),
                     ("articles", len(articles)), ("videos", len(videos))]:
        print(f"  {label:18} {n}")
    if unmatched:
        print(f"  unmatched travel windows: {', '.join(w['label'] for w in unmatched)}")


if __name__ == "__main__":
    main()
