# Unified CRM — Requirements (draft)

Captured from the CRM discussion on 2026-10-19. Companion to
[CRM-LANDSCAPE.md](CRM-LANDSCAPE.md), which describes the systems in use today.

> **Status:** analysis and design only. No build or migration has started.
> Work is planned to begin **Tuesday, 2026-10-20**.

## 1. Vision

Today donor, lead and call data is spread across Hello Leads, Tata Tele,
Exotel, Dhananjaya, the cold-data CRM and Excel sheets. The goal is **one
platform on Google Cloud** that holds every contact, every touchpoint and
every donation, and uses data analysis and AI to decide who to contact, for
what, and when — and who to stop spending money on.

## 2. Data that must come into the one platform

| Source | What comes in | How (initially) |
|---|---|---|
| Google / Meta / LinkedIn / Bing / ChatGPT ads | Leads (name, mobile, campaign) | Direct ad-platform integration (replaces Hello Leads) |
| Tele-calling | Remarks, status, callbacks, appointments, deal stage | Built-in tele-sales module (replaces Tata Tele) |
| Inbound calls to published numbers | Caller, call recording, who answered | Telephony integration (replaces Exotel's role) |
| Preacher (field) donations | Donors, donations, receipts | **Phase 1:** manual export of ~60k DMT donors from Dhananjaya → import. **Later:** nightly (midnight) API sync, once approved |
| Digital-marketing donations | Donor + donation | From the donation websites / payment gateway |
| Cold data | ~20–25 crore phone numbers | Bulk import from the cold-data CRM (currently offline — see §7) |
| Events / gated-community counters | Leads collected on the spot (e.g. Yatra interest) | Excel import / mobile entry |
| Campaign history (SMS, WhatsApp, RCS, email) | Every message sent and the response | Import from the campaign tools (source heard as "Carex" — verify) |
| WhatsApp / email messages | New contact details people send us | AI extraction → save as contact |
| Excel sheets | Archived Hello Leads leads (beyond 1 lakh), any other lists | Direct Excel import |

## 3. Replacement principle — build, verify, then switch off

Exotel, Tata Tele and Hello Leads are to be **replaced**, not just integrated —
paying for them while the data lives elsewhere is a waste of money. But:

1. Build the replacement module.
2. Run it in parallel and test completely.
3. Verify data and workflows with the teams who use them.
4. **Only then** stop the old tool.

No tool is switched off without verification.

**Dhananjaya is not replaced.** It stays the temple's receipt-generating ERP,
owned by the Donor Care Center. We only read our department's donor data
from it.

## 4. What the platform must know about each person

**Identity & contact** — name, mobile number(s), email, address, Google Maps
location, unique ID (with de-duplication — Dhananjaya already has duplicate
donor IDs).

**Family & occasions** — date of birth, wedding anniversary, children's and
grandchildren's birthdays and anniversaries, parents' death anniversaries
(many donors give on these days), gotra, nakshatra.

**Professional / wealth** — company or companies owned, industry, products
(for in-kind asks — cement, steel, ACs, refrigerators…), countries of
business, approximate net worth. Also car number where known.

**Relationship** — assigned preacher, source of the lead, which programmes
they're interested in (Yatra, donations, food products such as Vasudha, etc.).

**Every touchpoint**, per channel — calls made and received (with outcome),
SMS, WhatsApp, RCS, email; visits/meetings; Yatras taken; donations given;
times they declined; campaign spend on them.

> Field list to be finalised by studying what Hello Leads, Tata Tele, Exotel
> and Dhananjaya already capture — **adopt their fields, don't reinvent them.**

## 5. Analysis and AI — what it should answer

- **Who is most likely to respond** — for Yatra, for donations, for food
  products, for in-kind donations.
- **Who to stop targeting** — e.g. contacted 25 times with no donation →
  stop campaigning to them.
- **Who to cultivate** — e.g. donates every month → visit, give prasadam.
- **What's coming up** — birthdays, anniversaries, death anniversaries →
  timely reminders to the right preacher.
- **Return on spend** — money spent on campaigns per contact vs. what came back.

## 6. Constraints and compliance

- Donor data is **sensitive**: PAN, Aadhaar, family details, wealth. Access
  must be role-based — a preacher sees their own donors only.
- Must comply with India's **DPDP Act 2023** — consent for messaging (especially
  the 20-crore cold list), purpose limitation, and the right to erasure.
- Aadhaar numbers should only be stored if legally required, and then masked
  and encrypted.
- Dhananjaya access must be limited to **DMT-department donors only** — this is
  the condition for getting approval from Lakshmikant, Satyagar and
  Rajaram Prabhu.

## 7. Current state of the cold data

- ~20–25 crore numbers, held in the CRM Sachi Prabhu built.
- It is hosted on a **local server at Sachi Prabhu's place**, which is **not up
  right now** — the data is effectively offline.
- It was hosted locally to avoid cloud cost at the time. It needs to move
  online (Google Cloud) as part of this project.
- Sachi Prabhu's contact details: get from the team (not stored in this repo).

## 8. Next steps

- [ ] Get access to Hello Leads, Tata Tele and Exotel (from Hemchand) and
      export their field lists / sample data — this defines the data model.
- [ ] Get Sachi Prabhu's contact, bring the cold-data server back online,
      and check the data format.
- [ ] Export the ~60k DMT donors from Dhananjaya (manual, Phase 1).
- [ ] Confirm the campaign tool name ("Carex"?) and what history it can export.
- [ ] Draft the architecture on Google Cloud and the data model for review.
- [ ] Fix a **daily status-call time**, including while Prabhu is travelling
      to the dham.
