---
name: punya-kshetras-brand
description: Create branded yatra marketing collateral for Punya Kshetras / Hare Krishna Golden Temple (ISKCON, Hyderabad) – A4 brochure PDFs, 1080×1350 WhatsApp/Instagram posters and no-timing yatri itinerary PDFs with Google Maps links and a meal plan – in English plus Telugu, Hindi, Kannada and Tamil. Uses the official logos, colours, fonts, phone/website/social call-to-action, Srila Prabhupada quote, "Why Punya Kshetras" points, terms and the team's content rules (all-inclusive pricing wording, pure-veg meals, daily rhythm). Use whenever someone asks for a yatra/pilgrimage/tour brochure, poster, flyer, itinerary PDF or translation for Punya Kshetras, Hare Krishna Golden Temple or HKM Hyderabad, even if they don't name the skill.
---

# Punya Kshetras yatra collateral

Everything brand-related is fixed here, so every yatra looks and reads the same. Only the yatra content changes.

- `reference/brand.md`: logos, colours, fonts, contact and call-to-action details, page formats. **Read first.**
- `reference/content-rules.md`: the team's rules on price wording, meals, timings, maps and translations. **Read before writing any content.**
- `engine/PACKAGE_SPEC.md`: every field of a yatra's `package.py`.
- `examples/vaishno-devi-helicopter-4d/`: a complete worked example (3N/4D Vaishno Devi helicopter yatra, March 2027).

## What you need from the team (ask only for what's missing)
1. Yatra name, route, dates, duration, and the batch/registration-close date
2. Day-wise plan: places, overnight stops, transport (car/flight/helicopter/train), arrival and departure times
3. Price (per person, + 5% GST, flights excluded unless they say otherwise) and the inclusions
4. The USP to headline (e.g. helicopter, special Aarti, darshan arrangement)
5. Photos they want, or permission to use Wikimedia Commons images
6. Which languages they need (te, hi, kn, ta)

## Workflow for a new yatra
1. **Make a work folder:** copy `examples/vaishno-devi-helicopter-4d/` to `yatras/<slug>/` in the repo, or to the scratchpad. Delete its `img/`, `imgmap.json`, `i18n/*.json` and `restaurants.json` contents, and keep the structure.
2. **Schedule:** write `rows.json` with `engine/new_rows.py` (`m()` for map links, `d()` for directions, `save()` prints km per day and checks continuity). Follow the daily rhythm in content-rules: breakfast 07:30–08:30, leave 09:00, lunch near the temple.
3. **Restaurants:** research pure-veg places near each lunch stop (web search) and put a probable choice plus a backup with Maps links in `restaurants.json`.
4. **Photos:** put them in `img/` and register each in `imgmap.json` with its caption and credit. Credits print on the back cover.
5. **Content:** fill `package.py` (title, dates, price, kicker, highlights, day pages, inclusions/exclusions, flights, poster block, itinerary block). Brand constants (phone, websites, quote, Why us, terms) come from `engine/brand.py`. **Never re-type them in a package.** Use the `why`, `extra_terms`, `faq` overrides only for yatra-specific lines.
6. **Build:**
   ```bash
   bash .claude/skills/punya-kshetras-brand/engine/build.sh <workdir>            # English
   bash .claude/skills/punya-kshetras-brand/engine/build.sh <workdir> te hi kn ta # + languages
   ```
   Outputs go to `<workdir>/out/`: `<slug>-Brochure.pdf`, `-Poster.jpg/.png/.pdf`, `-Yatri-Itinerary.pdf`, and `out/<Language>/…`.
7. **Check:** the build reports overflowing pages. Fix them by shortening text. Look at the cover, the price page and the poster PNG (`build/prev_brochure-NN.png`, `out/*Poster.png`). Grep the text for banned payment words and for places the team removed.
8. **Translations:** if the build prints `TRANSLATION NEEDED`, translate `i18n/en.json` into `i18n/<lang>.json` (an object mapping each English string to its translation, covering every key). Use one subagent per language. Keep phone, websites, "Punya Kshetras", "ISKCON", GST, numbers, times and photo credits in English, and keep symbols (→ · ⇄ ₹). Rebuild. Untranslated strings are listed in `i18n/missing_<lang>.json`. When English changes later, translate only the new keys.
9. **Deliver:** copy the outputs to `docs/brochures/` (languages in `docs/brochures/<Language>/`), commit, and send the files to the user. Tell them to have a native speaker proofread translations before printing.

## Rules that are easy to forget
- Poster `hl` must have **exactly 8** short lines. Itinerary `special` takes 2 or 4 items; the 4 brand promise cards are added automatically.
- The yatri itinerary never shows timings.
- Write all-inclusive wording only: never "group pays", "complimentary", "MAP", "pay at counter", "optional (book online)".
- Say "probable" for restaurants and "as allotted" for anything a temple board controls.
- If the team changes a fact (a place removed, a price, an Aarti arrangement), change it everywhere: brochure, poster, itinerary, translations, and any living doc, Excel sheet or SQL content made for that yatra.

## Requirements
python3 with `bs4` and `Pillow`, node, and Playwright with Chromium (present in Claude Code cloud sessions). `engine/package.json` must stay: it keeps the renderers CommonJS inside this ES-module repo.
