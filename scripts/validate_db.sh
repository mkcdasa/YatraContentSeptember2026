#!/usr/bin/env bash
# Apply every migration and the generated seed to a throwaway database.
# Run before pushing schema changes: it catches syntax errors, bad enum casts
# and RLS policies that reference columns that do not exist.
set -euo pipefail
PSQL=${PSQL:-psql}
CONN=${CONN:-"-h /var/tmp/yatrapg -p 5433 -U postgres"}
DB=${DB:-yatra_validate}

$PSQL $CONN -q -c "drop database if exists $DB;" -c "create database $DB;"
$PSQL $CONN -d "$DB" -q -v ON_ERROR_STOP=1 -f scripts/supabase_stub.sql
for f in supabase/migrations/*.sql; do
  echo "  applying $(basename "$f")"
  $PSQL $CONN -d "$DB" -q -v ON_ERROR_STOP=1 -f "$f"
done
echo "  applying seed"
for f in supabase/seed/*.sql; do
  $PSQL $CONN -d "$DB" -q -v ON_ERROR_STOP=1 -f "$f"
done
$PSQL $CONN -d "$DB" -At -c "
  select 'yatras=' || (select count(*) from yatras)
      || ' destinations=' || (select count(*) from destinations)
      || ' itineraries=' || (select count(*) from itineraries)
      || ' itinerary_days=' || (select count(*) from itinerary_days)
      || ' batches=' || (select count(*) from yatra_batches)
      || ' pricing=' || (select count(*) from batch_pricing)
      || ' economics=' || (select count(*) from batch_economics)
      || ' windows=' || (select count(*) from travel_windows)
      || ' panchanga=' || (select count(*) from panchanga)
      || ' events=' || (select count(*) from calendar_events)
      || ' articles=' || (select count(*) from knowledge_articles)
      || ' videos=' || (select count(*) from videos);"
if [ "${1:-}" = "--rls" ]; then
  echo "  running RLS acceptance test"
  $PSQL $CONN -d "$DB" -q -v ON_ERROR_STOP=1 -f scripts/rls_test.sql 2>&1 | grep -E "pass|FAIL" || true
fi
echo "OK"
