# CRM Landscape — Hare Krishna Golden Temple, Hyderabad

Running note of the CRMs the temple uses today, how data moves between them,
and what each one is for. Captured from the CRM discussion on 2026-10-19.
Add to this file as each remaining system is walked through.

## Systems at a glance

| System | Role | Primary users |
|---|---|---|
| **Hello Leads** ([helloleads.io](https://www.helloleads.io)) | Central lead capture and donor/contact database | Digital marketing, field preachers on mobile |
| **Tata Tele** | Tele-calling and call-outcome tracking | Tele-sales team |
| **Razorpay** | Online donation payments — feeds donor details into Hello Leads | Donors (automatic) |
| _Others_ | _"Multiple CRMs" mentioned — not yet covered_ | — |

## Data flow

```
Google Ads ─┐
Meta Ads   ─┼──►  Hello Leads  ──auto-sync──►  Tata Tele (tele-sales calls)
Razorpay   ─┘     (lead + donor DB)
                       │
                       └──► assigned to field preachers (donor / good-contact leads)
```

1. A person clicks a Google or Meta ad and submits their details.
2. The lead lands in Hello Leads automatically; the team gets an email
   notification for each new lead.
3. Every lead is auto-pushed from Hello Leads to Tata Tele.
4. Tele-sales calls the lead in Tata Tele and records the outcome there
   (interested / not interested / call back, plus what the person said).
5. Promising leads — donors, good contacts — are also assigned from Hello
   Leads to preachers in the field.
6. When someone donates through Razorpay, their details go straight into
   Hello Leads.

## Hello Leads

**Purpose:** capture paid-ads leads (Google Ads, Meta Ads, all paid channels)
and serve as the master database of contacts and donors. Tele-calling is
**not** done in Hello Leads — that happens in Tata Tele.

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

## Tata Tele

**Purpose:** tele-sales. Receives every lead from Hello Leads automatically.
Callers make the calls and record:

- What the person said
- Status: interested / not interested / call back

## Razorpay

Donations made through Razorpay create or update the donor record in Hello
Leads directly.

## Open items

- [ ] Get Hello Leads login credentials (promised) and review the account
      first-hand — fields, pipelines, integrations, plan limits.
- [ ] Document the other CRMs in use ("we have multiple CRMs").
- [ ] Confirm whether call outcomes from Tata Tele sync back into Hello Leads,
      or stay only in Tata Tele.
- [ ] Find out where the archived Excel exports (leads beyond 1 lakh) are
      stored and whether they are ever re-used.
- [ ] Confirm exactly which Razorpay fields map into Hello Leads.
