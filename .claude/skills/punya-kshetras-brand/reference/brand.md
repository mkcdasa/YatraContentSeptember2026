# Punya Kshetras brand guide

Punya Kshetras is the pilgrimage service of Hare Krishna Golden Temple (ISKCON), Banjara Hills, Hyderabad. Every yatra collateral carries both identities.

## Logos and marks (`assets/brand/`)

| File | Use |
|---|---|
| `hkgt_logo.png` | Hare Krishna Golden Temple logo (new, 2026). Always top-left, on a white rounded box. |
| `hkgt_logo_white.png` | White version for dark backgrounds only. |
| `pk_logo.png` | Punya Kshetras logo ("Nourish your soul on sacred journeys"). Always top-right, on a white rounded box. |
| `seal.png` | Srila Prabhupada round seal. Centre-top on covers and posters, between the two logos. |
| `prabhupada.jpg` | Srila Prabhupada photo for the welcome page, captioned "His Divine Grace A.C. Bhaktivedanta Swami Srila Prabhupada, Founder-Acharya of ISKCON". |
| `../img/moments1.jpg`, `moments2.jpg` | Past-yatra group photos ("Why Punya Kshetras" page). |
| `../img/joined.jpg` | "Who joined our yatras" collage (Terms page). |

Never stretch, recolour or crop the logos. Keep the white box padding.

## Colours (CSS tokens in `assets/style.css`)

| Token | Hex | Use |
|---|---|---|
| `--plum3` | #2A0D3D | Darkest background, footers, poster base |
| `--plum` | #3A1452 | Headings, phone number, primary text accents |
| `--plum2` | #5B1F7E | Gradients with plum3 |
| `--coral` | #E8445A | Day badges, "Registrations close" chip, accents |
| `--orange` | #F28C28 | Gradient partner of coral (Book Now, duration pill, kicker badge) |
| `--gold` | #E7B24A | Ornaments, price badge gradient |
| `--gold2` | #F6D58B | Script titles on dark, highlights |
| `--cream` | #FFF7EA | Page background |
| `--ink` | #2A2131 | Body text |
| `--green` | #1F6B4F | Meal tags |

## Typography

- **Playfair Display**: titles and section headings.
- **Great Vibes**: script accent (second line of the title, "from Punya Kshetras", closing blessing).
- **Montserrat**: labels, chips, call-to-action, phone number.
- **Poppins**: body text.
- **Noto Sans / Noto Serif** (Telugu, Devanagari, Kannada, Tamil) are loaded automatically for translations. Letter-spacing is switched off for Indic scripts.

All fonts are bundled in `assets/fonts/` (no internet needed).

## Contact and call to action (use exactly)

- **Call to action:** "Book Now →" (coral→orange pill) + phone **95053 88886** (large, with phone icon)
- **Websites:** www.punyakshetras.com · www.hkmhyderabad.org
- **Social:** @punyakshetras (Facebook · Instagram · YouTube · X) · HareKrishnaGoldenTemple
- **Bookings email:** booking@punyakshetras.com
- **Cancellations (written):** connect@hkmhyderabad.org
- **Address:** Swayambhu Sri Lakshmi Narasimha Swamy Kshetram, Road #12, near Anti Corruption Bureau office, NBT Nagar, Banjara Hills, Hyderabad, Telangana 500034
- **Back-page lines:** "Pilgrimage is reconnection with God" · "For details & registration – please contact any temple devotee you are in touch with, or" + phone
- **Every cover and poster:** the pill "with ISKCON Hare Krishna Devotees"

## Standard brand content (in `engine/brand.py`)

- **Srila Prabhupada quote:** Srimad Bhagavatam 1.13.10, Purport ("The holy places all over the earth are meant for purifying…").
- **"How we are different"** (7 points): Sattvic food · Pre-approved stays · Comfortable transport · Care for seniors · Narration by devotees · Family-like yatra · No hidden charges.
- **"Curated special experiences"** (6 icons): Melodious bhajans & kirtans · Sthala purana narrations · Comfortable stay · Relaxed itinerary · Special care for seniors · Sattvic food.
- **Spiritual promise** (yatri itinerary): kirtans, bhajans, pastimes, explanations, sthala purana narrations and interactive sessions. Spiritually enriching, everything managed by Hare Krishna Golden Temple devotees, a very memorable experience.
- **Terms & Conditions:** booking & payment (2% extra on cards), cancellation slabs (more than 45 days: 30% retained; 45–30 days: 50%; under 30 days: no refund), rescheduling (once, 10%), medical, levies, conduct, cancellation by us, Hyderabad jurisdiction. Add yatra-specific terms (helicopter, baggage…) per package.

## Formats

| Collateral | Size | Notes |
|---|---|---|
| Brochure PDF | A4 portrait, 12–18 pages | Pages: cover, welcome, journey at a glance, one page per day, holy places, package details (includes/excludes/price/flights/meals), meal plan (if more than 12 meals), why us, tips (pack/do's/don'ts/FAQ), terms, back cover with photo credits |
| Poster | 1080×1350 px (Instagram/WhatsApp 4:5), JPG + PDF | Logos row, kicker badge, title, 3 photo circles, dates + duration, route, price badge, registration chip, 8 highlights, 6 experience icons, white Book Now bar |
| Yatri itinerary PDF | A4, 3–5 pages | No timings. Places with Google Maps links + activities per day; meal plan on its own page; help-line footer |
