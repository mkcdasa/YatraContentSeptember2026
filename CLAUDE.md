# CLAUDE.md

<!-- handoff:learnings:begin -->
## Session Learnings (auto-updated by handoff)

### Implicit Rules
- Grand Tour build: in punya-kshetras run python3 make_rows.py and python3 make_imgmap.py, then from itineraries/london-europe-yatra run bash ../../.claude/skills/punya-kshetras-brand/engine/build.sh punya-kshetras
- Build previews in punya-kshetras/build/prev_brochure-NN.png (build/ gitignored); remove out/*.png before commit
- Bing fetcher script was in scratchpad (bingfetch.py), not committed

### Key Decisions
- Decision: Grand Tour edition headlines sights (8 countries, 63 attractions, 11 UNESCO, Colosseum New7Wonder, Pisa Medieval Wonder) — Reason: user wants common-man appeal, not ISKCON temples
- Decision: temples kept in schedule with plain wording (make_rows.py TEMPLE map) — Reason: still part of itinerary, just not headline
- Decision: engine overrides with_line, quote/quote_by, welcome_img/cap/title, experiences, why_title, hl_title, places_header/places_title + attractions page; defaults unchanged — Reason: brand skill reusable for devotional yatras
- Decision: meal page two columns when >30 meals — Reason: 44 meals overflowed one page
- Decision: web images from Bing with source URLs in punya-kshetras/imgcredits.json, never printed — Reason: user accepts copyright risk; credits never on creatives
- Decision: price ₹5,49,000 + 5% GST + 2% TCS incl international flights & visas; no driver tips/optional extras/Who-can-join — Reason: prior user rules

<!-- handoff:learnings:end -->
