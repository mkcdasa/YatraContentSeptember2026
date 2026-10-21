-- 8 Days Vaishno Devi & Kashmir Pilgrimage Tour Package
-- Jammu – Katra – Vaishno Devi – Srinagar – Gulmarg – Sonamarg – Pahalgam – Srinagar (7 nights / 8 days)
--
-- Hand-authored content, not produced by scripts/import_content.py. Idempotent:
-- keyed on the yatra slug, safe to re-run after the team edits it in the app.

begin;

insert into yatras (slug,title,scope,nature,themes,nights,days,difficulty,senior_friendly,
  visa_required,summary,highlights) values (
  'vaishno-devi-kashmir-8-day',
  '8 Days Vaishno Devi & Kashmir Pilgrimage Tour Package',
  'domestic'::yatra_scope,'evergreen'::yatra_nature,'{}',7,8,2,true,false,
  'Jammu – Katra – Vaishno Devi – Srinagar – Gulmarg – Sonamarg – Pahalgam – Srinagar. Jammu temple circuit, helicopter darshan of Shri Mata Vaishno Devi with a night at Bhawan, then Kashmir''s temples and valleys: Kheer Bhawani, Shankaracharya, Jyeshta Devi, Martand, Avantipur, Gulmarg, Sonamarg and a visit to Pahalgam.',
  array[
    'Jammu Temple Circuit',
    'Helicopter Darshan of Shri Mata Vaishno Devi',
    'Morning Aarti at Bhawan',
    'Bhairon Baba Temple Visit',
    'Banganga & Darshani Deodi',
    'Shikara Ride on Dal Lake',
    'Maharani Temple, Gulmarg',
    'Kheer Bhawani Temple',
    'Martand Sun Temple',
    'Avantipur Temple Ruins',
    'Shankaracharya Temple',
    'Jyeshta Devi Temple',
    'Gulmarg, Sonamarg & Pahalgam Excursions'
  ])
on conflict (slug) do update set title=excluded.title, scope=excluded.scope,
  nature=excluded.nature, nights=excluded.nights, days=excluded.days,
  difficulty=excluded.difficulty, summary=excluded.summary, highlights=excluded.highlights;

insert into itineraries (yatra_id,version,title,intro,notes,is_current)
select y.id,1,'8 Days Vaishno Devi & Kashmir Pilgrimage Tour Package',
  'Jammu – Katra – Vaishno Devi – Srinagar – Gulmarg – Sonamarg – Pahalgam – Srinagar',
  E'Overnight stays: 02 Nights Jammu, 01 Night Bhawan, 03 Nights Srinagar, 01 Night Gulmarg.\nPrice: ₹1,00,000 per person + 5% GST, excluding flight charges. All-inclusive: hotels, all meals, helicopter, ropeway, battery car, Jammu–Srinagar flight, Gulmarg gondola, Thajiwas pony, shikara and transfers.\nFlights: arrive Jammu Airport on 13 March before 2 pm; Jammu → Srinagar on 16 March between 11 am and 12 noon; depart Srinagar Airport on 20 March after 2 pm.\nTour ends with the divine blessings of Mata Vaishno Devi and Lord Shiva. Jai Mata Di! Har Har Mahadev!',
  true
from yatras y where y.slug='vaishno-devi-kashmir-8-day'
on conflict (yatra_id,version) do update set title=excluded.title, intro=excluded.intro,
  notes=excluded.notes;

insert into itinerary_days (itinerary_id,day_number,title,body,stay)
select i.id,d.day_number,d.title,d.body,d.stay
from itineraries i join yatras y on y.id=i.yatra_id
cross join (values
  (1,'Jammu Arrival – Local Sightseeing',
   E'Arrive at Jammu Airport by 2 pm, meet our representative and transfer to the hotel.\nAfter freshening up, proceed for local sightseeing:\n- Raghunath Temple\n- Ranbireshwar Temple\n- Bawe Wali Mata Temple\n- Peer Kho Cave Temple\n- Bahu Fort\nReturn to the hotel in the evening.',
   'Jammu'),
  (2,'Jammu – Katra – Vaishno Devi by Helicopter',
   E'After breakfast, proceed to Katra (approx. 50 km / 1.5 hours).\nComplete Yatra registration formalities and report at Katra Helipad as per the allotted schedule.\nBoard the helicopter to Sanjichhat (flight duration approximately 5–8 minutes).\nRoute: Katra Helipad → Sanjichhat Helipad → Bhawan (approx. 2.5 km by battery car).\nProceed towards Shri Mata Vaishno Devi Bhawan and participate in the divine Evening Darshan and Aarti.',
   'Bhawan'),
  (3,'Morning Aarti – Bhairon Temple – Katra – Jammu',
   E'Early morning, attend the sacred Morning Aarti at Shri Mata Vaishno Devi Bhawan.\nLater, proceed to Bhairon Temple via Ropeway (optional). It is believed that the pilgrimage is completed only after visiting Bhairon Baba Temple.\nThereafter, return to Sanjichhat Helipad and board the helicopter back to Katra.\nAfter lunch, visit:\n- Banganga\n- Darshani Deodi\n- Katra Local Market\nIn the evening, drive back to Jammu (approx. 50 km) and check in to the same hotel as Day 1.',
   'Jammu'),
  (4,'Jammu – Flight to Srinagar',
   E'After breakfast, check out from the hotel and proceed to Jammu Airport.\nBoard your flight to Srinagar (departs between 11 am and 12 noon).\nUpon arrival in Srinagar, transfer to the hotel. After lunch, visit:\n- Shankaracharya Temple\n- Jyeshta Devi Temple\nIn the evening, enjoy a relaxing Shikara Ride on Dal Lake.',
   'Srinagar'),
  (5,'Srinagar – Gulmarg',
   E'After breakfast, proceed to Gulmarg.\nVisit:\n- Maharani Temple\n- Gulmarg Gondola Ride\n- Apharwat Peak\n- Snow Point\n- Scenic Himalayan Viewpoints\nEnjoy the breathtaking beauty of Gulmarg.',
   'Gulmarg'),
  (6,'Gulmarg – Sonamarg – Srinagar',
   E'After breakfast, proceed towards Sonamarg, popularly known as the "Meadow of Gold."\nVisit:\n- Thajiwas Glacier (pony ride)\n- Sindh River\n- Snow-covered Mountain Viewpoints\nEn route, visit:\n- Kheer Bhawani Temple, Tulmulla\nLater proceed to Srinagar.',
   'Srinagar'),
  (7,'Srinagar – Avantipur – Martand – Pahalgam – Srinagar',
   E'After breakfast, a day trip south of Srinagar.\nVisit:\n- Avantipur Temple Ruins\n- Martand Sun Temple\n- Pahalgam town (lunch and a short stroll)\nReturn to Srinagar in the evening.',
   'Srinagar'),
  (8,'Srinagar – Pampore – Departure',
   E'After breakfast, check out from the hotel and visit Pampore for saffron and dry-fruit shopping.\nAfter lunch, transfer to Srinagar Airport for departure flights after 2 pm, with divine blessings and memorable experiences.',
   null)
) as d(day_number,title,body,stay)
where y.slug='vaishno-devi-kashmir-8-day' and i.version=1
on conflict (itinerary_id,day_number) do update set title=excluded.title,
  body=excluded.body, stay=excluded.stay;

-- Departure: 13–20 March 2027
insert into yatra_batches (yatra_id,start_date,end_date,status) select y.id,'2027-03-13'::date,'2027-03-20'::date,'planned'::batch_status from yatras y where y.slug='vaishno-devi-kashmir-8-day' and not exists (select 1 from yatra_batches x where x.yatra_id=y.id and x.start_date='2027-03-13'::date);

-- Package price for this departure: ₹100,000 per person + 5% GST, excluding flight charges
insert into batch_pricing (batch_id,yatra_id,tier,amount,gst,currency,effective_from)
select b.id,y.id,'general'::price_tier,100000,5000,'INR','2026-10-21'::date
from yatras y join yatra_batches b on b.yatra_id=y.id and b.start_date='2027-03-13'::date
where y.slug='vaishno-devi-kashmir-8-day' and not exists (select 1 from batch_pricing p where p.batch_id=b.id and p.tier='general');

commit;
