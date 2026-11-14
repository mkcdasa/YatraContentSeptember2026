# Package spec (`package.py`)

One work folder per yatra departure:

```
<workdir>/
  package.py         PKG = dict(...)            (this file's fields)
  rows.json          minute-by-minute schedule  (see "rows.json")
  restaurants.json   optional, meal-plan restaurants for the yatri itinerary
  imgmap.json        {key: {"src": "img/<file>", "credit": "...", "cap": "..."}}
  img/               the photos named in imgmap.json
  i18n/<lang>.json   optional translations: {english string: translated string}
```

Build: `bash <skill>/engine/build.sh <workdir> [te hi kn ta]` → `<workdir>/out/`.
Brand images `prabhupada`, `moments1`, `moments2`, `joined` are always available as image keys.
The worked example is `examples/vaishno-devi-helicopter-4d/package.py`.

## Identity and dates

| Field | Req | Example | Used on |
|---|---|---|---|
| `key` | yes | `"vd4"` | internal id |
| `slug` | yes | `"Vaishno-Devi-Helicopter-Yatra-4D-13-16-March-2027"` | output file names |
| `title` / `title2` | yes | `"Vaishno Devi"` / `"Helicopter Yatra"` | big title, script subtitle (cover, poster, itinerary, footers) |
| `tagline` | yes | `"Jammu · Katra · Vaishno Devi · Katra · Jammu"` | route line under the dates |
| `dates` | yes | `"13 – 16 March 2027"` | cover, poster, itinerary |
| `dates_long` | yes | `"Saturday 13 – Tuesday 16 March 2027"` | price box |
| `start_date` | rec. | `"2027-03-13"` | per-day dates on day pages; omit for undated templates |
| `duration` | yes | `"3 Nights / 4 Days"` | cover, poster |
| `nights`, `days` | yes | `3`, `4` | stats |
| `km`, `temples` | opt | `136`, `6` | default stats |

## Price, registration, call to action

| Field | Req | Default / example |
|---|---|---|
| `price` | yes | `"₹50,000"` |
| `gst_note` | opt | `"+ 5% GST"` |
| `price_note` | opt | `"per person · all-inclusive · excluding flight charges"` |
| `reg_close` | opt | `"25 December 2026"` (price box: "Registrations close …") |
| `reg_short` | opt | `"25 Dec 2026"` (poster badge; defaults to `reg_close`) |
| `cover_note` | opt | defaults to `"Registrations close <reg_close>"`; e.g. `"… · limited helicopter seats"` |
| `seats_note` | opt | `"Limited seats."`, e.g. `"Limited seats (helicopter quota)."` |
| `flights` | opt | list of lines for the "Flight info · please book accordingly" card; `[]` hides it |
| `flights_title` | opt | card heading |

The phone number, websites, email, address, social line and "Book Now →" come from `engine/brand.py`. Never put them in a package.

## Cover and poster

| Field | Req | Notes |
|---|---|---|
| `kicker` | yes | pill above the title, e.g. `"Helicopter Yatra · Aarti at the Holy Cave"` |
| `show_heli_icon` | opt | `True` puts the helicopter icon in the kicker (helicopter yatras only) |
| `hero`, `hero_pos` | yes | cover background image key, CSS object-position |
| `cover_circles` | yes | 3 × `(img_key, "left:12mm;top:146mm")`; use left 12/83/154 mm, top 146/156/146 mm |
| `cover_feats` | yes | 4–6 short chips under the dates |
| `poster` | opt | `dict(hero, pos, circ=[3 keys], kicker, hl=[exactly 8 short highlights], price_small, reg)`; defaults derive from the cover |

## Brochure pages

| Field | Req | Notes |
|---|---|---|
| `greeting` | opt | welcome-page subtitle, default `"Hare Krishna!"` (e.g. `"Hare Krishna! Jai Mata Di!"`) |
| `intro` | yes | 3–4 sentence welcome paragraph |
| `highlights` | yes | 6–9 items (≤9 keeps one column; up to 14 switches to two columns) |
| `stays` | yes | `[("Jammu","2 Nights"),("Bhawan","1 Night")]` |
| `best` | yes | "Your departure" card text (weather/season for these dates) |
| `stats` | opt | `[(value,label),…]` journey-page tiles; default days, nights, km, temples; add `(2,"Helicopter rides")` etc. |
| `stops` | yes | journey route: `(place, subtitle, mode_to_next, distance_to_next)`; last stop has `""` mode |
| `journey_photos` | yes | 3 × `(img_key, caption)` |
| `daypages` | yes | one per day: `dict(n, title, stay or None, imgs=[2 keys], story, sig=(heading, text))` |
| `places` | yes | 6 (or 9) × `(img_key, name, one-line)` for the "Sacred places" grid |
| `incl`, `excl` | yes | inclusion / exclusion bullets (≤10 each) |
| `meal_note`, `meal_subtitle` | opt | used when there are more than 12 meals (separate meal page) |
| `why` | opt | full override of the 7 "How we are different" items (brand default otherwise) |
| `extra_terms` | opt | `[(title,text)]` inserted after "Rescheduling" (e.g. helicopter, baggage rules) |
| `faq_common` | opt | override the generic FAQs (brand default: ID, food) |
| `faq` | opt | yatra-specific FAQs appended after `faq_common` (2–4 keeps the page tidy) |
| `pack`, `dos`, `donts` | yes / opt | ≤7 items each; dos/donts default to brand lists |
| `back` | yes | back-cover background image key |
| `closing` | opt | back-cover script line and the "Departure · …" day badge, e.g. `"Jai Mata Di!"` |
| `timing_note` | opt | footnote under each day table |
| `rows` | opt | schedule file name, default `rows.json` |

## Yatri itinerary (no timings)

```python
itinerary=dict(
  hero="bhawan", kicker="Helicopter Yatra · Aarti at the Holy Cave",
  special=[("Helicopter yatra","…"),("Aarti at the Holy Cave","…")],  # shown BEFORE the 4 brand boxes
  days=[dict(title="Arrival in Jammu", stay="Jammu",                  # stay None on the last day
             places=[("Raghunath Temple","Raghunath Temple, Jammu","Darshan of Sri Rama, Sita and Lakshmana")],
             acts=["Get-to-know-each-other session","Evening kirtan and bhajans"])],
  footer_closing="Jai Mata Di!",   # optional, defaults to closing
  memo="…", meal_note="…")         # optional
```
`places` tuples are (shown name, Google Maps search text or full URL, what we do there). Every place gets a "Map ↗" link.
`special` should have an even count with the brand's 4, so 2 or 4 items.
If `days` is empty, no itinerary PDF is built.

## rows.json

A JSON list of rows: `[day, "HH:MM", "HH:MM", mode, from, to, km, activity, maps_url]`.
- `mode` drives the colour tag: `Car`, `Walk`, `Helicopter`, `Flight`, `Ropeway`, `Gondola`, `Shikara`, `Darshan`, `Aarti`, `Breakfast`, `Lunch`, `Dinner`, `Halt`, `Rest`, `Shopping`, `Sightseeing`, etc.
- `to` is `"—"` for stays at one place. `km` is road km for this leg (0 otherwise).
- Meals: `from` is the place name. It is the key into restaurants.json.
- Write it with `engine/new_rows.py` (`m()`, `d()`, `save()` also prints km per day and continuity checks).

## restaurants.json (optional)

```json
{"Pooja Vaishno Dhaba, Katra": [
   {"name": "Pooja Vaishno Dhaba", "note": "Pure veg, Main Bazar on Banganga Road", "map": "https://www.google.com/maps/search/?api=1&query=…"},
   {"name": "Madhuban Saattvik Restaurant", "note": "Backup · pure veg, no onion-garlic", "map": "…"}]}
```
Keys match a meal row's `from`. Meals without a key show the row's own place and map link.

## Translations

`build.sh` always writes `i18n/en.json`, a list of every visible English string. For each language, create
`i18n/<lang>.json` = `{english: translation}` covering every entry (te Telugu, hi Hindi, kn Kannada, ta Tamil).
Keep phone, websites, `Punya Kshetras`, `ISKCON`, `GST`, numbers, times and photo credits in English. Then
re-run `build.sh <workdir> te hi kn ta`. Missing strings are listed in `i18n/missing_<lang>.json`, and those pages show English for them.
Letter-spacing is removed and pages and posters auto-shrink to fit longer scripts.
