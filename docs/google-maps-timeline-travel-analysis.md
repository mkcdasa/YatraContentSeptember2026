# Analysing 15 Years of Google Maps Timeline for Travel Insights and Planning

*Research notes, October 2026*

## 1. What changed, and why it matters first

Google moved Timeline (formerly "Location History") from its servers to your phone during 2024–2025:

- **The web Timeline is gone.** You can't view it at timeline.google.com or maps.google.com anymore. It now lives only in the Google Maps app on the phone(s) that recorded it.
- **Google Takeout no longer includes your Timeline.** If your Takeout archive has no `Records.json` or `Semantic Location History` folder, Takeout won't work for this.
- **Old data survived only if you moved it to a device before your deadline.** The deadlines were between late 2024 and mid-2025. Data you didn't move was deleted. In 2025 Google also accidentally deleted some users' Timelines; those users could recover only if encrypted backup was turned on.
- **Auto-delete may be trimming your history right now.** Timeline lets you delete data older than 3, 18 or 36 months. Check that it says *"Don't auto-delete activity"*. Google also requires auto-delete to be off before you can turn on backup.

**Do this today, before any analysis:**

1. Open Google Maps → profile picture → **Your Timeline**. Scroll back to your earliest year (for you, around 2011) and confirm the old years are still there.
2. Turn **auto-delete off** and **encrypted backup on** (the cloud icon in Timeline).
3. **Export** a copy (steps below) and keep it in two places, for example a laptop and Google Drive or an external disk. The export is your raw data and can't be re-created.
4. Check older phones, or a phone a family member uses with the same account. During the migration, each device kept only what it had copied, so an old phone may hold years the current phone lacks.
5. If you exported Takeout before 2024, look in Drive and email for old `takeout-*.zip` files. Their `Location History/Semantic Location History/YYYY/` folders hold the full older history, including place names and addresses.

## 2. How to export your Timeline

| Device | Steps | File you get |
|---|---|---|
| **Android** | Settings app → Location → Location services → Timeline → **Export Timeline data** → Continue → choose a folder → Save | `Timeline.json` (`{"semanticSegments": [...]}`) |
| **iPhone** | Google Maps → profile picture → Your Timeline → ⋯ / Settings → **Export Timeline data** → save to Files | `location-history.json` (a JSON list) |
| **Old Takeout (pre-2024 archives)** | takeout.google.com, "Location History", if your account still offers it | `Records.json` (raw GPS) + `Semantic Location History/YYYY/YYYY_MONTH.json` (visits with place names) |

Menu wording varies by phone and app version. Google's help page has the current path: [Manage your Google Maps Timeline](https://support.google.com/maps/answer/6258979).

**What's in the file:** a list of *visits* (place ID, coordinates, start/end time, semantic type such as HOME/WORK), *activities* (trips between places, with distance and probable mode: walking, car, flight, train), and raw *timelinePath* GPS points. The new exports contain coordinates and Google Place IDs but **not place names or addresses**. To get city and country you have to reverse-geocode the coordinates (the script in §5 does this offline).

**Other Google data that fills gaps** (all still in [Google Takeout](https://takeout.google.com)):
- **Google Photos:** GPS tags on photos. They fill gaps when Timeline was off, and record *what* you did at each place.
- **Maps (your places):** saved and starred places, lists, reviews. Your stated wish list.
- **Gmail:** flight, train (IRCTC) and hotel confirmation emails. These are useful for checking trip dates and for years before Timeline was on.

## 3. Tools that can read your Timeline

No website or AI can *connect* to your Google Maps Timeline live. The data sits on your phone, and Google offers no Timeline API. Every tool works from the **exported file**. Prefer tools that process it locally in your browser or computer, because the file is a minute-by-minute record of where you lived, worked and slept for 15 years.

### a) Viewers and visualizers (put the map back on screen)

| Tool | What it does | Privacy |
|---|---|---|
| [Dawarich Timeline Visualizer](https://dawarich.app/tools/timeline-visualizer/) | Browser map of points and paths; open source | Runs in browser |
| [Dawarich Timeline Statistics](https://dawarich.app/tools/timeline-statistics/) | Lists countries and cities. Needs the older *Semantic Location History* format, which has addresses | Runs in browser |
| [Timeline Viewer](https://www.timelineviewer.com/), [Timeline Visualizer](https://timelinevisualizer.org/), [googlemapstimeline.com](https://www.googlemapstimeline.com/) | Web viewers / replay animations for the new export | Check each site's privacy statement |
| [kurupted/google-maps-timeline-viewer](https://github.com/kurupted/google-maps-timeline-viewer) | Open-source local viewer | Local |
| [RouteConverter](https://www.routeconverter.com/help/google-timeline/) | Converts Timeline to GPX, for Google Earth, Strava or GIS tools | Desktop |
| [Time-Mile](https://time-mile.com/guides/export-timeline-to-excel/), [MileageWise](https://www.mileagewise.com/google-maps-mileage-tracker/export-google-maps-timeline/) | Timeline to Excel/CSV (mileage-log focus) | Commercial |

### b) Counters and analyzers (countries, cities, days)

| Tool | Notes |
|---|---|
| [shawntabrizi/google-timeline-country-parser](https://github.com/shawntabrizi/google-timeline-country-parser) | Open source, offline. **Days per country per year** from the new `Timeline.json`; handles time zones and territories carefully. Countries only, no cities |
| [igormilla/google-timeline-analyzer](https://github.com/igormilla/google-timeline-analyzer) | Habit and lifestyle stats (time at home or work, commuting) |
| **`scripts/timeline_travel_stats.py` (this repo)** | Offline. All three formats. Produces **countries, cities, Indian states, trips per city, days, first and last visit, per-year summaries** as CSV plus a text summary for AI chat. See §5 |

### c) Long-term homes for the data (so you never lose it again)

| Tool | What it is |
|---|---|
| [Dawarich](https://dawarich.app/) | Open-source, self-hosted "Google Timeline replacement". Imports old and new Timeline formats, GPX, GeoJSON, OwnTracks. Shows a map, countries and cities stats, and yearly summaries. It can keep tracking via its phone app, so from now on your history is yours. Can be hosted cheaply (e.g. ElfHosted, Railway) or on a home server |
| OwnTracks / GPSLogger / Overland | Phone apps that record GPS to your own server or files, as a backup alongside Google |
| Google Earth / QGIS / kepler.gl | Free mapping tools. Load the GPX/CSV to build heat maps, route lines and animations |

### d) Travel-tracking apps (for planning and the "visited" map)

| App | Use |
|---|---|
| **Been** (iOS/Android) | Tap countries, states and cities you've visited; % of world, India states map. Fastest way to make a scratch-map from the countries list the script produces |
| **Visited** (iOS/Android) | Countries, regions, UNESCO sites and lists such as "Top 100 cities", "Wonders". Wish-list layer |
| **Polarsteps** | Automatic trip logging and journaling from now on; plans future trips with route suggestions |
| **Wanderlog / TripIt** | Itinerary planning: Wanderlog imports Google Maps saved lists; TripIt reads booking emails |
| **NomadMania / Most Traveled People** | Detailed region lists (1,300+ regions) to see what is "left" in each country |

I found no confirmation that these apps import Google Timeline files directly. In practice you feed them the country and city list from your analysis.

## 4. AI platforms: what they can and can't do

**No AI assistant can read your Timeline directly today.** Gemini works with Google Maps, Photos and Gmail, but I found no documentation saying it can query Timeline. "Ask Maps" (March 2026) personalises answers using places you searched and saved, not Timeline. A useful Google-only workflow does exist: Gemini with Photos access describes a trip day, and you check the stops in Timeline.

**What works well:** produce a compact summary first, then give that to an AI.

1. Run the script (§5) and get `countries.csv`, `cities.csv`, `by_year.csv`, `summary.txt`. These are a few KB, compared with a raw Timeline file of hundreds of MB.
2. Upload them to **Claude, ChatGPT (Advanced Data Analysis) or Gemini** and ask questions like the ones below. Uploading the summaries instead of the raw file also protects your privacy: they contain no home or work coordinates or timestamps.
3. For bigger work (all 15 years of raw points, maps, charts), use **Claude Code / ChatGPT data analysis / a Jupyter notebook with an AI assistant**. It can write and run Python (pandas, folium, plotly) on the CSVs on your own machine.

### Ready-to-use prompts

> **Travel profile.** "Here are my countries.csv, cities.csv and by_year.csv from 15 years of Google Timeline. Summarise my travel life: totals, the most-visited cities, which years I travelled most, how my travel changed over time, and which Indian states and union territories I've visited (list the ones I haven't)."

> **Gaps in India.** "Using cities.csv, list the Indian states I've visited and the ones I never have. Then list major pilgrimage destinations I haven't visited: the 12 Jyotirlingas, the Char Dham, the 4 Dhams, the 51 Shakti Peethas, the 108 Divya Desams, the major ISKCON temples, and the Kumbh Mela sites. Group them into efficient 4–7 day circuits starting from Hyderabad."

> **Next countries.** "Based on the countries I've visited and how long I stayed, suggest 10 countries I haven't visited. Use visa ease for an Indian passport, flight time from Hyderabad, cost, and similarity to places I've returned to often. Give the best month for each."

> **Repeat vs new.** "Which cities do I keep going back to, and which visits were one-offs? Suggest which I should revisit and which new cities are close to my frequent ones."

> **Plan.** "Make a 3-year travel plan: 2 international trips and 4 domestic trips a year, avoiding monsoon and peak heat, and favouring places I've never been."

> **Yatra / content angle.** "For each city I've visited 3+ times, list the temples and holy places there. Mark which ones I visited (visits.csv has coordinates) and which I missed nearby."

### Checklists AI can compare against

- **India:** 28 states and 8 union territories; UNESCO World Heritage sites in India (40+); 12 Jyotirlingas; Char Dham; Divya Desams; Shakti Peethas; Kumbh sites (Prayagraj, Haridwar, Ujjain, Nashik); the Vrindavan–Mathura, Jagannath Puri and Mayapur circuits.
- **World:** UN-member countries (193); UNESCO World Heritage list; the Travelers' Century Club list (330 "countries and territories"); and the NomadMania regions.

## 5. Do-it-yourself analysis with the script in this repo

`scripts/timeline_travel_stats.py` runs entirely on your computer, with no upload.

```bash
pip install reverse-geocode
python3 scripts/timeline_travel_stats.py Timeline.json -o my_travel --home-city Hyderabad
# You can mix formats: add location-history.json from an iPhone and any old Takeout
# "Semantic Location History" folder; the results are combined.
python3 scripts/timeline_travel_stats.py Timeline.json old_takeout/Semantic\ Location\ History -o my_travel
```

**What it produces**

| File | Contents |
|---|---|
| `visits.csv` | Every place visit with date, coordinates, city, state, country |
| `countries.csv` | Each country with days spent, separate trips, first and last visit |
| `cities.csv` | Each city/town with state, country, days, number of separate trips, first and last visit. This answers "how many times did I visit each city in India" |
| `by_year.csv` | Countries and cities per year |
| `summary.txt` | A readable overview to paste into an AI chat |

**How it counts.** A *trip* is a run of days in a place; a gap of more than 2 days starts a new trip. Cities come from the offline GeoNames dataset (towns with population ≥ 15,000 by default). Lower it with `--min-population 1000` to separate small pilgrimage towns such as Vrindavan from Mathura. Very large cities sometimes show up as neighbourhoods (e.g. "Business Bay, Dubai"); the `state` column groups them, and an AI or a spreadsheet pivot table can merge them.

**Ideas for more analysis** (ask an AI to write the code):
- Heat map of all 15 years on one map (folium / kepler.gl), plus a separate layer per year.
- Distance travelled per year by mode (flight, train, car) from the `activity` segments.
- "Firsts" timeline: the date you first set foot in each country or state.
- Seasonality: which months you travel, so you can plan around your own habits.
- Merge with Google Photos GPS to show the photos from each trip.

## 6. Privacy and safety

- The raw Timeline is very sensitive: it reveals your home, workplace, daily routine and the people you visit. Keep the raw file offline or in encrypted storage.
- Share only aggregated results (country and city lists) with web tools and AI chats. Before uploading `visits.csv` to any AI, remove the HOME/WORK rows or round the coordinates.
- Prefer open-source or in-browser tools. Read the privacy policy of any web viewer before uploading.

## 7. Suggested roadmap

1. **This week:** check auto-delete, turn on backup, export from every phone, and find old Takeout zips.
2. **Next:** run the script and review `countries.csv` / `cities.csv`.
3. **Then:** upload the summaries to Claude/ChatGPT/Gemini with the prompts in §4 to get gap lists and a multi-year travel plan.
4. **Long term:** self-host Dawarich (or keep exporting every 6 months) so the next 15 years are under your control. Use Been or Visited for the scratch-map and Polarsteps or Wanderlog to plan.

## Sources

- [Google Maps Help: Manage your Google Maps Timeline](https://support.google.com/maps/answer/6258979?hl=en&co=GENIE.Platform%3DAndroid)
- [TechRadar: Timeline switch deadline](https://www.techradar.com/phones/youve-got-more-time-the-great-google-maps-timeline-switch-gets-a-new-deadline-date)
- [PhoneArena: Google to delete Maps Timeline, save it now](https://www.phonearena.com/news/google-to-delete-your-maps-timeline-location-history-soon-save-it-now_id164762)
- [PhoneArena: Google accidentally erases Timeline data](https://www.phonearena.com/news/google-accidentally-erases-users-timeline-data_id168748)
- [Android Authority: Google Maps killing Timeline web access](https://androidauthority.com/google-maps-killing-timeline-web-access-3449017)
- [MakeUseOf: Google Maps remembers more than you realize](https://www.makeuseof.com/google-maps-remembers-tons/)
- [Android Police: Gemini + Google Maps for vacation photos](https://www.androidpolice.com/gemini-and-google-maps-talk-to-each-other-vacation-photos-make-sense/)
- [Dawarich: What's inside your Google Timeline export](https://dawarich.app/blog/whats-inside-your-google-timeline-export/)
- [Dawarich vs Google Timeline](https://dawarich.app/docs/comparisons/vs-google-timeline/)
- [Dawarich: Best Google Timeline alternatives 2026](https://dawarich.app/blog/best-google-timeline-alternatives-in-2026-ranked/)
- [shawntabrizi/google-timeline-country-parser](https://github.com/shawntabrizi/google-timeline-country-parser)
- [igormilla/google-timeline-analyzer](https://github.com/igormilla/google-timeline-analyzer)
- [RouteConverter: Google Timeline to GPX](https://www.routeconverter.com/help/google-timeline/)
- [Timelinevisualizer.net: How to export Google Timeline](https://www.timelinevisualizer.net/how-to-export-google-timeline/)
- [Time-Mile: Export Timeline to Excel](https://time-mile.com/guides/export-timeline-to-excel/)
- [TechRadar: Polarsteps travel tracker](https://techradar.com/phones/polarsteps-is-the-free-app-that-tracks-your-travels-and-it-just-made-my-new-years-resolutions-list)
- [Cal Poly: Apps that track your travels](https://grandavehousing.calpoly.edu/news/apps-that-track-your-travels)
