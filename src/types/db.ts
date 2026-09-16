/**
 * Domain types mirroring supabase/migrations.
 *
 * These are hand-written and deliberately narrower than generated types: the UI
 * only ever needs the columns listed here, and keeping them by hand means the
 * app compiles without a Supabase connection. Regenerate the exhaustive version
 * with `npm run db:types` when you need it.
 */

export type AppRole = 'admin' | 'staff' | 'tour_leader' | 'yatri'
export type YatraScope = 'domestic' | 'national' | 'international'
export type YatraNature = 'seasonal' | 'evergreen' | 'risky' | 'special'
export type BatchStatus = 'planned' | 'open' | 'filling' | 'full' | 'completed' | 'cancelled'
export type PriceTier = 'general' | 'premium'
export type VendorKind =
  | 'hotel' | 'dmc' | 'helicopter' | 'airline' | 'transport'
  | 'insurance' | 'catering' | 'guide' | 'permit' | 'other'
export type PlaceKind =
  | 'jyotirlinga' | 'shakti_peetha' | 'divya_desam' | 'char_dham'
  | 'iskcon' | 'unesco' | 'river' | 'temple' | 'other'
export type EventKind =
  | 'iskcon_festival' | 'hindu_festival' | 'public_holiday'
  | 'special_occasion' | 'departure' | 'marriage_season'
export type VideoKind = 'expert' | 'destination' | 'promo' | 'training' | 'testimonial'
export type Visibility = 'public' | 'staff'

export interface Profile {
  id: string
  full_name: string | null
  email: string | null
  phone: string | null
  city: string | null
  role: AppRole
  is_active: boolean
}

export interface Yatra {
  id: string
  slug: string
  title: string
  scope: YatraScope
  nature: YatraNature
  themes: string[]
  nights: number | null
  days: number | null
  min_pax: number | null
  summary: string | null
  highlights: string[]
  inclusions: string[]
  exclusions: string[]
  difficulty: number | null
  senior_friendly: boolean
  visa_required: boolean
  visa_notes: string | null
  repeatable_per_year: number | null
  hero_image_url: string | null
  is_published: boolean
}

export interface TravelWindow {
  id: string
  yatra_id: string
  best_months: number[]
  shoulder_months: number[]
  avoid_months: number[]
  open_months: number | null
  weather_note: string | null
  caution: string | null
}

export interface YatraNote {
  id: string
  yatra_id: string
  verdict: 'pro' | 'con'
  body: string
  weight: number
}

export interface Itinerary {
  id: string
  yatra_id: string
  version: number
  title: string | null
  intro: string | null
  notes: string | null
  is_current: boolean
}

export interface ItineraryDay {
  id: string
  itinerary_id: string
  day_number: number
  title: string | null
  body: string | null
  stay: string | null
  meals: string | null
}

export interface YatraBatch {
  id: string
  yatra_id: string
  start_date: string
  end_date: string | null
  status: BatchStatus
  seats_total: number | null
  seats_left: number | null
  departure_city: string | null
  notes: string | null
}

export interface BatchPricing {
  id: string
  batch_id: string | null
  yatra_id: string | null
  tier: PriceTier
  amount: number
  gst: number
  tcs: number
  total: number
  currency: string
}

export interface BatchEconomics {
  id: string
  yatra_id: string | null
  batch_id: string | null
  expected_pax: number | null
  ticket_avg: number | null
  expected_revenue: number | null
  expected_surplus: number | null
  margin_pct: number | null
  notes: string | null
}

export interface Destination {
  id: string
  slug: string
  name: string
  kinds: PlaceKind[]
  deity: string | null
  region: string | null
  city: string | null
  state: string | null
  country: string
  best_months: number[]
  avoid_months: number[]
  best_time_note: string | null
  sevas: string[]
  speciality: string | null
  description: string | null
  map_url: string | null
  image_url: string | null
}

export interface Pastime {
  id: string
  destination_id: string | null
  title: string
  source: string | null
  body: string
  lang: string
}

export interface Vendor {
  id: string
  name: string
  kind: VendorKind
  city: string | null
  state: string | null
  country: string | null
  contact_person: string | null
  phone: string | null
  alt_phone: string | null
  email: string | null
  website: string | null
  map_url: string | null
  rating: number | null
  is_preferred: boolean
  notes: string | null
}

export interface VendorRate {
  id: string
  vendor_id: string
  yatra_id: string | null
  service: string
  rate: number
  unit: string
  currency: string
  valid_from: string | null
  valid_to: string | null
  is_final: boolean
  terms: string | null
}

export interface CalendarEvent {
  id: string
  on_date: string
  kind: EventKind
  title: string
  tithi: string | null
  masam: string | null
  temple: string | null
  deity: string | null
  significance: string | null
  yatra_id: string | null
}

export interface Panchanga {
  on_date: string
  tithi: string | null
  masam: string | null
  paksha: string | null
  nakshatra: string | null
  yoga: string | null
  karana: string | null
}

export interface Video {
  id: string
  title: string
  youtube_id: string | null
  url: string
  kind: VideoKind
  channel: string | null
  notes: string | null
}

export interface KnowledgeArticle {
  id: string
  slug: string
  title: string
  category: string
  body_md: string
  visibility: Visibility
}

export interface FinanceReport {
  id: string
  title: string
  period: string | null
  yatra_id: string | null
  summary: string | null
  file_path: string | null
  created_at: string
}

/** v_upcoming_departures */
export interface UpcomingDeparture {
  batch_id: string
  start_date: string
  end_date: string | null
  status: BatchStatus
  seats_total: number | null
  seats_left: number | null
  departure_city: string | null
  yatra_id: string
  slug: string
  title: string
  scope: YatraScope
  nature: YatraNature
  nights: number | null
  days: number | null
  difficulty: number | null
  hero_image_url: string | null
  days_away: number
}

/** v_yatra_profitability */
export interface YatraProfitability {
  yatra_id: string
  slug: string
  title: string
  scope: YatraScope
  nature: YatraNature
  repeatable_per_year: number | null
  batches_this_year: number
  avg_margin_pct: number | null
  total_expected_surplus: number | null
  avg_general_price: number | null
}

/** v_calendar_day */
export interface CalendarDaySummary {
  on_date: string
  tithi: string | null
  masam: string | null
  paksha: string | null
  nakshatra: string | null
  iskcon_count: number
  hindu_count: number
  departure_count: number
  total_count: number
}

export interface SearchHit {
  kind: 'yatra' | 'destination' | 'vendor' | 'article'
  id: string
  title: string
  subtitle: string | null
  slug: string | null
}
