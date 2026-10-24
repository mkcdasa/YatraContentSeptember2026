"""Build London_Europe_Yatra_Minute_Itinerary.xlsx from itinerary_data.py.

    python3 build_workbook.py            # writes the .xlsx next to this file
"""
import datetime as dt
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import itinerary_data as D  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "London_Europe_Yatra_Minute_Itinerary.xlsx")

FONT = "Arial"
SAFFRON = "E8892B"
HEAD = PatternFill("solid", fgColor="1F4E79")
DAYBAND = PatternFill("solid", fgColor="FCE4CC")
MEAL = PatternFill("solid", fgColor="E2EFDA")
MOVE = PatternFill("solid", fgColor="DDEBF7")
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
LINK = Font(name=FONT, size=9, color="0563C1", underline="single")
BODY = Font(name=FONT, size=9)

# Real elapsed minutes for rows whose clock times sit in two time zones.
# IST = UTC+5:30, BST = UTC+1, CEST = UTC+2, GST (Gulf) = UTC+4.
TZ_OFFSET = {"IST": 330, "BST": 60, "CEST": 120, "GST": 240}


def tm(s):
    h, m = map(int, s.split(":"))
    return dt.time(h, m)


def real_minutes(row):
    a, b = row["tz"].split("→")
    sh, sm = map(int, row["start"].split(":"))
    eh, em = map(int, row["end"].split(":"))
    start = sh * 60 + sm - TZ_OFFSET[a]
    end = eh * 60 + em - TZ_OFFSET[b]
    while end <= start:
        end += 1440
    return end - start


def header(ws, cols, widths):
    ws.append(cols)
    for i, w in enumerate(widths, 1):
        c = ws.cell(row=ws.max_row, column=i)
        c.font = Font(name=FONT, bold=True, color="FFFFFF", size=10)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="center")
        c.border = BOX
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = ws.cell(row=ws.max_row + 1, column=1)


def style_row(ws, r, ncols, fill=None):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=r, column=c)
        if cell.font != LINK:
            cell.font = BODY
        cell.alignment = WRAP
        cell.border = BOX
        if fill:
            cell.fill = fill


def title_block(ws, text, sub=None):
    ws.append([text])
    ws.cell(row=ws.max_row, column=1).font = Font(name=FONT, bold=True, size=14, color=SAFFRON)
    if sub:
        ws.append([sub])
        ws.cell(row=ws.max_row, column=1).font = Font(name=FONT, italic=True, size=9, color="595959")
    ws.append([])


def readme(wb):
    ws = wb.active
    ws.title = "Read me"
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 110
    title_block(ws, f"{D.YATRA['title']} – Minute-by-minute itinerary (DRAFT for fine-tuning)",
                "Hare Krishna! Everything here can be edited. Durations and daily km recalculate automatically.")
    rows = [
        ("Yatra", f"{D.YATRA['title']} {D.YATRA['subtitle']}"),
        ("Dates", D.YATRA["dates"] + ". Out: Hyderabad EK 525/EK 31 (LHR T3 16:10) and Bangalore EY 1013/EY 67 (LHR T4 18:45) on 17 Apr. Back: EY 82 Malpensa 11:40 on 2 May → Abu Dhabi → EY 352 Hyderabad 02:45 / EY 232 Bangalore 03:15 on 3 May."),
        ("Countries", ", ".join(D.YATRA["countries"])),
        ("Organised by", D.YATRA["organiser"]),
        ("Contact", D.YATRA["contact"]),
        ("Package price", D.YATRA["price"]),
        ("Mode of transport", "Private coach for every road movement. Exceptions are marked in the Mode column: Flight, Ferry (Dover–Calais), Boat, Cable car (Titlis), Train (Lucerne–Interlaken)."),
        ("Meals", "Breakfast: hotel (complimentary). Lunch: Indian restaurant or ISKCON temple prasadam near the sightseeing. Dinner: at the hotel (Satvik menu pre-agreed or an Indian caterer delivering). The 'Provided by' column names the provider for every meal."),
        ("Distances & times", "Coach estimates from route knowledge, NOT live Google Maps results. Click the 'Route' link on each movement to verify km and time, then overwrite the numbers. Coaches are slower than cars."),
        ("Time zones", "Times are local. UK = BST (IST − 4:30). Continent = CEST (IST − 3:30). Abu Dhabi = GST (IST − 1:30). Flight and ferry rows show local clock times; their Duration is the real elapsed time."),
        ("Ekadasi", "Kamada Ekadasi 17 Apr (travel day; break fast London 18 Apr 05:59–10:40). Varuthini Ekadasi 2 May (flight home; break fast in India 3 May before ~10:00)."),
        ("Status column", "Use the dropdown: Draft → To verify → Booked → Confirmed. Filter on it to see what is still open."),
        ("Sheets", "Budget · Day summary · Minute-by-minute · Meal plan · Places & maps · Entry tickets · Pros & cons · Challenges · Do's & don'ts · Visa documents · Inclusions · Practical info"),
        ("Source", "2024 posters (15N/16D, 8 countries), brochure PDF, inclusions/exclusions sheet, Schengen biometric guidelines, shortlisted 2027 flights, team budget sheet; prices and events checked 22 Oct 2026."),
    ]
    for k, v in rows:
        ws.append([k, v])
        ws.cell(row=ws.max_row, column=1).font = Font(name=FONT, bold=True, size=10)
        ws.cell(row=ws.max_row, column=2).font = Font(name=FONT, size=10)
        ws.cell(row=ws.max_row, column=2).alignment = WRAP


COLS = ["Day", "Date", "Time zone", "Start", "End", "Duration (min)", "Type", "From", "To / Place",
        "Mode", "Distance (km)", "Activities & details", "Meal provided by", "Google Maps",
        "Notes / to verify", "Status"]
WIDTHS = [5, 10, 9, 7, 7, 9, 14, 24, 30, 9, 9, 60, 30, 12, 34, 11]


def minute_sheet(wb):
    ws = wb.create_sheet("Minute-by-minute")
    header(ws, COLS, WIDTHS)
    dv = DataValidation(type="list", formula1='"Draft,To verify,Booked,Confirmed"', allow_blank=True)
    ws.add_data_validation(dv)
    first = ws.max_row + 1
    for d in D.DAYS:
        ws.append([d["day"], dt.date.fromisoformat(d["date"]), d["tz"], None, None, None,
                   f"DAY {d['day']} · {d['dow']}", "", d["title"], "", None,
                   f"Overnight: {d['overnight']}", "", "", "", ""])
        r = ws.max_row
        style_row(ws, r, len(COLS), DAYBAND)
        for c in range(1, len(COLS) + 1):
            ws.cell(row=r, column=c).font = Font(name=FONT, bold=True, size=10)
        ws.cell(row=r, column=2).number_format = "dd-mmm-yy"
        for row in d["rows"]:
            tz = row["tz"] or d["tz"]
            if "→" in tz and row["kind"] == "Transfer" and row["mode"] in ("Flight", "Ferry"):
                dur = real_minutes(dict(row, tz=tz))
            else:
                dur = None
            ws.append([
                d["day"], dt.date.fromisoformat(d["date"]), tz, tm(row["start"]), tm(row["end"]), None,
                row["mode"] + " transfer" if row["kind"] == "Transfer" else row["kind"],
                D.PLACES[row["frm"]][0] if row["frm"] else "",
                D.PLACES[row["to"]][0],
                row["mode"], row["km"] or None, row["detail"], row["meal_by"],
                "Route" if row["kind"] == "Transfer" else "Location",
                row["note"], "Draft",
            ])
            r = ws.max_row
            ws.cell(row=r, column=6).value = dur if dur is not None else f"=ROUND(MOD(E{r}-D{r},1)*1440,0)"
            ws.cell(row=r, column=2).number_format = "dd-mmm-yy"
            ws.cell(row=r, column=4).number_format = "hh:mm"
            ws.cell(row=r, column=5).number_format = "hh:mm"
            ws.cell(row=r, column=11).number_format = "#,##0"
            link = ws.cell(row=r, column=14)
            link.hyperlink = row["link"]
            link.font = LINK
            fill = MEAL if row["kind"] in ("Breakfast", "Lunch", "Dinner") else MOVE if row["kind"] == "Transfer" else None
            style_row(ws, r, len(COLS), fill)
            dv.add(ws.cell(row=r, column=16))
    last = ws.max_row
    ws.auto_filter.ref = f"A{first - 1}:P{last}"
    return first, last


def day_summary(wb, first, last):
    ws = wb.create_sheet("Day summary", 1)
    cols = ["Day", "Date", "Route", "Overnight", "Coach km", "Coach time incl. breaks (h:mm)",
            "Driver-hours check (EU: max 9 h/day)", "First start", "Last end", "Planned walks (km)"]
    header(ws, cols, [5, 10, 60, 22, 10, 12, 26, 10, 10, 10])
    m = "'Minute-by-minute'!"
    top = ws.max_row + 1
    for d in D.DAYS:
        ws.append([d["day"], dt.date.fromisoformat(d["date"]), d["title"], d["overnight"]])
        r = ws.max_row
        rng = lambda col: f"{m}${col}${first}:${col}${last}"  # noqa: E731
        ws.cell(row=r, column=5).value = f'=SUMIFS({rng("K")},{rng("A")},A{r},{rng("J")},"Coach")'
        ws.cell(row=r, column=6).value = f'=SUMIFS({rng("F")},{rng("A")},A{r},{rng("J")},"Coach")/1440'
        ws.cell(row=r, column=7).value = (f'=IF(F{r}*24>9,"OVER 9 h – revise",IF(F{r}*24>6,"Long day – 45 min break + rest stops",'
                                          f'IF(F{r}*24>4.5,"45 min break needed","OK")))')
        ws.cell(row=r, column=8).value = f'=_xlfn.MINIFS({rng("D")},{rng("A")},A{r})'
        ws.cell(row=r, column=9).value = f'=_xlfn.MAXIFS({rng("E")},{rng("A")},A{r})'
        ws.cell(row=r, column=10).value = f'=SUMIFS({rng("K")},{rng("A")},A{r},{rng("J")},"Walk")'
        ws.cell(row=r, column=10).number_format = "0.0"
        ws.cell(row=r, column=2).number_format = "dd-mmm-yy"
        ws.cell(row=r, column=5).number_format = "#,##0"
        ws.cell(row=r, column=6).number_format = "[h]:mm"
        ws.cell(row=r, column=8).number_format = "hh:mm"
        ws.cell(row=r, column=9).number_format = "hh:mm"
        style_row(ws, r, len(cols))
    bottom = ws.max_row
    ws.append(["", "", "TOTAL by coach", "", f"=SUM(E{top}:E{bottom})", f"=SUM(F{top}:F{bottom})"])
    r = ws.max_row
    ws.cell(row=r, column=5).number_format = "#,##0"
    ws.cell(row=r, column=6).number_format = "[h]:mm"
    style_row(ws, r, len(cols))
    for c in range(1, len(cols) + 1):
        ws.cell(row=r, column=c).font = Font(name=FONT, bold=True, size=10)
    ws.append([])
    ws.append(["", "", "Day 1 and Day 16 flights, the ferry, boats, cable cars and the train are excluded from coach km and hours. 'Planned walks' counts only the walking legs between points; add ~1–1.5 km for walking inside each attraction."])
    ws.cell(row=ws.max_row, column=3).font = Font(name=FONT, italic=True, size=9)


def meal_sheet(wb):
    ws = wb.create_sheet("Meal plan")
    cols = ["Day", "Date", "Meal", "Start", "End", "Where", "Provided by", "Notes", "Google Maps", "Booking status"]
    header(ws, cols, [5, 10, 10, 7, 7, 40, 45, 40, 12, 13])
    dv = DataValidation(type="list", formula1='"Not booked,Enquired,Booked,Confirmed"', allow_blank=True)
    ws.add_data_validation(dv)
    for d in D.DAYS:
        for row in d["rows"]:
            if row["kind"] not in ("Breakfast", "Lunch", "Dinner"):
                continue
            ws.append([d["day"], dt.date.fromisoformat(d["date"]), row["kind"], tm(row["start"]), tm(row["end"]),
                       D.PLACES[row["to"]][0], row["meal_by"], row["detail"] or row["note"], "Location",
                       "Not booked"])
            r = ws.max_row
            ws.cell(row=r, column=2).number_format = "dd-mmm-yy"
            ws.cell(row=r, column=4).number_format = "hh:mm"
            ws.cell(row=r, column=5).number_format = "hh:mm"
            ws.cell(row=r, column=9).hyperlink = D.maps_place(row["to"])
            ws.cell(row=r, column=9).font = LINK
            style_row(ws, r, len(cols), MEAL if row["kind"] == "Lunch" else None)
            dv.add(ws.cell(row=r, column=10))
    ws.append([])
    ws.append(["", "", "Rules", "", "", "Satvik: no onion, garlic, eggs, meat or fish; pure-veg kitchen where possible. Confirm in writing 2 weeks ahead, reconfirm 48 h ahead. Temple prasadam: inform the temple of numbers and arrival time; offer a donation."])
    ws.cell(row=ws.max_row, column=6).alignment = WRAP
    ws.cell(row=ws.max_row, column=6).font = BODY


def places_sheet(wb):
    ws = wb.create_sheet("Places & maps")
    header(ws, ["#", "Place", "City", "Country", "Google Maps search text", "Open in Google Maps"], [4, 50, 16, 16, 60, 14])
    for i, (k, (name, query, city, country)) in enumerate(D.PLACES.items(), 1):
        ws.append([i, name, city, country, query, "Open map"])
        r = ws.max_row
        ws.cell(row=r, column=6).hyperlink = D.maps_place(k)
        ws.cell(row=r, column=6).font = LINK
        style_row(ws, r, 6)


def tickets_sheet(wb):
    ws = wb.create_sheet("Entry tickets")
    title_block(ws, "Entry tickets – adult price per person (official 2026 rates)",
                f"Checked {D.FX_ASOF}. Edit a price or an exchange rate and the INR columns and totals update.")
    fx_row = {}
    for cur, rate in D.FX.items():
        ws.append([f"INR per 1 {cur}", rate])
        fx_row[cur] = ws.max_row
        ws.cell(row=ws.max_row, column=1).font = Font(name=FONT, bold=True, size=10)
        ws.cell(row=ws.max_row, column=2).font = Font(name=FONT, size=10, color="0000FF")
    ws.append([])
    cols = ["Day", "Place", "In plan?", "Currency", "Price (local)", "Price (INR)", "Notes", "Source"]
    header(ws, cols, [5, 44, 9, 9, 12, 12, 46, 14])
    ws.freeze_panes = None
    first = ws.max_row + 1
    for day, place, planned, cur, price, note, src in D.ENTRY_TICKETS:
        ws.append([day, place, "Yes" if planned else "Optional", cur, price, None, note, "Open" if src else ""])
        r = ws.max_row
        ws.cell(row=r, column=6).value = f'=IF(E{r}="","",E{r}*$B${fx_row[cur]})'
        ws.cell(row=r, column=5).number_format = "#,##0.00"
        ws.cell(row=r, column=6).number_format = "#,##0"
        if src:
            ws.cell(row=r, column=8).hyperlink = src
            ws.cell(row=r, column=8).font = LINK
        style_row(ws, r, len(cols))
        ws.cell(row=r, column=5).font = Font(name=FONT, size=9, color="0000FF")
    last = ws.max_row
    ws.append(["", "Total – tickets in the plan (per adult)", "", "", "", f'=SUMIFS(F{first}:F{last},C{first}:C{last},"Yes")'])
    ws.append(["", "Total – optional extras if all taken (per adult)", "", "", "", f'=SUMIFS(F{first}:F{last},C{first}:C{last},"Optional")'])
    for r in (ws.max_row - 1, ws.max_row):
        ws.cell(row=r, column=6).number_format = "#,##0"
        style_row(ws, r, len(cols))
        for c in (2, 6):
            ws.cell(row=r, column=c).font = Font(name=FONT, bold=True, size=10)
    planned_total_row = ws.max_row - 1
    ws.append([])
    ws.append(["", "Group costs (not per person): Zaanse Schans coach parking €35–55/day; Volendam coach parking €15–25; Louvre group fee €90 per 7–20; Dover–Calais ferry by quote; Venice access fee – overnight guests in Mestre exempt but must register."])
    ws.cell(row=ws.max_row, column=2).font = Font(name=FONT, italic=True, size=9)
    return fx_row, planned_total_row


def budget_sheet(wb, fx_row, tickets_total_row):
    ws = wb.create_sheet("Budget", 1)
    title_block(ws, "Budget per yatri – cost against the ₹5,00,000 price",
                "Blue cells are inputs. Group costs are divided by the number of yatris. GST (5%) and TCS (5%) are collected on top of the price and passed on, so they are not costs here.")
    inp = {}
    for label, val, fmt in (("Yatris (paying)", D.DEFAULT_PAX, "0"), ("Package price per person (₹)", D.PRICE_PP, "#,##0"),
                            ("Contingency (% of costs)", D.CONTINGENCY_PCT, "0%")):
        ws.append([label, val])
        r = ws.max_row
        inp[label] = f"$B${r}"
        ws.cell(row=r, column=1).font = Font(name=FONT, bold=True, size=10)
        ws.cell(row=r, column=2).font = Font(name=FONT, size=10, color="0000FF")
        ws.cell(row=r, column=2).number_format = fmt
    fx = {"INR": None}
    for cur in D.FX:
        ws.append([f"INR per 1 {cur}", f"='Entry tickets'!B{fx_row[cur]}"])
        fx[cur] = f"$B${ws.max_row}"
        ws.cell(row=ws.max_row, column=1).font = Font(name=FONT, size=10)
        ws.cell(row=ws.max_row, column=2).font = Font(name=FONT, size=10, color="008000")
    pax, price, cont = inp["Yatris (paying)"], inp["Package price per person (₹)"], inp["Contingency (% of costs)"]
    ws.append([])

    # hotel table
    ws.append(["Hotels (twin share)", "Nights", "Room rate / night", "Currency", "Per person (₹)"])
    for c in range(1, 6):
        ws.cell(row=ws.max_row, column=c).font = Font(name=FONT, bold=True, color="FFFFFF", size=10)
        ws.cell(row=ws.max_row, column=c).fill = HEAD
    h_first = ws.max_row + 1
    for city, n, rate, cur in D.HOTELS:
        ws.append([city, n, rate, cur])
        r = ws.max_row
        ws.cell(row=r, column=5).value = f"=B{r}*C{r}*{fx[cur]}/2"
        ws.cell(row=r, column=3).font = Font(name=FONT, size=9, color="0000FF")
        ws.cell(row=r, column=5).number_format = "#,##0"
        style_row(ws, r, 5)
        ws.cell(row=r, column=3).font = Font(name=FONT, size=9, color="0000FF")
    h_last = ws.max_row
    ws.append(["Total hotels", f"=SUM(B{h_first}:B{h_last})", "", "", f"=SUM(E{h_first}:E{h_last})"])
    hotel_total = f"E{ws.max_row}"
    style_row(ws, ws.max_row, 5)
    ws.append([])

    cols = ["Cost line", "Basis", "Amount", "Currency", "₹ per person", "Team sheet ₹", "Difference ₹", "Group total ₹", "Note"]
    ws.append(cols)
    for i, w in enumerate([52, 8, 12, 9, 13, 13, 13, 14, 50], 1):
        c = ws.cell(row=ws.max_row, column=i)
        c.font = Font(name=FONT, bold=True, color="FFFFFF", size=10)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True)
        ws.column_dimensions[get_column_letter(i)].width = w
    b_first = ws.max_row + 1
    for line, basis, amt, cur, team_key, note in D.BUDGET:
        ws.append([line, basis, amt, cur, None, D.TEAM_SHEET.get(team_key) if team_key else None, None, None, note])
        r = ws.max_row
        rate = fx[cur] if cur != "INR" else "1"
        if basis == "pp":
            ws.cell(row=r, column=5).value = f"=C{r}*{rate}"
        elif basis == "group":
            ws.cell(row=r, column=5).value = f"=C{r}*{rate}/{pax}"
        elif basis == "hotels":
            ws.cell(row=r, column=5).value = f"={hotel_total}"
        elif basis == "tickets":
            ws.cell(row=r, column=5).value = f"='Entry tickets'!F{tickets_total_row}"
        ws.cell(row=r, column=7).value = f'=IF(F{r}="","",E{r}-F{r})'
        ws.cell(row=r, column=8).value = f"=E{r}*{pax}"
        for c in (3, 5, 6, 7, 8):
            ws.cell(row=r, column=c).number_format = "#,##0"
        style_row(ws, r, len(cols))
        if amt is not None:
            ws.cell(row=r, column=3).font = Font(name=FONT, size=9, color="0000FF")
    b_last = ws.max_row
    rows_out = {}
    for label, f_pp, f_team in (
        ("Subtotal", f"=SUM(E{b_first}:E{b_last})", f"=SUM(F{b_first}:F{b_last})"),
        ("Contingency", f"=E{b_last + 1}*{cont}", ""),
        ("TOTAL COST per yatri", f"=E{b_last + 1}+E{b_last + 2}", f"=F{b_last + 1}"),
        ("Package price per yatri", f"={price}", f"={price}"),
        ("SURPLUS / (SHORTFALL) per yatri", f"=E{b_last + 4}-E{b_last + 3}", f"=F{b_last + 4}-F{b_last + 3}"),
        ("Margin % of price", f"=E{b_last + 5}/E{b_last + 4}", f"=F{b_last + 5}/F{b_last + 4}"),
        ("Price needed for a 5% margin", f"=E{b_last + 3}/0.95", ""),
    ):
        ws.append([label, "", "", "", f_pp, f_team or None, None, None, ""])
        r = ws.max_row
        rows_out[label] = r
        if label not in ("Margin % of price", "Price needed for a 5% margin", "Package price per yatri"):
            ws.cell(row=r, column=8).value = f"=E{r}*{pax}"
        fmt = "0.0%" if label.startswith("Margin") else "#,##0;(#,##0)"
        for c in (5, 6, 8):
            ws.cell(row=r, column=c).number_format = fmt
        style_row(ws, r, len(cols))
        for c in (1, 5, 6, 8):
            ws.cell(row=r, column=c).font = Font(name=FONT, bold=True, size=10)
    ws.append([])
    # sensitivity on group size
    ws.append(["Group size sensitivity", "Yatris", "", "", "Cost per yatri", "Surplus per yatri", "", "Group surplus"])
    for c in range(1, 9):
        ws.cell(row=ws.max_row, column=c).font = Font(name=FONT, bold=True, color="FFFFFF", size=10)
        ws.cell(row=ws.max_row, column=c).fill = HEAD
    pp_part = f'SUMIFS(E{b_first}:E{b_last},B{b_first}:B{b_last},"<>group")'
    grp_total = f'SUMIFS(H{b_first}:H{b_last},B{b_first}:B{b_last},"group")'
    for n in (30, 35, 40, 45, 49):
        ws.append(["", n])
        r = ws.max_row
        ws.cell(row=r, column=5).value = f"=({pp_part}+{grp_total}/B{r})*(1+{cont})"
        ws.cell(row=r, column=6).value = f"={price}-E{r}"
        ws.cell(row=r, column=8).value = f"=F{r}*B{r}"
        for c in (5, 6, 8):
            ws.cell(row=r, column=c).number_format = "#,##0;(#,##0)"
        style_row(ws, r, 8)
    ws.column_dimensions["A"].width = 52


def simple_sheet(wb, name, cols, widths, rows, title=None):
    ws = wb.create_sheet(name)
    if title:
        title_block(ws, title)
    header(ws, cols, widths)
    for row in rows:
        ws.append(list(row))
        style_row(ws, ws.max_row, len(cols))
    return ws


def main():
    wb = Workbook()
    readme(wb)
    first, last = minute_sheet(wb)
    day_summary(wb, first, last)
    meal_sheet(wb)
    places_sheet(wb)
    fx_row, tickets_total_row = tickets_sheet(wb)
    budget_sheet(wb, fx_row, tickets_total_row)
    simple_sheet(wb, "Pros & cons", ["Day", "Pros", "Cons / watch-outs"], [5, 70, 70], D.PROS_CONS)
    simple_sheet(wb, "Challenges", ["Challenge", "What happens", "Mitigation"], [28, 60, 70], D.CHALLENGES)
    n = max(len(D.DOS), len(D.DONTS))
    simple_sheet(wb, "Do's & don'ts", ["Do", "Don't"], [70, 70],
                 [(D.DOS[i] if i < len(D.DOS) else "", D.DONTS[i] if i < len(D.DONTS) else "") for i in range(n)])
    simple_sheet(wb, "Visa documents", ["Document", "Requirement", "Ready? (Y/N)"], [28, 100, 12], [(a, b, "") for a, b in D.VISA_DOCS],
                 title="Schengen biometrics – documents to carry (keep a scan of each for the UK visa)")
    m = max(len(D.INCLUSIONS), len(D.EXCLUSIONS))
    simple_sheet(wb, "Inclusions", ["Inclusions", "Exclusions"], [60, 70],
                 [(D.INCLUSIONS[i] if i < len(D.INCLUSIONS) else "", D.EXCLUSIONS[i] if i < len(D.EXCLUSIONS) else "") for i in range(m)])
    simple_sheet(wb, "Practical info", ["Topic", "Details"], [22, 120], D.PRACTICAL)
    for ws in wb.worksheets:
        ws.sheet_view.zoomScale = 100
        ws.page_setup.orientation = "landscape"
        ws.page_setup.fitToWidth = 1
    wb.save(OUT)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
