"""Single source of content for every deliverable in this folder.

The Word documents, the slide deck, the Excel tracker and the mind map are all
generated from the structures below, so a change here flows everywhere:

    python3 business-plans/prasadam-vertical/src/build_all.py
"""

TITLE = "Prasadam, Sweets & Savories Vertical"
SUBTITLE = "Business Plan, Roadmap & Project Management Plan"
ORG = "Hare Krishna Golden Temple (ISKCON), Banjara Hills, Hyderabad"
PREPARED_FOR = "Temple management, Production (Prabhu) and DMTT"
SOURCE_MEETING = "Prasadam Revenue Generation Plan meeting, 26 September 2026"
VERSION = "v1.2, 21 October 2026"

# Anything marked [ESTIMATE] must be replaced with the 6–12 month order data
# (action item A4) before it is used to commit money.

VISION = (
    "Make prasadam, sweets and savories one of the organisation's biggest "
    "verticals: first in Hyderabad, then across South India and all of India, "
    "and eventually in export markets. Profits fund our own kitchen, our own "
    "staff and machinery, and the temple's service to society."
)

MISSION = (
    "Offer pure, satvik, preservative-free prasadam, prepared with devotion and "
    "offered to Sri Sri Radha Krishna, to every audience we already touch: "
    "visitors, donors, devotees, companies, institutions, communities and online "
    "buyers. Production is done by the temple kitchen; marketing, technology and "
    "sales are done by the DMTT; every rupee and hour is tracked for ROI."
)

ONE_LINE_PITCH = (
    "Temple-made satvik sweets and savories, from the house of Radha Krishna, "
    "sold through every circle the temple already reaches: counters, restaurant, "
    "corporate gifting, white-label, catering, communities, e-commerce and, later, "
    "QSRs and exports."
)

# --------------------------------------------------------------------------
# What was said in the meeting, grouped. Nothing is dropped, however small.
# --------------------------------------------------------------------------
MEETING_INSIGHTS = [
    ("Why now", [
        "Mukunda Dasa is already driving revenue generation for the temple from several sources (gift items, e-commerce); prasadam is one of them.",
        "\"Already we are late. If not today, tomorrow we have to start.\" Target to be doing this at scale within one year at most.",
        "First-mover advantage: no temple in the Bangalore group of temples has done this at large scale yet; the market is untapped.",
        "Earlier attempts (with Vasudha, with T-Hub and Justdial.com founders and government networks) stalled because margins did not work and nobody owned production. Now a dedicated production lead (Prabhu) is in place, so the missing piece is solved.",
        "Division of labour: \"You take care of production. We take care of marketing and technology.\"",
        "A devotee must own the vision for 5–10 years and keep driving it.",
    ]),
    ("Brand advantage", [
        "When customers hear it is from ISKCON, customer acquisition is easy; people trust the name.",
        "Competing small shops often use chemicals and artificial colours; buyers do not trust them.",
        "Positioning: 'from the house of Radha Krishna', satvik, pure, without preservatives. People will pay for that.",
        "Strong SEO and digital presence: anyone searching for ISKCON Hyderabad finds our pages first.",
        "Proposal discussed to move email addresses to an iskconhyderabad.org-style domain for brand consistency.",
        "Brand-building stunt idea: an India Book of Records / world-record attempt (e.g. via the 'Mandal Yatra' platform) for a large-quantity preparation, used on social media and the website.",
    ]),
    ("Existing assets to reuse", [
        "Huge databases, networks and warm contacts who have already contributed to the temple.",
        "Existing system for dispatching prasadam to online donors all over India; other departments already copy this system.",
        "Existing human resources, spaces, vendor list and negotiated rates.",
        "Existing e-commerce experience: Shopify, order management, fastest-courier comparison.",
        "Subhadra Radha Devi Mataji has shipped around 15,000 parcels via Amazon across the country and knows fastest shipping.",
        "AI engineers and data scientists in the team; cross-sell databases; SMS, WhatsApp, RCS, Google Ads, Meta Ads and organic marketing.",
        "A new kitchen was recently inaugurated.",
        "Wooden gift boxes are already available in the storeroom; see-through plastic boxes already in use.",
        "Personal network in the trade: Mukunda Dasa's cousins run a large sweets business in Malaysia and have supplied bahumana sweets before; family has long experience in this business.",
    ]),
    ("Named contacts and circles", [
        "MNR group: 42 institutions (schools, colleges: medical, engineering, commerce, arts). Staff and student gifting at Dasara.",
        "Steel/foundry company owners with ~10,000 employees across Karnataka, AP, Telangana, Kerala, Tamil Nadu.",
        "T-Hub mentors, directors, CEOs, founders.",
        "Event-management firms, e.g. Naukaran Entertainment (Kavitaji); high-profile Dasara Dandiya events attended by prominent people.",
        "Telangana Chamber of Commerce (president is close); member companies registered on its platform.",
        "Rotary, Round Table, Alpha Circle, BNI.",
        "Institute of Company Secretaries and chartered accountants, Hyderabad chapter (president, secretary).",
        "About 100 gated communities with weekend flea markets; organisers have given free stalls before.",
        "About 100 companies currently in touch; outbound selling is possible with manpower.",
        "Chinmaya Mission Bhagavad Gita recitation event asked for 50,000 meals over two days: an order we should not lose.",
        "Big donors (e.g. from large showrooms) phone asking for 5 kg of namkeen in the rainy season.",
        "Three companies have asked us for gift boxes, calendars and Dasara gifts; we could not serve them yet (\"my heart is paining\").",
        "A partner has offered network, funds and execution for 100 restaurants / 100 QSRs in Hyderabad under the brand (KFC-style popularity).",
    ]),
    ("Festival counters evidence", [
        "Janmashtami 2026: almost all prasadam counters sold out; around ₹6 lakh sales. Target: 10 times more.",
        "A family member of the production lead watched the corner stall for four hours; continuous crowds.",
        "Mahalaya (Pitru Paksha) brings many people for service; a figure of about 200 lakh was mentioned for last year (the transcript is unclear on what it measured). Put sweets and savories stalls there too.",
        "One stall causes queues of 10–50 people and others walk away; put many stalls in a row.",
        "Place stalls where footfall is: entrance, exit (especially the darshan exit queue), Goshala walking path, staircases, garden, near benches and the waterfall, from Goshala entrance to Samskara hall.",
        "A counter in a garden where people do not gather is of no use; traffic goes out through the exit.",
        "Permanent pagodas that can be closed in rain and opened otherwise; costing was requested earlier but not done.",
        "The restaurant should take over the entire lawn on festival days: chairs, round tables, full-length counters, sweets and savories in a full row.",
        "Answer to 'the temple is becoming commercial': this is passive selling. We are not pushing; people choose to approach a stall.",
        "Shelf-stable stock is the hedge: if festival sales fall short, sell the balance online / via Instagram with a small discount.",
    ]),
    ("Pricing and unit economics", [
        "Two options: premium price for limited premium customers (limited staff, high revenue per order), or competitive price for huge volumes.",
        "Illustration used: 1 lakh orders per month at a small ticket making ₹10 lakh, versus 10,000 premium orders.",
        "Premium alone cannot cover capex, rent, electricity and salaries; it is a niche and hard to push.",
        "Decision: run two segments. The mass segment keeps the kitchen running (rotation, maintenance); premium adds margin.",
        "Very attractive packaging wins the market.",
        "Big brands have entered (a well-known brand now sells a full range of laddus and products), which proves the market.",
        "Prabhu will give good costing for mass and premium items; we help Prabhu grow so he gets volume-based better pricing.",
        "Jaggery is costlier than sugar; sugar is acceptable. Prefer jaggery-based where price allows; pick whichever gives the better price.",
        "Namkeen for diabetics, who cannot eat sweets.",
    ]),
    ("Production and capacity", [
        "Production lead currently has 4 people; will add people directly for good orders.",
        "Internal demand exists daily: donor campaigns, Culture Connect, the corporate relations department, the new Virpaksha campaign (daily donors).",
        "Weekly minimum order with one fixed delivery day (4 deliveries a month) so the kitchen can plan.",
        "Festival months (hero campaigns) communicated in advance through the system with quantities from the calendar.",
        "An exclusive cook for our orders if we commit volume.",
        "Last Krishna-related order was received and prepared quickly even at the last minute.",
        "Procurement rule: stop giving prasadam orders to anyone else; order only from the internal production lead.",
        "Infrastructure can be established if needed; later, a separate building outside the temple can be converted into a unit, as other temples do.",
        "Catering needs heavy capex and infrastructure; plan it as its own vertical.",
        "A pantry/service area exists near the restaurant; cooking happens in the main kitchen.",
    ]),
    ("Products", [
        "Criterion one: shelf life of 15–20 days.",
        "Kaja (including square kaja), khara (savoury) and sweet items.",
        "Groundnut chikki; black til and white til chikkis.",
        "Puri unde (puffed-rice balls) with jaggery, coconut and elaichi; poha puffed-rice variant for health-conscious buyers.",
        "Laddus and a 250 g weekly new item in a see-through box, which had very good response.",
        "Namkeens / mixtures.",
        "Pickles, papads, masala powders, sambar powder: another vertical.",
        "Dry fruits for gifting.",
        "Samples shown of small machines (e.g. a small red machine) for making items.",
    ]),
    ("Governance and ROI", [
        "Track from DMTT how much effort, time and energy was spent and how much revenue was generated for the temple.",
        "If someone asks 'you spent this much, what did we get back?', the ROI must be clearly visible.",
        "Budget for prasadam must be stated per department: LLP, Culture Connect, online donors.",
        "Approval path: production lead discusses with his reporting manager; then one meeting of Mukunda Dasa, the production lead and the manager to finalise.",
    ]),
    ("Learning visits and long-term vision", [
        "Visit ISKCON Mysore (prasadam there is very good) and Ahmedabad; spend a day with those devotees. Introductions available.",
        "Tech-platform thinking: Zomato, Swiggy, Zerodha, Amazon own little but scale through technology. Our scale will also come from technology.",
        "Long-term: 100 employees, export to different countries, 100 QSRs.",
        "Other related ideas raised: dairy products and ghee; temple advertising projects; education company in 150 languages; Krishna-conscious games; audio/video in 50 languages (outside this plan's scope but share the same DMTT capability).",
    ]),
    ("Smaller details also mentioned", [
        "About 10 days was mentioned for samples and feasibility on internal-department pricing.",
        "\"In 65 days we can do it\" was said about getting the vertical moving before the hero campaigns.",
        "Hero campaigns named: Dasara, Ganesh Chaturthi, New Year, Pitru Paksha, Acharya month and other temple festivals.",
        "Vasudha is not a competitor; it works on a different platform. Few other temple groups produce sweets and savories at scale.",
        "Mukunda Dasa recently visited a well-known business that now sells a full range of laddus and products, and brought back samples.",
        "A visitor with long-running business in Europe offered a connection.",
        "Companies already pay some vendor for festival gifts; middlemen in purchase departments may take commission, but owners prefer a source they trust.",
        "Gift boxes can carry the client's branding with a sticker; earlier requests were refused because no facility existed.",
        "Chinmaya Mission's 50,000-meal enquiry was passed to a professor contact; it should not be lost.",
        "Google has given the organisation ₹75 lakh in funding for technology products (context for DMTT's capacity).",
        "Some passages of the transcript are garbled (names, a few numbers); points are recorded as heard.",
    ]),
]

# --------------------------------------------------------------------------
# Research: external facts, with sources
# --------------------------------------------------------------------------
MARKET_FACTS = [
    ("India packaged sweets market", "₹8,431 crore in 2025, forecast ₹30,506 crore by 2034 (≈16% CAGR). Boxes are the largest packaging format (49%).", "IMARC Group", "https://www.imarcgroup.com/india-packaged-sweets-market"),
    ("India namkeen market", "Expected to grow by USD 4.89 billion between 2025 and 2030 at ≈10.2% CAGR; Tier-II/III retail expansion is a driver.", "Technavio", "https://www.technavio.com/report/namkeen-market-industry-in-india-analysis"),
    ("Corporate gifting", "India's corporate gifting market could cross ₹27,000 crore by 2030, with organised players taking nearly half.", "Chococraft industry note", "https://www.chococraft.in/blogs/corporate-gifts/corporate-gifting-industry-india-2025-2030"),
    ("Diwali gifting mix", "About 58% of Diwali gifts in 2025 were for corporate celebrations and 42% personal.", "Outlook India / MyFlowerTree report", "https://www.outlookindia.com/xhub/featured-insights/diwali-gifting-report-2025-what-india-is-really-buying-for-the-festival-of-lights"),
    ("Premiumisation", "Consumers increasingly prefer premium packaged sweets, curated hampers and customised assortments.", "Mordor Intelligence", "https://www.mordorintelligence.com/industry-reports/india-sweets-market"),
    ("GST 2.0", "From 22 Sept 2025, pre-packaged and labelled namkeen, bhujia and mixtures moved from 12% to 5% GST; sweets are at 5%. Lower tax helps the mass segment.", "Upstox / GST Council 56th meeting", "https://upstox.com/news/personal-finance/latest-updates/gst-rate-cut-2025-namkeens-bhujia-and-other-pre-packaged-and-labelled-goods-to-get-cheaper-from-september-22/article-180743/"),
    ("FSSAI licence thresholds", "From 1 April 2026 Basic Registration covers turnover up to ₹1.5 crore (was ₹12 lakh); Central Licence threshold raised from ₹20 crore to ₹50 crore; State Licence in between.", "Mondaq / FSSAI order of 13 March 2026", "https://www.mondaq.com/india/food-and-drugs-law/1801924/fssai-raises-turnover-limits-for-food-business-registration-and-licensing"),
    ("Labelling", "Pre-packaged sweets must show date of manufacture and best-before date. The best-before display for loose sweets on trays is now voluntary (recommended anyway).", "FSSAI / Free Press Journal", "https://www.freepressjournal.in/mumbai/fssai-removes-mandatory-best-before-date-requirement-for-non-packaged-sweets-fda-to-intensify-festival-season-inspections"),
    ("Temple precedent", "ISKCON Govinda's (Bangalore) runs an online store with same-day delivery slots for sweets, snacks, bakery, thalis and catering.", "iskcongovindas.in", "https://iskcongovindas.in/"),
    ("Local competition", "Hyderabad incumbents: G Pulla Reddy (since 1948, pure ghee, gifting page), Almond House (ships worldwide), Vellanki Foods, Dadu's, Pista House, Olive Mithai, Godavari Vantillu.", "Brand sites / IndiaShopping", "https://indiashopping.io/blogs/route-to-roots/famous-sweet-shops-in-hyderabad"),
]

COMPETITORS = [
    ("G Pulla Reddy Sweets", "Heritage pure-ghee brand; strong gifting and online", "Premium", "Temple sanctity + satvik + cause; prasadam is offered to the Deity"),
    ("Almond House", "Premium dry-fruit sweets, global shipping", "Premium", "Price flexibility (mass tier), institutional network"),
    ("Vellanki Foods / Godavari Vantillu", "Andhra traditional snacks, pickles, powders; online", "Mid", "Brand trust, festival footfall, donor base"),
    ("Pista House / Dadu's / Olive Mithai", "Retail chains, festival boxes", "Mid–Premium", "No-chemical, no-colour promise; spiritual story"),
    ("Online gifting platforms", "Aggregators (IGP, FNP, etc.) curate hampers", "Mid", "Direct relationships with company owners; white-label"),
    ("Other temple Govinda's", "ISKCON Bangalore, Jaipur, Ahmedabad stores", "Mid", "Not competitors but partners and benchmarks; Hyderabad has no scale player"),
    ("Big national brands", "Haldiram's, Bikaji, and new entrants selling laddus", "Mass–Mid", "Freshness, devotion, local connect; competitive pricing on mass tier"),
]

SWOT = {
    "Strengths": [
        "ISKCON / Hare Krishna brand trust built over decades",
        "Satvik, preservative-free, offered-to-Deity positioning",
        "Warm network: company owners, chambers, BNI, Rotary, institutions",
        "Large donor databases and top SEO ranking",
        "Existing dispatch system, Shopify skills, negotiated vendor rates",
        "Proven festival demand (Janmashtami sold out)",
        "In-house AI, data and marketing team (DMTT)",
    ],
    "Weaknesses": [
        "Kitchen capacity: 4 people today",
        "No dedicated packaging, design and pricing kit yet",
        "No historical cost/demand data compiled",
        "Limited cold chain and storage",
        "Production and marketing in different reporting lines",
        "Premium-only pricing would not cover fixed costs",
    ],
    "Opportunities": [
        "Dasara, Diwali, New Year, Sankranti corporate gifting",
        "White-label for companies' staff and clients",
        "100 gated communities, weekend flea markets",
        "Large event catering (e.g. 50,000 meals)",
        "E-commerce pan-India; diaspora / export (Malaysia, Europe)",
        "QSR franchise with an interested partner",
        "GST cut to 5% on namkeen; growing packaged-sweets market (≈16% CAGR)",
    ],
    "Threats": [
        "Established Hyderabad sweet brands and national players",
        "Perception that the temple is 'commercialising' prasadam",
        "Food-safety incident damaging brand reputation",
        "Trademark/brand-use questions on the ISKCON name",
        "Ingredient price swings (ghee, jaggery, nuts)",
        "Festival demand volatility and weather",
    ],
}

# --------------------------------------------------------------------------
# Target audiences (circles)
# --------------------------------------------------------------------------
AUDIENCES = [
    {
        "name": "Temple visitors and festival crowds",
        "circle": "Circle 1: those who come to us",
        "who": "Daily visitors, weekend families, festival crowds (Janmashtami, Mahalaya, Ratha Yatra, Gaura Purnima, etc.)",
        "needs": "Quick purchase, prasadam to take home, meals on the lawn",
        "offer": "Restaurant, lawn food court, multiple festival stalls, take-home packs, 250 g see-through boxes",
        "channel": "Stalls at entrance/exit/Goshala path, restaurant, QR menus, UPI",
        "price": "Mass tier ₹30–₹250",
    },
    {
        "name": "Donors and life members",
        "circle": "Circle 1: those who come to us",
        "who": "Online donors across India, big donors, sponsors, Virpaksha daily donors",
        "needs": "Blessed prasadam at home; gifts for family and staff",
        "offer": "Donor prasadam packs, bahumana boxes, 5 kg namkeen tins, festival hampers",
        "channel": "Existing donor dispatch system, WhatsApp, donor-care calls",
        "price": "Mid to premium",
    },
    {
        "name": "Internal departments",
        "circle": "Circle 1: those who come to us",
        "who": "Culture Connect, LLP, online donor team, corporate relations, campaigns",
        "needs": "Reliable weekly supply at an agreed rate",
        "offer": "Weekly standing order, one fixed delivery day, festival top-ups",
        "channel": "Internal order form in the system; monthly budget per department",
        "price": "Internal transfer price (cost + agreed margin)",
    },
    {
        "name": "Corporate companies",
        "circle": "Circle 2: those we go to (B2B)",
        "who": "Owners/HR/admin of firms with 500–10,000+ staff (steel, IT, pharma, real estate, T-Hub startups)",
        "needs": "Festival gifts for staff and clients, on time, branded, within budget",
        "offer": "Own-brand gift boxes (3 tiers) and white-label boxes with company branding; samples, menu, price list",
        "channel": "Owner-level meetings (Mukunda Dasa + production rep), chamber and BNI referrals, LinkedIn, email",
        "price": "₹250–₹2,500 per box; volume slabs",
    },
    {
        "name": "Educational institutions",
        "circle": "Circle 2: those we go to (B2B)",
        "who": "MNR group (42 institutions) and other school/college chains",
        "needs": "Gifts for staff and students; event snacks",
        "offer": "Low-ticket student packs, staff boxes, event catering",
        "channel": "Chairman relationships; academic-calendar planning",
        "price": "Mass tier with bulk slabs",
    },
    {
        "name": "Associations and professional networks",
        "circle": "Circle 2: those we go to (B2B)",
        "who": "Telangana Chamber of Commerce, BNI, Rotary, Round Table, Alpha Circle, ICSI/ICAI Hyderabad chapters",
        "needs": "Member gifts, event hampers, meeting snacks",
        "offer": "Co-branded hampers, member discount codes, event snack boxes",
        "channel": "Presidents/secretaries, chapter meetings, newsletters",
        "price": "Mid tier",
    },
    {
        "name": "Event management companies",
        "circle": "Circle 2: those we go to (B2B)",
        "who": "Firms running Dandiya, weddings, corporate events (e.g. Naukaran Entertainment)",
        "needs": "Return gifts, event food counters",
        "offer": "Return-gift boxes, live counters, catering",
        "channel": "Partner commission / referral fee",
        "price": "Mid tier",
    },
    {
        "name": "Gated communities",
        "circle": "Circle 3: open public (B2C outside)",
        "who": "~100 gated communities with weekend flea markets",
        "needs": "Tasty, pure snacks; festival supplies",
        "offer": "Weekend stall with top sellers, pre-order for festivals, community WhatsApp group",
        "channel": "Flea-market organisers (free stalls offered before), RWA committees",
        "price": "Mass tier",
    },
    {
        "name": "Life-event families (open circle)",
        "circle": "Circle 3: open public (B2C outside)",
        "who": "Families holding house-warming, naming ceremony, birthdays, weddings, car/vehicle puja, shop openings, shraddha",
        "needs": "Prasadam packs, return gifts, satvik catering",
        "offer": "Occasion packs, catering menus, bulk sweets",
        "channel": "Google Ads, Instagram, referrals, temple ceremony desk",
        "price": "Mid tier",
    },
    {
        "name": "Online shoppers across India",
        "circle": "Circle 4: digital",
        "who": "Social-media followers, NRIs sending gifts home, health-conscious buyers",
        "needs": "Trusted, pure, shelf-stable sweets delivered fast",
        "offer": "Shopify store + Amazon; subscriptions; diabetic-friendly namkeen; jaggery range",
        "channel": "Meta Ads, Google Ads, WhatsApp, RCS, SMS, SEO, influencers",
        "price": "Mid tier + shipping",
    },
    {
        "name": "Health-conscious and diabetic buyers",
        "circle": "Circle 4: digital",
        "who": "Buyers avoiding refined sugar, chemicals and colours",
        "needs": "Jaggery-based, low-sugar, millet, poha puffed rice",
        "offer": "'Satvik Wellness' sub-range; namkeen for diabetics",
        "channel": "Content marketing, doctors/yoga communities",
        "price": "Premium",
    },
    {
        "name": "Institutional bulk / large gatherings",
        "circle": "Circle 5: scale",
        "who": "Spiritual/cultural organisations (e.g. Chinmaya Mission 50,000 meals), government and corporate events",
        "needs": "Very large volumes, on time, hygienic",
        "offer": "Bulk meal packets, prasadam packs, catering",
        "channel": "Direct leadership contact; tender responses",
        "price": "Per-plate contract",
    },
    {
        "name": "QSR and restaurant diners",
        "circle": "Circle 5: scale",
        "who": "Urban young families and office-goers wanting pure veg fast food",
        "needs": "Fast, affordable, pure veg",
        "offer": "Satvik QSR outlets (franchise with partner), later fine dine",
        "channel": "Franchise partner, food-delivery apps",
        "price": "₹99–₹399 meals",
    },
    {
        "name": "Export and diaspora",
        "circle": "Circle 5: scale",
        "who": "Indian diaspora (Malaysia, Europe, USA, Middle East), ISKCON temples abroad, Indian grocery stores",
        "needs": "Authentic long-shelf-life sweets, pickles, powders",
        "offer": "Export-grade packaged range",
        "channel": "Family business in Malaysia, European contacts, APEDA, Amazon Global",
        "price": "Export pricing",
    },
]

# --------------------------------------------------------------------------
# Business models / revenue streams
# --------------------------------------------------------------------------
STREAMS = [
    {
        "id": "R1", "name": "Internal supply to departments",
        "what": "Weekly standing orders to Culture Connect, LLP, online donors dispatch, corporate relations and campaigns, with one fixed delivery day and festival top-ups.",
        "why": "Guaranteed base load for the kitchen from day one; replaces outside vendors.",
        "how": "Order-trend analysis (6–12 months) → minimum weekly quantity per department → internal price list → order form in the system.",
        "phase": "Phase 0–1", "capex": "Low", "margin": "Low–Medium",
        "kpi": "Weekly order fulfilment %, on-time %, internal cost saved vs outside vendors",
    },
    {
        "id": "R2", "name": "Festival stalls and counters",
        "what": "Rows of stalls at high-footfall points on festival days; permanent rain-proof pagodas; restaurant takes the entire lawn.",
        "why": "Proven: Janmashtami 2026 sold out at ≈₹6 lakh with limited counters. Target 10×.",
        "how": "Footfall map → stall layout (entrance, exit queue, Goshala path, staircases, garden, waterfall, Samskara) → UPI + POS → stock plan from calendar → leftovers go online.",
        "phase": "Phase 1 onward", "capex": "Medium (pagodas)", "margin": "High",
        "kpi": "Sales per festival, sales per stall per hour, stock-out time, leftover %",
    },
    {
        "id": "R3", "name": "Temple restaurant and lawn food court",
        "what": "Restaurant as the daily anchor; on festival days full-length counters, chairs and round tables across the lawn.",
        "why": "Captures every visitor; 365-day revenue.",
        "how": "Menu engineering, QR ordering, festival lawn SOP, rental furniture contracts.",
        "phase": "Phase 1–3", "capex": "Medium", "margin": "Medium",
        "kpi": "Daily covers, average bill, festival-day revenue",
    },
    {
        "id": "R4", "name": "Corporate gifting (own brand)",
        "what": "Dasara, Diwali, New Year, Sankranti and other gift boxes in three tiers, with dry fruits and sweets; samples, menu, price list.",
        "why": "About 58% of Diwali gifting is corporate; our network reaches owners directly; three companies have already asked.",
        "how": "Gift catalogue + samples → owner meetings (Mukunda Dasa with production rep) → PO with 50% advance → production calendar → dispatch.",
        "phase": "Phase 1 onward", "capex": "Low (packaging)", "margin": "High",
        "kpi": "Boxes sold, average order value, repeat clients, advance collected",
    },
    {
        "id": "R5", "name": "White-label / co-branded gifting",
        "what": "Same boxes with the client's logo and message (sticker or printed sleeve), so their brand travels with our prasadam.",
        "why": "Companies are already paying some vendor; the owner prefers a trusted source.",
        "how": "Brand-sticker template, MOQ per design, proof approval, 10–15 day lead time.",
        "phase": "Phase 1 onward", "capex": "Low", "margin": "High",
        "kpi": "White-label orders, lead time, design approval cycle",
    },
    {
        "id": "R6", "name": "Daily snacking (365-day retail)",
        "what": "Sweets and savories unconnected to festivals: chikkis, kaja, khara, namkeen, puri unde, laddus, 250 g weekly specials.",
        "why": "Evergreen demand; rotation keeps the kitchen busy.",
        "how": "Top-10 SKU list, standard pack sizes, shelf-life testing, temple shop + restaurant + online.",
        "phase": "Phase 1–2", "capex": "Low", "margin": "Medium",
        "kpi": "Units per SKU per week, sell-through, returns/spoilage",
    },
    {
        "id": "R7", "name": "E-commerce (own store + marketplaces)",
        "what": "Shopify store and Amazon listing for shelf-stable items, pan-India shipping, subscriptions, donor bundles.",
        "why": "Scale through technology; reuse donor dispatch and Amazon experience (≈15,000 parcels).",
        "how": "Catalogue & photography → Shopify + payment + courier aggregator → Amazon → ads funnel → WhatsApp retargeting.",
        "phase": "Phase 2", "capex": "Low", "margin": "Medium",
        "kpi": "Orders/month, CAC, ROAS, repeat rate, delivery TAT",
    },
    {
        "id": "R8", "name": "Catering and bulk meals",
        "what": "Satvik catering for house programmes, life events, corporate and institutional events; bulk meal packets (e.g. 50,000 meals).",
        "why": "Strong demand; many requests already; high visibility for the brand.",
        "how": "Start with drop-off catering from existing kitchen; partner kitchens for very large orders; later dedicated catering unit.",
        "phase": "Phase 2–4", "capex": "High (at scale)", "margin": "Medium",
        "kpi": "Events/month, plates served, per-plate margin, feedback score",
    },
    {
        "id": "R9", "name": "Gated community flea markets",
        "what": "Weekend stalls in ~100 gated communities, pre-orders for festivals, community WhatsApp groups.",
        "why": "Access already exists; organisers have given free stalls.",
        "how": "Mobile stall kit, 2-person team, route calendar, lead capture for donor/preaching programmes.",
        "phase": "Phase 2", "capex": "Low", "margin": "Medium",
        "kpi": "Events/month, sales/event, leads captured",
    },
    {
        "id": "R10", "name": "Outbound B2B and life-event sales",
        "what": "Sell to companies, event managers and families for openings, naming ceremonies, birthdays, weddings, vehicle pujas.",
        "why": "The open 'public circle' beyond our own contacts.",
        "how": "Sales executive, CRM pipeline, Google Ads for 'satvik catering Hyderabad', referral fees for event planners.",
        "phase": "Phase 2–3", "capex": "Low", "margin": "Medium",
        "kpi": "Leads, conversion %, revenue per salesperson",
    },
    {
        "id": "R11", "name": "Pickles, papads and powders",
        "what": "Masala powders, sambar powder, pickles, papads: very long shelf life, ideal for online and export.",
        "why": "Adjacent vertical with low spoilage; strong Andhra/Telangana demand.",
        "how": "Recipe standardisation, lab testing, FSSAI labelling, co-packer if needed.",
        "phase": "Phase 3", "capex": "Low–Medium", "margin": "Medium–High",
        "kpi": "SKUs live, online share, export enquiries",
    },
    {
        "id": "R12", "name": "QSR and fine-dine restaurants",
        "what": "Satvik quick-service outlets under the brand via the interested franchise partner; vision of 100 QSRs in Hyderabad; later fine dine.",
        "why": "Partner offers network, funds and execution; pure-veg QSR is under-served.",
        "how": "Brand licence agreement, central kitchen, 1–3 pilot outlets, SOPs, then scale.",
        "phase": "Phase 4–5", "capex": "Partner-funded", "margin": "Royalty 4–8% [ESTIMATE]",
        "kpi": "Outlets live, royalty income, food-safety audit scores",
    },
    {
        "id": "R13", "name": "Exports and diaspora",
        "what": "Long-shelf-life range for diaspora markets and temples abroad.",
        "why": "Family business in Malaysia; European contacts; ISKCON global network.",
        "how": "Central FSSAI licence + IEC + APEDA; export partner; destination-country labelling.",
        "phase": "Phase 5", "capex": "Medium", "margin": "Medium–High",
        "kpi": "Countries served, export revenue",
    },
    {
        "id": "R14", "name": "Donor and sponsor packs",
        "what": "Bahumana gift boxes for big donors, sponsor prasadam for festivals, 5 kg namkeen tins in monsoon.",
        "why": "Deepens donor relationships; big donors already ask.",
        "how": "Donor-care team offers packs with campaigns; sponsorship tiers include prasadam.",
        "phase": "Phase 1 onward", "capex": "Low", "margin": "Medium",
        "kpi": "Packs sent, donor retention uplift",
    },
]

BUSINESS_IDEAS = [
    ("Satvik Subscription Box", "Monthly box of 4–6 seasonal sweets and savories delivered to homes and offices; donor-exclusive pricing."),
    ("Festival Pre-order App/Page", "Pre-book Janmashtami/Diwali boxes online; pick up at a dedicated counter to avoid queues; stock planned from pre-orders."),
    ("Corporate 'Prasadam Friday'", "Weekly snack trays for company pantries on a subscription contract."),
    ("Student and hostel packs", "Low-ticket packs for MNR and other institutions during exams and festivals."),
    ("Diabetic-friendly namkeen line", "Clearly labelled low-sugar/no-sugar range for donors who cannot eat sweets."),
    ("Jaggery & millet wellness range", "Premium health range (jaggery chikki, millet laddu, poha puffed-rice unde)."),
    ("Occasion kits", "House-warming, naming ceremony, vehicle puja, shraddha and wedding return-gift kits."),
    ("Monsoon namkeen tins", "5 kg tins for big donors and showrooms in the rainy season."),
    ("World-record event", "Largest laddu / largest chikki / most prasadam packets in a day for PR (India Book of Records)."),
    ("Live-kitchen experiences", "Weekend 'make your own laddu' workshops for families and corporate teams."),
    ("Temple-to-desk vending", "Branded shelf-stable snack racks in corporate offices and co-working spaces."),
    ("Instagram flash sales", "Clear post-festival leftover stock with limited-time offers."),
    ("Referral programme for event planners", "Commission for every catering or return-gift order referred."),
    ("Sponsor-a-box", "Donors sponsor prasadam boxes distributed to the needy on festivals (cause marketing)."),
    ("Travelling prasadam (Yatra tie-in)", "Shelf-stable packs for yatris on the temple's pilgrimage tours (links to the Yatra department)."),
    ("NRI gifting portal", "Order from abroad, delivered to family in India for festivals."),
]

# --------------------------------------------------------------------------
# Products
# --------------------------------------------------------------------------
PRODUCTS = [
    # name, category, shelf life (days), tier, sweetener, pack sizes, notes
    ("Groundnut chikki", "Sweet – brittle", "60–90", "Mass", "Jaggery", "100 g, 200 g, 500 g", "Top shelf-life item; ideal for online and gifting"),
    ("Til chikki (black & white)", "Sweet – brittle", "60–90", "Mass/Premium", "Jaggery", "100 g, 200 g", "Sankranti hero product"),
    ("Dry-fruit chikki", "Sweet – brittle", "45–60", "Premium", "Jaggery/Sugar", "200 g, gift tin", "Corporate gifting"),
    ("Puri unde (puffed-rice balls)", "Sweet – laddu", "20–30", "Mass", "Jaggery, coconut, elaichi", "6-pc, 12-pc", "Karnataka favourite; light, healthy"),
    ("Poha puffed-rice unde", "Sweet – laddu", "20–30", "Wellness", "Jaggery", "6-pc", "For health-conscious buyers"),
    ("Kaja / square kaja", "Sweet – fried", "15–20", "Mass", "Sugar syrup", "250 g, 500 g", "Andhra classic"),
    ("Besan / boondi laddu", "Sweet – laddu", "10–15", "Mass/Premium", "Sugar, ghee", "250 g, 500 g, 1 kg", "Festival and temple staple"),
    ("Dry-fruit laddu", "Sweet – laddu", "20–30", "Premium", "Dates/jaggery", "250 g, gift box", "No added sugar option"),
    ("Mysore pak", "Sweet – ghee", "15–20", "Premium", "Sugar, ghee", "250 g, 500 g", "Gift box star"),
    ("Khara / mixture namkeen", "Savory", "30–45", "Mass", "—", "200 g, 500 g, 5 kg tin", "Diabetic-friendly choice"),
    ("Chakli / murukku", "Savory", "30–45", "Mass", "—", "200 g, 400 g", "All-season"),
    ("Ribbon pakoda / chekkalu", "Savory", "30–45", "Mass", "—", "200 g", "Telangana favourite"),
    ("Roasted/spiced nuts", "Savory", "60–90", "Premium", "—", "150 g tins", "Gift boxes"),
    ("Masala powders & sambar powder", "Pantry", "180+", "Mid", "—", "100 g, 250 g", "Pickles/powders vertical"),
    ("Pickles", "Pantry", "180+", "Mid", "—", "250 g, 500 g", "Satvik (no onion/garlic) differentiator"),
    ("Papads", "Pantry", "180+", "Mass", "—", "200 g", "Long shelf life"),
    ("Dry fruits assortment", "Gifting", "90+", "Premium", "—", "Gift boxes", "Wooden box option"),
    ("Weekly special (250 g box)", "Rotating", "7–20", "Mass", "Varies", "250 g see-through", "Already tested with very good response"),
]

GIFT_TIERS = [
    ("Seva box", "₹250–₹450", "3 items (chikki, namkeen, laddu) in a see-through or card box with brand sticker", "Staff gifting at scale, students, communities"),
    ("Utsav box", "₹600–₹1,200", "5–6 items including a premium sweet and dry fruits in a printed rigid box", "Employees, association members, donors"),
    ("Vaikuntha box", "₹1,500–₹3,000+", "Wooden box, dry fruits, premium sweets, small Deity picture / Gita card", "Clients, VIPs, directors, big donors"),
    ("White-label add-on", "+₹15–₹60 per box", "Client logo sticker/sleeve, greeting card, custom message", "Any tier, MOQ applies"),
]

PACKAGING = [
    "See-through plastic boxes (already in use) for counters and the 250 g weekly item; move to food-grade PET with tamper seal.",
    "Branded stickers: temple brand + FSSAI number + MFD/best-before + ingredients + veg mark; client stickers for white-label.",
    "Printed rigid boxes for the Utsav tier; wooden boxes (stock in storeroom) for the Vaikuntha tier.",
    "Gift sleeve with a short story card: 'Prepared with devotion and offered to Sri Sri Radha Krishna'.",
    "Tins for 5 kg namkeen and premium nuts.",
    "Eco option: kraft paper boxes and cloth bags for premium buyers; reduce single-use plastic over time.",
    "Every pack carries a QR code to the online store and to donation pages (cross-sell).",
]

# --------------------------------------------------------------------------
# Pricing strategy
# --------------------------------------------------------------------------
PRICING = [
    ("Mass / competitive tier", "Priced at or slightly below local shop prices; high volume; keeps the kitchen running and covers fixed costs (rent, salaries, power).", "Counters, communities, internal supply, student packs"),
    ("Premium tier", "Premium ingredients (pure ghee, dry fruits, jaggery), premium packaging; limited volumes, high margin.", "Corporate VIP boxes, donors, online wellness range"),
    ("Internal transfer price", "Cost + agreed small margin; fixed for a quarter; budget per department.", "Culture Connect, LLP, online donors"),
    ("Volume slabs (B2B)", "e.g. 100–499 boxes list price; 500–1,999 −5%; 2,000+ −8% [ESTIMATE]; 50% advance, balance before dispatch.", "Corporate and institutional orders"),
    ("Festival pricing", "Fixed MRP; combos for quick checkout (₹100/₹200/₹500) to reduce queues.", "Festival stalls"),
]

UNIT_ECONOMICS = [
    # item, price, ingredients, packaging, labour+overhead, gross margin %
    ("Seva box (₹350)", 350, 140, 35, 50),
    ("Utsav box (₹900)", 900, 360, 90, 110),
    ("Vaikuntha box (₹2,000)", 2000, 850, 300, 200),
    ("Chikki 200 g (₹80)", 80, 32, 8, 12),
    ("Namkeen 500 g (₹180)", 180, 75, 12, 25),
    ("Festival combo (₹200)", 200, 80, 12, 28),
]

# --------------------------------------------------------------------------
# Marketing plan
# --------------------------------------------------------------------------
MARKETING = [
    ("Brand story", "'From the house of Radha Krishna': satvik, pure, no preservatives, no artificial colours, offered to the Deity, profits support temple service."),
    ("Databases", "Segment donor, visitor, event and corporate databases; AI scoring to find likely buyers (DMTT data scientists)."),
    ("WhatsApp / SMS / RCS", "Festival broadcast calendars, catalogue links, one-tap reorder, community groups for gated societies."),
    ("Google Ads", "Search: 'Diwali gift boxes Hyderabad', 'corporate gifts Hyderabad', 'satvik catering', 'pure ghee sweets online'."),
    ("Meta Ads & Instagram", "Reels of prasadam preparation, Deity offering, festival crowds; flash sales for leftovers; retargeting."),
    ("SEO & content", "Leverage existing top ranking; product pages, recipes, 'why satvik' articles; Google Business Profile for the food court."),
    ("Owner-level selling", "Personal meetings with company owners via chambers, BNI, Rotary, T-Hub; sample box + catalogue + price list."),
    ("Events & PR", "Record attempts, Dandiya tie-ups, stalls at chamber and BNI events; press on 'temple kitchen goes online'."),
    ("On-campus visibility", "Signage and QR codes at darshan exit, Goshala, waterfall, restaurant; 'take prasadam home' messaging."),
    ("Cross-sell", "QR on every pack to store and donation pages; prasadam with donation receipts; yatra packs."),
]

MARKETING_FUNNEL = [
    ("Awareness", "Festival crowds, social reels, SEO, chamber/BNI events"),
    ("Interest", "Catalogue on WhatsApp, website product pages, sample boxes"),
    ("Consideration", "Owner meeting, price list, white-label mock-up, reviews"),
    ("Purchase", "Online checkout / PO with advance / UPI at stall"),
    ("Delivery & delight", "On-time dispatch, story card, feedback call"),
    ("Repeat & referral", "Festival calendar reminders, subscription, referral rewards"),
]

# --------------------------------------------------------------------------
# Operations
# --------------------------------------------------------------------------
OPERATIONS = [
    ("Kitchen & production", "Start in the existing/new kitchen with 4 staff + 1 hire now; add seasonal staff for hero campaigns; exclusive cook once weekly volume is committed; later a dedicated unit (converted building outside the temple)."),
    ("Standard recipes", "Written recipes and yield sheets for every SKU so taste and cost stay constant; batch records."),
    ("Shelf-life & quality", "Lab shelf-life test per SKU before online launch; moisture-proof packing; first-in-first-out; batch codes."),
    ("Procurement", "Use negotiated temple vendor rates; bulk-buy ghee, jaggery, groundnut, dry fruits before festival season; two suppliers per key item."),
    ("Storage", "Dry store with racks, pest control and temperature/humidity monitoring; separate finished-goods store."),
    ("Order management", "One system for all orders (internal, B2B, online, festival): Shopify/ERP + production calendar; weekly minimum orders; festival forecasts from the calendar."),
    ("Fulfilment", "Reuse donor-dispatch set-up; courier aggregator for fastest partner; own vehicle for Hyderabad B2B; Amazon for marketplace."),
    ("Festival stall SOP", "Layout map, stall kit (pagoda, table, POS, UPI QR, signage), cash-handling rules, hourly restocking runners, stock-out alerts."),
    ("Compliance", "FSSAI registration/licence matched to turnover, labelling (MFD, best-before, ingredients, veg mark, FSSAI no.), GST 5%, trade licence, fire NOC, staff medical checks, water testing."),
    ("Finance & ROI (DMTT)", "Separate cost centre; track revenue, ingredient cost, packaging, salaries, marketing, hours spent by each team; monthly P&L and ROI dashboard."),
]

ORG_ROLES = [
    ("Executive sponsor", "Temple leadership", "Approves budget, brand use and major decisions"),
    ("Vertical lead – marketing, sales & technology", "Mukunda Dasa", "Vision, network, marketing, e-commerce, DMTT reporting"),
    ("Production lead", "Prabhu (production)", "Recipes, costing, samples, capacity, kitchen team"),
    ("Production manager (reporting line)", "Production lead's manager", "Approves production commitments and resources"),
    ("E-commerce & logistics advisor", "Subhadra Radha Devi Mataji", "Shopify/Amazon, fastest shipping"),
    ("Corporate sales representative", "To be assigned by Mukunda Dasa", "Joins owner meetings; manages B2B pipeline"),
    ("Order coordinator (new hire)", "To hire now", "Order confirmations, internal orders, production calendar"),
    ("Design & packaging", "DMTT designer", "Catalogue, boxes, stickers, white-label mock-ups"),
    ("Data & AI", "DMTT data scientists", "Demand analysis, targeting, ROI dashboard"),
    ("Finance", "Accounts team", "Cost centre, GST, P&L, ROI"),
    ("Quality & compliance", "To assign", "FSSAI, labelling, hygiene audits"),
]

# --------------------------------------------------------------------------
# Roadmap
# --------------------------------------------------------------------------
PHASES = [
    {
        "name": "Phase 0 – Foundation",
        "window": "26 Sep – 10 Oct 2026 (2 weeks)",
        "goal": "Data, decisions and a ready-to-sell kit",
        "items": [
            "Share order confirmation details requested by production",
            "Analyse 6–12 months of prasadam purchases and order volumes",
            "Estimate weekly minimum and festival peak demand",
            "Budget per department (LLP, Culture Connect, online donors)",
            "Final product list, quantities and samples from production",
            "Costing and two-tier pricing (mass and premium)",
            "Hire one additional production/order person",
            "Gift catalogue, menu, price list, sample boxes, sticker templates",
            "Decision meeting: Mukunda Dasa + production lead + his manager",
            "Set up DMTT cost centre and ROI tracking sheet",
            "Check FSSAI licence scope and brand-use approval",
        ],
    },
    {
        "name": "Phase 1 – Pilot: Dasara & Diwali",
        "window": "11 Oct – 30 Nov 2026",
        "goal": "Prove corporate gifting, stalls and internal supply",
        "items": [
            "Owner meetings with 20+ companies, MNR, chambers, BNI",
            "Serve the three companies that already asked",
            "White-label boxes for first clients",
            "Mahalaya / Pitru Paksha and Dasara stalls in multiple locations",
            "Diwali gift box production and dispatch",
            "Weekly standing internal orders live",
            "Leftover stock sold online / Instagram",
            "Post-pilot review: sales, margin, hours, lessons",
        ],
    },
    {
        "name": "Phase 2 – Launch channels",
        "window": "Dec 2026 – Mar 2027",
        "goal": "Year-round revenue and digital sales",
        "items": [
            "Shopify store + Amazon listing for shelf-stable range",
            "Shelf-life lab tests and full FSSAI labelling",
            "New Year, Sankranti (til chikki), Vaikuntha Ekadashi, Gita Jayanti campaigns",
            "Gated community weekend stalls (start 10, grow to 30)",
            "Catering pilot: house programmes and small events",
            "Satvik subscription box beta",
            "CRM and B2B sales executive",
        ],
    },
    {
        "name": "Phase 3 – Scale in Hyderabad",
        "window": "Apr – Sep 2027",
        "goal": "10× festival sales and new product lines",
        "items": [
            "Permanent rain-proof pagodas; lawn food-court SOP",
            "Pickles, papads and powders line",
            "Janmashtami 2027 target: 10× 2026 counter sales",
            "Catering scale-up; partner kitchens for 50,000-meal orders",
            "Learning visits: ISKCON Mysore and Ahmedabad",
            "Year-1 review and Year-2 budget",
        ],
    },
    {
        "name": "Phase 4 – Dedicated unit & QSR pilot",
        "window": "Oct 2027 – Sep 2028 (Year 2)",
        "goal": "Own capacity, machinery and first outlets",
        "items": [
            "Dedicated production unit (converted building), machinery",
            "State/Central FSSAI licence as turnover grows",
            "Brand licence agreement with QSR partner; 1–3 pilot outlets",
            "Pan-India e-commerce push; corporate contracts across South India",
            "Team of ~25–40",
        ],
    },
    {
        "name": "Phase 5 – National & export",
        "window": "Year 3–5 (2028–2031)",
        "goal": "A national vertical with exports",
        "items": [
            "Scale QSRs towards the 100-outlet Hyderabad vision",
            "Export via Malaysia and Europe contacts; APEDA/IEC",
            "Replicate model with other temples",
            "~100 employees",
        ],
    },
]

# Hero campaign calendar (dates approximate; confirm with the temple Panchang)
FESTIVALS = [
    ("Mahalaya / Pitru Paksha", "26 Sep – 10 Oct 2026", "Stalls for devotees doing service; prasadam packs", "Medium"),
    ("Navaratri & Dasara (Vijayadashami)", "11 – 20 Oct 2026", "Corporate & institution gifting, Dandiya tie-ups", "Very high"),
    ("Deepavali", "8 Nov 2026", "Gift boxes, white-label, donors", "Very high"),
    ("Kartika month / Damodara", "Oct – Nov 2026", "Lamp-offering visitors; stalls", "High"),
    ("Gita Jayanti", "Dec 2026", "Gita + prasadam gift packs", "Medium"),
    ("New Year", "1 Jan 2027", "Corporate new-year gifting", "High"),
    ("Vaikuntha Ekadashi", "Dec 2026 / Jan 2027", "Huge footfall; stalls", "Very high"),
    ("Makara Sankranti", "14 Jan 2027", "Til chikki, sweets, gifting", "High"),
    ("Gaura Purnima / Holi", "Mar 2027", "Stalls, festival feast", "Medium"),
    ("Ugadi & Sri Rama Navami", "Mar – Apr 2027", "Ugadi packs, gifting", "Medium"),
    ("Narasimha Chaturdashi", "May 2027", "Stalls", "Medium"),
    ("Ratha Yatra", "Jun – Jul 2027", "Street stalls along the route", "High"),
    ("Sri Krishna Janmashtami", "Aug/Sep 2027", "10× target on counters, online pre-orders", "Very high"),
    ("Ganesh Chaturthi", "Sep 2027", "Laddu/modak demand, gifting", "High"),
]

# --------------------------------------------------------------------------
# Financial projection [ESTIMATE] – Year 1 = Oct 2026–Sep 2027
# --------------------------------------------------------------------------
REVENUE_Y1 = [
    # stream, Y1 (₹ lakh), Y2 multiplier, Y3 multiplier, gross margin %, basis
    ("Internal supply (R1)", 36, 1.3, 1.2, 25, "₹3 L/month average across departments"),
    ("Festival stalls (R2)", 45, 1.8, 1.5, 50, "Janmashtami 2027 ₹30 L (5× first year) + other festivals ₹15 L"),
    ("Restaurant & lawn uplift (R3)", 18, 1.5, 1.4, 35, "Incremental ₹1.5 L/month"),
    ("Corporate gifting – own brand (R4)", 30, 2.2, 1.8, 40, "Diwali/Dasara 5,000 boxes × ₹450 + New Year/Sankranti"),
    ("White-label gifting (R5)", 12, 2.5, 1.8, 40, "8–10 clients"),
    ("Daily snacking retail (R6)", 15, 1.8, 1.6, 40, "Top-10 SKUs via shop and counters"),
    ("E-commerce (R7)", 18, 3.0, 2.0, 30, "Ramp ₹0.5 L → ₹3 L/month"),
    ("Catering & bulk meals (R8)", 20, 2.5, 2.0, 25, "Events + 1 large order"),
    ("Gated communities (R9)", 10, 2.0, 1.5, 40, "10→30 communities, ₹12k–₹15k per event"),
    ("Outbound B2B & life events (R10)", 8, 2.5, 2.0, 35, "Sales executive from Phase 2"),
    ("Pickles, papads, powders (R11)", 4, 3.0, 2.0, 40, "Launch Phase 3"),
    ("Donor & sponsor packs (R14)", 8, 1.5, 1.3, 35, "Bahumana, monsoon tins"),
    ("QSR royalty (R12)", 0, 0, 0, 100, "Year 2 pilots; Year 3 royalty modelled separately"),
]

OPEX_Y1 = [
    # item, ₹ lakh Y1, note
    ("Additional staff salaries", 24, "1 order coordinator now + seasonal cooks + sales exec (Phase 2)"),
    ("Marketing (ads, content, samples)", 12, "≈5% of revenue"),
    ("Packaging design & moulds", 3, "One-time catalogue, dies, stickers"),
    ("Pagodas & stall kits", 6, "Rain-proof pagodas, tables, signage, POS"),
    ("Technology (Shopify, apps, POS, CRM)", 3, "Subscriptions and integrations"),
    ("Utilities & kitchen overheads (allocated)", 8, "Power, gas, water, maintenance"),
    ("Compliance, testing, licences", 2, "Shelf-life tests, FSSAI, audits"),
    ("Logistics not charged to customers", 5, "Free-shipping offers, B2B deliveries"),
    ("Contingency", 4, "≈5%"),
]

CAPEX = [
    ("Small machines (chikki cutter, laddu maker, sealing, packing)", "₹8–15 L", "Phase 2–3"),
    ("Permanent pagodas (8–12 units)", "₹6–12 L", "Phase 3"),
    ("Storage racks, dehumidifier, weighing & labelling", "₹3–5 L", "Phase 2"),
    ("Dedicated production unit fit-out", "₹50 L–1.5 Cr", "Phase 4 (only after demand is proven)"),
    ("Delivery vehicle", "₹8–12 L", "Phase 3–4"),
]

# --------------------------------------------------------------------------
# Project management
# --------------------------------------------------------------------------
OBJECTIVES = [
    ("O1", "Launch the vertical with a ready sales kit", "Catalogue, prices, samples and packaging ready by 10 Oct 2026"),
    ("O2", "Win Dasara/Diwali corporate orders", "≥ 5,000 gift boxes and ≥ 10 corporate/institution clients by 8 Nov 2026 [ESTIMATE]"),
    ("O3", "Stabilise internal supply", "100% of internal prasadam orders placed with in-house production by Nov 2026"),
    ("O4", "Go online", "Shopify + Amazon live with ≥ 12 SKUs by 31 Jan 2027"),
    ("O5", "10× festival counters", "Janmashtami 2027 counter sales ≥ ₹60 lakh (10× 2026) as stretch; ₹30 lakh base"),
    ("O6", "Prove ROI", "Monthly DMTT ROI report from Nov 2026; vertical cash-positive by month 6"),
    ("O7", "Year-1 revenue", "₹2.2 crore gross revenue Oct 2026–Sep 2027 [ESTIMATE]"),
]

SCOPE_IN = [
    "Sweets, savories, gift boxes, pickles/papads/powders",
    "Internal supply, festival stalls, restaurant/lawn, corporate & white-label gifting",
    "E-commerce, gated communities, outbound B2B, catering (pilot scale), donor packs",
    "Packaging, pricing, marketing, technology, ROI tracking",
    "Planning for QSR partnership and exports (execution later phases)",
]
SCOPE_OUT = [
    "Building a new dedicated production facility in Year 1",
    "Opening QSR outlets in Year 1",
    "Education company, games, audio/video, advertising projects (separate initiatives)",
    "Dairy/ghee production (evaluate separately)",
]

WBS = [
    # id, task, owner, start, end, depends, phase, deliverable
    ("1", "Initiation & governance", "", "2026-09-26", "2026-10-10", "", "Phase 0", ""),
    ("1.1", "Send detailed vertical plan to stakeholders", "Mukunda Dasa", "2026-09-26", "2026-09-30", "", "Phase 0", "This plan"),
    ("1.2", "Production lead reviews plan with his manager", "Production lead", "2026-09-30", "2026-10-03", "1.1", "Phase 0", "Feedback"),
    ("1.3", "Decision meeting (Mukunda Dasa, production lead, manager)", "Mukunda Dasa", "2026-10-05", "2026-10-05", "1.2", "Phase 0", "Signed-off charter"),
    ("1.4", "Set up DMTT cost centre and ROI tracker", "DMTT / Finance", "2026-09-29", "2026-10-06", "", "Phase 0", "ROI dashboard v1"),
    ("1.5", "Confirm brand-use approval and FSSAI scope", "Quality & compliance", "2026-09-29", "2026-10-09", "", "Phase 0", "Compliance note"),
    ("2", "Demand & data", "", "2026-09-26", "2026-10-06", "", "Phase 0", ""),
    ("2.1", "Provide order confirmation info to production", "Order coordinator", "2026-09-26", "2026-09-29", "", "Phase 0", "Order sheet"),
    ("2.2", "Analyse 6–12 months prasadam purchases & volumes", "DMTT data", "2026-09-27", "2026-10-03", "", "Phase 0", "Trend report"),
    ("2.3", "Estimate weekly minimum & festival peaks", "DMTT data", "2026-10-02", "2026-10-06", "2.2", "Phase 0", "Demand forecast"),
    ("2.4", "Department budgets (LLP, Culture Connect, online donors)", "Mukunda Dasa", "2026-09-29", "2026-10-04", "", "Phase 0", "Budget sheet"),
    ("3", "Product, costing & packaging", "", "2026-09-28", "2026-10-12", "", "Phase 0", ""),
    ("3.1", "Propose budget & item list to production for samples", "Mukunda Dasa", "2026-09-28", "2026-09-30", "", "Phase 0", "Sample request"),
    ("3.2", "Identify more long-shelf-life products", "Production lead", "2026-09-28", "2026-10-04", "", "Phase 0", "Extended item list"),
    ("3.3", "Samples & costing sheets (mass & premium)", "Production lead", "2026-10-01", "2026-10-08", "3.1", "Phase 0", "Costing sheets"),
    ("3.4", "Pricing & gift tiers finalised", "Mukunda Dasa", "2026-10-06", "2026-10-09", "3.3", "Phase 0", "Price list"),
    ("3.5", "Packaging, stickers, catalogue, menu design", "DMTT designer", "2026-09-30", "2026-10-10", "", "Phase 0", "Sales kit"),
    ("3.6", "Sample gift boxes assembled for pitching", "Production lead", "2026-10-08", "2026-10-12", "3.3,3.5", "Phase 0", "10 sample boxes"),
    ("4", "Resources", "", "2026-09-26", "2026-10-15", "", "Phase 0", ""),
    ("4.1", "Hire additional production/order person", "Production lead", "2026-09-26", "2026-10-10", "", "Phase 0", "New hire"),
    ("4.2", "Assign corporate sales representative", "Mukunda Dasa", "2026-09-29", "2026-10-03", "", "Phase 0", "Named rep"),
    ("4.3", "Seasonal staff plan for Dasara/Diwali", "Production lead", "2026-10-05", "2026-10-15", "2.3", "Phase 0", "Staff roster"),
    ("5", "Pilot: Dasara & Diwali", "", "2026-10-10", "2026-11-30", "", "Phase 1", ""),
    ("5.1", "Owner meetings (companies, MNR, chambers, BNI)", "Mukunda Dasa + sales rep", "2026-10-10", "2026-10-31", "3.6", "Phase 1", "Meeting log, POs"),
    ("5.2", "Serve the three companies that already asked", "Sales rep", "2026-10-10", "2026-10-18", "3.6", "Phase 1", "3 orders"),
    ("5.3", "Mahalaya & Dasara stall roll-out", "Production lead", "2026-10-08", "2026-10-20", "4.3", "Phase 1", "Stall sales report"),
    ("5.4", "Weekly internal standing orders live", "Order coordinator", "2026-10-12", "2026-10-19", "2.3", "Phase 1", "Weekly schedule"),
    ("5.5", "Diwali gift production & dispatch", "Production lead", "2026-10-20", "2026-11-06", "5.1", "Phase 1", "Delivered orders"),
    ("5.6", "Sell leftovers online / Instagram", "DMTT", "2026-11-09", "2026-11-20", "5.5", "Phase 1", "Clearance report"),
    ("5.7", "Pilot review & lessons learned", "Mukunda Dasa", "2026-11-23", "2026-11-30", "5.6", "Phase 1", "Review deck"),
    ("6", "Channel launch", "", "2026-12-01", "2027-03-31", "", "Phase 2", ""),
    ("6.1", "Shelf-life lab tests & labels", "Quality & compliance", "2026-12-01", "2026-12-31", "", "Phase 2", "Test reports"),
    ("6.2", "Shopify store live", "DMTT e-commerce", "2026-12-01", "2027-01-15", "6.1", "Phase 2", "Live store"),
    ("6.3", "Amazon listing", "E-commerce advisor", "2027-01-05", "2027-01-31", "6.2", "Phase 2", "Live listing"),
    ("6.4", "New Year, Vaikuntha Ekadashi & Sankranti campaigns", "DMTT", "2026-12-10", "2027-01-15", "", "Phase 2", "Campaign reports"),
    ("6.5", "Gated community stalls (10 → 30)", "Sales rep", "2027-01-10", "2027-03-31", "", "Phase 2", "Event log"),
    ("6.6", "Catering pilot", "Production lead", "2027-01-15", "2027-03-31", "", "Phase 2", "5+ events"),
    ("6.7", "CRM + B2B sales executive", "Mukunda Dasa", "2027-01-01", "2027-02-15", "", "Phase 2", "CRM live"),
    ("6.8", "Subscription box beta", "DMTT", "2027-02-01", "2027-03-31", "6.2", "Phase 2", "100 subscribers"),
    ("7", "Scale in Hyderabad", "", "2027-04-01", "2027-09-30", "", "Phase 3", ""),
    ("7.1", "Pagoda costing, procurement & installation", "Facilities", "2027-04-01", "2027-06-30", "", "Phase 3", "Pagodas installed"),
    ("7.2", "Pickles, papads, powders launch", "Production lead", "2027-04-15", "2027-06-30", "6.1", "Phase 3", "New SKUs"),
    ("7.3", "Learning visits: Mysore & Ahmedabad", "Production lead", "2027-04-15", "2027-05-15", "", "Phase 3", "Visit report"),
    ("7.4", "Janmashtami 2027 10× plan & execution", "Mukunda Dasa + Production lead", "2027-06-01", "2027-09-05", "7.1", "Phase 3", "Festival report"),
    ("7.5", "Year-1 review & Year-2 budget", "Mukunda Dasa", "2027-09-10", "2027-09-30", "7.4", "Phase 3", "Annual report"),
    ("8", "Year 2+: unit, QSR, exports", "", "2027-10-01", "2028-09-30", "", "Phase 4", ""),
    ("8.1", "Dedicated production unit business case & build", "Temple leadership", "2027-10-01", "2028-03-31", "7.5", "Phase 4", "Unit live"),
    ("8.2", "QSR brand licence & 1–3 pilots", "Mukunda Dasa", "2027-10-01", "2028-06-30", "7.5", "Phase 4", "Pilot outlets"),
    ("8.3", "Export readiness (IEC, APEDA, partners)", "Mukunda Dasa", "2028-01-01", "2028-09-30", "8.1", "Phase 4", "First export order"),
]

RACI_ACTIVITIES = [
    # activity, sponsor, Mukunda Dasa, Production lead, Prod manager, DMTT, Sales rep, Finance, Quality
    ("Vertical strategy & budget", "A", "R", "C", "C", "C", "I", "C", "I"),
    ("Product list, recipes, samples", "I", "C", "R/A", "C", "I", "I", "I", "C"),
    ("Costing & pricing", "I", "A", "R", "C", "C", "C", "C", "I"),
    ("Packaging & catalogue design", "I", "A", "C", "I", "R", "C", "I", "C"),
    ("Corporate & white-label sales", "I", "A", "C", "I", "C", "R", "I", "I"),
    ("Festival stalls", "I", "A", "R", "C", "C", "C", "C", "C"),
    ("Internal weekly orders", "I", "A", "R", "I", "C", "I", "C", "I"),
    ("E-commerce & logistics", "I", "A", "C", "I", "R", "I", "C", "I"),
    ("Compliance (FSSAI, labels, hygiene)", "I", "C", "R", "C", "I", "I", "I", "A"),
    ("ROI tracking & reporting", "I", "A", "C", "I", "R", "I", "R", "I"),
    ("Hiring & staffing", "I", "C", "R", "A", "I", "I", "C", "I"),
    ("Capex (pagodas, machines, unit)", "A", "R", "C", "C", "I", "I", "C", "C"),
]
RACI_ROLES = ["Sponsor", "Mukunda Dasa", "Production lead", "Prod. manager", "DMTT", "Sales rep", "Finance", "Quality"]

RISKS = [
    # id, risk, likelihood (1-5), impact (1-5), mitigation, owner
    ("R-01", "Kitchen cannot meet Diwali peak volume", 4, 5, "Forecast from order data; seasonal staff; cap orders by capacity; 50% advance; partner kitchens on standby", "Production lead"),
    ("R-02", "Premium-only pricing fails to cover fixed costs", 3, 4, "Two-tier model; mass tier for volume; monthly margin review", "Mukunda Dasa"),
    ("R-03", "Food-safety incident harms temple reputation", 2, 5, "FSSAI compliance, hygiene SOPs, batch codes, shelf-life tests, staff medical checks, recall plan", "Quality"),
    ("R-04", "Use of the ISKCON name on commercial packaging questioned", 3, 4, "Written approval from temple leadership / group legal; consistent brand guidelines; consider a sub-brand", "Sponsor"),
    ("R-05", "Perception that prasadam is being commercialised", 3, 3, "Passive selling, devotional messaging, transparent use of proceeds, prasadam offered first", "Mukunda Dasa"),
    ("R-06", "Ingredient price spikes (ghee, jaggery, nuts)", 4, 3, "Forward-buy before season, two suppliers, sugar/jaggery flexibility, price validity clauses", "Production lead"),
    ("R-07", "Festival sales below plan; leftover stock", 3, 3, "Shelf-stable SKUs, pre-orders, online/Instagram clearance", "DMTT"),
    ("R-08", "Late B2B deliveries during peak", 3, 4, "Production calendar, cut-off dates, dispatch buffer, own vehicle", "Order coordinator"),
    ("R-09", "Staff overload across departments", 4, 3, "Dedicated hires; clear RACI; hours tracked in DMTT", "Prod. manager"),
    ("R-10", "Online shipping damage/spoilage", 3, 3, "Moisture-proof packs, tested courier partners, only shelf-stable items online", "E-commerce advisor"),
    ("R-11", "Rain disrupts festival stalls", 3, 3, "Rain-proof pagodas; indoor fallback locations", "Facilities"),
    ("R-12", "Cash/stock leakage at stalls", 2, 3, "UPI-first, POS, stock reconciliation per shift", "Finance"),
    ("R-13", "QSR partner quality not aligned with temple standards", 3, 5, "Strict brand licence, audits, satvik SOPs, exit clauses", "Sponsor"),
    ("R-14", "Regulatory changes (FSSAI, GST)", 2, 2, "Quarterly compliance review", "Finance"),
]

KPIS = [
    ("Revenue", "Monthly gross revenue by stream", "₹ lakh", "Monthly"),
    ("Gross margin", "Revenue minus ingredients, packaging, direct labour", "%", "Monthly"),
    ("ROI", "(Contribution − DMTT & marketing cost) ÷ total invested cost", "%", "Monthly"),
    ("Hours invested", "Hours spent by DMTT, production, sales on the vertical", "hours", "Weekly"),
    ("Festival sales", "Sales per festival and per stall-hour", "₹", "Per event"),
    ("Corporate pipeline", "Leads, meetings, proposals, POs, boxes", "count", "Weekly"),
    ("Online", "Orders, conversion rate, CAC, ROAS, repeat rate", "various", "Weekly"),
    ("Operations", "On-time delivery %, order fill rate, spoilage %", "%", "Weekly"),
    ("Quality", "Complaints per 1,000 orders; audit score", "count / score", "Monthly"),
    ("Customer", "Rating, NPS, repeat B2B clients", "score", "Quarterly"),
]

GOVERNANCE = [
    ("Daily (festival weeks)", "Stand-up: production + stalls + dispatch", "Production lead"),
    ("Weekly", "Order & pipeline review (orders, production plan, sales pipeline, issues)", "Mukunda Dasa"),
    ("Monthly", "P&L and ROI review with DMTT & finance; KPI dashboard", "Mukunda Dasa + Finance"),
    ("After each hero campaign", "Post-campaign review and lessons learned", "Vertical lead"),
    ("Quarterly", "Steering review with temple leadership; budget and capex decisions", "Sponsor"),
]

COMMS_PLAN = [
    ("Temple leadership", "Monthly ROI report, quarterly steering deck", "Email + meeting"),
    ("Production team", "Weekly production plan, festival forecasts", "System + WhatsApp group"),
    ("Internal departments", "Order cut-offs, price list, delivery day", "System notice"),
    ("Corporate clients", "Catalogue, quotes, order status", "Email, WhatsApp"),
    ("Donors & public", "Festival campaigns, launches", "WhatsApp, SMS, social, website"),
]

ACTION_ITEMS = [
    ("A1", "Provide the order confirmation information requested for prasadam orders", "Production team (order coordinator)", "29 Sep 2026"),
    ("A2", "Hire an additional person for prasadam production work", "Production lead", "10 Oct 2026"),
    ("A3", "Propose available budget and requested items to production for samples and planning", "Mukunda Dasa's team", "30 Sep 2026"),
    ("A4", "Analyse 6–12 months of prasadam purchases and order volumes; share regular and festival estimates", "DMTT data", "3 Oct 2026"),
    ("A5", "Prepare and send the detailed plan for the prasadam and sweets vertical", "Mukunda Dasa", "30 Sep 2026 (this document)"),
    ("A6", "Identify additional prasadam products with longer shelf life", "Production lead", "4 Oct 2026"),
    ("A7", "Prepare packaging and product presentation for bulk corporate gifting", "DMTT designer + Production lead", "10 Oct 2026"),
    ("A8", "Send a representative to support meetings with large company owners", "Mukunda Dasa", "3 Oct 2026"),
    ("A9", "Hold the finalisation meeting on products and quantities", "Mukunda Dasa", "5 Oct 2026"),
    ("A10", "Route all prasadam orders only to the internal production lead", "All departments", "Immediate"),
    ("A11", "Get pagoda costing done", "Facilities", "31 Oct 2026"),
    ("A12", "Respond to the Chinmaya Mission 50,000-meal request", "Mukunda Dasa", "Immediate"),
]

OPEN_QUESTIONS = [
    "Final product list, quantities and weekly minimum per department?",
    "Budget allocated for prasadam per department (LLP, Culture Connect, online donors)?",
    "Pricing model split between premium and competitive tiers?",
    "Real production capacity per day now, with one more hire, and at peak with seasonal staff?",
    "Which infrastructure and staffing investments are justified before demand is validated?",
    "Brand name on packs: 'ISKCON Hyderabad', 'Hare Krishna Golden Temple', or a sub-brand?",
    "Which FSSAI licence covers commercial sale and e-commerce, and does it cover off-site stalls?",
    "Transfer-pricing and profit-sharing between production and marketing teams?",
    "Who owns catering for very large orders (50,000 meals) until a catering unit exists?",
]

SOURCES = [(f[0], f[3]) for f in MARKET_FACTS] + [
    ("G Pulla Reddy gifting", "https://gpullareddysweets.com/pages/gifting"),
    ("Almond House", "https://almondhouse.com/"),
    ("Hare Krishna Golden Temple", "https://hkmhyderabad.org/"),
]
