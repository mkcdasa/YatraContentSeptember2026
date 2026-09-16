import { supabase } from '@/lib/supabase'
import type { SearchHit } from '@/types/db'

/**
 * One RPC across yatras, destinations, vendors and articles. It runs as the
 * caller (security invoker), so a yatri's results never include a vendor.
 */
export async function searchAll(query: string, limit = 20): Promise<SearchHit[]> {
  const q = query.trim()
  if (q.length < 2) return []
  const { data, error } = await supabase.rpc('search_all', { q, lim: limit })
  if (error) throw error
  return (data ?? []) as SearchHit[]
}
