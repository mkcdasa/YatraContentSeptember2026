# CRM Landscape — Hare Krishna Golden Temple, Hyderabad

Running note of the CRMs the temple uses today, how data moves between them,
and what each one is for. Captured from the CRM discussions on 2026-10-19.
Add to this file as each remaining system is walked through.

> **Never commit logins, passwords or donor records to this repository.**
> Keep credentials in a password manager and refer to them here by owner only.

**Goal:** bring all of these systems into **one platform** — see
[UNIFIED-CRM-REQUIREMENTS.md](UNIFIED-CRM-REQUIREMENTS.md).

## Systems at a glance

| System | Role | Direction | Data held |
|---|---|---|---|
| **Hello Leads** ([helloleads.io](https://www.helloleads.io)) | Lead capture + mobile donor/contact database | Inbound from ads | Paid-ads leads, donor profiles (capped at 1 lakh) |
| **Tata Tele** (TataBusiness.com) | Tele-sales CRM | Outbound calls (also receives inbound leads) | Call remarks, status, callbacks, deal stage |
| **Exotel** | Cloud telephony for the public numbers | Inbound calls | Call recordings, caller numbers |
| **Razorpay** | Online donation payments | — | Feeds donor details into Hello Leads |
| **Cold-data CRM** (built by Sachi Kumar Gauranga Das) | Bulk prospect database | Outbound / campaigns | ~20 crore cleaned phone numbers |
| **Donation websites** (harekrishnagoldentemple.org and others) | Online donation pages | Inbound | Feed every donation into Dhananjaya |
| **Dhananjaya ERP** (Donor Care Center) | Temple-wide donation ERP and receipt generator, open-source | — | Live donations; ~60–70k DMT-department donors |

## Data flow

```
Google / Meta / LinkedIn / Bing / ChatGPT Ads ─┐
Razorpay donations ────────────────────────────┼──►  Hello Leads ──┬──► Tata Tele ──► tele-sales executives
                                               │   (lead + donor   │    (outbound calls, remarks,
                                               │    database)      │     callbacks, deal stage)
                                               │                   └──► field preachers (donors / good contacts)
                                               │
Public calls to temple / Yatra numbers ──► Exotel ──► rings 5–10 executives at once ──► Tata Tele

Donation websites (harekrishnagoldentemple.org, …) ──► Dhananjaya ERP ──► donation receipt (PDF)
Donations entered by preachers in the Dhananjaya app ─┘   (all temple donors; mobile app only, no API yet)

Yatra websites — separate from the donation websites; NOT linked to Dhananjaya
Cold-data CRM (20 crore numbers) — separate, not linked
```

## Hello Leads

**Purpose:** capture leads from every paid channel — Google Ads, Meta Ads,
LinkedIn Ads, Bing Ads, ChatGPT Ads — and serve as the master database of
contacts and donors. A person sees the ad, submits name and mobile number,
and the lead lands in Hello Leads; the team gets an email for each new lead.
Tele-calling is **not** done here.

From Hello Leads, leads are routed two ways:

- **Tata Tele** — for the tele-sales team to call.
- **Field preachers** — donors and good contacts are assigned directly.

**Why we use it:** the mobile UI/UX is very good. A preacher travelling to
meet donors can pull up everything on their phone:

- Donor name, mobile number, email address
- Google Maps location
- Donation history — what was given and when
- Nakshatra and gotra
- Birthday and wedding anniversary

**Cost constraint:** it is expensive, so the account is capped at
**1 lakh (100,000) leads**. When the count goes over, older leads are
downloaded and archived to Excel sheets and removed from Hello Leads.

**Razorpay:** when someone donates through Razorpay, their details go straight
into Hello Leads.

## Tata Tele — outbound tele-sales

**Purpose:** the tele-sales CRM for **outbound** calls. Leads arrive from Hello
Leads (and inbound callers arrive from Exotel — the two are integrated) and are
**auto-assigned** to tele-sales executives.

For each lead the executive calls and records:

- Remarks — what the person said
- Status — interested / not interested / call back later
- Appointment or callback date (e.g. "call me after a month, I'm abroad").
  On that date the executive gets an automatic email reminder/notification.

Each executive has a **dashboard** showing interested vs not interested,
which yatra the lead is for, and the deal stage (closed / not closed /
in progress). The complete customer interaction history lives in Tata Tele.

## Exotel — inbound calls

**Purpose:** handle calls **from** the public to the temple's published
numbers, and capture those callers as hot leads — someone who calls is
already interested.

| Number | Published as | Treated as |
|---|---|---|
| 95053 88886 | Yatra Department number — social media, posters, websites | Every caller is a Yatra enquiry |
| 95056 88881 | HKGT / Golden Temple contact number — published everywhere | General / all other purposes |

**How a call is handled today:**

- The old IVR menu ("Welcome to Hare Krishna Golden Temple… press 1 for Yatra,
  2 for Donor Care Center, 3 for food, 4 for congregation") has been
  **removed on both numbers** — callers didn't have the patience for it.
- Instead, the call **rings 5–10 executives' mobiles simultaneously**
  (~10 tele-sales executives). Whoever picks up gets that lead assigned
  by default.
- **Every call is recorded**, so executives know conversations are monitored.
- Inbound callers also flow into Tata Tele.

**Owners:** Hemchand and Venkatesh handle the technical side.

## Cold-data CRM

- A separate CRM built by **Sachi Kumar Gauranga Das** (already demoed).
- Started from ~**50 crore** phone numbers; filtered by name and cleaned with
  Python down to ~**20 crore**.
- Not connected to Hello Leads or Tata Tele.

## Donation websites

Dhananjaya does not collect donor data on its own — it receives it from the
donation websites. **Document the websites before Dhananjaya** when mapping
the flow.

- **harekrishnagoldentemple.org** — main donation website; every donation made
  here flows into Dhananjaya, which generates the receipt.
- **thehkm.org** — another donation site.
- In total there are **4–5 websites**, one per channel: SMS, WhatsApp,
  RCS marketing, and Google/Meta Ads each have their own landing site.
- **Yatra is completely separate.** The Yatra websites are not the donation
  websites and are not linked to Dhananjaya. (Yatra flow to be mapped as its
  own "step one".)

## Dhananjaya ERP — Donor Care Center (DCC)

- Web dashboard: [erp.hkmhyd.org.in](https://erp.hkmhyd.org.in/app/seva-donation-dashboard).
- Open-source ERP used temple-wide by the Donor Care Center. **All donation
  receipts are generated here only** — whether the donation came from a
  website or was entered by a preacher. It is **live data**, updated every day.
- Holds ~**60k donors** from our (DMT) department — under our login plus two or
  three other preacher codes — alongside every other preacher's donors.
- **Access today:** mobile app only. Our login shows the donation report but
  **not full donor details** — no permission yet. No web/API access.
- Donor data is sensitive; privacy and confidentiality are strictly maintained.

**What the mobile app does (walkthrough):**

- **Search donor** → donor profile with a **unique donor ID**, mobile number,
  email, address, PAN, Aadhaar, assigned **preacher name**, gotra, nakshatra.
- **Stats** — total donated, partnership, breakdown by trust.
- **Donation receipts** — list of each donation (amount, date); tap one to open
  the PDF receipt.
- **Send WhatsApp or email** to the donor directly from the app.
- **Reminders** — set a date and custom message: birthday, wedding anniversary,
  death anniversary, anything else.
- **Festival seva slot booking** — the amount on a donor's receipts can be
  **redeemed** to book festival seva slots. Purely amount-based, no
  discretion: you can only book up to what has been donated.

**Data-quality issue — duplicate donors:** a donor is supposed to have exactly
one donor ID, but in practice the same person can have **several donor IDs**
(created under different names or trusts). Any integration will need
de-duplication.

**Path to API integration:**

1. Lakshmikant Prabhu (Finance / DCC) to request approval.
2. Satyagar Prabhu to approve (we will also ask him directly).
3. Rajaram Prabhu (develops the ERP) to build the integration.
4. All of us to meet on Zoom.

Expected concern: that we'd pull other preachers' donor data. We must clearly
justify and limit the scope to **DMT-department donors only** — the "how" to be
worked out with Rajaram Prabhu.

## Open items

- [ ] Get Hello Leads login and review the account — fields, pipelines,
      integrations, plan limits.
- [x] Walkthrough of the Dhananjaya mobile app (done 2026-10-19).
- [ ] List all 4–5 donation websites with their exact URLs and channel
      (SMS / WhatsApp / RCS / Ads).
- [ ] Clarify how Razorpay fits: does a website donation go to Hello Leads
      (via Razorpay), to Dhananjaya, or both?
- [ ] Map the Yatra flow separately (websites, enquiries, bookings).
- [ ] Plan de-duplication of donor IDs before any Dhananjaya integration.
- [ ] Set up the Zoom meeting with Lakshmikant, Satyagar and Rajaram Prabhu
      for Dhananjaya API access (DMT donors only).
- [ ] Clarify: does **every** Hello Leads lead go to Tata Tele, or only a
      selected subset? (Mentioned both ways.)
- [ ] Confirm whether Tata Tele call outcomes sync back into Hello Leads.
- [ ] Find where the archived Excel exports (leads beyond 1 lakh) are stored.
- [ ] Confirm which Razorpay fields map into Hello Leads.
- [ ] Check the consent / DPDP Act position before calling or messaging the
      20-crore cold-data list.
- [ ] Document any remaining CRMs not yet covered.
