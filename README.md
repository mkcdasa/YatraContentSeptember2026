# Yatra Knowledge Base

A mobile-first PWA for the Yatra Department of Hare Krishna Golden Temple,
Hyderabad. One place for itineraries, the yatra calendar, temple reference data,
vendor contacts with negotiated rates, and per-yatra economics.

Built to be used by ~100 people across the country — coordinators, tour leaders,
the finance team and yatris — on the phones they already carry.

- **Stack**: React 18 · TypeScript · Vite · Tailwind · React Router · TanStack
  Query · Supabase (Postgres + Auth + Storage) · vite-plugin-pwa
- **Deploys to**: Lovable (which syncs this repository's `main` branch)

## Quick start

```bash
npm install
cp .env.example .env.local        # fill in your Supabase URL and anon key
npm run dev
```

## Setting up the database

```bash
# 1. Apply the schema to your Supabase project
supabase link --project-ref <your-ref>
supabase db push

# 2. Generate and load the content extracted from the department's workbooks.
#    Seed files are generated, not committed — see supabase/seed/README.md.
python3 scripts/import_content.py --src source-content --out supabase/seed
for f in supabase/seed/*.sql; do psql "$SUPABASE_DB_URL" -f "$f"; done
```

Migrations live in `supabase/migrations/` and run in filename order:

| File | What it does |
| --- | --- |
| `…000100_schema.sql` | Tables, enums, triggers, the `profiles` role model |
| `…000200_rls.sql` | Row Level Security policies, grants, storage buckets |
| `…000300_views.sql` | Read models (`v_upcoming_departures`, …) and `search_all` |

## Re-importing content

The department's source of truth was 22 spreadsheet tabs and two Word documents.
`scripts/import_content.py` parses them into idempotent SQL:

```bash
pip install openpyxl python-docx
mkdir -p source-content            # git-ignored; put the originals here
python3 scripts/import_content.py --src source-content --out supabase/seed
```

Re-running is safe: every statement is `ON CONFLICT DO UPDATE` or guarded by
`NOT EXISTS`, keyed on slugs. After the team starts editing inside the app, the
importer is only for backfilling new source material.

## Validation

Nothing here needs a Supabase connection — it all runs against a throwaway
Postgres.

```bash
npm run typecheck                  # TypeScript across the app
npm run build                      # production bundle + service worker
./scripts/validate_db.sh --rls     # apply migrations + seed, then run RLS tests
python3 scripts/check_queries.py   # every table/column/RPC used by src/data exists
```

`scripts/rls_test.sql` is the important one. It asserts that a yatri cannot read
vendors, negotiated rates, pricing, margins or finance reports, cannot write
content, cannot promote themselves, and cannot surface a vendor through search —
while staff can do all of it. Run it after any policy change.

## Who sees what

| | Yatri | Tour leader / Staff | Admin |
| --- | :-: | :-: | :-: |
| Itineraries, calendar, temples, handbooks, videos | ✓ | ✓ | ✓ |
| Departure dates and seats | ✓ | ✓ | ✓ |
| Package pricing | | ✓ | ✓ |
| Vendors and negotiated rates | | ✓ | ✓ |
| Margins, surplus, finance reports | | ✓ | ✓ |
| Edit content | | ✓ | ✓ |
| Change roles | | | ✓ |

Enforced by Postgres RLS, not by the UI. The React `StaffOnly` component only
keeps empty panels from rendering.

The first account to sign up becomes `admin`; everyone after that starts as
`yatri` and is promoted from **More → People & roles**.

## Documentation

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — data model, security model, decisions
- [`docs/UX-RESEARCH.md`](docs/UX-RESEARCH.md) — competitive research and what it changed
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — the 14 requested features, phased
