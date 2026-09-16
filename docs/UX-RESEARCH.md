# UI/UX research and what it changed

Desk research across the current travel-app field, then a deliberate decision
about which conventions apply to a **knowledge base used by a working team**
rather than a booking funnel.

## What the field does

**Mobile is the whole game.** Around 80% of travellers now use mobile apps for
booking, itinerary planning and real-time alerts, and roughly 70% of Gen Z and
millennial travellers prefer an app over a desktop site.
([JPLoft](https://www.jploft.com/blog/how-to-design-a-travel-app),
[G&CO](https://www.g-co.agency/insights/top-travel-mobile-app-design-trends-ui-inspiration))

**Bottom navigation, five items.** Effectively universal — Airbnb, Booking.com,
Klook, MakeMyTrip. Thumb reach decides the layout, not the sitemap.

**Chip-row filtering above a card list.** Horizontally scrolling filter chips
with an overflow sheet for the long tail. Skyscanner is the reference for doing
this well: filters, sorting, comparison and honest loading feedback.
([StartDesigns](https://www.startdesigns.com/blog/ui-ux-design-examples/))

**Progressive disclosure on detail screens.** Tabs or accordions, because a
tour package has more attributes than a phone screen has room.

**Cross-device continuity.** Travellers start on one device and finish on
another; synced state and a universal login are expected, not a feature.

**Multi-stop planning is the differentiator.** Wanderlog's advantage is handling
genuinely multi-stop trips in detail where competitors flatten them.
([DesignRush](https://www.designrush.com/best-designs/apps/travel))

**Indian tour operators are booking-first.** Veena World and Thomas Cook both
ship customer apps for browsing packages, viewing itineraries and paying.
Neither exposes an internal staff view — no vendor rates, no margin data, no
institutional knowledge.
([Veena World](https://play.google.com/store/apps/details?id=app.veenaworld.com),
[Thomas Cook](https://play.google.com/store/apps/details?id=com.mobicule.thomascook.tcholidayapp))
Tour-operator back-office software covers itinerary building, supplier rates and
payment tracking, but as desktop SaaS.
([AltexSoft](https://www.altexsoft.com/blog/tour-operator-software/))

## The gap this app sits in

Consumer travel apps are optimised to convert a stranger. Operator back-office
tools are optimised for a desk. Neither serves **a coordinator on a phone who
already knows the business and needs an answer in ten seconds** — which months
are safe, what the hotel's negotiated rate is, what the tithi is today, whether
this yatra actually makes money.

So the conventions were adopted where they are about phones, and rejected where
they are about selling.

## Adopted

| Pattern | Where |
| --- | --- |
| Five-item bottom tab bar | Home · Yatras · Calendar · Explore · More |
| Search-first home | Search bar directly under the greeting; global search from the header on every screen |
| Horizontal chip filters + overflow sheet | Yatras and Explore; the sheet holds month, theme and suitability |
| Tabbed detail screen | Overview · Itinerary · Dates · Season · Pros & cons · Vendors · Economics |
| Bottom sheets for detail-in-context | Vendor contact card, filters, add-a-note |
| Skeletons, never spinners | Every list and detail screen |
| 44px minimum targets, safe-area insets | `.tap` utility; header and tab bar respect the notch and home indicator |
| Light and dark themes | System-following by default, overridable in More |

## Rejected, and why

**Large hero photography.** Beautiful in Airbnb, wrong here. The department has
no photo library, and stock imagery on a Kailash page would be dishonest about
conditions. Typography and colour carry the hierarchy instead.

**AI itinerary generation.** The 2026 trend is conversational trip building. The
itineraries here are institutional assets refined over years, with specific
darshan timings and temple relationships. Generating them would destroy the
asset.

**Booking funnel, urgency, price anchoring.** Out of scope for v1 by decision.
"4 seats left" appears because it is operationally true, not as a conversion
device.

**Infinite scroll.** 2,257 places with explicit pagination beats an unbounded
list you cannot return to a position in.

## What the research did not supply

The single most useful component in the app has no analogue in any travel app
surveyed.

**The season strip** renders all twelve months as one row of coloured cells —
green for best, amber for shoulder, red for avoid — collapsing four of the
requested features (calendar, perfect weather, avoid extreme weather, seasonal)
into something readable at a glance and legible in both themes. Consumer apps
have no equivalent because they only ever show you dates that are already
bookable. An operator needs to see the whole year, including the parts that are
closed, and why.

It appears on every yatra's Season tab and on every temple page that has month
data.

## Verification

The interface was rendered in a real Chromium at 390×844 (iPhone 14 class) as
both a staff user and a yatri, across all ten routes, in light and dark. No
console errors; staff-only surfaces confirmed absent for the yatri — including
when the URL is typed directly.
