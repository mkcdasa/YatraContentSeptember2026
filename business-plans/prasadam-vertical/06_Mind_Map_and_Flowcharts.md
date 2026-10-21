# Prasadam, Sweets & Savories Vertical: Mind Map & Flowcharts

Hare Krishna Golden Temple (ISKCON), Banjara Hills, Hyderabad · v1.2, 21 October 2026

GitHub renders these Mermaid diagrams. The fully detailed, clickable mind map is `03_Mind_Map.html` (open it in any browser).

## Mind map (overview)

```mermaid
mindmap
  root((Prasadam Vertical))
    Audiences
      Visitors & festivals
      Donors
      Internal depts
      Companies & institutions
      Communities
      Online & NRI
    Revenue streams
      Stalls & restaurant
      Corporate gifting
      White-label
      E-commerce
      Catering
      QSR & export
    Products
      Chikkis & laddus
      Kaja & khara
      Namkeen
      Puri unde
      Pickles & powders
      Gift boxes
    Pricing
      Mass tier
      Premium tier
      Internal price
      B2B volume slabs
    Marketing
      ISKCON brand
      Databases & AI
      WhatsApp & SMS
      Google & Meta ads
      Owner meetings
    Operations
      Kitchen + 1 hire
      Recipes & costing
      Shelf-life tests
      Dispatch
      FSSAI & GST
    Roadmap
      0 Foundation
      1 Dasara-Diwali pilot
      2 Launch channels
      3 Scale Hyderabad
      4 Unit & QSR
      5 National & export
    Governance
      DMTT ROI
      Weekly review
      Risk register
      KPIs
```

## Order-to-delivery flow (all channels)

```mermaid
flowchart TD
  A[Order comes in] --> B{Channel?}
  B -->|Internal dept| C[Weekly standing order<br/>fixed delivery day]
  B -->|Corporate / white-label| D[Quote + 50% advance<br/>sticker proof approved]
  B -->|Online store / Amazon| E[Shopify / Amazon order]
  B -->|Festival stall| F[Pre-packed combos<br/>UPI at counter]
  C --> G[Order system<br/>tag stream + campaign]
  D --> G
  E --> G
  F --> G
  G --> H[Production plan<br/>weekly + festival calendar]
  H --> I[Cook in temple kitchen]
  I --> J[QC + shelf-life check]
  J --> K[Pack + label<br/>MFD, best-before, FSSAI]
  K --> L{Delivery}
  L -->|Hyderabad B2B| M[Own vehicle]
  L -->|Pan-India| N[Courier aggregator / Amazon]
  L -->|On campus| O[Stall / restaurant]
  M --> P[Payment + feedback]
  N --> P
  O --> P
  P --> Q[DMTT ROI dashboard]
```

## Corporate gifting sales flow

```mermaid
flowchart TD
  A[Build target list<br/>chamber, BNI, Rotary, T-Hub, MNR, donors] --> B[Rank by staff size]
  B --> C[Warm intro by Mukunda Dasa]
  C --> D[Owner / HR meeting<br/>sample box + catalogue + price list]
  D --> E{Own brand or white-label?}
  E -->|Own brand| F[Pick tier: Seva / Utsav / Vaikuntha]
  E -->|White-label| G[Logo mock-up within 48 h]
  F --> H[Quote with volume slab + delivery date]
  G --> H
  H --> I{PO + 50% advance?}
  I -->|No| J[Follow up; next festival reminder]
  I -->|Yes| K[Lock production slot]
  K --> L[Produce, pack, sticker]
  L --> M[Dispatch before cut-off]
  M --> N[Collect balance; feedback call]
  N --> O[Add to festival calendar for repeat]
```

## Festival stall operations

```mermaid
flowchart TD
  A[Festival on calendar] --> B[Forecast from last year + pre-orders]
  B --> C[Book seasonal staff + raw material]
  C --> D[Produce shelf-stable stock early]
  D --> E[Map footfall: entrance, exit queue,<br/>Goshala path, stairs, garden, waterfall]
  E --> F[Set up row of stalls / pagodas<br/>+ lawn food court]
  F --> G[Sell: combos + UPI + hourly restock]
  G --> H{Stock left?}
  H -->|Yes| I[Sell online / Instagram within 48 h]
  H -->|No| J[Record stock-out time for next year]
  I --> K[Post-festival review: sales, margin, hours]
  J --> K
```

## Decision and phase-gate flow

```mermaid
flowchart TD
  A[Plan sent by Mukunda Dasa] --> B[Production lead reviews with his manager]
  B --> C[Decision meeting: Mukunda Dasa + production lead + manager]
  C --> D{Approved?}
  D -->|Changes| A
  D -->|Yes| E[Foundation sprint: data, samples, pricing, sales kit, hire]
  E --> F[Pilot: Dasara + Diwali]
  F --> G{Pilot ROI positive?}
  G -->|No| H[Fix pricing / capacity / channels]
  H --> F
  G -->|Yes| I[Phase 2: e-commerce, communities, catering]
  I --> J[Phase 3: pagodas, pickles, 10x Janmashtami]
  J --> K{Demand proven?}
  K -->|Yes| L[Phase 4: dedicated unit + QSR pilot]
  L --> M[Phase 5: national + export]
```

## DMTT ROI tracking flow

```mermaid
flowchart LR
  A[Every order tagged<br/>stream R1-R14 + campaign] --> D[Monthly P&L by stream]
  B[Costs: ingredients, packaging,<br/>labour, marketing, overheads] --> D
  C[Weekly hours log<br/>DMTT, production, sales] --> D
  D --> E[ROI % = contribution / total cost]
  E --> F[One-page report to leadership]
```

## Roadmap timeline

```mermaid
timeline
  title Prasadam vertical roadmap
  26 Sep – 10 Oct 2026 : Foundation : Data, decisions and a ready-to-sell kit
  11 Oct – 30 Nov 2026 : Pilot: Dasara & Diwali : Prove corporate gifting, stalls and internal supply
  Dec 2026 – Mar 2027 : Launch channels : Year-round revenue and digital sales
  Apr – Sep 2027 : Scale in Hyderabad : 10× festival sales and new product lines
  Oct 2027 – Sep 2028 : Dedicated unit & QSR pilot : Own capacity, machinery and first outlets
  Year 3–5 : National & export : A national vertical with exports
```
