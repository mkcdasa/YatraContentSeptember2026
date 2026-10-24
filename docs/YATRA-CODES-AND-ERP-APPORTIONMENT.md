# Punyakshetra Yatra Codes & ERP Cost Apportionment

Project document for the Finance team · ISKCON / Hare Krishna Movement Hyderabad · Punyakshetra Yatra
As of 24 October 2026. Shareable, editable copy: https://claude.ai/artifact/WH9Bzy6cFFzM4DEBfY8qMt

## 1. Executive summary

Every rupee the yatra business earns or spends should carry one short, human-readable Yatra Code, so the ERP can print a true profit and loss for every yatra and every departure without any manual spreadsheet work. This document gives the Finance team that code standard, the full code catalogue, the cost and revenue heads, the marketing channel codes, the overhead apportionment rules and the ERP configuration needed to make it work.

The code reads like the yatra itself. `CDH-5N6D` is Char Dham by Helicopter, 5 nights 6 days. `CDH-5N6D-26B03` is its third 2026 departure. `KMSL-12N13D` is Kailash Manasarovar by land, 13 days. `AHB-1N2D` is the Ahobilam weekend yatra. A coordinator, a telecaller, an accountant and the ERP all use the same string.

Why this is needed now, from what the current files show:

- The FY 2026-27 yatra report (April to August 2026) records receipts of Rs 6.44 crore and a gross surplus of Rs 87 lakh, but the overhead lines show `#REF!` errors and last year's Rs 76.36 lakh of common expenses were split 50:50 between Summer Char Dham and Manasarovar by assumption, not by any driver.
- Between April and August 2026 the common pool (advertisements Rs 22.7 lakh, staff cost Rs 46.6 lakh, other expenses Rs 13.0 lakh, total Rs 82.2 lakh) was only partly apportioned; Rs 69.4 lakh was still pending apportionment in the provisional report.
- Revenue is tagged by Seva Code and Preacher Code in the donation system, but expenses are tagged only by ledger and trust, so marketing spend, telesales salaries and coordinator travel cannot be traced to the yatra they served.
- Vendor advances from the 2019 Char Dham (Monal Resort, Shivalik Valley, Godwin Hospitality and others) still appear as open advances in the HoD advance list, which shows that advances are not being closed against yatra-tagged invoices.
- The Source of the lead column in the 2026 registration sheets (USA, Vrindavan) is blank, so cost per booking by channel cannot be computed today.

What the finance team gets from this document:

1. A code standard and a catalogue of 70 plus yatra codes covering every yatra in the 2026 brochures, the weekend yatra brochure, the 2026-27 report and the 2027 plans.
2. A departure (batch) numbering rule, and the hierarchy Yatra, Batch, Pilgrim that every transaction attaches to.
3. A chart of cost heads for direct yatra costs, with the account numbers and the vendor types seen in past yatra reports.
4. Revenue, GST, TCS, refund and donation tagging rules.
5. Marketing and sales channel codes with a campaign code format that the ad platforms, the SMS and WhatsApp vendors, telesales and AI voice calling can all carry.
6. A three-tier apportionment model for salaries, rent, electricity, software, administration and fixed assets, with drivers and a worked example on real 2026 numbers.
7. ERP master data, mandatory field rules, validations and the monthly close procedure.
8. The reports and KPIs management will receive, and a phased rollout plan to go live for departures from January 2027.

Sources used: the Yatra Calendar 2026 workbook, the two 2026 brochures (All Yatras in 2026 and Weekend Yatras), the FY 2026-2027 Yatra Reports August 2026 workbook, Updated Salaries and Fixed Expenses Sep 2026, Monthly Salaries and Monthly Expenses 2025, the Char Dham and Vrindavan, Kumbh Mela and Ayodhya, Sri Lanka, Puri and Dwaraka, and Nepal revenue and expenditure reports, the USA 2025 budgeting and costing sheet, the Kailash 2026 and Amarnath and Vaishno Devi sheets, the Char Dham cost calculators, the Paid Marketing Plan, the Telugu AI voice agent script, and vendor mails (Heli Yatra, Veena World, Adiona, Karix, Google and Facebook ad invoices).

## 2. Scope, objectives and design principles

The system covers every yatra sold under the Punya Kshetras brand of Hare Krishna Golden Temple, Hyderabad, whichever trust books the revenue or pays the bill. Today that spans five legal entities: Hare Krishna Movement Hyderabad (HKMH), Hare Krishna Movement India (HKMI), Touchstone Foundation Hyderabad (TSFH), Radha Govinda International (RGI) and Golden Avatar (GAVPL), plus partner temples who share yatras (HKM Madhya Pradesh, HKM Chennai, ISKCON Bangalore, Vaikuntha Chaitanya Mission). The code is the same across all of them. Entity is a separate ERP dimension.

**Objectives**

1. One code per yatra product, one sub-code per departure, used on every sales receipt, purchase order, vendor invoice, expense claim, salary allocation and marketing invoice.
2. Gross profit per departure visible within 15 days of the return date, net profit after overhead within 30 days of month end.
3. Marketing cost per lead and per booking by channel and by yatra, so ad budgets follow proven returns.
4. Vendor advances, pilgrim receivables and refunds tracked per departure, so no advance stays open after a yatra closes.
5. Inter-trust and partner-temple sharing settled by a documented rule, not by memory.

**Design principles for the code**

| Principle | What it means in practice |
| --- | --- |
| Readable, not numeric | A person reads `CDH-5N6D` and knows the yatra. No lookup needed. The ERP keeps an internal numeric ID for joins. |
| Short enough to type | Yatra code 7 to 11 characters, departure code 13 to 17 characters. Fits a receipt line, an SMS template name and a Google Ads campaign name. |
| Stable | A yatra code never changes once issued. If the product changes materially (new duration, new mode), a new code is issued and the old one is retired, never reused. |
| One meaning per segment | Destination, mode of travel, nights and days each occupy a fixed position, so sorting and filtering work in any spreadsheet or ERP. |
| Batch is a child, never a new product | The same product repeated nine times in a season is one yatra code with nine batch codes. Profitability rolls up from batch to yatra to category to year. |
| Attributes live in master data, not the code | Price tier (General or Premium), trust, season, min pax, preacher and partner temple are fields on the master or on the transaction, so the code stays short. |
| No orphan money | Every profit-and-loss transaction must carry either a yatra code, an overhead pool code or a non-yatra code. The ERP rejects a posting without one. |

**Out of scope for this document**: temple donation sevas that are not yatras, the Kalyanam and eCommerce lines named in the hiring plan, and the website and CRM build. They get their own codes under the same pattern later.

## 3. The Yatra Code standard

A yatra code has three segments joined by a hyphen: destination, mode of travel and duration. A departure code adds a fourth segment for the year and batch number.

```
YATRA CODE      DEST + MODE  -  nN mD
                CDH          -  5N6D          Char Dham, Helicopter, 5 nights 6 days

DEPARTURE CODE  DEST + MODE  -  nN mD  -  YY B nn
                CDH          -  5N6D   -  26 B 03    third 2026 departure of that yatra
```

**Segment 1: Destination** (2 to 4 capital letters). The first letters of the place or the yatra theme. The full list is in section 4. Examples: `CD` Char Dham, `KMS` Kailash Manasarovar, `SLR` Sri Lanka Ramayan, `AHB` Ahobilam, `USA` United States temples.

**Segment 2: Mode of travel** (1 capital letter, appended to the destination without a space). It states the defining mode that drives cost and price, not every vehicle used.

| Letter | Mode | Use when | Examples |
| --- | --- | --- | --- |
| H | Helicopter | Helicopter charter is the main cost and the selling point | `CDH`, `DDH`, `KBH`, `AVDH` |
| A | Aerial darshan by aircraft | Fixed-wing flight darshan (Kailash aerial) | `KMSA` |
| L | Land route across a border | Overland by coach through Nepal and Tibet | `KMSL` |
| R | Road | Bus, coach or car is the main transport within India; flights to the start city are pass-through | `CDR`, `PDSR`, `VRNR` |
| F | Flight-based international | International air package where flights are included in the price | `USAF`, `EURF`, `SLRF`, `CTHF` |
| T | Train | Train is the main transport | `MYPT` |
| S | Ship or cruise | Cruise or ferry is the main leg | reserved |
| W | Weekend | 1 night 2 days domestic weekend yatra by road or short flight | `AHBW`, `TPTW`, `KSHW` |

The W mode replaces R for the weekend brochure products so that the whole weekend family sorts and reports together.

**Segment 3: Duration** nights then days, written `5N6D`. Always write both. A day trip is `0N1D`. The 13-day Kailash land yatra is `12N13D`.

**Segment 4: Departure (batch)** `YYBnn`. YY is the last two digits of the departure year, B is the literal letter, nn is the batch serial within that calendar year in date order starting at 01. Batch serials restart every year. A cancelled batch keeps its serial and is flagged cancelled in the master; the serial is never reissued.

**Examples read aloud**

| Code | Reads as |
| --- | --- |
| `CDH-5N6D` | Char Dham by helicopter, 5 nights 6 days (the product) |
| `CDH-5N6D-26B01` | Its first departure of 2026 (25 to 30 April 2026) |
| `DDH-3N4D-26B02` | Do Dham by helicopter, 3 nights 4 days, second 2026 departure |
| `KMSL-12N13D-26B03` | Kailash Manasarovar land route, 13 days, third 2026 batch (16 August 2026) |
| `USAF-16N17D-26B02` | USA East and West Coast temples, 17 days, second 2026 departure (21 September 2026) |
| `AHBW-1N2D-26B04` | Ahobilam weekend yatra, fourth 2026 weekend |
| `SLRF-9N10D-26B01` | Sri Lanka Ramayan with Srirangam, 10 days, first 2026 batch |

**Rules the ERP enforces**

1. Uppercase only, hyphen as the only separator, no spaces.
2. Destination plus mode is unique in the master. Two products with the same destination, mode and duration are the same product and share one code; a different itinerary of the same length gets a version note in the master, not a new code.
3. A yatra code is created only by Finance on request from the Yatra Manager, through the master data form in section 10. Sales, marketing and vendors cannot invent codes.
4. Departure codes are generated by the ERP from the start date. Nobody types the serial.
5. Three reserved prefixes exist beside yatra codes: `OH-` overhead pools, `NY-` non-yatra activity that passes through yatra bank accounts, and `GRP-` custom private group yatras (section 4). They follow the same tagging rules so nothing is left untagged.

**Why not the existing seva codes**: the donation system today uses free-text seva codes such as `KUMBHYA`, `NEPAL MUKTINATH YATRA` and `PURI YATRA`. They identify the yatra but not the year, the batch or the mode, and they are not consistent across trusts. The new yatra code becomes the seva code for all yatra receipts from go-live, and the old codes are mapped to the new ones in the appendix for historical reporting.

## 4. Master Yatra Code catalogue

The catalogue below assigns a code to every yatra found in the 2026 brochures, the Weekend Yatras brochure, the Yatra Calendar 2026 workbook, the FY 2026-27 report and the 2027 planning sheets. Prices are the published General tier amount before 5 percent GST, and exclude flights unless stated. Where the source gives no duration the Nights and Days segment is marked confirm and the Yatra Manager fills it before the code is activated. The master sheet ALL YATRAS WITH DATES AND BUDGET in the Yatra Calendar 2026 workbook (182 rows) remains the source for batch dates and both price tiers; Finance should reconcile every row of that sheet to this catalogue during Phase 1.

**A. Himalayan and North India premium yatras**

| Code | Yatra | Duration | Published price (Rs) | 2026 batches and notes |
| --- | --- | --- | --- | --- |
| `CDH-5N6D` | Char Dham by Helicopter (Yamunotri, Gangotri, Kedarnath, Badrinath) | 5N6D | 2,94,999 + GST, ex flights | 9 batches 25 Apr to 20 Jun 2026, 12 seats each; also Sep to Oct post-monsoon. B2B cost Rs 2,07,000 per pax (Heli Yatra pre-block) |
| `DDH-3N4D` | Do Dham by Helicopter (Kedarnath, Badrinath) | 3N4D | 1,88,000 + GST | B2B cost Rs 1,32,000 per pax; family and charter variants priced per calculator |
| `KBH-1N2D` | Kedarnath and Badrinath by Helicopter | 1N2D | 1,35,999 + GST, ex flights | From Oct 2024 posting calendar |
| `KBH-2N3D` | Kedarnath, Badrinath, Rishikesh by Helicopter | 2N3D | 1,56,999 + GST | From 2025 cost calculator |
| `CDR-confirm` | Summer Char Dham by road (SCDY) | confirm | per batch costing | FY 2026-27 report: May to Jun 2026 receipts Rs 2.89 crore, surplus Rs 48.6 lakh. The 2019 edition had 95 pax at Rs 74,000 |
| `CDRW-confirm` | Winter Char Dham by road (Winter Summerdham) | confirm | per batch | Oct 2026 provisional: 6 pax, Rs 13 lakh revenue |
| `KMSL-12N13D` | Kailash Manasarovar land route ex Kathmandu | 12N13D | 2,99,000 + 5% GST + 5% TCS | Batches 31 May, 5 Jul, 16 Aug 2026; Sep 2026 batch 2 had 15 pax, Rs 67.7 lakh receipts |
| `KMSA-2N3D` | Kailash Manasarovar Aerial Darshan (Nepalgunj) | 2N3D | 75,000 + GST + Lucknow flights | Maha Shivaratri 14 to 16 Feb 2026; 25 and 30 pax aerial batches Feb and Mar 2026 |
| `KMSA-5N6D` | Kailash Aerial Darshan with Kashi, Ayodhya, Triveni | 5N6D | 1,08,000 + GST + flights | 11 to 16 Feb 2026 |
| `NMKF-5N6D` | Nepal Muktinath Yatra (with Pokhara to Jomsom flights) | 5N6D | 95,000 + GST + 5% TCS | 24 May 2026 batch; 2022 edition 55 pax at Rs 39,000 operator cost |
| `NMKF-confirm` | Nepal Muktinath, Janakpur, Lumbini add-on variant | confirm | per quote | Named in the AI voice script and 2027 Muktinath plus Kailash sheet |
| `MKKL-confirm` | Muktinath plus Kailash combined (2027) | confirm | per quote | 5 batches planned May to Sep 2027 (10 May, 8 Jun, 8 Jul, 6 Aug, 5 Sep) |
| `AVDH-7N8D` | Amarnath and Vaishno Devi by Helicopter with Kashmir | 7N8D | 1,00,000 + GST, ex flights | Jul 2025 pilot (4 pax); direct cost Rs 65,650 to 75,650 per pax |
| `VSDH-3N4D` | Vaishno Devi by Helicopter | 3N4D | 50,000 + GST, ex flights | Direct cost Rs 29,850 to 41,100 per pax; 2027 dates 9 Jan, 6 Feb, 13 Mar |
| `KAT-3N4D` | Kashi, Ayodhya, Triveni Sangam (Magha Mela special) | 3N4D | 40,000 + GST, ex flights | 11 to 14 Feb 2026 |
| `KTS-2N3D` | Kashi and Triveni Sangam | 2N3D | 35,000 + GST, ex flights | Window 10 Jan to 16 Feb 2026; Jul 2026 Kashi batch had 7 lakh receipts |
| `KRA-2N3D` | Shivaratri special: Kashi, Rameshwaram, Arunachalam | 2N3D | 55,000 + GST, ex flights | 14 to 16 Feb 2026 |
| `VRNR-3N4D` | Vrindavan Holi Yatra | 3N4D | 45,000 + GST, ex flights | 1 to 8 Mar 2026 window |
| `VRNR-4N5D` | Vrindavan Yatra (Kartik or November) | 4N5D | 55,000 + GST + flights pass-through | 2 to 6 Nov 2026, single supplement Rs 10,000 to 12,000 |
| `VRND-confirm` | Vrindavan Donors Yatra (FOLK and donor groups) | confirm | 49,000 (2019) | 24 pax in 2019; donor relationship yatra, costed separately |
| `BDK-3N4D` | Baidyanath and Kamakhya | 3N4D | 40,000 + GST, ex flights | 11 to 14 Mar 2026, ends at Bengaluru |
| `UBY-confirm` | North (Uttara) Bharat Yatra | confirm | per quote | Oct to Nov 2026 provisional, 5 pax, Rs 12 lakh |
| `KMB-confirm` | Kumbh Mela and Ayodhya | confirm | per edition | Prayagraj 2019: 3 batches, 119 pax, Rs 23.2 lakh; 2025 Kumbh costing sheet exists |
| `MYPT-4N5D` | Mayapur Yatra | 4N5D | per budget | 17 to 21 Jun 2025 budget; 2018 costing |
| `PURR-2N3D` | Puri Jagannath Ratha Yatra | 2N3D | 35,000 + GST, ex flights | 15 to 17 Jul 2026; Jul 2026 receipts Rs 4.7 lakh |
| `PKMR-confirm` | Puri, Jagannath, Konark, Mayapur combined | confirm | per quote | Named in the AI voice script |

**B. South and West India premium yatras**

| Code | Yatra | Duration | Published price (Rs) | 2026 batches and notes |
| --- | --- | --- | --- | --- |
| `AHBR-1N2D` | Ahobilam Nava Narasimha Yatra | 1N2D | 10,000 + GST | 28 to 29 Mar 2026 (brochure); weekend brochure lists Rs 24,999, reconcile tier |
| `MDSR-2N3D` | Madurai and Srirangam | 2N3D | 35,000 + GST, ex flights | 9 to 11 Jan 2026 |
| `MLDR-2N3D` | Malainadu Divya Desam (Kerala) | 2N3D | 30,000 + GST, ex flights | 27 to 29 Mar 2026 |
| `PDSR-5N6D` | Pancha Dwaraka and Somnath | 5N6D | 55,000 + GST, ex flights | 24 to 29 Jan 2026; 2020 Dwaraka edition Rs 10.05 lakh revenue |
| `WBYR-confirm` | West Bharat Yatra 2027 (USA group, Laxmi Mataji) | confirm | per quote | Private group, code under GRP rules below |
| `UDPR-confirm` | Udupi and coastal Karnataka | confirm | per edition | Revenue and expenditure account exists for a UDP yatra |

**C. International yatras**

| Code | Yatra | Duration | Published price (Rs) | 2026 batches and notes |
| --- | --- | --- | --- | --- |
| `USAF-16N17D` | USA East and West Coast ISKCON temples | 16N17D | 5,49,000 incl flights + 5% GST + 5% TCS | 22 Apr to 8 May 2026 and 21 Sep to 7 Oct 2026; Oct 2026 provisional 107 pax, Rs 1.12 crore. Veena World land package 30 pax; 2025 edition 36 pax with GAVPL and HKM MP |
| `USAF-E-confirm` | USA East Coast only | confirm | per Adiona and Veena World quotes | 9-day and Chicago 3N4D variants priced for 2 pax |
| `USAF-W-confirm` | USA West Coast only | confirm | per quote | Adiona proposal Sep 2026 |
| `EURF-14N15D` | Wonders of Europe with ISKCON temples | 14N15D | 5,25,000 incl GST, TCS, flights, visa, insurance | 1 to 15 Jun 2026; 2024 edition included Dubai and UK |
| `UKEF-confirm` | UK and Europe (Bhaktivedanta Manor, Radhadesh) | confirm | per quote | Payments to Golden Avatar tracked in a separate sheet |
| `SLRF-7N8D` | Sri Lanka Ramayan Yatra | 7N8D | 85,000 + GST, ex flights | 21 to 28 Feb 2026; Feb 2022 edition 27 pax, Rs 20.2 lakh revenue, 37% margin |
| `SLRF-9N10D` | Sri Lanka Ramayan with Srirangam (Magha Masam) | 9N10D | 1,25,000 + 5% TCS + 5% GST + flights | 20 Feb to 1 Mar 2026 |
| `CTHF-confirm` | Cambodia and Thailand (Angkor Wat) | confirm | per quote | Named in the AI voice script positioning |

**D. Weekend yatras** (all `W` mode, 1N2D, Rs 24,999 + GST ex flights, from the Weekend Yatras 2025-26 brochure)

| Code | Weekend yatra | Code | Weekend yatra |
| --- | --- | --- | --- |
| `AHBW-1N2D` | Ahobilam | `MGLW-1N2D` | Mangalagiri |
| `ARNW-1N2D` | Arunachalam | `MYSW-1N2D` | Mysore |
| `AYOW-1N2D` | Ayodhya | `NGNW-1N2D` | Nageshwarnath (28 Oct, 4, 11, 18 Nov) |
| `BDCW-1N2D` | Bhadrachalam | `NMSW-1N2D` | Naimisharanya |
| `CDBW-1N2D` | Chidambaram | `NSKW-1N2D` | Nasik |
| `CKTW-1N2D` | Chitrakoot | `PLNW-1N2D` | Palani |
| `DWKW-1N2D` | Dwaraka | `PDPW-1N2D` | Pandharpur |
| `GVRW-1N2D` | Guruvayur | `PURW-1N2D` | Puri |
| `HMPW-1N2D` | Hampi | `RMSW-1N2D` | Rameshwaram |
| `HRDW-1N2D` | Haridwar | `RSKW-1N2D` | Rishikesh |
| `KNCW-1N2D` | Kanchipuram | `SMHW-1N2D` | Simhachalam |
| `KKMW-1N2D` | Kanyakumari | `SOMW-1N2D` | Somnath (Kartik Somavaram) |
| `KSHW-1N2D` | Kashi | `SRGW-1N2D` | Srirangam |
| `KKSW-1N2D` | Kukke Subramanya | `TNJW-1N2D` | Thanjavur |
| `KBKW-1N2D` | Kumbakonam | `TVMW-1N2D` | Thiruvananthapuram |
| `MDUW-1N2D` | Madurai | `TSRW-1N2D` | Thrissur |
| `TPTW-1N2D` | Tirupati | `UDPW-1N2D` | Udupi Krishna |
| `UJNW-1N2D` | Ujjain | `VRNW-1N2D` | Vrindavan |
| `YDGW-1N2D` | Yadagiri Gutta | `ANVW-1N2D` | Annavaram |

**E. Private and custom group yatras** use the prefix `GRP-` followed by a short group tag and the base yatra code, for example `GRP-LXM-WBYR-2027` for the West Bharat Yatra for the USA group, or `GRP-CHK-CDH-5N6D` for a chartered private helicopter Char Dham for one family. The base code lets the group yatra roll up with its product for category reporting while keeping its own P&L.

**F. Reserved non-yatra codes**

| Code | Use |
| --- | --- |
| `OH-YAT` | Yatra department overhead pool (coordinators, telesales, yatra admin, accounts for yatra) |
| `OH-MKT` | Marketing and online presence overhead pool (digital team, designers, video, SEO, PPC staff, tools) |
| `OH-ADM` | Office and administration pool (Banjara Hills office rent, electricity, water, internet, HR, office associate) |
| `OH-FIN` | Finance, audit, statutory and bank charges pool |
| `OH-FA` | Depreciation pool for shared fixed assets |
| `NY-TEMPLE` | Non-yatra temple activity paid through yatra accounts (for example Janmashtami promotions seen in the 2019 Char Dham report), excluded from yatra P&L |
| `NY-FUND` | Fund raising and donor care activity by shared staff, excluded from yatra P&L |

## 5. Departure (batch) coding and the Yatra, Batch, Pilgrim hierarchy

Money attaches at three levels. The product level (yatra code) carries evergreen costs such as itinerary design, brochure artwork and always-on search ads. The departure level (batch code) carries everything bought for a dated group: helicopter seats, hotel nights, coach hire, pujas, the coordinator's travel. The pilgrim level carries each person's receipts, refunds, flight pass-through and add-ons. Reports roll up from pilgrim to batch to yatra to category to financial year.

```
Category            Himalayan premium          (report grouping, not a code)
  Yatra (product)   CDH-5N6D                   Char Dham by Helicopter 5N6D
    Batch           CDH-5N6D-26B01             25 to 30 Apr 2026, 12 seats
      Pilgrim       CDH-5N6D-26B01 / P-000123  receipt, GST, TCS, flight, add-ons, refund
      Vendor PO     CDH-5N6D-26B01 / PO-5120   Heli Yatra 12 seats, hotels, pujas
      Staff cost    CDH-5N6D-26B01 / EXP-0231  coordinator flights and allowances
    Batch           CDH-5N6D-26B02             2 to 7 May 2026
    ...
    Batch           CDH-5N6D-26B09             15 to 20 Jun 2026
```

**Batch master fields** (one row per departure; the ERP generates the code)

| Field | Rule |
| --- | --- |
| Batch code | `YATRACODE-YYBnn`, generated from start date |
| Start date, end date | Mandatory; end date = start date + days minus 1 |
| Departure city | Hyderabad, Bengaluru, Chennai, Delhi, Kathmandu, Lucknow, as sold |
| Seats planned, minimum pax | From the calendar sheet (Min Reg column); drives break-even |
| Status | Planned, Open, Filling, Full, Departed, Completed, Cancelled, Closed |
| Price tier rows | General and Premium amounts, GST, TCS, effective date (matches batch_pricing in the knowledge base) |
| Booking trust | Which entity issues receipts for this batch (HKMH, TSFH, RGI, HKMI, GAVPL) |
| Partner share | Partner temple codes and their seat counts when a yatra is shared (for example HKM Hyderabad 11 and HKM Chennai 10 on the Kailash Aerial batch) |
| Operator | Main DMC or operator (Heli Yatra, Veena World, Well Nepal, Trip to Temples, Golden Avatar) |
| Coordinator, kirtaniya, preacher in charge | Employee codes, used to allocate their salary days |
| Campaign window | Promotion start date to departure date; used for overhead allocation (section 9) |
| Close date | Date Finance locks the batch after all invoices and refunds are in |

**Status rules that protect the numbers**

- Receipts can be posted only to batches in Open, Filling or Full status.
- Purchase orders can be raised only against batches in Open to Departed status, and only up to the approved batch budget unless the Yatra Manager approves an overrun.
- A batch moves to Closed only when: all vendor invoices are received, all advances are knocked off against invoices, all pilgrim refunds are paid, the coordinator's expense claim is settled, and the overhead allocation for its last active month has run. Finance locks it; later entries need a reopen approval.
- A Cancelled batch keeps its code. Costs that cannot be recovered (non-refundable deposits, ads already run) stay on the cancelled batch so the loss is visible, and the batch is reported in a Cancelled yatras line, not hidden in overhead.

**Pilgrim record fields that matter to Finance**: pilgrim ID, batch code, tier, registered by (employee or preacher code), lead source channel code (section 8), campaign code, trust that issued the receipt, receipt numbers and dates, yatra amount, GST, TCS, flight pass-through, single occupancy supplement, concession, payment gateway charge, total receivable, amount paid, pending, refund amount and date, cancellation stage. These are the columns already kept by hand in the Vrindavan Nov 2026 and USA Sep 2026 registration sheets; the ERP replaces those sheets.

**Shared and partner yatras**: when HKM Hyderabad sells seats on a batch run with partner temples (USA 2025 with HKM MP and Golden Avatar, Kailash Aerial with HKM Chennai), each partner's pilgrims carry the same batch code with the partner code on the pilgrim row. Income stays with the booking trust, common costs are paid by one entity and recharged by seat count, which is the rule minuted in the Kailash 2026 action items (every Monday HKM MP and HKM Hyderabad transfer in proportion to yatris enrolled). The recharge is posted as an inter-unit invoice tagged to the batch code so each entity's P&L shows its own share.

## 6. Direct cost heads (chart of accounts for a yatra)

Every direct cost line in the ERP carries a cost head from this list plus a batch code. The heads are built from what actually appears in the past yatra expenditure reports: the 2019 Char Dham payments through Kotak and cash, the Kumbh Mela 2019 expenditure, the Sri Lanka, Dwaraka and Puri reports, the Nepal 2022 report, the USA 2025 costing sheet, the Kailash 2026 sheet, the Amarnath and Vaishno Devi costing, the Vrindavan Nov 2026 registration sheet and the KL Preaching cost calculator. Account numbers follow a 5-series so they sit together in any trial balance.

| Account | Cost head | What goes here | Seen in source files as |
| --- | --- | --- | --- |
| 5100 | Tour operator or DMC package | Lump-sum land package bought from an operator, net of GST input | Veena World USA land package, Well Nepal (Rs 39,000 x 55 pax), Trip to Temples, Golden Avatar invoices, Arvind Prabhu yatra expense invoices with 2% TDS |
| 5110 | Helicopter charter and seats | Heli seats, charter, extra body-weight charges, helipad transfers | Heli Yatra Rs 2,07,000 pre-block, Himalayan Heli, Indocopter, Thumby heli taxi, GMVN Kedarnath heli Rs 2,39,326, Mukmit (Vaishno Devi and Amarnath) |
| 5120 | Flights: pilgrims (pass-through) | Tickets bought for pilgrims and recovered from them | Vrindavan Nov 2026 Rs 21,455 to 22,711 per pax, IndiGo and MakeMyTrip receipts, Haribol air tickets |
| 5121 | Flights: included in package | International or domestic airfare that is part of the price | USA Rs 2,30,000 approx per pax, Europe, Sri Lanka |
| 5130 | Train | Rail tickets for pilgrims and staff | MakeMyTrip rail e-tickets 2025 (Hyderabad, Delhi, Dehradun, Tirupati, Bengaluru legs) |
| 5140 | Coach and bus hire | AC coaches, diesel paid in cash, state taxes, tolls, parking | Honey Holidays Rs 5.8 lakh plus diesel, Patel and Travels Rs 2.22 lakh, state tax at Chitrakoot and Jhansi |
| 5150 | Cars, taxis and local transport | Innova, tempo traveller, autos, Uber, e-rickshaw, shikara, battery car, ropeway | Innova 4 days Rs 5,000 to 7,000, Uber London and Amsterdam, tuk-tuk Janakpur, ropeway and battery car Rs 600 |
| 5160 | Boats, ferries and cruises | Boat rides, ferry crossings, lake and river boats | Yamuna boat ride, Nagadweepam ferry, Bentota boat, Delft ship Rs 10,000, Dal Lake shikara |
| 5200 | Accommodation | Hotel rooms, resorts, ashram and guest house stays, dormitory at Vaishno Devi, single-occupancy cost | Shivalik Valley, Monal, Godwin, Garhwal Palace, Toshali Puri, Regenta Ahmedabad, Radhe Reality Dwaraka, Ramada Jammu, The Postcard Gir, Hyatt Centric Dehradun (Heli Yatra) |
| 5210 | Prasadam and meals | Cooks, hotel meals, ISKCON prasadam, snacks, tea, water, fruits, dinner at resorts | Sujal Kumar Rs 3 lakh (2019), Munesh Kumar Sharma Kumbh prasadam, HKM Puri prasadam, water bottles, Veena World extra meals |
| 5220 | Special pujas, darshan and seva tickets | Abhishekams, aratis, VIP darshan, panda dakshina, temple entry | Badrinath Maha Abhishekam Rs 5,500, Kedarnath Rudra Abhishekam Rs 15,000, Kapoor arati, Vishnu Sahasranama path, Atka arati Rs 3,000, panda charges Puri and Sakshi Gopal |
| 5230 | Permits, entry tickets and registrations | Government yatra registration, Kailash permit, monument entry, national park fees | GMVN registration Rs 11,760 and 2,200, Kailash permit, Sigiriya, Statue of Unity Rs 1,900 to 2,280, Kandy tickets, Gangaramaya |
| 5240 | Visa, passport and consular | Visa fees, VFS, slot booking, DS-160 processing, interview preparation | US embassy fee Rs 17,020, RCS slot booking Rs 25,000, interview prep Rs 10,000, Visa Mate Rs 20,920, VFS France and Schengen, Tibet and China visa |
| 5250 | Travel insurance and medical | Insurance policies, doctor on tour, oxygen, first aid | Bajaj Allianz travel policy, 1 male doctor on Kailash |
| 5260 | Guides, pandits and local staff | ISKCON temple guide fees, Chinese and Nepali guides, pandit ji for hawan, local escorts | Hindi-speaking Chinese guide, Nepal guide, Bageshwari hawan pandit |
| 5270 | Kirtaniya, brahmachari and tour leader costs | Fees, dakshina, accommodation, travel and prasadam of devotee staff on the yatra | KL calculator: kirtaniya Rs 1,100 per day fee, Rs 8,100 per yatra; brahmachari Rs 23,200; staff Rs 6,800 |
| 5271 | Coordinator and staff travel | Flights, trains, hotels and allowances of yatra coordinators and office staff travelling with the batch | Ashram devotee flights Rs 1,02,781 (Nepal 2022), staff train tickets Rs 11,612, staff food at stations |
| 5280 | Welcome kit and yatra kit | Chanting bag, mantra card, book, water bottles, t-shirt, sling bag, Rudraksh, luggage tags, badges, ID cards | Yatra tags and luggage cards Rs 23,000, chanting bags Rs 2,800, kurtas, welcome kit (Kailash) |
| 5281 | Gifts, bahumana and take-home | Gifts to pilgrims, bahumana for devotees and hosts, sweets | Bahumana Rs 750 per yatri (KL calculator), bahumana TSF Hyd Rs 6,300, gifts and promotions |
| 5290 | Equipment hire and consumables for the tour | PA systems, vessels, cooking equipment, winter clothing for staff, packing and luggage transport | S V Electronics PA systems Rs 99,000, luggage transport Hyderabad to Delhi Rs 2,000, winter clothes, vessels packing |
| 5300 | Photography, videography and live streaming | Crew travel, fees, drone and edit for the yatra record and promotion | Videography team Rs 1,00,000 (Nepal 2022), photographer and video editors on tour |
| 5310 | Pilgrim add-ons (pass-through) | Horse, porter, sherpa, pony, palki, Darchen stay for non-trekkers, extra Rishikesh days | Kailash horse Rs 50,000, private sherpa, Rishikesh add-on Rs 8,000 per day |
| 5320 | Cancellation and no-show charges | Vendor cancellation fees, unused seats, visa-rejection losses not recovered from the pilgrim | USA 2026 visa rejections with Rs 52,020 spent per pax; last-minute cancellation sheet in USA 2025 costing |
| 5330 | Forex, bank and payment gateway charges on yatra money | Currency purchase (500 euros Rs 49,000), card charges, gateway fees on pilgrim payments, TCS cash-flow cost | Omni card platform charges (Yatra), payment gateway charges column, AMEX and ICICI foreign spends |
| 5340 | Tips, dakshina and gratuities | Driver tips, hotel staff tips, temple dakshina not covered under 5220 | Tips excluded from Europe price, dakshina lines in cash sheets |
| 5350 | Communication and SIM on tour | International SIM, roaming, local recharges, WhatsApp groups | Recharge charges, telephone charges |
| 5360 | Contingency and miscellaneous tour expense | Anything under Rs 2,000 not fitting above, medicines bought on tour, band-aid, lassi, ice cream | Cash sheets 2013 to 2022 show hundreds of such lines; cap each at Rs 2,000 and require a coordinator note |

**Direct marketing for one batch or yatra** (sections 8 and 9 explain allocation; these heads are the posting targets)

| Account | Cost head | What goes here |
| --- | --- | --- |
| 5400 | Paid digital ads, yatra-specific | Google Ads and Meta Ads campaigns whose campaign code names a yatra or batch |
| 5410 | SMS, WhatsApp and RCS sends, yatra-specific | Karix, MIT Infocom, Gupshup and Tata Tele DLT campaigns sent for a named yatra |
| 5420 | AI voice calling, yatra-specific | Vendor minutes or per-call charges for a yatra campaign |
| 5430 | Print, brochure, poster and hoarding | Amazing Graphics, C Laxman, Behtar Technology, brochure printing, standees |
| 5440 | Events, melas and roadshows | Stall rent, decoration, prasadam at a promotional event for a yatra |
| 5450 | Agency and creative fees, yatra-specific | DYGN Media, Digital Makeba retainers when billed per yatra; freelance designers |
| 5460 | Referral incentives and partner commissions | Commission to partner temples, preacher incentives if any, affiliate fees |

**Posting rules**

1. A vendor invoice that covers several batches (one Heli Yatra invoice for three weeks of departures) is split across batch codes by seats at posting time. The ERP line-level split does this; no lump posting to the yatra code.
2. Pass-through heads (5120, 5310) always have a matching revenue line under 4120 and 4310 for the same pilgrim, so their margin is zero by design and they never distort gross margin.
3. Cash paid on tour is posted from the coordinator's expense claim, line by line with the cost head and batch code, within 7 days of return. The claim form replaces the Payments through Cash sheets.
4. Advances to vendors are posted as advances against the batch code and knocked off when the invoice arrives. An advance that is still open 60 days after the batch end date appears on the exception report.
5. GST input credit on 5100 to 5460 is tracked by entity so that the credit received by HKM Hyderabad from Golden Avatar (the GST sheet in the Kailash 2026 workbook) is reconciled per batch.

## 7. Revenue tagging: packages, add-ons, taxes, refunds and donations

Every receipt from a pilgrim is split into its components at the time of posting so that the batch P&L shows true yatra revenue, pass-through recoveries and tax liabilities separately. The split mirrors the columns the team already keeps by hand (Yatra Amount, 5% GST, 5% TCS, Flight Charges, Single Occupancy, Concession, Payment Gateway charges, Total Receivables).

| Account | Revenue head | Rule |
| --- | --- | --- |
| 4100 | Yatra fee, General tier | Base package amount before GST; the pilgrim's tier is a field on the pilgrim row |
| 4101 | Yatra fee, Premium tier | Same, premium tier |
| 4110 | Single occupancy supplement | Rs 10,000 to 12,000 on Vrindavan 2026; separate so room economics can be checked |
| 4120 | Flight recovery (pass-through) | Matches cost head 5120; posted at the actual ticket cost, difference to the pilgrim (Flight Diff Amount) stays here |
| 4130 | Concession and discount (negative) | Family and senior concessions, the 5% special price concession, reduced-cost seats for devotee parents; always posted as a negative line so the list price is preserved for analysis |
| 4140 | Visa and consular recovery (pass-through) | Matches 5240 where the pilgrim bears the fee |
| 4310 | Add-on recovery (pass-through) | Horse, porter, sherpa, extra days, extra meals, pujas booked on request; matches 5310 and 5220 as applicable |
| 4400 | Cancellation retention | Amount retained when a pilgrim cancels; posted at the date of cancellation decision, with the refund posted against the original receipt |
| 4500 | Partner temple seat revenue | Seats sold through a partner temple on a batch run by HKM Hyderabad, at the inter-unit price |
| 4600 | Sponsorship and subsidy income | Donor sponsoring devotee parents or brahmacharis on a yatra (Kumbh 2019: 5, 3 and 1 sponsored pax per batch) |
| 4700 | Annadanam and seva donations raised on a yatra | Donations collected during or for a yatra (Rs 6.5 lakh on Char Dham 2019, Rs 75,000 on Vrindavan 2019); reported below gross margin as Other yatra income, with their own seva code |
| 4800 | Other yatra income | Forex gain, vendor refunds and credits, interest on yatra advances |
| 2410 | GST output payable (liability, not revenue) | 5% on 4100, 4101, 4110 and service add-ons |
| 2420 | TCS collected (liability, not revenue) | 5% on overseas packages (USA, Europe, Kailash, Sri Lanka, Nepal where applicable); refundable to the pilgrim through income tax, so never income |
| 1310 | Pilgrim receivables | Total receivable less paid; aged per batch |
| 2310 | Pilgrim advances and refunds payable | Amounts received for batches not yet departed and refunds due |

**Receipt rules**

1. One receipt per pilgrim per payment, each carrying batch code, tier, trust, registered-by code, preacher code, lead source and campaign code. Multi-instalment pilgrims (USA 2026 had up to seven payments) appear as several receipts on one pilgrim row.
2. The seva code on the donation receipt printed by the DCC system is the batch code from go-live. For the transition, the old free-text codes map as in the appendix.
3. Receipts in cash, bank transfer, UPI, cheque and card are all posted the same way; the mode is a field. Cash collected on tour by the coordinator is receipted the same day on the mobile ERP form.
4. Revenue is recognised on the departure date of the batch. Money received before departure sits in 2310 as pilgrim advances. This single rule fixes the timing distortion in the monthly report where April receipts and June departures land in different months.
5. A refund is posted against the original receipt with reason code: pilgrim cancelled before cut-off, pilgrim cancelled after cut-off, visa rejected, batch cancelled by us, medical. Reasons feed the cancellation KPI.
6. GST and TCS are computed by the ERP from the tier and the yatra type; they are not typed.

**Pricing master**: each batch holds the General and Premium price, GST rate, TCS rate, inclusions and exclusions text, and effective dates. The International Yatras sheet already works to a target margin (Profit 45 percent column); the ERP keeps that target margin on the batch so the planned versus actual margin report in section 11 can be produced without a spreadsheet.

## 8. Marketing and sales channel coding

Marketing money is traceable to a yatra only if the campaign carries the yatra code at the moment it is created on the ad platform, the SMS gateway, the WhatsApp template, the telesales dialler and the AI voice vendor. The channel code set below is fixed; the campaign code is built from it.

**Channel codes**

| Code | Channel | Vendors and tools seen in the files | Cost is captured from |
| --- | --- | --- | --- |
| `GAD` | Google Ads (Search, Performance Max, Display, YouTube) | Google Ads account 556-209-2928; plan: Rs 2,500 per day Performance Max | Monthly Google invoice, split by campaign report |
| `MTA` | Meta Ads (Facebook and Instagram) | Punya Kshetras and Viswa Vijeyatha ad accounts; Rs 2.6 to 4.1 lakh per month Apr to Aug 2026 | Meta invoice, split by campaign report |
| `SMS` | Bulk SMS | MIT Infocom (Rs 2.95 lakh in Apr and May 2026), Karix monthly invoices, Rapid SMS proposal, Tata Tele DLT | Vendor invoice plus sent-count report per template |
| `WAP` | WhatsApp business messaging and broadcasts | Karix and Gupshup (WhatsApp Business Platform), Cooby, WhatsApp groups run by coordinators | Vendor invoice per template; manual broadcasts at zero media cost but staff time |
| `RCS` | Rich Communication Services messages | Karix RCS | Vendor invoice per campaign |
| `TLS` | Human telesales | Telesales Manager and 5 to 6 tele sales executives (Yatra department), Exotel cloud telephony, daily call reports | Salary allocation by call minutes per yatra from the dialler, plus Exotel charges |
| `AIV` | AI voice calling | Telugu AI voice agent (vendor demo script prepared Aug 2026), outcome classifications such as interested_high_intent | Vendor per-minute or per-call invoice per campaign |
| `SEO` | Organic search and website | punyakshetras.com, SEO specialist and digital SEO staff, GoDaddy domains and hosting, Supermetrics | Staff allocation plus tool subscriptions |
| `YTB` | YouTube and social organic | Video editors, content creator, photographer, Runway and Envato subscriptions | Staff allocation plus tools |
| `PRN` | Print, posters and brochures | Amazing Graphics, C Laxman, Behtar Technology, Yatra Brochure 2025-26 print | Vendor invoice |
| `EVT` | Events, festivals and roadshows | Temple festival counters, Janmashtami, corporate visits | Event expense claim |
| `PRC` | Preacher and devotee referral | Preacher codes already on receipts (MKCD, GKLD, SRTD, NMMD, BLGD and others) | No media cost; attribution only |
| `REF` | Past yatri and word of mouth referral | Who Joined our Yatras list, repeat pilgrims | No media cost; attribution only |
| `PTN` | Partner temples | HKM MP, HKM Chennai, ISKCON Bangalore, VCM | Seat-share recharge |
| `CRP` | Corporate and institutional groups | Big C, Penna Cement, Malla Reddy Group, Sreenidhi, Anoo's and others on the Who Joined list | Account manager allocation |
| `WEB` | Website direct enquiry and booking form | Enquiry forms, booking@punyakshetras.com, CRM executive | CRM subscription allocation |

**Campaign code format**

```
CHANNEL - YATRACODE - YYMM - nn
MTA - CDH-5N6D - 2602 - 01      Meta campaign for Char Dham heli, started Feb 2026, first of the month
SMS - AHBW-1N2D - 2611 - 02     second SMS blast in Nov 2026 for Ahobilam weekend
GAD - BRAND - 2601 - 01         brand or always-on search campaign not tied to one yatra
TLS - USAF-16N17D - 2510 - 01   telesales campaign for the USA 2026 yatra started Oct 2025
AIV - SLRF-7N8D - 2612 - 01     AI voice calling for Sri Lanka Feb 2027 batch
```

The campaign code is typed as the campaign name in Google Ads and Meta, as the template or sender name in Karix, Gupshup and MIT Infocom, as the campaign field in the dialler and the AI voice vendor, and as utm_campaign in every link. The CRM stores it on every lead. The pilgrim record inherits it when the lead converts. A brand campaign uses `BRAND` instead of a yatra code and is allocated by the rule in section 9.

**Lead source on every pilgrim** is mandatory from go-live. It is one channel code plus the campaign code where one exists. The registration forms used for Vrindavan and USA 2026 already have the column; it is blank today, which is why cost per booking cannot be computed. The telesales daily report (for example 25 November 2025: 18 calls for USA, Puri and Ramayan yatras) becomes a dialler export tagged by yatra code instead of an email.

**Marketing cost capture, by channel**

1. Platforms with campaign-level reports (GAD, MTA): the monthly invoice is posted to 5400 and split across campaign codes using the platform's spend by campaign export. Brand spend goes to `OH-MKT`.
2. Messaging vendors (SMS, WAP, RCS): the invoice is split by template or sender in proportion to messages sent per campaign. Shared database sends promoting several yatras in one message are split equally across the yatras named in the message.
3. Telesales (TLS): salaries and Exotel charges go to `OH-YAT`, then allocate monthly by call minutes per yatra code from the dialler report. Until the dialler tags calls, use the daily report counts.
4. AI voice (AIV): invoiced per campaign; posted directly to 5420 against the batch.
5. Agencies and retainers (DYGN Media, Digital Makeba, Srinivas Mahankali, Aniket): monthly retainer to `OH-MKT`; any work order for a named yatra to 5450 against the batch.
6. Staff in marketing and online presence (Head Digital Marketing, PPC, SEO, CRM, designers, video editors, content creator, photographer, full-stack developer): the share of their cost tagged to the Yatra department in the salary sheet goes to `OH-MKT` and is allocated by the rule in section 9.

**What this makes possible**: cost per lead and cost per booking by channel and by yatra, return on ad spend per batch, and a monthly marketing mix review that compares the Rs 22.7 lakh of advertisements in April to August 2026 against the bookings each channel produced.

## 9. Overhead apportionment: salaries, rent, electricity, administration, purchases and fixed assets

Three tiers of cost reach a batch. Tier 1 is tagged directly at source. Tier 2 is yatra-specific marketing tagged by campaign code. Tier 3 is everything shared, collected in the five overhead pools and allocated every month by a driver that reflects how the cost was actually consumed. The 50:50 split used for last year's Rs 76.36 lakh is replaced by these drivers.

```
Source documents                  Tier                               Batch profit and loss
Vendor PO and invoice   ───►  Tier 1: Direct cost            ───►  Net yatra revenue
Pilgrim receipt                   (tagged to the batch at source)      less direct cost
Payroll and time sheet  ───►  Tier 2: Direct marketing       ───►  = Gross surplus
Marketing invoice                 (by campaign code)                   less direct marketing
Expense claim on tour   ───►  Tier 3: Overhead pools         ───►  = Contribution
                                  OH-YAT OH-MKT OH-ADM OH-FIN OH-FA     less allocated overhead
                                  (allocated monthly by driver)        = Net surplus
                                                                       plus donations raised on tour
```

Direct costs and campaign-coded marketing land on the batch at posting time; only the five overhead pools wait for the monthly allocation journal.

**Tier 3 pools and drivers**

| Pool | What sits in it (from the Sep 2026 salary and fixed expense sheet and the FY 2026-27 ledger) | Primary driver | Fallback driver |
| --- | --- | --- | --- |
| `OH-YAT` Yatra department | Yatra Manager, senior yatra coordinators, senior yatra admin executive, admin executive, tele sales manager and 5 to 6 tele sales executives, fund raising executives tagged to Yatra, accounts executive and junior accounts executive for yatra, kirtaniyas when not on tour, Exotel, Keka HR software share, Otter, Google storage | Telesales and coordinator time: call minutes per yatra from the dialler and days on tour from the batch master | Revenue share of batches active in the month |
| `OH-MKT` Marketing and online presence | Head of Digital Marketing, PPC specialist, SEO specialist and digital SEO, CRM executive, full-stack developer, graphics HOD, senior and junior graphic designers, video editors, content creator, photographer, marketing consultants (Srinivas Mahankali, DYGN Media), tools (Supermetrics, Envato, Runway, Notion, Screencastify, Cooby, Scribd, GoDaddy, Anthropic and ChatGPT subscriptions), brand ad spend | Leads created per yatra in the month from the CRM | Revenue share |
| `OH-ADM` Office and administration | Banjara Hills office rent Rs 93,000 and the RGI rent Rs 5,900, electricity (Rs 8,800 to 21,500 per month), water, Excitel and Jio internet, HR manager and HR executive share, office associate, printing and stationery, local conveyance (common), prasadam charges (common), courier, Omni card platform (common), electronics under Rs 10,000, Naukri, Indeed and Apna subscriptions | Headcount days of yatra staff working on each yatra (from the same time driver as `OH-YAT`) | Revenue share |
| `OH-FIN` Finance and statutory | Bank charges, credit card charges, consultancy charges of CA Shivakumar and Bangalore CA, statutory filings, GBC membership fee share, TDS interest, audit fees | Revenue share | Equal share per active batch |
| `OH-FA` Depreciation of shared assets | Laptops and desktops on the IT hardware asset tracker (Punyakshetra location), office furniture, PA systems, cooking vessels, cameras and video gear | Asset-specific: tour equipment by pax-days of batches that carried it; office IT by the same driver as the owner's pool | Revenue share |

**Rules**

1. An employee is costed at full cost to company including PF, ESI and medical insurance, multiplied by the Yatra-department share recorded in the salary sheet (for example 90 percent RGI and 10 percent CC for a senior yatra coordinator, 25 percent HKM Hyderabad and 75 percent RGI for the senior yatra admin executive). Only the yatra share enters a pool; the rest goes to `NY-FUND` or the other departments.
2. An employee who travels with a batch is charged directly to that batch (Tier 1, account 5271) for the tour days plus two preparation days, at daily cost = monthly cost to company divided by 26. The remaining days of the month stay in the pool.
3. The campaign window decides which batches are active in a month: a batch is active from its promotion start date (the first campaign code dated for it, or 120 days before departure, whichever is earlier) to its end date. Only active batches receive overhead for that month. Expenses incurred for a departure in a later financial year are deferred on the batch (the Future Yatra Expenses line in the current report, for example the Rs 9,960 on Manasarovar batch 3) and released on departure.
4. Allocation runs on the fifth working day after month end as a system journal, one line per batch per pool, reversible. Finance reviews the driver data before posting.
5. Costs in `NY-TEMPLE` and `NY-FUND` are never allocated to yatras. The 2019 report rightly separated Janmashtami promotions and Rs 23.5 lakh transferred to HKM general; the ERP enforces that with the NY codes.
6. Fixed assets above Rs 10,000 are capitalised with a cost centre of the owning pool. Depreciation runs monthly at Income Tax or Companies Act rates as the trust's auditor requires, posted to `OH-FA`, then allocated. Tour assets (PA systems Rs 99,000 in 2019, vessels, cameras) carry a usage log by batch code.
7. Inter-trust recharges follow the Kailash 2026 minute: one entity pays common costs and invoices the others by seat count every Monday; the recharge carries the batch code and the receiving trust.

**Worked example on the April to August 2026 numbers**

The FY 2026-27 report gives, for April to August 2026, direct yatra receipts of Rs 6,43,86,757 and direct expenditure of Rs 5,56,79,783, a gross surplus of Rs 87,06,974 (13.5 percent). The common pool for the same five months was Rs 82,22,315: advertisements Rs 22,66,576, staff cost Rs 46,57,915, other expenses Rs 12,97,824. With the drivers not yet captured, revenue share is the fallback for all three pools; the table shows what that produces. Once the dialler, CRM and batch-day drivers exist, the staff and marketing lines will move toward the yatras that consumed the calls and leads, which is the point of the system.

| Yatra (Apr to Aug 2026) | Receipts (Rs) | Direct cost (Rs) | Gross surplus (Rs) | Revenue share | Overhead allocated (Rs) | Net surplus (Rs) | Net margin |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Summer Char Dham by road (May, Jun) | 3,31,78,344 | 3,02,37,878 | 29,40,466 | 51.5% | 42,37,000 | (12,96,534) | (3.9%) |
| Kailash Manasarovar land, batch 1 | 2,88,63,665 | 2,40,02,462 | 48,61,203 | 44.8% | 36,86,000 | 11,75,203 | 4.1% |
| Kashi (Jul) | 7,00,000 | 3,17,079 | 3,82,921 | 1.1% | 89,000 | 2,93,921 | 42.0% |
| Nepal (May) | 6,64,807 | 5,88,060 | 76,747 | 1.0% | 85,000 | (8,253) | (1.2%) |
| Puri (Jul) | 4,71,429 | 3,16,157 | 1,55,272 | 0.7% | 60,000 | 95,272 | 20.2% |
| Kailash Aerial (Apr) | 3,16,661 | 1,98,000 | 1,18,661 | 0.5% | 40,000 | 78,661 | 24.8% |
| USA (Apr receipts) | 1,91,851 | 20,148 | 1,71,703 | 0.3% | 25,000 | 1,46,703 | 76.5% |
| Total | 6,43,86,757 | 5,56,79,783 | 87,06,974 | 100% | 82,22,000 | 4,84,974 | 0.8% |

Two lessons follow even from this rough cut. First, the two large yatras absorb almost all overhead whichever driver is used, so their pricing must carry roughly Rs 3,000 to 4,000 of overhead per pilgrim on a 100-pilgrim batch. Second, the USA line is distorted because April receipts are advances for a later departure; revenue recognition on departure (section 7) removes that distortion. The Kailash batch 2 in September (15 pax, receipts Rs 67.65 lakh, direct cost Rs 57.05 lakh, provisional overhead Rs 17 lakh, net loss Rs 6.4 lakh) and the Kailash Aerial October batch (21 pax, net loss Rs 12.2 lakh after Rs 17 lakh overhead) show why a per-pax overhead view is needed before approving small batches.

**Planned versus actual**: every batch budget is entered in the same cost heads before launch (the Char Dham, Amarnath and Vaishno Devi, USA and KL Preaching calculators already do this per pax). The ERP then reports budget, committed (open purchase orders), actual and variance per head, so overruns such as the extra 13 meals on the USA land package are visible before the invoice arrives.

## 10. ERP configuration specification

The design works in any ERP that supports multi-entity accounting with two or more analytical dimensions on every journal line (Tally Prime with cost centres and cost categories, Zoho Books with tags, ERPNext with projects and cost centres, Odoo with analytic accounts, SAP Business One with dimensions). The ERP developer on staff builds the masters below; Finance owns the data.

**Analytical dimensions on every posting line**

| Dimension | Values | Mandatory on |
| --- | --- | --- |
| Entity (company) | HKMH, HKMI, TSFH, RGI, GAVPL | Every line |
| Yatra or pool code | Any batch code, `OH-` pool, `NY-` code or `GRP-` code | Every P&L line; the ERP rejects a blank |
| Cost or revenue head | Accounts in sections 6 and 7 | Every line |
| Channel and campaign | Channel code, campaign code | Marketing lines (5400 to 5460, brand spend) and every pilgrim receipt |
| Employee | Employee code | Payroll, expense claims, time allocations |
| Vendor | Vendor code with kind | Purchase orders, invoices, advances |
| Partner | Partner temple code | Shared batches |

**Master data tables**

| Master | Key fields | Owner | Source today |
| --- | --- | --- | --- |
| Yatra master | Yatra code, title, category (Himalayan, South and West, International, Weekend, Group), destination list, mode, nights, days, min pax, difficulty, senior friendly, visa required, themes, default operator, status, retired date | Yatra Manager proposes, Finance approves | Yatra Calendar 2026 workbook; knowledge base `yatras` table |
| Batch master | Section 5 fields | Yatra admin | ALL YATRAS WITH DATES AND BUDGET sheet; `yatra_batches` |
| Price master | Batch code, tier, amount, GST rate, TCS rate, effective from, inclusions, exclusions, target margin | Yatra Manager, Finance approves | `batch_pricing`; International Yatras sheet |
| Batch budget | Batch code, cost head, budget amount, per-pax or lump, note | Yatra Manager | Costing calculators |
| Cost head master | Account, name, pass-through flag, GST input flag, TDS section | Finance | This document |
| Vendor master | Vendor code, kind (hotel, DMC, helicopter, airline, transport, insurance, catering, guide, permit, visa, marketing, software, other), city, GST number, PAN, TDS rate, bank details, preferred flag, negotiated rates with validity | Yatra admin, Finance verifies | `vendors` and `vendor_rates`; vendor mails |
| Customer (pilgrim) master | Pilgrim ID, name, phone, email, ID document, city, preacher code, first lead source, first campaign, corporate or group tag, repeat count | Yatra admin and telesales | Registration sheets, DCC donor records |
| Channel and campaign master | Channel code, campaign code, yatra code, start, end, budget, platform ID, owner | Marketing head, Finance approves budget | Ad accounts, vendor dashboards |
| Employee master | Employee code, name, department, designation, cost to company, entity split percentages, yatra share percentage, default pool, manager | HR | Updated Salaries and Fixed Expenses Sep 2026 |
| Allocation rule master | Pool, driver, fallback, effective dates | Finance | Section 9 |
| Partner master | Partner code, temple, contact, recharge basis | Yatra Manager | Kailash 2026 action items |
| Asset register | Asset code, description, cost, date, pool or batch, depreciation rate, usage log | Finance | IT Hardware Asset Tracker |

**Transaction tagging rules**

| Document | Must carry | Validation |
| --- | --- | --- |
| Sales order and receipt | Batch code, tier, trust, registered-by, preacher code, lead source, campaign, payment mode | Batch must be Open to Full; amount split into heads automatically; receipt number sequence per trust |
| Purchase order | Batch code (or pool), cost head, vendor, quantity, rate, GST, TDS, expected date | Budget check against batch budget; approval by Yatra Manager above Rs 50,000, by management above Rs 5 lakh |
| Vendor invoice | Same as PO plus invoice number; multi-batch split allowed by seats or nights | Three-way match with PO and goods or service confirmation by the coordinator |
| Vendor advance | Batch code, vendor, PO reference | Auto-knock-off on invoice; exception report at 60 days |
| Expense claim (coordinator on tour) | Batch code per line, cost head per line, bill attached flag, place | Lines above Rs 2,000 need a bill image; claim submitted within 7 days of return |
| Payroll journal | Employee code, entity split, yatra share, pool | Monthly, generated from the employee master; tour days moved to batch by the time driver |
| Marketing invoice | Campaign codes with amounts (campaign split sheet attached) | Sum of splits equals invoice; brand share to `OH-MKT` |
| Allocation journal | Pool, driver value per batch, amount per batch | Generated, reviewed, posted, reversible |
| Inter-unit invoice | Batch code, from entity, to entity, basis (seats) | Mirrors in both entities in the same month |
| Refund | Original receipt, reason code, amount, approval | Approval by Yatra Manager; cancellation retention posted automatically |

**Workflows the ERP must run**

1. Yatra launch: Yatra Manager raises the yatra and batch master request with budget and prices; Finance approves; codes go live; marketing creates campaign codes.
2. Lead to booking: CRM lead with channel and campaign converts to a pilgrim and a sales order; receipts post against it; the pilgrim appears on the batch manifest.
3. Procure to pay: PO against batch budget, advance, confirmation on tour, invoice match, payment, TDS deduction, GST input.
4. Tour close: coordinator claim, final vendor invoices, refunds, batch close checklist, batch locked.
5. Month close: payroll with time driver, marketing split, allocation journal, inter-unit invoices, reports published.

**Integrations in order of value**: dialler (Exotel) call export by yatra code; ad platform spend by campaign (Google Ads API, Meta Marketing API, or Supermetrics which is already paid for); messaging vendor delivery reports (Karix, Gupshup, MIT Infocom); AI voice vendor call logs; DCC donation system seva code sync; the Yatra Knowledge Base app, whose `yatras`, `yatra_batches`, `batch_pricing`, `batch_economics`, `vendors` and `vendor_rates` tables map one to one onto the masters above and can be fed from the ERP nightly so staff see margins on their phones.

**Access control**: pilgrims and tour leaders never see cost, margin or vendor rates; coordinators see their batch budget and claims; telesales see leads and receipts; Finance sees everything; management sees reports. This mirrors the role model already enforced in the knowledge base.

## 11. Reports and KPIs

All reports are produced by the ERP from tagged data; none needs a spreadsheet. Each is available at batch, yatra, category, entity and financial-year level.

**Batch profit and loss** (the core report, one page per departure)

```
Revenue        4100 Yatra fee General + 4101 Premium + 4110 Single supplement
               - 4130 Concessions
             = Net yatra revenue
Pass-through   4120 Flights, 4140 Visa, 4310 Add-ons  less  5120, 5240 (pilgrim share), 5310   (nets to zero)
Direct cost    5100 to 5360 (operator, heli, transport, stay, prasadam, pujas, permits, staff on tour, kits, cancellation, forex)
             = GROSS SURPLUS and gross margin percent
Direct mktg    5400 to 5460 by campaign code
             = CONTRIBUTION after marketing
Overhead       OH-YAT, OH-MKT, OH-ADM, OH-FIN, OH-FA allocations
             = NET SURPLUS and net margin percent
Other income   4700 Annadanam and seva donations, 4800 Other
             = SURPLUS INCLUDING DONATIONS
Memo           Pax, seats, revenue per pax, direct cost per pax, overhead per pax, break-even pax
```

**Standard reports**

| Report | Frequency | Reader | Content |
| --- | --- | --- | --- |
| Batch P&L with budget versus actual | On batch close and monthly while active | Yatra Manager, management | The structure above, with budget, committed, actual and variance per head |
| Yatra P&L (all batches of a product, year to date) | Monthly | Management | Rolls batches up; shows repeat count and average margin, as the knowledge base Finance screen does today |
| Category and entity P&L | Monthly | Trustees, auditors | Himalayan, South and West, International, Weekend, Group by entity |
| Marketing effectiveness | Monthly | Marketing head, management | Spend, leads, bookings, cost per lead, cost per booking, return on ad spend by channel, campaign and yatra |
| Telesales productivity | Weekly | Telesales manager | Calls, minutes, leads, bookings and revenue per executive and per yatra from the dialler |
| Receivables and advances | Weekly | Yatra admin, Finance | Pilgrim pending amounts by batch and due date; vendor advances open with age; the 2019 Char Dham advances would have been caught at 60 days |
| Cancellations and refunds | Monthly | Management | Count, value, reason codes (pilgrim, visa rejected, batch cancelled, medical), retention income |
| Overhead allocation statement | Monthly | Finance | Pool totals, driver values, allocation per batch, unallocated balance (must be zero) |
| Inter-unit and partner settlement | Monthly | Finance of each trust | Recharges by batch, GST input credit transfers, balances |
| Cash forecast by batch | Weekly | Finance | Receipts due, vendor instalments due (Heli Yatra 40 percent at contract, 30 percent after 30 days, 40 percent at 40 days before flying), refunds due |
| Provisional yatra outlook | Monthly | Management | Upcoming batches with expected pax, revenue, direct cost, allocated overhead and projected margin, replacing the Provisional Yatra table in the current report |

**KPI definitions**

| KPI | Formula | Target or watch level |
| --- | --- | --- |
| Gross margin | Gross surplus divided by net yatra revenue | Published target margin per batch (International sheet uses 45 percent on cost); watch below 15 percent |
| Net margin | Net surplus divided by net yatra revenue | Positive on every batch; portfolio target set yearly |
| Overhead per pax | Allocated overhead divided by pax | Compare with price; Apr to Aug 2026 implied roughly Rs 3,000 to 4,000 per pax on large batches |
| Break-even pax | Fixed batch costs divided by (price minus variable cost per pax) | Must be below minimum registration in the batch master |
| Seat occupancy | Pax divided by seats planned | Watch below 70 percent |
| Cost per lead | Channel spend divided by leads tagged to the channel | Tracked per channel per yatra |
| Cost per booking (customer acquisition cost) | Channel spend plus allocated telesales cost divided by bookings | Compared with gross surplus per pax |
| Return on ad spend | Net yatra revenue from bookings attributed to paid campaigns divided by paid spend | Watch below 5x |
| Marketing share of revenue | All marketing cost divided by net yatra revenue | Watch above 8 percent |
| Cancellation rate | Cancelled pilgrims divided by registered | By reason; visa rejection rate separately for USA and Europe |
| Collection efficiency | Received before departure divided by total receivable | 100 percent before departure except approved exceptions |
| Advance ageing | Vendor advances open beyond batch end plus 60 days | Zero |
| Repeat rate | Pilgrims with a previous yatra divided by pax | Grows the REF channel |
| Days to close | Batch end date to batch locked | 30 days or less |

## 12. Implementation roadmap, governance and data quality

Go-live target is all departures from 1 January 2027 fully tagged, with the FY 2026-27 history re-coded by 31 March 2027 so that the April 2027 financial year opens clean.

| Phase | Dates | Work | Done when |
| --- | --- | --- | --- |
| 0. Approve | 27 Oct to 7 Nov 2026 | Management approves the code standard, catalogue, cost heads, pools and drivers in this document; Yatra Manager fills every confirm duration and reconciles the 182-row master sheet | Signed-off catalogue |
| 1. Masters | 10 Nov to 5 Dec 2026 | ERP developer builds dimensions and masters; Finance loads yatra, batch, price, cost head, vendor, employee, allocation and partner masters; marketing renames live campaigns with campaign codes | Masters loaded and test-posted |
| 2. Pilot | 8 to 31 Dec 2026 | Run three live batches end to end in the ERP in parallel with the old sheets: a weekend yatra, a Char Dham helicopter departure and the Sri Lanka February batch sales; coordinator claim form on mobile | Pilot P&Ls match the manual sheets |
| 3. Go-live | 1 Jan 2027 | All receipts, POs, invoices, claims and marketing invoices tagged; registration sheets retired; lead source mandatory | First monthly close on the ERP for January 2027 |
| 4. Allocation and reports | Feb to Mar 2027 | Dialler, CRM and ad platform drivers connected; first driver-based allocation for January; report pack issued; FY 2026-27 history re-coded by batch | March 2027 close with full report pack |
| 5. Steady state | Apr 2027 onward | Quarterly review of drivers and margins; annual catalogue refresh when the next brochure is designed | Standing agenda item |

**Governance**

| Role | Responsibility |
| --- | --- |
| Management (MKCD, STDD) | Approves the standard, target margins, and any new pool or driver; receives the monthly report pack |
| Finance lead (accounts executive for yatra, with the CA) | Owns the code catalogue, cost head master, allocation rules, month close and batch close; the only role that creates codes |
| Yatra Manager | Proposes yatras and batches with budgets and prices; approves POs up to limit; signs off batch close checklist |
| Yatra admin executives | Maintain batch and pilgrim data, receipts, manifests, vendor advances |
| Marketing head | Creates campaign codes, attaches spend splits to every marketing invoice, owns lead-source completeness |
| Telesales manager | Ensures every call and lead carries a yatra code in the dialler and CRM |
| HR manager | Keeps the employee master entity and yatra share percentages current |
| ERP developer | Builds and maintains dimensions, validations, allocation journal and integrations |
| Internal audit (quarterly) | Samples 30 transactions per quarter for correct tagging; reviews unallocated balances and open advances |

**Data quality controls**

1. No P&L posting without a yatra, pool or NY code (hard stop).
2. No pilgrim receipt without lead source and registered-by (hard stop).
3. No marketing invoice without a campaign split equal to the invoice (hard stop).
4. Weekly exception report: pilgrims with pending balance past due, vendor advances open past 60 days after batch end, batches past end date not closed in 30 days, campaigns with spend but zero leads, employees with no entity split.
5. Monthly: unallocated pool balance must be zero; inter-unit balances must agree across entities; GST and TCS liabilities reconcile to returns.
6. Quarterly: driver review; a driver that moves a pool by more than 20 percent from the fallback is documented.

**Known clean-up items before go-live**

- Close or write off the 2019 to 2020 vendor advances still listed in HoD Advances (Dygn Media, Garhwal Palace, Godwin Hospitality, Hotel Divine, Monal Resort, Shivalik Valley, Radhe Reality, The Holiday Resorts, Patel Travels).
- Fix the `#REF!` links in the FY 2026-27 report so the opening apportionment balance is known.
- Re-code last year's Rs 76.36 lakh apportioned 50:50, and the Rs 69.4 lakh pending apportionment for April to August 2026, by batch using the fallback driver so FY 2026-27 closes on the new basis.
- Collect lead source for every 2026 pilgrim already registered (USA September, Vrindavan November, Kailash batches) from the telecallers' records.
- Reconcile the Ahobilam price (Rs 10,000 in the 2026 brochure, Rs 24,999 in the weekend brochure) and confirm every duration marked confirm in section 4.
- Agree with partner temples the recharge basis for shared 2027 batches (Muktinath plus Kailash, USA) before their first receipt.

## 13. Appendices

**A. Data dictionary for the yatra code**

| Position | Name | Type and length | Allowed values | Example |
| --- | --- | --- | --- | --- |
| 1 | Destination | 2 to 4 uppercase letters | From the catalogue; new ones issued by Finance | `CD`, `KMS`, `AHB` |
| 2 | Mode | 1 uppercase letter | H, A, L, R, F, T, S, W | `H` |
| 3 | Nights | 1 to 2 digits + N | 0 to 99 | `5N` |
| 4 | Days | 1 to 2 digits + D | nights + 1 normally | `6D` |
| 5 | Year | 2 digits | Departure calendar year | `26` |
| 6 | Batch serial | B + 2 digits | 01 to 99 in date order within the year | `B03` |

Regular expression for validation: `^[A-Z]{2,4}[HALRFTSW]-\d{1,2}N\d{1,2}D(-\d{2}B\d{2})?$`

**B. Mapping of existing seva codes and sheet names to new codes**

| Existing label | New code |
| --- | --- |
| KUMBHYA (2019) | `KMB-confirm-19B01`, `19B02`, `19B03` |
| NEPAL MUKTINATH YATRA (2022) | `NMKF-confirm-22B01` |
| PURI YATRA (2020) | `PURR-2N3D-20B01` |
| Char Dham Yatra 2019 (road, 95 pax) | `CDR-confirm-19B01` |
| FOLK Vrindavan Yatra 2019 | `VRND-confirm-19B01` |
| Srilanka Ramayan Feb 2022 | `SLRF-7N8D-22B01` |
| Dwaraka Yatra Feb 2020 | `PDSR-5N6D-20B01` |
| Europe 2024 (with Dubai, UK) | `EURF-confirm-24B01` |
| USA Yatra 2025 (36 pax, Veena World) | `USAF-16N17D-25B01` |
| Aerial Yatra Apr 2026 | `KMSA-2N3D-26B01` |
| Summer CDY May to Jun 2026 | `CDR-confirm-26B01` and `26B02` |
| Kailash Yatra 31 May to 12 Jun 2026 | `KMSL-12N13D-26B01` |
| Kailash Yatra Batch 2 (Sep 2026) | `KMSL-12N13D-26B02` |
| Puri Yatra 12 to 16 Jul 2026 | `PURR-2N3D-26B01` |
| Kashi Yatra 22 to 25 Jul 2026 | `KTS-2N3D-26B02` |
| USA Yatra Oct 2026 | `USAF-16N17D-26B02` |
| Winter Summerdham Oct 2026 | `CDRW-confirm-26B01` |
| Kailash Aerial Oct to Nov 2026 | `KMSA-2N3D-26B03` |
| North (Uttara) India Yatra Oct to Nov 2026 | `UBY-confirm-26B01` |
| Vrindavan 2 to 6 Nov 2026 | `VRNR-4N5D-26B01` |

**C. Worked tagging examples**

| Transaction | Entity | Code | Head | Channel or other |
| --- | --- | --- | --- | --- |
| Heli Yatra invoice, 12 seats at Rs 2,07,000 for 2 to 7 May 2026 | HKMH | `CDH-5N6D-26B02` | 5110 | Vendor HELIYATRA |
| Receipt Rs 75,000 from a Vrindavan pilgrim on 29 Sep 2026 | TSFH | `VRNR-4N5D-26B01` | 4100 Rs 55,000; 2410 Rs 2,750; 4120 Rs 17,250 (part flight) | Lead `PRC`, preacher SUND |
| Meta Ads invoice Jun 2026 Rs 4,09,142 | RGI | split by campaign: `MTA-CDH-5N6D-2604-01`, `MTA-KMSL-12N13D-2603-01`, `MTA-BRAND-2606-01` | 5400 and `OH-MKT` | Channel `MTA` |
| MIT Infocom SMS Rs 2,95,000 Apr 2026 | RGI | `SMS-CDR-...-2604-01` and `SMS-KMSL-12N13D-2604-01` by sends | 5410 | Channel `SMS` |
| Senior yatra coordinator salary May 2026 | RGI 90%, CC 10% | 12 tour days to `CDR-confirm-26B01` (5271); 14 days to `OH-YAT` | 5271, `OH-YAT` | Employee code |
| Banjara Hills office rent Rs 93,000 May 2026 | TSFH | `OH-ADM` | 6xxx rent | Allocated 5th working day |
| US embassy fee Rs 17,020 paid by RCS for a USA pilgrim | TSFH | `USAF-16N17D-26B02` | 5240, recovered via 4140 | Pilgrim ID |
| Visa rejected pilgrim refund Rs 1,40,000 | TSFH | `USAF-16N17D-26B02` | against original receipt; retention to 4400; unrecovered fee to 5320 | Reason VISA |
| PA system Rs 99,000 bought for Char Dham 2019 | HKMH | Asset, pool `OH-FA`, usage log by batch | Depreciation | Asset register |
| Janmashtami promotions paid from yatra account | HKMH | `NY-TEMPLE` | Not in yatra P&L | |

**D. Source documents referred to** (all in the Yatra Google Drive): Yatra Calendar 2026 (sheets: Dashboard, ALL YATRAS WITH DATES AND BUDGET, International Yatras, Management Budget for VIPs, Copy of Sheet for Management, Special festival Yatras, Temples and special Poojas, All Yatra Itineraries, Muktinath plus Kailash); All Yatras in 2026 by ISKCON Hare Krishna Temple (brochure); Weekend Yatras organised by Hare Krishna Temple (brochure); FY 2026-2027 Yatra Reports August 2026; Updated Salaries and Fixed Expenses Sep 2026 V2; Monthly Salaries and Monthly Expenses 2025; Char Dham and Vrindavan Final Revenue and Expenditure Report 3 Yatras; Kumbh Mela and Ayodhya Yatra Revenue and Expenditure; FINAL Srilanka Jagannath Puri Dwaraka Yatras Revenue Expenditure Reports V2; Nepal Yatra Revenue and Expenditure Report; Copy of Expenses Sheet Europe; Budgeting Costing Sheet End to End details USA Yatra 2025 (8 Nov 2025); Kailash Manasa Sarovar Yatra 2026; Amarnath and Vaishno Devi yatra 15 to 23 July; Cost calculator for char dham 2025; KL Preaching Yatra Cost Calculator System; Vrindavan Yatra 2 to 6 Nov 2026; USA Yatra 21 Sept to 7 Oct 2026; Paid Marketing Plan for Punyakshetras; Punyakshetras Telugu AI Voice Agent Demo Script; IT Hardware Asset Tracker DMT; and the mails from Heli Yatra (Pre-Block 2026), Veena World, Adiona Travels, Karix, Google Ads and Facebook ad invoice summaries, and the Char Dham Yatra P&L status thread of October 2023.

**E. Open questions for management**

- [ ] Confirm the durations marked confirm in section 4 and retire any yatra not planned for 2027.
- [ ] Decide the target net margin per category (the International sheet implies 45 percent on cost; large road yatras ran near zero after overhead in 2026).
- [ ] Decide whether brand ad spend (`BRAND` campaigns) is allocated by leads or kept in `OH-MKT` and allocated by revenue.
- [ ] Choose the ERP platform and confirm it supports two mandatory analytical dimensions per line plus campaign tagging.
- [ ] Agree whether annadanam and seva donations raised on a yatra are reported inside yatra results or passed to the temple, since this changes the headline surplus (Rs 6.5 lakh on Char Dham 2019).
- [ ] Agree the partner recharge basis (seats, revenue or cost) for shared batches with HKM MP, HKM Chennai and ISKCON Bangalore.
- [ ] Confirm the salary allocation percentages in the September 2026 sheet are the ones to load, including staff moving trusts from October 2026.
