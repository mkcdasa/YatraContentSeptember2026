import { supabase } from '@/lib/supabase'
import type {
  BatchEconomics, BatchPricing, Itinerary, ItineraryDay, TravelWindow,
  UpcomingDeparture, Yatra, YatraBatch, YatraNote, YatraProfitability,
} from '@/types/db'

export interface YatraFilters {
  search?: string
  scope?: string[]
  nature?: string[]
  theme?: string
  /** 1-12; matches yatras whose travel window says this month is good */
  month?: number
  maxDifficulty?: number
  seniorFriendly?: boolean
}

export async function listYatras(filters: YatraFilters = {}): Promise<Yatra[]> {
  let q = supabase.from('yatras').select('*').eq('is_published', true).order('title')

  if (filters.search) q = q.ilike('title', `%${filters.search}%`)
  if (filters.scope?.length) q = q.in('scope', filters.scope)
  if (filters.nature?.length) q = q.in('nature', filters.nature)
  if (filters.theme) q = q.contains('themes', [filters.theme])
  if (filters.maxDifficulty) q = q.lte('difficulty', filters.maxDifficulty)
  if (filters.seniorFriendly) q = q.eq('senior_friendly', true)

  const { data, error } = await q
  if (error) throw error
  return data ?? []
}

/**
 * Month filtering lives here rather than in the query because travel_windows is
 * a separate table and PostgREST cannot express "array contains" across a join
 * in one request. Two small requests beat a database view nobody can read.
 */
export async function listYatrasForMonth(month: number): Promise<Yatra[]> {
  const { data: windows, error } = await supabase
    .from('travel_windows')
    .select('yatra_id, best_months, shoulder_months')
  if (error) throw error

  const ids = (windows ?? [])
    .filter((w) => w.best_months?.includes(month) || w.shoulder_months?.includes(month))
    .map((w) => w.yatra_id)
  if (!ids.length) return []

  const { data, error: e2 } = await supabase
    .from('yatras').select('*').in('id', ids).eq('is_published', true).order('title')
  if (e2) throw e2
  return data ?? []
}

export async function getYatra(slug: string): Promise<Yatra | null> {
  const { data, error } = await supabase.from('yatras').select('*').eq('slug', slug).maybeSingle()
  if (error) throw error
  return data
}

export async function getTravelWindow(yatraId: string): Promise<TravelWindow | null> {
  const { data, error } = await supabase
    .from('travel_windows').select('*').eq('yatra_id', yatraId).maybeSingle()
  if (error) throw error
  return data
}

export async function getItinerary(
  yatraId: string,
): Promise<{ itinerary: Itinerary; days: ItineraryDay[] } | null> {
  const { data: itinerary, error } = await supabase
    .from('itineraries').select('*')
    .eq('yatra_id', yatraId).eq('is_current', true)
    .order('version', { ascending: false }).limit(1).maybeSingle()
  if (error) throw error
  if (!itinerary) return null

  const { data: days, error: e2 } = await supabase
    .from('itinerary_days').select('*')
    .eq('itinerary_id', itinerary.id).order('day_number')
  if (e2) throw e2
  return { itinerary, days: days ?? [] }
}

export async function listBatches(yatraId: string): Promise<YatraBatch[]> {
  const { data, error } = await supabase
    .from('yatra_batches').select('*').eq('yatra_id', yatraId).order('start_date')
  if (error) throw error
  return data ?? []
}

export async function listNotes(yatraId: string): Promise<YatraNote[]> {
  const { data, error } = await supabase
    .from('yatra_notes').select('*').eq('yatra_id', yatraId)
    .order('weight', { ascending: false })
  if (error) throw error
  return data ?? []
}

export async function addNote(input: {
  yatra_id: string; verdict: 'pro' | 'con'; body: string; weight: number
}) {
  const { error } = await supabase.from('yatra_notes').insert(input)
  if (error) throw error
}

export async function deleteNote(id: string) {
  const { error } = await supabase.from('yatra_notes').delete().eq('id', id)
  if (error) throw error
}

export async function upcomingDepartures(limit = 12): Promise<UpcomingDeparture[]> {
  const { data, error } = await supabase
    .from('v_upcoming_departures').select('*').limit(limit)
  if (error) throw error
  return data ?? []
}

/* --- staff tier: RLS returns an empty set for a yatri, never an error ------ */

export async function listPricing(yatraId: string): Promise<BatchPricing[]> {
  const { data, error } = await supabase
    .from('batch_pricing').select('*').eq('yatra_id', yatraId).order('tier')
  if (error) throw error
  return data ?? []
}

export async function getEconomics(yatraId: string): Promise<BatchEconomics[]> {
  const { data, error } = await supabase
    .from('batch_economics').select('*').eq('yatra_id', yatraId)
  if (error) throw error
  return data ?? []
}

export async function profitability(): Promise<YatraProfitability[]> {
  const { data, error } = await supabase
    .from('v_yatra_profitability').select('*')
    .order('avg_margin_pct', { ascending: false, nullsFirst: false })
  if (error) throw error
  return data ?? []
}

export async function listThemes(): Promise<string[]> {
  const { data, error } = await supabase.from('yatras').select('themes').eq('is_published', true)
  if (error) throw error
  const set = new Set<string>()
  for (const row of data ?? []) for (const t of row.themes ?? []) set.add(t)
  return [...set].sort()
}
