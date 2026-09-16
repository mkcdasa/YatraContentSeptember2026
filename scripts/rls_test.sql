-- ============================================================================
-- RLS acceptance test.
--
-- The whole premise of this app is that yatris and staff share one database and
-- one codebase while negotiated rates, margins and finance reports stay staff-
-- only. That is a security property, so it gets a test rather than a comment.
--
-- Run with scripts/validate_db.sh --rls
-- ============================================================================
\set ON_ERROR_STOP on
set client_min_messages = notice;

-- three users, three roles
insert into auth.users (id, email) values
  ('11111111-1111-1111-1111-111111111111', 'admin@example.org'),
  ('22222222-2222-2222-2222-222222222222', 'staff@example.org'),
  ('33333333-3333-3333-3333-333333333333', 'yatri@example.org');

update profiles set role = 'admin' where id = '11111111-1111-1111-1111-111111111111';
update profiles set role = 'staff' where id = '22222222-2222-2222-2222-222222222222';
update profiles set role = 'yatri' where id = '33333333-3333-3333-3333-333333333333';

insert into vendors (name, kind, city, phone) values ('Test Hotel', 'hotel', 'Haridwar', '+910000000000');
insert into vendor_rates (vendor_id, service, rate)
  select id, 'Deluxe twin sharing', 4500 from vendors where name = 'Test Hotel';

create or replace function assert_eq(actual bigint, expected bigint, label text) returns void
language plpgsql as $$
begin
  if actual is distinct from expected then
    raise exception 'FAIL % — expected %, got %', label, expected, actual;
  end if;
  raise notice 'pass  %', label;
end $$;

-- ---------------------------------------------------------------------------
-- as a yatri
-- ---------------------------------------------------------------------------
set role authenticated;
set request.jwt.claim.sub = '33333333-3333-3333-3333-333333333333';

select assert_eq((select count(*) from vendors),         0, 'yatri sees no vendors');
select assert_eq((select count(*) from vendor_rates),    0, 'yatri sees no negotiated rates');
select assert_eq((select count(*) from batch_pricing),   0, 'yatri sees no pricing');
select assert_eq((select count(*) from batch_economics), 0, 'yatri sees no margins');
select assert_eq((select count(*) from finance_reports), 0, 'yatri sees no finance reports');
select assert_eq((select count(*) from knowledge_articles where visibility = 'staff'), 0,
                 'yatri sees no staff-only articles');

-- but the itineraries and calendar are readable, which is the point
do $$ begin
  if (select count(*) from yatras) = 0 then raise exception 'FAIL yatri cannot read yatras'; end if;
  if (select count(*) from itinerary_days) = 0 then raise exception 'FAIL yatri cannot read itinerary days'; end if;
  if (select count(*) from calendar_events) = 0 then raise exception 'FAIL yatri cannot read calendar'; end if;
  raise notice 'pass  yatri reads yatras, itineraries and calendar';
end $$;

-- and cannot write, nor promote itself
do $$ begin
  begin
    insert into yatras (slug, title) values ('hacked', 'Hacked');
    raise exception 'FAIL yatri was able to insert a yatra';
  exception when insufficient_privilege or check_violation then
    raise notice 'pass  yatri cannot insert a yatra';
  end;
  begin
    update profiles set role = 'admin' where id = auth.uid();
    if found then raise exception 'FAIL yatri escalated to admin'; end if;
    raise notice 'pass  yatri cannot self-promote';
  exception when insufficient_privilege or check_violation then
    raise notice 'pass  yatri cannot self-promote';
  end;
end $$;

-- ---------------------------------------------------------------------------
-- as staff
-- ---------------------------------------------------------------------------
set request.jwt.claim.sub = '22222222-2222-2222-2222-222222222222';
do $$ begin
  if (select count(*) from vendors) = 0 then raise exception 'FAIL staff cannot read vendors'; end if;
  if (select count(*) from vendor_rates) = 0 then raise exception 'FAIL staff cannot read rates'; end if;
  if (select count(*) from batch_pricing) = 0 then raise exception 'FAIL staff cannot read pricing'; end if;
  if (select count(*) from batch_economics) = 0 then raise exception 'FAIL staff cannot read economics'; end if;
  raise notice 'pass  staff reads vendors, rates, pricing and economics';
end $$;

insert into yatras (slug, title) values ('staff-created', 'Staff Created Yatra');
do $$ begin raise notice 'pass  staff can write content'; end $$;

-- search must not leak a vendor to a yatri
set request.jwt.claim.sub = '33333333-3333-3333-3333-333333333333';
select assert_eq((select count(*) from search_all('Test Hotel')), 0, 'search leaks no vendor to a yatri');

reset role;
