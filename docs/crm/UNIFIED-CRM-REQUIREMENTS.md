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
| Bulk messaging providers — **Karix, PayTM Intelligence, GupShup, Tata** (SMS / RCS / WhatsApp to crores of numbers from the cold data) | Per message: sent, delivered, not delivered, etc. | API integration with each provider |
| Google Contacts / phone contacts | Fresh contacts | Daily sync by AI agents |
| WhatsApp / email messages | New contact details people send us | AI extraction → save as contact |
| Excel sheets | Archived Hello Leads leads (beyond 1 lakh), any other lists | Direct Excel import |

## 2a. Source-data migration plan by stage (from Prabhu's written plan)

Purpose of all data: **Fund Raising marketing and Yatra marketing.**

### Stage 1 — existing sources

| Source | Plan |
|---|---|
| **Hello Leads** ([helloleads.io](https://www.helloleads.io/)) — Google Ads & Meta Ads, online DMT leads | All **new** leads stored directly to the cloud |
| **Exotel** ([exotel.com](https://exotel.com/)) — inbound IVRS on **95053 88886** (Yatra) and **95056 88881** (HKGT); 10 employees' mobiles ring simultaneously | Bring inbound call data to the cloud |
| **Tata Tele** ([tatatelebusiness.com](https://www.tatatelebusiness.com/)) — tele-caller remarks | **Bridge connection**: updates from Tata Tele flow into the cloud |
| **Cold data (DBMS)** — 20 crore contacts on Sachi Kumar Gauranga Dasa's computer (acting as the server) | Move to the cloud, with a **monthly / occasional import** function |
| **Messaging providers** — Karix, PayTM Intelligence, GupShup, Tata | API integration: messages sent, delivered, not delivered, etc. |

### Stage 2 — event leads

- Temple festival leads and gated-community event leads (via Hello Leads) →
  live data saved directly to the ERP through a form → **synced to the cloud
  daily**.
- Websites: [thehkm.org](https://thehkm.org/),
  [harekrishnagoldentemple.org](https://harekrishnagoldentemple.org/).

### Stage 3 — ERPs and spreadsheets

- **Yatra ERP** → Yatris data → live data, **synced daily** to the cloud
  (plan lists "60k donors" here — confirm whether that figure belongs to the
  Yatra ERP or to Dhananjaya).
- **Dhananjaya ERP** ([erp.hkmhyd.org.in](https://erp.hkmhyd.org.in/app/seva-donation-dashboard))
  → field-preacher (LLP) donors → live data, **synced daily** to the cloud
  (requires the API approval described in §6).
- **Excel data** → imported directly to the cloud with an import function.

### Stage 4 — AI agents

- Save new contact details that surface in personal communication
  (WhatsApp, email, SMS, etc.).
- Sync fresh contacts **daily** from Google Contacts / phone contacts.

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
- [ ] Get API access / delivery-report docs from Karix, PayTM Intelligence,
      GupShup and Tata.
- [ ] Get access to the Yatra ERP and confirm what Yatri data it holds.
- [ ] Confirm the "60k donors" figure — Yatra ERP or Dhananjaya?
- [ ] Draft the architecture on Google Cloud and the data model for review.

## 9. Working rhythm

- **One status call per day at 2:30** with Prabhu (AM or PM to confirm —
  night-time was mentioned as the only time that works). One call only, not
  many through the day.
- This project is the main priority on that call: CRM progress first, other
  topics after.
- These notes are to be shared on Slack as well.
