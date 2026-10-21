# London Europe Yatra – minute-by-minute itinerary

15 nights / 16 days, 8 countries, by private coach. Drafted from the 2024
posters, brochure, inclusions sheet and Schengen biometric guidelines.

| File | What it is |
| --- | --- |
| `London_Europe_Yatra_Minute_Itinerary.xlsx` | The working sheet: every movement with start/end, km, Google Maps link, meal provider, status dropdown. Durations and daily coach km are formulas. |
| `itinerary_data.py` | Single source of the plan (places, days, rows, do's/don'ts, risks). |
| `build_workbook.py` | Regenerates the .xlsx from the data. |
| `doc_markdown.py` | Renders the living document's tables from the same data. |

```bash
pip install openpyxl
python3 itineraries/london-europe-yatra/build_workbook.py
```

Distances and drive times are coach estimates, not live Google Maps results.
Verify each with its Route link before finalising.
