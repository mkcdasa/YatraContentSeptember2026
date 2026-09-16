import { supabase } from '@/lib/supabase'
import type { Vendor, VendorKind, VendorRate } from '@/types/db'

/**
 * Staff tier. Under RLS a yatri gets an empty array here, not a 403, so the UI
 * simply has nothing to show rather than an error to explain.
 */
export async function listVendors(filters: { search?: string; kind?: VendorKind } = {}) {
  let q = supabase.from('vendors').select('*').order('is_preferred', { ascending: false }).order('name')
  if (filters.search) q = q.ilike('name', `%${filters.search}%`)
  if (filters.kind) q = q.eq('kind', filters.kind)
  const { data, error } = await q
  if (error) throw error
  return (data ?? []) as Vendor[]
}

export async function getVendor(id: string): Promise<Vendor | null> {
  const { data, error } = await supabase.from('vendors').select('*').eq('id', id).maybeSingle()
  if (error) throw error
  return data
}

export async function listRates(vendorId: string): Promise<VendorRate[]> {
  const { data, error } = await supabase
    .from('vendor_rates').select('*').eq('vendor_id', vendorId)
    .order('is_final', { ascending: false }).order('service')
  if (error) throw error
  return data ?? []
}

export async function ratesForYatra(yatraId: string) {
  const { data, error } = await supabase
    .from('vendor_rates')
    .select('*, vendors(id, name, kind, city, phone, contact_person)')
    .eq('yatra_id', yatraId)
    .order('is_final', { ascending: false })
  if (error) throw error
  return (data ?? []) as (VendorRate & {
    vendors: Pick<Vendor, 'id' | 'name' | 'kind' | 'city' | 'phone' | 'contact_person'> | null
  })[]
}

export async function upsertVendor(input: Partial<Vendor> & { name: string }) {
  const { data, error } = await supabase.from('vendors').upsert(input).select().single()
  if (error) throw error
  return data as Vendor
}

export async function upsertRate(input: Partial<VendorRate> & { vendor_id: string; service: string; rate: number }) {
  const { error } = await supabase.from('vendor_rates').upsert(input)
  if (error) throw error
}

export async function deleteVendor(id: string) {
  const { error } = await supabase.from('vendors').delete().eq('id', id)
  if (error) throw error
}
