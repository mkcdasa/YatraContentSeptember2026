-- ============================================================================
-- Yatra Knowledge Base — core schema
-- Hare Krishna Golden Temple, Yatra Department
-- ============================================================================
create extension if not exists "pgcrypto";
create extension if not exists "pg_trgm";

-- ---------------------------------------------------------------------------
-- Enums
-- ---------------------------------------------------------------------------
create type app_role       as enum ('admin', 'staff', 'tour_leader', 'yatri');
create type yatra_scope    as enum ('domestic', 'national', 'international');
create type yatra_nature   as enum ('seasonal', 'evergreen', 'risky', 'special');
create type batch_status   as enum ('planned', 'open', 'filling', 'full', 'completed', 'cancelled');
create type price_tier     as enum ('general', 'premium');
create type vendor_kind    as enum ('hotel', 'dmc', 'helicopter', 'airline', 'transport', 'insurance', 'catering', 'guide', 'permit', 'other');
create type place_kind     as enum ('jyotirlinga', 'shakti_peetha', 'divya_desam', 'char_dham', 'iskcon', 'unesco', 'river', 'temple', 'other');
create type event_kind     as enum ('iskcon_festival', 'hindu_festival', 'public_holiday', 'special_occasion', 'departure', 'marriage_season');
create type video_kind     as enum ('expert', 'destination', 'promo', 'training', 'testimonial');
create type audience       as enum ('public', 'staff');
create type verdict        as enum ('pro', 'con');

-- ---------------------------------------------------------------------------
-- Identity
-- ---------------------------------------------------------------------------
create table profiles (
  id          uuid primary key references auth.users on delete cascade,
  full_name   text,
  email       text,
  phone       text,
  city        text,
  role        app_role not null default 'yatri',
  is_active   boolean  not null default true,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);
comment on table profiles is 'One row per signed-in user. role drives every RLS policy in this schema.';

-- SECURITY DEFINER so RLS policies can read the caller''s role without
-- recursing into profiles'' own policies.
create or replace function auth_role() returns app_role
language sql stable security definer set search_path = public as $$
  select role from profiles where id = auth.uid()
$$;

create or replace function is_staff() returns boolean
language sql stable security definer set search_path = public as $$
  select coalesce((select role in ('admin','staff','tour_leader') from profiles where id = auth.uid()), false)
$$;

create or replace function is_admin() returns boolean
language sql stable security definer set search_path = public as $$
  select coalesce((select role = 'admin' from profiles where id = auth.uid()), false)
$$;

-- Every new auth user gets a profile. First user in an empty table becomes admin
-- so the deployment is not locked out of its own admin screens.
create or replace function handle_new_user() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into profiles (id, email, full_name, role)
  values (
    new.id,
    new.email,
    coalesce(new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'name', split_part(new.email, '@', 1)),
    case when (select count(*) from profiles) = 0 then 'admin'::app_role else 'yatri'::app_role end
  );
  return new;
end $$;

create trigger on_auth_user_created
  after insert on auth.users for each row execute function handle_new_user();

-- ---------------------------------------------------------------------------
-- Places: temples, Jyotirlingas, Shakti Peethas, Divya Desams, rivers
-- ---------------------------------------------------------------------------
create table destinations (
  id            uuid primary key default gen_random_uuid(),
  slug          text unique not null,
  name          text not null,
  kinds         place_kind[] not null default '{}',
  deity         text,
  region        text,
  city          text,
  state         text,
  country       text not null default 'India',
  best_months   smallint[] not null default '{}',   -- 1..12
  avoid_months  smallint[] not null default '{}',
  best_time_note text,
  sevas         text[] not null default '{}',
  speciality    text,
  description   text,
  map_url       text,
  image_url     text,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);
create index on destinations using gin (kinds);
create index on destinations (state);
create index destinations_search_idx on destinations using gin (
  (name || ' ' || coalesce(deity,'') || ' ' || coalesce(city,'') || ' ' || coalesce(state,'')) gin_trgm_ops
);

-- Sthala-purana / lila narrations attached to a place
create table pastimes (
  id             uuid primary key default gen_random_uuid(),
  destination_id uuid references destinations on delete cascade,
  title          text not null,
  source         text,                       -- Bhagavatam, Padma Purana, ...
  body           text not null,
  lang           text not null default 'en',
  created_at     timestamptz not null default now()
);
create index on pastimes (destination_id);

-- ---------------------------------------------------------------------------
-- Yatras
-- ---------------------------------------------------------------------------
create table yatras (
  id                uuid primary key default gen_random_uuid(),
  slug              text unique not null,
  title             text not null,
  scope             yatra_scope not null default 'domestic',
  nature            yatra_nature not null default 'evergreen',
  themes            text[] not null default '{}',  -- Dwadasha Jyotirlinga, Ramayana Trail...
  nights            smallint,
  days              smallint,
  min_pax           smallint default 30,
  summary           text,
  highlights        text[] not null default '{}',
  inclusions        text[] not null default '{}',
  exclusions        text[] not null default '{}',
  difficulty        smallint check (difficulty between 1 and 5),  -- 1 easy .. 5 Kailash
  senior_friendly   boolean not null default true,
  visa_required     boolean not null default false,
  visa_notes        text,
  repeatable_per_year smallint,                -- "8 times a year" lives here
  hero_image_url    text,
  is_published      boolean not null default true,
  created_at        timestamptz not null default now(),
  updated_at        timestamptz not null default now()
);
create index on yatras (scope);
create index on yatras using gin (themes);

create table yatra_destinations (
  yatra_id       uuid references yatras on delete cascade,
  destination_id uuid references destinations on delete cascade,
  sequence       smallint,
  primary key (yatra_id, destination_id)
);

-- When a yatra should and should not run. Feature 6, 7 and 13.
create table travel_windows (
  id            uuid primary key default gen_random_uuid(),
  yatra_id      uuid references yatras on delete cascade,
  best_months   smallint[] not null default '{}',
  shoulder_months smallint[] not null default '{}',
  avoid_months  smallint[] not null default '{}',
  open_months   smallint,                      -- "9 months", "5 months"
  weather_note  text,
  caution       text,                          -- permit delays, snowfall, monsoon
  created_at    timestamptz not null default now()
);
create unique index on travel_windows (yatra_id);

-- Feature 2: pros and cons, captured as reviewable rows rather than prose.
create table yatra_notes (
  id         uuid primary key default gen_random_uuid(),
  yatra_id   uuid not null references yatras on delete cascade,
  verdict    verdict not null,
  body       text not null,
  weight     smallint not null default 3 check (weight between 1 and 5),
  created_by uuid references profiles,
  created_at timestamptz not null default now()
);
create index on yatra_notes (yatra_id);

-- ---------------------------------------------------------------------------
-- Itineraries (versioned — an itinerary is edited season after season)
-- ---------------------------------------------------------------------------
create table itineraries (
  id          uuid primary key default gen_random_uuid(),
  yatra_id    uuid not null references yatras on delete cascade,
  version     smallint not null default 1,
  title       text,
  intro       text,
  notes       text,
  is_current  boolean not null default true,
  created_at  timestamptz not null default now(),
  unique (yatra_id, version)
);
create index on itineraries (yatra_id) where is_current;

create table itinerary_days (
  id            uuid primary key default gen_random_uuid(),
  itinerary_id  uuid not null references itineraries on delete cascade,
  day_number    smallint not null,
  title         text,
  body          text,
  stay          text,
  meals         text,
  created_at    timestamptz not null default now(),
  unique (itinerary_id, day_number)
);

-- ---------------------------------------------------------------------------
-- Departures and money
-- ---------------------------------------------------------------------------
create table yatra_batches (
  id          uuid primary key default gen_random_uuid(),
  yatra_id    uuid not null references yatras on delete cascade,
  start_date  date not null,
  end_date    date,
  status      batch_status not null default 'planned',
  seats_total smallint,
  seats_left  smallint,
  departure_city text,
  notes       text,
  created_at  timestamptz not null default now()
);
create index on yatra_batches (start_date);
create index on yatra_batches (yatra_id, start_date);

-- STAFF ONLY. Negotiated numbers never reach a yatri''s device.
create table batch_pricing (
  id         uuid primary key default gen_random_uuid(),
  batch_id   uuid references yatra_batches on delete cascade,
  yatra_id   uuid references yatras on delete cascade,
  tier       price_tier not null default 'general',
  amount     numeric(12,2) not null,
  gst        numeric(12,2) not null default 0,
  tcs        numeric(12,2) not null default 0,
  total      numeric(12,2) generated always as (amount + gst + tcs) stored,
  currency   char(3) not null default 'INR',
  effective_from date,
  created_at timestamptz not null default now(),
  check (batch_id is not null or yatra_id is not null)
);
create index on batch_pricing (yatra_id, tier);

-- STAFF ONLY. Feature 5 and 11: what actually makes money.
create table batch_economics (
  id                uuid primary key default gen_random_uuid(),
  batch_id          uuid references yatra_batches on delete cascade,
  yatra_id          uuid references yatras on delete cascade,
  expected_pax      smallint,
  ticket_avg        numeric(12,2),
  expected_revenue  numeric(14,2),
  cost_flights      numeric(14,2) default 0,
  cost_helicopter   numeric(14,2) default 0,
  cost_transport    numeric(14,2) default 0,
  cost_prasadam     numeric(14,2) default 0,
  cost_events       numeric(14,2) default 0,
  cost_marketing    numeric(14,2) default 0,
  cost_salary       numeric(14,2) default 0,
  cost_admin        numeric(14,2) default 0,
  cost_prep         numeric(14,2) default 0,
  total_expenditure numeric(14,2),
  expected_surplus  numeric(14,2),
  margin_pct        numeric(6,2),
  notes             text,
  created_at        timestamptz not null default now(),
  check (batch_id is not null or yatra_id is not null)
);
create index on batch_economics (yatra_id);

-- ---------------------------------------------------------------------------
-- Vendors and negotiated rates — STAFF ONLY (feature 9)
-- ---------------------------------------------------------------------------
create table vendors (
  id             uuid primary key default gen_random_uuid(),
  name           text not null,
  kind           vendor_kind not null default 'other',
  city           text,
  state          text,
  country        text default 'India',
  contact_person text,
  phone          text,
  alt_phone      text,
  email          text,
  website        text,
  map_url        text,
  rating         smallint check (rating between 1 and 5),
  is_preferred   boolean not null default false,
  notes          text,
  created_at     timestamptz not null default now(),
  updated_at     timestamptz not null default now()
);
create index on vendors (kind);
create index on vendors (city);

create table vendor_rates (
  id             uuid primary key default gen_random_uuid(),
  vendor_id      uuid not null references vendors on delete cascade,
  yatra_id       uuid references yatras on delete set null,
  destination_id uuid references destinations on delete set null,
  service        text not null,                 -- "Deluxe twin sharing, AP"
  rate           numeric(12,2) not null,
  unit           text not null default 'per person per night',
  currency       char(3) not null default 'INR',
  valid_from     date,
  valid_to       date,
  is_final       boolean not null default false, -- negotiated and signed off
  terms          text,
  created_at     timestamptz not null default now()
);
create index on vendor_rates (vendor_id);
create index on vendor_rates (yatra_id);

-- ---------------------------------------------------------------------------
-- Calendar (feature 3, 8) — panchanga + festivals + departures in one grain
-- ---------------------------------------------------------------------------
create table calendar_events (
  id           uuid primary key default gen_random_uuid(),
  on_date      date not null,
  kind         event_kind not null,
  title        text not null,
  tithi        text,
  masam        text,
  paksha       text,
  nakshatra    text,
  yoga         text,
  karana       text,
  temple       text,
  deity        text,
  significance text,
  yatra_id     uuid references yatras on delete set null,
  destination_id uuid references destinations on delete set null,
  created_at   timestamptz not null default now()
);
create index on calendar_events (on_date);
create index on calendar_events (kind, on_date);

-- Panchanga is one row per date, independent of whether anything is scheduled.
-- Keeping it out of calendar_events stops every tithi becoming a fake "event".
create table panchanga (
  on_date    date primary key,
  tithi      text,
  masam      text,
  paksha     text,
  nakshatra  text,
  yoga       text,
  karana     text
);

-- ---------------------------------------------------------------------------
-- Library: YouTube (feature 14) and written knowledge
-- ---------------------------------------------------------------------------
create table videos (
  id             uuid primary key default gen_random_uuid(),
  title          text not null,
  youtube_id     text,
  url            text not null,
  kind           video_kind not null default 'expert',
  channel        text,
  yatra_id       uuid references yatras on delete set null,
  destination_id uuid references destinations on delete set null,
  notes          text,
  created_at     timestamptz not null default now()
);
create index on videos (kind);

create table knowledge_articles (
  id          uuid primary key default gen_random_uuid(),
  slug        text unique not null,
  title       text not null,
  category    text not null,         -- packing, sos, hospitality, marketing, orientation
  body_md     text not null,
  visibility  audience not null default 'public',
  yatra_id    uuid references yatras on delete set null,
  updated_at  timestamptz not null default now(),
  created_at  timestamptz not null default now()
);
create index on knowledge_articles (category);

-- Feature 11: finance team output, stored as a record with an optional file.
create table finance_reports (
  id          uuid primary key default gen_random_uuid(),
  title       text not null,
  period      text,                  -- "FY 2025-26 Q1"
  yatra_id    uuid references yatras on delete set null,
  summary     text,
  file_path   text,                  -- Supabase Storage object path
  uploaded_by uuid references profiles,
  created_at  timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- updated_at maintenance
-- ---------------------------------------------------------------------------
create or replace function touch_updated_at() returns trigger
language plpgsql as $$
begin new.updated_at = now(); return new; end $$;

create trigger t_profiles    before update on profiles    for each row execute function touch_updated_at();
create trigger t_destinations before update on destinations for each row execute function touch_updated_at();
create trigger t_yatras      before update on yatras      for each row execute function touch_updated_at();
create trigger t_vendors     before update on vendors     for each row execute function touch_updated_at();
create trigger t_articles    before update on knowledge_articles for each row execute function touch_updated_at();
