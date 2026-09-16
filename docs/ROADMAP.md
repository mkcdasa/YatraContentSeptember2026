# Roadmap

## The fourteen requested features

| # | Feature | Status | Where |
| --- | --- | --- | --- |
| 1 | All itineraries | **Shipped** | 53 itineraries, 322 days — Yatra → Itinerary |
| 2 | Pros and cons | **Shipped** | `yatra_notes`, staff-editable — Yatra → Pros & cons |
| 3 | Calendar | **Shipped** | 985 panchanga days, 842 events — Calendar tab |
| 4 | Repeat trips 8×/year | **Shipped** | `repeatable_per_year` + batches-this-year — Profitability |
| 5 | More profitable | **Shipped** | Margin ranking — Profitability |
| 6 | Perfect weather | **Shipped** | Season strip, green months |
| 7 | Avoid extreme weather | **Shipped** | Season strip, red months + caution card |
| 8 | Special events | **Shipped** | Festival events on the calendar |
| 9 | Vendor contacts & negotiated pricing | **Shipped (schema + UI)** | Vendors tab — needs data entry |
| 10 | Pastimes | **Shipped (schema + UI)** | Temple pages — needs content |
| 11 | Finance team reports | **Shipped (schema + UI)** | Profitability → reports, private bucket |
| 12 | Visa related | **Partial** | `visa_required` / `visa_notes` flags; no per-country guide yet |
| 13 | Seasonal | **Shipped** | `nature` classification + travel windows |
| 14 | YouTube videos from experts | **Shipped (4 links imported)** | Video library — needs curation |

## What "needs data" means

Nine of the fourteen are complete end to end from the imported content. Three
have working schema and UI but thin data, because the source files carried
little of it:

- **Vendors** — the Evernote notes name vendors (Himalayan, Heli Yatra, Veena
  World, RCS, Rao Travels, Jet Wing, Well Nepal) but hold no phone numbers or
  rates. That is an afternoon of data entry, not development.
- **Pastimes** — the temple sheet has sevas and specialities, not narrations.
- **Videos** — four YouTube links were found in the notes. The "industry
  experts" library needs curating.

## Phase 2

**Offline (the big one).** You chose online-only. Your own itineraries go to
Kailash, Amarnath and Ahobilam, where there is no signal. The groundwork is
laid: all reads go through `src/data/`, and the service worker already caches
REST responses network-first. Adding a "download this yatra pack before you
leave" button — itinerary, hotel contacts, packing list, SOS protocol, cached
for the trip — is the highest-value next thing anyone could build here.

**Admin editing UI.** Staff can currently add pros/cons and change roles in-app.
Editing itineraries, vendors and rates still means the Supabase table editor.
Forms for `yatras`, `itinerary_days`, `vendors` and `vendor_rates` would close
the loop and retire the spreadsheets.

**Telugu.** You chose English for v1. Schema-wise this is additive: a
`translations` table keyed on (table, row id, column, lang), or `_te` columns on
the handful of user-facing text fields. Doing it before the team enters a lot of
content is much cheaper than after.

**Route mapping.** `yatra_destinations` exists and is empty. Linking each yatra
to its stops would give a map view and "which yatras visit Tirupati".

## Phase 3

- **Enquiry capture** — a yatri taps "interested", staff get a lead. The natural
  bridge to the booking flow you deferred.
- **SOS protocol per yatra** — the notes call for it explicitly; currently a
  generic article.
- **Tour-leader mode** — attendance, incidents and expenses recorded on the
  road. Needs offline writes, so it follows Phase 2.
- **Pushkaram and Kumbh planning** — these repeat on 12-year cycles and deserve
  their own long-range view.
