# AGENTS.md

<!-- handoff:learnings:begin -->
## Session Learnings (auto-updated by handoff)

### Implicit Rules
- Branch claude/new-session-yaq8x4; commits end with Co-Authored-By + Claude-Session lines; no model id in commits
- Rebuild: python3 marketing/build_marketing.py, build_photo_poster.py, export_word_data.py, node marketing/build_word.cjs, then node marketing/render.cjs + render_photo_poster.cjs from repo root; prefix YATRA_BRAND=bhakti for Bhakti; NODE_PATH=$(npm root -g)
- Excel recalc: python3 /mnt/skills/public/xlsx/scripts/recalc.py file.xlsx 60
- Living doc: Claude Docs project 41969992-a942-449c-8cfc-39fa59681168, node 01869f60-e37d; link https://claude.ai/artifact/96kSc9Lverwvxj1phuNgjZ
- Bhakti Yatra brand assets originally from branch claude/pensive-galileo-twgsa0 docs/brand/
- User addressed as Hare Krishna Prabhu; terse instructions

### Key Decisions
- Decision: price Rs 5,49,000 incl. international flights + 5% GST + 2% TCS — Reason: user final; TCS refunded via ITR
- Decision: daily 07:30 programme, 08:00–09:00 breakfast, 09:00 departure; exceptions Day 14 Rome train, Day 16 flight — Reason: user instruction; fixed departures
- Decision: London Day 2 Akshaya Patra Watford, Bhaktivedanta Manor Sunday programme, Tussauds, ISKCON Soho, Covent Garden; Day 3 Changing of Guard, King's Gallery, Tower/Koh-i-Noor, Tower Bridge, Thames boat, London Eye, Westminster — Reason: user dropped Oxford/Cotswolds; one-direction routing
- Decision: Lion King only as Plan B Sun matinee; no ROH show on dates — Reason: no Monday show; Tosca 17/20 Apr only
- Decision: never print photo credits on creatives — Reason: user explicit, accepts licence risk; credits kept in marketing/photos/credits.json
- Decision: brand switch in marketing/brand.py (YATRA_BRAND=bhakti) rewrites HKGT HTML/Word into Bhakti (ISKCON Vijay Nagar-Indore + Bhakti Yatra logos, purple, phones +91 72248 64316 / +91 92570 45200, Bhaktiyatra social) — Reason: one source, two brands
- Decision: Bhakti versions say only 'International flights included', no city/airline — Reason: user instruction for Indore audience
- Decision: driver tips + optional extras removed from all creatives, kept in internal Excel — Reason: user instruction; costing stays correct
- Decision: shareable docs exclude budget, margin, fares, hotel rates, ticket costs — Reason: external audience

<!-- handoff:learnings:end -->
