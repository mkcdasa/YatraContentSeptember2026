---
date: 2026-11-03T02:13:52.141Z
project: YatraContentSeptember2026
session: 8a3dde17
schema_version: 1
next_steps_count: 4
has_blockers: false
keywords: london europe yatra, bhakti yatra, posters, brochure, word itinerary, itinerary_data, brand.py, photo poster
headline: Goal: plan + market London Europe Yatra 2027 (17 Apr–2 May 2027, 15N/16D, 8 countries, coach) for Hare Krishna Golden Te
---

# Session Handoff Snapshot
> **Generated:** 11/3/2026, 2:13:52 AM

## 🎯 High-Level Objective
* **Goal:** Goal: plan + market London Europe Yatra 2027 (17 Apr–2 May 2027, 15N/16D, 8 countries, coach) for Hare Krishna Golden Temple Hyderabad, plus Bhakti Yatra (Hare Krishna Movement Indore) rebrand. Intent: one data source drives Excel, living doc and all creatives so plan and marketing never drift.

## 📌 Current State & Next Steps
* **Status:** Done: all creatives both brands rendered, pushed to claude/new-session-yaq8x4. Remaining: user feedback; hotels/some lunch restaurants TBC; Tower of London price unverified; Titlis group discount 10% vs 20% unconfirmed.
* **Next Action:** Await user feedback on HKGT and Bhakti creatives

### Remaining Queue
- [ ] Ask/decide: drop Golconda and ISKCON Bangalore mentions in Bhakti versions; remove free optional mentions (morning japa, Cologne walk, Titlis Cliff Walk)
- [ ] Add HKGT logo when provided
- [ ] Confirm Titlis group discount and Tower of London price; fill TBC hotels and lunch restaurants

## 🛠️ Modified Files Delta
* itineraries/london-europe-yatra/itinerary_data.py: London Days 2-3 redesign, retimes, BOOKING list, ticket links/prices, price 549000
* itineraries/london-europe-yatra/build_workbook.py: Booking guide sheet, planned-walks column, price text
* itineraries/london-europe-yatra/marketing/build_marketing.py: 4 posters + brochure; tips/optional removed
* itineraries/london-europe-yatra/marketing/build_photo_poster.py + fetch_photos.py + photos/: 2-page photo poster, no credits
* itineraries/london-europe-yatra/marketing/brand.py: HKGT/Bhakti brand settings, colour map, no-city flight text
* itineraries/london-europe-yatra/marketing/export_word_data.py + build_word.cjs: Word itinerary, brand-aware, filters internal + extras
* itineraries/london-europe-yatra/marketing/render.cjs, render_photo_poster.cjs: brand-aware output paths
* itineraries/london-europe-yatra/marketing/out/ and out/bhakti-yatra/: rendered JPG/PDF/DOCX

## 🚫 Failed Approaches (DO NOT RETRY)
* Approach: Wikimedia API search/imageinfo in loops → Result: HTTP 429 rate limits → Lesson: batch slowly; download thumbs directly from thumb.wikimedia.org using saved URLs
* Approach: render.js with require → Result: fails, repo package.json is ESM → Lesson: use .cjs for node scripts
* Approach: Claude Docs block replace without guards / using char ids → Result: refused → Lesson: whole-block replace needs ifHash+ifRev; use block ids; find-text edits for small changes
* Approach: photo credits line on poster → Result: user rejected → Lesson: never include credits in creatives

## 🔑 Crucial Context & Implicit Rules
* Branch claude/new-session-yaq8x4; commits end with Co-Authored-By + Claude-Session lines; no model id in commits
* Rebuild: python3 marketing/build_marketing.py, build_photo_poster.py, export_word_data.py, node marketing/build_word.cjs, then node marketing/render.cjs + render_photo_poster.cjs from repo root; prefix YATRA_BRAND=bhakti for Bhakti; NODE_PATH=$(npm root -g)
* Excel recalc: python3 /mnt/skills/public/xlsx/scripts/recalc.py file.xlsx 60
* Living doc: Claude Docs project 41969992-a942-449c-8cfc-39fa59681168, node 01869f60-e37d; link https://claude.ai/artifact/96kSc9Lverwvxj1phuNgjZ
* Bhakti Yatra brand assets originally from branch claude/pensive-galileo-twgsa0 docs/brand/
* User addressed as Hare Krishna Prabhu; terse instructions

## Key Decisions
- Decision: price Rs 5,49,000 incl. international flights + 5% GST + 2% TCS — Reason: user final; TCS refunded via ITR
- Decision: daily 07:30 programme, 08:00–09:00 breakfast, 09:00 departure; exceptions Day 14 Rome train, Day 16 flight — Reason: user instruction; fixed departures
- Decision: London Day 2 Akshaya Patra Watford, Bhaktivedanta Manor Sunday programme, Tussauds, ISKCON Soho, Covent Garden; Day 3 Changing of Guard, King's Gallery, Tower/Koh-i-Noor, Tower Bridge, Thames boat, London Eye, Westminster — Reason: user dropped Oxford/Cotswolds; one-direction routing
- Decision: Lion King only as Plan B Sun matinee; no ROH show on dates — Reason: no Monday show; Tosca 17/20 Apr only
- Decision: never print photo credits on creatives — Reason: user explicit, accepts licence risk; credits kept in marketing/photos/credits.json
- Decision: brand switch in marketing/brand.py (YATRA_BRAND=bhakti) rewrites HKGT HTML/Word into Bhakti (ISKCON Vijay Nagar-Indore + Bhakti Yatra logos, purple, phones +91 72248 64316 / +91 92570 45200, Bhaktiyatra social) — Reason: one source, two brands
- Decision: Bhakti versions say only 'International flights included', no city/airline — Reason: user instruction for Indore audience
- Decision: driver tips + optional extras removed from all creatives, kept in internal Excel — Reason: user instruction; costing stays correct
- Decision: shareable docs exclude budget, margin, fares, hotel rates, ticket costs — Reason: external audience

## 🙋 User Decisions (made by the human)
- **Final price Rs 5,49,000 incl. international flights + 5% GST + 2% TCS**
  - Reason: Trip dates final
- **Drop Oxford and Cotswolds; add listed London sights**
  - Reason: More time for attractions
- **No photo credits on any creative**
  - Reason: Accepts licence risk
- **Bhakti Yatra versions: international flights included, no city**
  - Rejected: Indore via Delhi/Mumbai
- **Remove driver tips and optional extras completely from posters and PDFs**

## Summary
Built minute itinerary data (itinerary_data.py), Excel (build_workbook.py), Claude Docs living doc, booking guide, 4 posters, 2-page photo poster, A4 brochure, Word itinerary; both brands via YATRA_BRAND switch. Last steps: Bhakti versions with no departure city; driver tips + optional extras removed from all creatives.

---
*A short hint surfaces on session start; full context loads only if your next prompt matches a keyword above, or via manual `/handoff-resume`. The same record is available as a sibling `.json` file for external tools.*