-- ============================================================================
-- Row Level Security
--
-- Two tiers, deliberately blunt so they are auditable at a glance:
--
--   PUBLIC   readable by any signed-in user, including yatris.
--            Itineraries, destinations, calendar, pastimes, videos, public
--            knowledge articles, batches (dates and seats, never money).
--
--   STAFF    readable only by admin / staff / tour_leader.
--            Vendors, negotiated rates, pricing, economics, finance reports,
--            staff-only articles.
--
-- Writes are staff-or-admin everywhere. Nothing is writable by a yatri.
-- ============================================================================

alter table profiles           enable row level security;
alter table destinations       enable row level security;
alter table pastimes           enable row level security;
alter table yatras             enable row level security;
alter table yatra_destinations enable row level security;
alter table travel_windows     enable row level security;
alter table yatra_notes        enable row level security;
alter table itineraries        enable row level security;
alter table itinerary_days     enable row level security;
alter table yatra_batches      enable row level security;
alter table batch_pricing      enable row level security;
alter table batch_economics    enable row level security;
alter table vendors            enable row level security;
alter table vendor_rates       enable row level security;
alter table calendar_events    enable row level security;
alter table videos             enable row level security;
alter table knowledge_articles enable row level security;
alter table finance_reports    enable row level security;
alter table panchanga          enable row level security;

-- --- profiles ---------------------------------------------------------------
create policy "read own profile"    on profiles for select using (id = auth.uid());
create policy "staff read profiles" on profiles for select using (is_staff());
create policy "update own profile"  on profiles for update using (id = auth.uid())
  -- a user may edit their own name and city but never promote themselves
  with check (id = auth.uid() and role = (select role from profiles where id = auth.uid()));
create policy "admin writes profiles" on profiles for all using (is_admin()) with check (is_admin());

-- --- public-tier content: read for all authenticated, write for staff --------
do $$
declare t text;
begin
  foreach t in array array[
    'destinations','pastimes','yatras','yatra_destinations','travel_windows',
    'yatra_notes','itineraries','itinerary_days','yatra_batches','calendar_events','videos','panchanga'
  ] loop
    execute format('create policy "read %1$s" on %1$I for select to authenticated using (true)', t);
    execute format('create policy "staff write %1$s" on %1$I for all to authenticated using (is_staff()) with check (is_staff())', t);
  end loop;
end $$;

-- --- staff-tier content ------------------------------------------------------
do $$
declare t text;
begin
  foreach t in array array['vendors','vendor_rates','batch_pricing','batch_economics','finance_reports'] loop
    execute format('create policy "staff read %1$s" on %1$I for select to authenticated using (is_staff())', t);
    execute format('create policy "staff write %1$s" on %1$I for all to authenticated using (is_staff()) with check (is_staff())', t);
  end loop;
end $$;

-- --- knowledge articles: row-level visibility flag ---------------------------
create policy "read public articles" on knowledge_articles for select to authenticated
  using (visibility = 'public' or is_staff());
create policy "staff write articles" on knowledge_articles for all to authenticated
  using (is_staff()) with check (is_staff());

-- --- storage: finance reports and hero images --------------------------------
insert into storage.buckets (id, name, public)
values ('finance', 'finance', false), ('media', 'media', true)
on conflict (id) do nothing;

create policy "staff read finance objects" on storage.objects for select
  using (bucket_id = 'finance' and is_staff());
create policy "staff write finance objects" on storage.objects for insert
  with check (bucket_id = 'finance' and is_staff());
create policy "anyone reads media" on storage.objects for select
  using (bucket_id = 'media');
create policy "staff writes media" on storage.objects for insert
  with check (bucket_id = 'media' and is_staff());

-- ---------------------------------------------------------------------------
-- Grants.
--
-- Supabase's model is broad table grants gated by RLS, not narrow grants. Being
-- explicit here means the schema behaves identically on a plain Postgres used
-- for CI, and means a future table added without a policy fails closed (no
-- policy = no rows) rather than depending on inherited defaults.
-- ---------------------------------------------------------------------------
grant usage on schema public to anon, authenticated;
grant select, insert, update, delete on all tables in schema public to authenticated;
grant select on all tables in schema public to anon;
grant execute on all functions in schema public to anon, authenticated;
grant usage, select on all sequences in schema public to authenticated;

alter default privileges in schema public
  grant select, insert, update, delete on tables to authenticated;
alter default privileges in schema public grant execute on functions to anon, authenticated;
