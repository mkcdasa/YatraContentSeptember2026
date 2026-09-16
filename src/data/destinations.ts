import { supabase } from '@/lib/supabase'
import type { Destination, Pastime, PlaceKind } from '@/types/db'

export interface DestinationFilters {
  search?: string
  kinds?: PlaceKind[]
  state?: string
  month?: number
}

const PAGE = 40

export async function listDestinations(
  filters: DestinationFilters = {},
  page = 0,
): Promise<{ rows: Destination[]; hasMore: boolean }> {
  let q = supabase
    .from('destinations')
    .select('*')
    .order('name')
    .range(page * PAGE, page * PAGE + PAGE) // one extra row tells us if more exist

  if (filters.search) {
    const s = `%${filters.search}%`
    q = q.or(`name.ilike.${s},deity.ilike.${s},city.ilike.${s}`)
  }
  if (filters.kinds?.length) q = q.overlaps('kinds', filters.kinds)
  if (filters.state) q = q.eq('state', filters.state)
  if (filters.month) q = q.contains('best_months', [filters.month])

  const { data, error } = await q
  if (error) throw error
  const rows = data ?? []
  return { rows: rows.slice(0, PAGE), hasMore: rows.length > PAGE }
}

export async function getDestination(slug: string): Promise<Destination | null> {
  const { data, error } = await supabase
    .from('destinations').select('*').eq('slug', slug).maybeSingle()
  if (error) throw error
  return data
}

export async function listPastimes(destinationId: string): Promise<Pastime[]> {
  const { data, error } = await supabase
    .from('pastimes').select('*').eq('destination_id', destinationId).order('title')
  if (error) throw error
  return data ?? []
}

export async function listStates(): Promise<string[]> {
  const { data, error } = await supabase
    .from('destinations').select('state').not('state', 'is', null)
  if (error) throw error
  return [...new Set((data ?? []).map((r) => r.state as string))].sort()
}

/** Places on a yatra's route, in visiting order. */
export async function destinationsForYatra(yatraId: string): Promise<Destination[]> {
  const { data, error } = await supabase
    .from('yatra_destinations')
    .select('sequence, destinations(*)')
    .eq('yatra_id', yatraId)
    .order('sequence')
  if (error) throw error
  return (data ?? []).flatMap((r) => (r.destinations ? [r.destinations as unknown as Destination] : []))
}
