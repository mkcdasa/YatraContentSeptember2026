# Seed data

The `.sql` files in this directory are **generated, not committed**.

They are produced from the department's own workbooks and Word documents by
`scripts/import_content.py`, and they are deliberately git-ignored for two
reasons:

1. They are a build artifact. The source of truth is `source-content/` (also
   git-ignored) plus the importer.
2. They carry personal contact details — named devotees, doctors and donors —
   lifted from the meeting notes. Those belong in the database behind RLS, not
   in a repository history that is hard to redact after the fact.

## Regenerating

```bash
pip install openpyxl python-docx
mkdir -p source-content          # drop the original .xlsx / .docx files here
python3 scripts/import_content.py --src source-content --out supabase/seed
```

You get numbered files. **Load them in filename order** — batches resolve their
yatra by slug, so `02_yatras.sql` has to land before `03_batches.sql`:

```bash
for f in supabase/seed/*.sql; do psql "$SUPABASE_DB_URL" -f "$f"; done
```

Every statement is `ON CONFLICT DO UPDATE` or guarded by `NOT EXISTS`, keyed on
slugs, so re-running is safe after the team has started editing in the app.

Expected yield from the September 2026 source files:

| File | Rows |
| --- | --- |
| `01_destinations_a…d.sql` | 2,257 temples, Jyotirlingas, Shakti Peethas, Divya Desams, rivers, UNESCO sites |
| `02_yatras.sql` | 73 yatras from the budget sheets (a further 51 come from itinerary headings) |
| `03_batches.sql` | 118 departures |
| `04_pricing.sql` | 212 price rows, general and premium |
| `05_economics.sql` | 111 costings |
| `06_travel_windows.sql` | 19 best/shoulder/avoid month sets |
| `07_panchanga.sql` | 985 days |
| `08_calendar_events.sql` | 842 festivals and occasions |
| `09_itineraries.sql` | 53 itineraries, 345 days |
| `10_articles.sql` | 6 handbooks |
| `11_videos.sql` | 4 videos |

The importer prints anything it could not match rather than dropping it
silently — currently two travel windows ("Char Dham Helicopter", "USA") that
have no corresponding yatra.
