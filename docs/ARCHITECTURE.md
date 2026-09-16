# Architecture

## The shape of the problem

The Yatra Department already has the knowledge. It is spread across 22
spreadsheet tabs, a 6,000-paragraph Word document of itineraries, and an
Evernote export of meeting notes. The problem is not capture, it is **retrieval
on a phone, by the right person, at the moment it matters** — a coordinator
checking whether October is safe for Kailash while standing in a temple
corridor, or a finance lead asking which yatra actually repeats profitably.

Two facts drive every decision below:

1. **Staff and yatris share one app.** Negotiated rates, margins and HNI
   contacts sit in the same database as the itineraries yatris read. The
   separation has to be enforced by the database, not by hiding buttons.
2. **Content volume is lopsided.** ~2,250 places and ~1,000 calendar days
   against ~124 yatras. Browsing needs filters and pagination; yatras can be
   listed whole.

## Stack and why

| Choice | Reason |
| --- | --- |
| Vite + React + TS + Tailwind | Lovable's native stack, so the repo round-trips through Lovable's editor without a translation layer |
| Supabase | Postgres with RLS is the only part of the stack that can enforce the staff/yatri split at the data layer. Auth and Storage come with it |
| TanStack Query | Caching and request dedup for free; `staleTime: 60s` matters on hotel wifi |
| React Router + `React.lazy` | Every screen is its own chunk — first load is ~143 kB gzipped instead of 153 kB monolithic, and staff screens never ship to a yatri's phone |
| vite-plugin-pwa | Installable home-screen app, precached shell |

## Layers

```
src/
  lib/          supabase client, formatting, design tokens
  types/db.ts   hand-written domain types mirroring the schema
  data/         every Supabase query in the app — the only place `supabase` is imported
  hooks/        useAuth (session + role), useTheme, useDebounced
  components/   ui/ primitives, app/ domain components
  pages/        one file per screen
  routes/       route table, auth and role guards
```

**All database access lives in `src/data/`.** Pages never call `supabase`
directly. This is what makes `scripts/check_queries.py` possible: it parses that
one directory and checks every table, column and RPC against a real database, so
a typo that PostgREST would only reveal at runtime fails the build instead.

## Data model

Seven clusters:

**Identity** — `profiles` (1:1 with `auth.users`, carries `role`). Three
`SECURITY DEFINER` helpers (`auth_role`, `is_staff`, `is_admin`) let policies
read the caller's role without recursing into `profiles`' own policies. A
trigger creates the profile on signup and makes the first-ever user `admin`.

**Places** — `destinations` (Jyotirlingas, Shakti Peethas, Divya Desams, rivers,
UNESCO sites and plain temples, distinguished by a `place_kind[]` array so one
row can be several things at once — Srisailam is both a Jyotirlinga and a Shakti
Peetha) and `pastimes` hanging off them.

**Yatras** — `yatras`, `yatra_destinations`, `travel_windows` (best / shoulder /
avoid months), `yatra_notes` (pros and cons as rows, not prose).

**Itineraries** — `itineraries` versioned per yatra with `itinerary_days`
beneath. Versioning matters because an itinerary is edited season after season
and last year's needs to stay readable.

**Departures and money** — `yatra_batches` (dates, seats) is public-tier;
`batch_pricing` and `batch_economics` are staff-tier. Splitting money out of the
batch row is what lets a yatri see "2–5 Oct, 4 seats left" without seeing the
margin on it.

**Vendors** — `vendors` and `vendor_rates`, entirely staff-tier.

**Library** — `calendar_events` + `panchanga` (separate, because a tithi is not
an event and folding them together turns every day into a fake festival),
`videos`, `knowledge_articles` with a per-row `visibility` flag, and
`finance_reports` pointing at a private Storage bucket.

## Security model

Two tiers, deliberately blunt so they can be audited at a glance:

- **Public tier** — readable by any signed-in user: destinations, pastimes,
  yatras, itineraries, batches, travel windows, notes, calendar, panchanga,
  videos, public articles.
- **Staff tier** — `is_staff()` only: vendors, vendor rates, pricing, economics,
  finance reports, staff articles.

Writes are staff-or-admin on everything. Role changes are admin-only, and the
`profiles` update policy explicitly forbids a user changing their own role.

Grants are broad and RLS is the gate — Supabase's model — but stated explicitly
in the migration rather than inherited, so the schema behaves identically on the
plain Postgres used for testing, and a table added later without a policy fails
closed.

Views use `security_invoker = true` so they inherit their base tables' policies;
`search_all()` is `SECURITY INVOKER` for the same reason, which is why a yatri
searching "Himalayan Heli" gets nothing.

### What proves it

`scripts/rls_test.sql` creates three users, one per role, and asserts twelve
properties. All twelve pass:

```
pass  yatri sees no vendors
pass  yatri sees no negotiated rates
pass  yatri sees no pricing
pass  yatri sees no margins
pass  yatri sees no finance reports
pass  yatri sees no staff-only articles
pass  yatri reads yatras, itineraries and calendar
pass  yatri cannot insert a yatra
pass  yatri cannot self-promote
pass  staff reads vendors, rates, pricing and economics
pass  staff can write content
pass  search leaks no vendor to a yatri
```

## The import pipeline

`scripts/import_content.py` is a one-way ETL, not a sync. It:

- reads the state-banner structure of the temple sheet (a row with one filled
  cell is a state heading, not data);
- merges the holy-places master into the same `destinations` rows by slug, so
  Srisailam accumulates `['temple', 'jyotirlinga']` rather than duplicating;
- parses `"May, June, Spetember"` and `"Nov to Feb"` into month arrays, typos
  included — the source spells February three different ways;
- walks the itinerary document's `Heading 1` / `Day N` structure into
  `itineraries` + `itinerary_days`, keeping the longest version when a yatra
  appears twice;
- classifies scope, nature and difficulty from the title (Kailash is a 5);
- matches the Dashboard's destination names ("Kailash - Land Route") to package
  names ("KAILASA MANASA SAROVAR YATRA") on shared token stems, and **prints
  what it could not match** rather than silently dropping it.

The generated SQL is **not committed** — it is a build artifact, and it carries
personal contact details from the meeting notes that should live behind RLS
rather than in a repository history. See `supabase/seed/README.md`.

Current yield, verified by applying it to a real Postgres:

```
yatras=124  destinations=2257  itineraries=53  itinerary_days=322
batches=97  pricing=187  economics=49  windows=19
panchanga=985  events=842  articles=6  videos=4
```

## Decisions worth knowing

**Avoid beats best.** The Char Dham rows list the same months under "Best
Season" and "Dates to Avoid". `SeasonStrip` resolves the contradiction toward
caution: a month marked avoid renders red even if it is also marked best.
Better to warn wrongly than to invite wrongly onto a Himalayan road.

**Panchanga is its own table.** Folding tithi and nakshatra into
`calendar_events` would have made all 985 days "events" and rendered a calendar
where nothing stands out.

**Month filtering is two queries, not a join.** PostgREST cannot express "array
contains" across a join in one request. Two small requests intersected in
`Yatras.tsx` beat a database view nobody on the team can read or change.

**Error messages are unwrapped.** Supabase rejects with a plain object, not an
`Error`. `errorMessage()` handles both, so staff see
"column x does not exist" instead of "Something went wrong."

**Offline is deferred, not designed out.** v1 is online-only as specified. The
service worker already runs network-first over `/rest/v1/` with a 24-hour cache,
and all reads go through `src/data/`. Making the app work at Kailash means
adding a local store behind that one directory — not restructuring the app.
