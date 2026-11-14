# Brand-wide constants for Punya Kshetras / Hare Krishna Golden Temple collateral.
# Nothing here is yatra-specific: per-yatra text lives in the work folder's package.py.
#
# Colour tokens (defined in assets/style.css :root):
#   --plum #3A1452  --plum2 #5B1F7E  --plum3 #2A0D3D   deep purple backgrounds, headings
#   --coral #E8445A --red #D42A2F    --orange #F28C28  call-to-action gradients, badges
#   --gold #E7B24A  --gold2 #F6D58B                    accents, script titles on dark
#   --cream #FFF7EA (page) --ink #2A2131 (text) --muted #6E6077 --line #EADFCB --green #1F6B4F (ticks, meals)
# Fonts: Playfair Display (headings), Great Vibes (script), Poppins (body), Montserrat (labels);
# Noto Sans/Serif Telugu, Devanagari, Kannada, Tamil for translations (assets/fonts/indic).

CONTACT=dict(phone="95053 88886",web1="www.punyakshetras.com",web2="www.hkmhyderabad.org",social="@punyakshetras",
  social_line="Facebook · Instagram · YouTube · X: @punyakshetras · HareKrishnaGoldenTemple",
  email="booking@punyakshetras.com",cancel_email="connect@hkmhyderabad.org",
  address="Swayambhu Sri Lakshmi Narasimha Swamy Kshetram, Road #12, near Anti Corruption Bureau office, NBT Nagar, Banjara Hills, Hyderabad, Telangana 500034")
ORG_LINE="Punya Kshetras is the pilgrimage service of Hare Krishna Golden Temple, Banjara Hills, Hyderabad. Every yatra is led by devotees, with kirtan, japa and the glories of each holy place narrated along the way, sattvic food, careful planning and special attention to elders."
WITH_LINE="with ISKCON Hare Krishna Devotees"
CTA="Book Now →"
BACK_TAGLINE="Pilgrimage is reconnection with God"
PRABHUPADA_QUOTE=("The holy places all over the earth are meant for purifying the polluted consciousness of the human being by an atmosphere surcharged with the presence of the Lord's unalloyed devotees. If anyone visits a holy place, he must search out the pure devotees residing in such holy places, take lessons from them, try to apply such instructions in practical life and thus gradually prepare oneself for moksha.","Srimad Bhagavatam 1.13.10, Purport")

WHY=[("Sattvic food","Pure-vegetarian meals planned for every day; no onion-garlic on request"),
("Pre-approved stays","Hotels checked and approved by Punya Kshetras, not booked blind"),
("Comfortable transport","Clean, well-kept vehicles with experienced hill drivers"),
("Care for seniors","Escorts throughout, unhurried pace, help at every step"),
("Narration by devotees","Sthala purana and the glories of each holy place, in Telugu, Hindi and English"),
("Family-like yatra","Kirtan, japa and satsang every day with ISKCON Hare Krishna devotees"),
("No hidden charges","All-inclusive: stays, meals and transfers in one clear package price")]
EXPERIENCES=["Melodious bhajans & kirtans","Sthala purana narrations","Comfortable stay","Relaxed itinerary","Special care for seniors","Sattvic food"]

# Package extra_terms are inserted after "Rescheduling".
TERMS=[
("Booking & payment","Seats are confirmed only after the advance is received. Full and final payment is due before departure; yatris cannot join the tour otherwise. We accept bank transfer, UPI, cheque and cash; card payments carry 2% extra."),
("Cancellation by yatri","Requests must be sent in writing to {cancel_email}. More than 45 days before travel: 30% of tour cost retained, 70% refunded. 45 to 30 days: 50% retained. Less than 30 days, no-show, or after the tour starts: no refund. Refunds are paid after 30 days of cancellation."),
("Rescheduling","Allowed once, subject to availability, on payment of 10% of the tour cost, if requested at least 7 days before travel. Later requests are treated as a cancellation."),
("Medical","Please tell us about any medical condition or special need at the time of booking. Consult your doctor before the yatra. Punya Kshetras is not liable for medical emergencies; evacuation costs are borne by the yatri."),
("Government levies","Any increase in taxes, temple or government charges after booking is payable by the yatris before departure."),
("Conduct","We may cancel the participation of any yatri who is unruly, intoxicated or unsafe to travel, without refund."),
("Cancellation by us","If we cancel the yatra, the amount paid is refunded in full; no compensation is payable for consequential loss."),
("Disputes","Subject to the jurisdiction of courts in Hyderabad, Telangana. Booking implies acceptance of these terms.")]
FAQ_COMMON=[
("What ID do I need?","Original Aadhaar or passport for every yatri, for hotels, temple registration and flights."),
("What food is served?","Pure-vegetarian meals throughout; no onion-garlic food on request.")]
COMMON_DOS=["Carry original photo ID at all times","Report 10 minutes before every departure","Stay with your buddy; wear the group scarf","Use cloak rooms before darshan"]
COMMON_DONTS=["No phones, cameras or leather goods in darshan areas","Don't buy prasad from touts","Don't wear new shoes","Don't leave the group without telling the leader"]

# Yatri itinerary "A spiritually enriching yatra" boxes (package may prepend its own highlights).
SPECIAL=[("Kirtan & bhajans","Every day, on the road, at the temples and in the evenings"),
 ("Pastimes & sthala purana","The glories and history of each holy place, narrated by devotees"),
 ("Interactive sessions","Q&A, sharing of realisations and getting to know fellow yatris"),
 ("Cared for by devotees","Every detail managed by Hare Krishna Golden Temple devotees, with special care for seniors")]
MEMO="Filled with kirtans, bhajans, pastimes and sthala purana narrations – a truly memorable experience."
MEAL_TABLE_NOTE="All meals are included. Lunch restaurants are our probable choices near each temple and may change on the day for timing, crowd or quality. Tap any name or place for its Google Maps location. No onion-garlic food on request."
TIMING_NOTE="Timings are indicative and may change with flight slots, weather and darshan queues. Distances by road are approximate."

HELI='<svg viewBox="0 0 64 40" class="hico"><rect x="6" y="3" width="52" height="3" rx="1.5"/><rect x="30" y="5" width="4" height="7"/><path d="M14 22c0-6 6-11 16-11h6c8 0 14 6 14 13 0 4-3 7-7 7H24c-6 0-10-4-10-9z"/><path d="M14 21H3l-2-6h4l3 4h6z"/><path d="M22 34h28l2 3H20z"/></svg>'
PHONE_SVG='<svg viewBox="0 0 24 24" width="{w}" height="{w}" fill="{c}" style="{s}"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>'
PIN='<svg viewBox="0 0 24 24" class="pin"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>'
ICON=lambda p:f'<svg viewBox="0 0 24 24" fill="none" stroke="#D42A2F" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{p}</svg>'
ICONS=[ICON('<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>'),
ICON('<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>'),
ICON('<path d="M2 18v-6a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v6"/><path d="M2 18h20M4 10V6h7v4"/>'),
ICON('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
ICON('<circle cx="9" cy="7" r="3"/><path d="M3 21v-2a5 5 0 0 1 10 0v2"/><path d="M17 11v10M17 11l3 3"/>'),
ICON('<path d="M3 12h18a9 9 0 0 1-18 0z"/><path d="M8 8c0-2 2-2 2-4M13 8c0-2 2-2 2-4"/>')]

# Brand images available to every package (merged into the package imgmap).
BRAND_IMG={"prabhupada":{"src":"brand/prabhupada.jpg"},"moments1":{"src":"img/moments1.jpg"},
 "moments2":{"src":"img/moments2.jpg"},"joined":{"src":"img/joined.jpg"}}
LANGS={"te":"Telugu","hi":"Hindi","kn":"Kannada","ta":"Tamil"}
