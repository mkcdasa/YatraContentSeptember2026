-- 4 Days Vaishno Devi Helicopter Package
-- Jammu – Katra – Vaishno Devi – Katra – Jammu (3 nights / 4 days)
--
-- Hand-authored content, not produced by scripts/import_content.py. Idempotent:
-- keyed on the yatra slug, safe to re-run after the team edits it in the app.

begin;

insert into yatras (slug,title,scope,nature,themes,nights,days,difficulty,senior_friendly,
  visa_required,summary,highlights) values (
  'vaishno-devi-helicopter-package',
  '4 Days Vaishno Devi Helicopter Package',
  'domestic'::yatra_scope,'evergreen'::yatra_nature,'{}',3,4,2,true,false,
  'Jammu – Katra – Vaishno Devi – Jammu. Raghunath and Ranbireshwar temples in Jammu, helicopter from Katra to Sanjichhat, Evening Darshan and Aarti, a night at Bhawan, Morning Aarti and Bhairon Baba Temple, then Banganga, Darshani Deodi and Katra market before returning to Jammu.',
  array[
    'Raghunath & Ranbireshwar Temples, Jammu',
    'Helicopter Yatra: Katra ⇄ Sanjichhat both ways',
    'Shri Mata Vaishno Devi Darshan',
    'Atka Aarti at the Holy Cave, arranged once for the group',
    'Bhairon Baba Temple Visit',
    'Banganga Darshan & Darshani Deodi',
    'Shopping at Katra Market'
  ])
on conflict (slug) do update set title=excluded.title, scope=excluded.scope,
  nature=excluded.nature, nights=excluded.nights, days=excluded.days,
  difficulty=excluded.difficulty, summary=excluded.summary, highlights=excluded.highlights;

insert into itineraries (yatra_id,version,title,intro,notes,is_current)
select y.id,1,'4 Days Vaishno Devi Helicopter Package',
  'Jammu – Katra – Vaishno Devi – Jammu',
  E'Overnight stays: 02 Nights Jammu, 01 Night Bhawan.\nPrice: ₹50,000 per person + 5% GST, excluding flight charges. All-inclusive: stays, all meals, helicopter, ropeway, battery car and transfers.\nFlights: arrive Jammu Airport on 13 March before 2 pm; depart Jammu Airport on 16 March after 2 pm.\nTour ends with the divine blessings of Mata Vaishno Devi. Jai Mata Di!',
  true
from yatras y where y.slug='vaishno-devi-helicopter-package'
on conflict (yatra_id,version) do update set title=excluded.title, intro=excluded.intro,
  notes=excluded.notes;

insert into itinerary_days (itinerary_id,day_number,title,body,stay)
select i.id,d.day_number,d.title,d.body,d.stay
from itineraries i join yatras y on y.id=i.yatra_id
cross join (values
  (1,'Jammu Arrival – Local Sightseeing',
   E'Arrive at Jammu Airport by 2 pm, meet our representative and transfer to the hotel.\nAfter lunch, visit:\n- Raghunath Temple\n- Ranbireshwar Temple\n- Raghunath Bazaar (shopping)\nReturn to the hotel in the evening.',
   'Jammu'),
  (2,'Jammu – Katra – Vaishno Devi by Helicopter',
   E'After breakfast, proceed to Katra (approx. 50 km / 1.5 hours).\nComplete Yatra registration formalities and report at Katra Helipad as per the allotted schedule.\nBoard the helicopter to Sanjichhat (flight duration approximately 5–8 minutes).\nRoute: Katra Helipad → Sanjichhat Helipad → Bhawan (approx. 2.5 km by battery car).\nProceed towards Shri Mata Vaishno Devi Bhawan and participate in the divine Evening Darshan. The Atka Aarti at the Holy Cave (main temple) is arranged once for the group – this evening or the next morning, as allotted by the Shrine Board.',
   'Bhawan'),
  (3,'Bhawan – Bhairon Temple – Katra – Jammu',
   E'Early morning, japa and darshan at Bhawan (or the Morning Atka Aarti, if that is the group''s allotted slot).\nLater, proceed to Bhairon Temple via Ropeway (optional). It is believed that the pilgrimage is completed only after visiting Bhairon Baba Temple.\nThereafter, return to Sanjichhat Helipad and board the helicopter back to Katra.\nAfter lunch, visit:\n- Banganga (darshan at the sacred stream)\n- Darshani Deodi\n- Katra Local Market\nIn the evening, drive back to Jammu (approx. 50 km) and check in to the same hotel as Day 1.',
   'Jammu'),
  (4,'Jammu – Departure',
   E'After breakfast, check out from the hotel and transfer to Jammu Airport (approx. 7 km) for return flights after 2 pm, with divine blessings and cherished memories.',
   null)
) as d(day_number,title,body,stay)
where y.slug='vaishno-devi-helicopter-package' and i.version=1
on conflict (itinerary_id,day_number) do update set title=excluded.title,
  body=excluded.body, stay=excluded.stay;

-- Departure: 13–16 March 2027
insert into yatra_batches (yatra_id,start_date,end_date,status) select y.id,'2027-03-13'::date,'2027-03-16'::date,'planned'::batch_status from yatras y where y.slug='vaishno-devi-helicopter-package' and not exists (select 1 from yatra_batches x where x.yatra_id=y.id and x.start_date='2027-03-13'::date);

-- 2027 season, one batch a month, chosen for weather and to avoid Navratri crowds
insert into yatra_batches (yatra_id,start_date,end_date,status) select y.id,'2027-04-17'::date,'2027-04-20'::date,'planned'::batch_status from yatras y where y.slug='vaishno-devi-helicopter-package' and not exists (select 1 from yatra_batches x where x.yatra_id=y.id and x.start_date='2027-04-17'::date);
insert into yatra_batches (yatra_id,start_date,end_date,status) select y.id,'2027-05-08'::date,'2027-05-11'::date,'planned'::batch_status from yatras y where y.slug='vaishno-devi-helicopter-package' and not exists (select 1 from yatra_batches x where x.yatra_id=y.id and x.start_date='2027-05-08'::date);
insert into yatra_batches (yatra_id,start_date,end_date,status) select y.id,'2027-06-05'::date,'2027-06-08'::date,'planned'::batch_status from yatras y where y.slug='vaishno-devi-helicopter-package' and not exists (select 1 from yatra_batches x where x.yatra_id=y.id and x.start_date='2027-06-05'::date);
insert into yatra_batches (yatra_id,start_date,end_date,status) select y.id,'2027-09-18'::date,'2027-09-21'::date,'planned'::batch_status from yatras y where y.slug='vaishno-devi-helicopter-package' and not exists (select 1 from yatra_batches x where x.yatra_id=y.id and x.start_date='2027-09-18'::date);
insert into yatra_batches (yatra_id,start_date,end_date,status) select y.id,'2027-10-16'::date,'2027-10-19'::date,'planned'::batch_status from yatras y where y.slug='vaishno-devi-helicopter-package' and not exists (select 1 from yatra_batches x where x.yatra_id=y.id and x.start_date='2027-10-16'::date);

-- Winter batches: Feb 2027, then Dec 2027 – Mar 2028 (avoiding the Christmas–New Year rush, Republic Day, Holi and Navratri)
insert into yatra_batches (yatra_id,start_date,end_date,status) select y.id,'2027-02-13'::date,'2027-02-16'::date,'planned'::batch_status from yatras y where y.slug='vaishno-devi-helicopter-package' and not exists (select 1 from yatra_batches x where x.yatra_id=y.id and x.start_date='2027-02-13'::date);
insert into yatra_batches (yatra_id,start_date,end_date,status) select y.id,'2027-12-04'::date,'2027-12-07'::date,'planned'::batch_status from yatras y where y.slug='vaishno-devi-helicopter-package' and not exists (select 1 from yatra_batches x where x.yatra_id=y.id and x.start_date='2027-12-04'::date);
insert into yatra_batches (yatra_id,start_date,end_date,status) select y.id,'2028-01-15'::date,'2028-01-18'::date,'planned'::batch_status from yatras y where y.slug='vaishno-devi-helicopter-package' and not exists (select 1 from yatra_batches x where x.yatra_id=y.id and x.start_date='2028-01-15'::date);
insert into yatra_batches (yatra_id,start_date,end_date,status) select y.id,'2028-02-12'::date,'2028-02-15'::date,'planned'::batch_status from yatras y where y.slug='vaishno-devi-helicopter-package' and not exists (select 1 from yatra_batches x where x.yatra_id=y.id and x.start_date='2028-02-12'::date);
insert into yatra_batches (yatra_id,start_date,end_date,status) select y.id,'2028-03-18'::date,'2028-03-21'::date,'planned'::batch_status from yatras y where y.slug='vaishno-devi-helicopter-package' and not exists (select 1 from yatra_batches x where x.yatra_id=y.id and x.start_date='2028-03-18'::date);

-- Package price for every 2027–28 departure: ₹50,000 per person + 5% GST, excluding flight charges
insert into batch_pricing (batch_id,yatra_id,tier,amount,gst,currency,effective_from)
select b.id,y.id,'general'::price_tier,50000,2500,'INR','2026-10-21'::date
from yatras y join yatra_batches b on b.yatra_id=y.id and b.start_date between '2027-01-01'::date and '2028-03-31'::date
where y.slug='vaishno-devi-helicopter-package' and not exists (select 1 from batch_pricing p where p.batch_id=b.id and p.tier='general');

commit;
