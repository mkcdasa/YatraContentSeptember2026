-- 4 Days Vaishno Devi Helicopter Package
-- Jammu – Katra – Vaishno Devi – Jammu (3 nights / 4 days)
--
-- Hand-authored content, not produced by scripts/import_content.py. Idempotent:
-- keyed on the yatra slug, safe to re-run after the team edits it in the app.

begin;

insert into yatras (slug,title,scope,nature,themes,nights,days,difficulty,senior_friendly,
  visa_required,summary,highlights) values (
  'vaishno-devi-helicopter-package',
  '4 Days Vaishno Devi Helicopter Package',
  'domestic'::yatra_scope,'evergreen'::yatra_nature,'{}',3,4,2,true,false,
  'Jammu – Katra – Vaishno Devi – Jammu. Jammu temple sightseeing, helicopter from Katra to Sanjichhat, Evening Darshan and Aarti, a night at Bhawan, Morning Aarti and Bhairon Baba Temple before returning to Katra.',
  array[
    'Jammu Temple Sightseeing',
    'Helicopter Ride from Katra to Sanjichhat',
    'Shri Mata Vaishno Devi Darshan',
    'Morning Aarti at Bhawan',
    'Bhairon Baba Temple Visit',
    'Banganga & Darshani Deodi Visit',
    'Shopping at Katra Market'
  ])
on conflict (slug) do update set title=excluded.title, scope=excluded.scope,
  nature=excluded.nature, nights=excluded.nights, days=excluded.days,
  difficulty=excluded.difficulty, summary=excluded.summary, highlights=excluded.highlights;

insert into itineraries (yatra_id,version,title,intro,notes,is_current)
select y.id,1,'4 Days Vaishno Devi Helicopter Package',
  'Jammu – Katra – Vaishno Devi – Jammu',
  E'Overnight stays: 01 Night Jammu, 01 Night Bhawan, 01 Night Katra.\nTour ends with the divine blessings of Mata Vaishno Devi. Jai Mata Di!',
  true
from yatras y where y.slug='vaishno-devi-helicopter-package'
on conflict (yatra_id,version) do update set title=excluded.title, intro=excluded.intro,
  notes=excluded.notes;

insert into itinerary_days (itinerary_id,day_number,title,body,stay)
select i.id,d.day_number,d.title,d.body,d.stay
from itineraries i join yatras y on y.id=i.yatra_id
cross join (values
  (1,'Jammu Arrival – Local Sightseeing',
   E'Upon arrival at Jammu Airport or Railway Station, meet our representative and transfer to the hotel.\nAfter freshening up, proceed for local sightseeing:\n- Raghunath Temple\n- Ranbireshwar Temple\n- Bawe Wali Mata Temple\n- Peer Kho Cave Temple\n- Bahu Fort\nReturn to the hotel in the evening.',
   'Jammu'),
  (2,'Jammu – Katra – Vaishno Devi by Helicopter',
   E'After breakfast, proceed to Katra (approx. 50 km / 1.5 hours).\nComplete Yatra registration formalities and report at Katra Helipad as per the allotted schedule.\nBoard the helicopter to Sanjichhat (flight duration approximately 5–8 minutes).\nRoute: Katra Helipad → Sanjichhat Helipad → Bhawan (approx. 2.5 km by walk, pony, palki, or battery vehicle).\nProceed towards Shri Mata Vaishno Devi Bhawan and participate in the divine Evening Darshan and Aarti.',
   'Bhawan'),
  (3,'Morning Aarti – Bhairon Temple – Return to Katra',
   E'Early morning, attend the sacred Morning Aarti at Shri Mata Vaishno Devi Bhawan.\nLater, proceed to Bhairon Temple via Ropeway (optional). It is believed that the pilgrimage is completed only after visiting Bhairon Baba Temple.\nThereafter, return to Sanjichhat Helipad and board the helicopter back to Katra.\nUpon arrival, check in to the hotel and relax.\nIn the evening, enjoy free time for shopping and exploring:\n- Banganga\n- Darshani Deodi\n- Katra Local Market',
   'Katra'),
  (4,'Katra – Jammu – Departure',
   E'After breakfast, check out from the hotel and proceed towards Jammu.\nTransfer to Jammu Airport or Railway Station for your onward journey with divine blessings and cherished memories.',
   null)
) as d(day_number,title,body,stay)
where y.slug='vaishno-devi-helicopter-package' and i.version=1
on conflict (itinerary_id,day_number) do update set title=excluded.title,
  body=excluded.body, stay=excluded.stay;

-- Departure: 13–16 March 2027
insert into yatra_batches (yatra_id,start_date,end_date,status) select y.id,'2027-03-13'::date,'2027-03-16'::date,'planned'::batch_status from yatras y where y.slug='vaishno-devi-helicopter-package' and not exists (select 1 from yatra_batches x where x.yatra_id=y.id and x.start_date='2027-03-13'::date);

commit;
