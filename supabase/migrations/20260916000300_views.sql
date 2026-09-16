-- ============================================================================
-- Read models. Views inherit RLS from their base tables when created with
-- security_invoker, so the staff/public split above still holds.
-- ============================================================================

-- Upcoming departures with just enough yatra context for a card.
create view v_upcoming_departures with (security_invoker = true) as
select b.id as batch_id, b.start_date, b.end_date, b.status, b.seats_total, b.seats_left,
       b.departure_city, y.id as yatra_id, y.slug, y.title, y.scope, y.nature,
       y.nights, y.days, y.difficulty, y.hero_image_url,
       (b.start_date - current_date) as days_away
from yatra_batches b
join yatras y on y.id = b.yatra_id
where b.start_date >= current_date and y.is_published
order by b.start_date;

-- Feature 4 and 5 in one row per yatra: how often it repeats and what it earns.
-- Staff-only in practice because batch_economics and batch_pricing are staff-tier.
create view v_yatra_profitability with (security_invoker = true) as
select y.id as yatra_id, y.slug, y.title, y.scope, y.nature,
       y.repeatable_per_year,
       count(distinct b.id) filter (where extract(year from b.start_date) = extract(year from current_date)) as batches_this_year,
       avg(e.margin_pct)                as avg_margin_pct,
       sum(e.expected_surplus)          as total_expected_surplus,
       avg(p.total) filter (where p.tier = 'general') as avg_general_price
from yatras y
left join yatra_batches   b on b.yatra_id = y.id
left join batch_economics e on e.yatra_id = y.id
left join batch_pricing   p on p.yatra_id = y.id
group by y.id;

-- Calendar grain: one row per date with everything happening that day.
create view v_calendar_day with (security_invoker = true) as
select coalesce(e.on_date, p.on_date) as on_date,
       p.tithi, p.masam, p.paksha, p.nakshatra,
       count(e.id) filter (where e.kind = 'iskcon_festival') as iskcon_count,
       count(e.id) filter (where e.kind = 'hindu_festival')  as hindu_count,
       count(e.id) filter (where e.kind = 'departure')       as departure_count,
       count(e.id)                                           as total_count
from panchanga p
full outer join calendar_events e on e.on_date = p.on_date
group by coalesce(e.on_date, p.on_date), p.tithi, p.masam, p.paksha, p.nakshatra;

-- ---------------------------------------------------------------------------
-- Cross-entity search. Runs as invoker so a yatri can never surface a vendor.
-- ---------------------------------------------------------------------------
create or replace function search_all(q text, lim int default 20)
returns table (kind text, id uuid, title text, subtitle text, slug text)
language sql stable security invoker set search_path = public as $$
  (select 'yatra', y.id, y.title,
          coalesce(y.summary, y.scope::text), y.slug
   from yatras y where y.title ilike '%'||q||'%' and y.is_published limit lim)
  union all
  (select 'destination', d.id, d.name,
          concat_ws(' · ', d.deity, d.state), d.slug
   from destinations d
   where d.name ilike '%'||q||'%' or d.deity ilike '%'||q||'%' or d.city ilike '%'||q||'%' limit lim)
  union all
  (select 'vendor', v.id, v.name,
          concat_ws(' · ', v.kind::text, v.city), null
   from vendors v where v.name ilike '%'||q||'%' limit lim)
  union all
  (select 'article', a.id, a.title, a.category, a.slug
   from knowledge_articles a where a.title ilike '%'||q||'%' limit lim);
$$;
