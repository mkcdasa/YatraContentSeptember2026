import { supabase } from '@/lib/supabase'
import { toISODate } from '@/lib/utils'
import type { CalendarDaySummary, CalendarEvent, Panchanga } from '@/types/db'

const monthBounds = (year: number, month1: number) => ({
  from: toISODate(new Date(year, month1 - 1, 1)),
  to: toISODate(new Date(year, month1, 0)),
})

export async function monthSummary(year: number, month1: number): Promise<CalendarDaySummary[]> {
  const { from, to } = monthBounds(year, month1)
  const { data, error } = await supabase
    .from('v_calendar_day').select('*')
    .gte('on_date', from).lte('on_date', to).order('on_date')
  if (error) throw error
  return data ?? []
}

export async function eventsForDay(date: string): Promise<CalendarEvent[]> {
  const { data, error } = await supabase
    .from('calendar_events').select('*').eq('on_date', date).order('kind')
  if (error) throw error
  return data ?? []
}

export async function panchangaForDay(date: string): Promise<Panchanga | null> {
  const { data, error } = await supabase
    .from('panchanga').select('*').eq('on_date', date).maybeSingle()
  if (error) throw error
  return data
}

/** Departures inside a month, for the calendar's departure dots. */
export async function departuresInMonth(year: number, month1: number) {
  const { from, to } = monthBounds(year, month1)
  const { data, error } = await supabase
    .from('v_upcoming_departures').select('*')
    .gte('start_date', from).lte('start_date', to).order('start_date')
  if (error) throw error
  return data ?? []
}

export async function todayPanchanga(): Promise<Panchanga | null> {
  return panchangaForDay(toISODate(new Date()))
}

export async function todayEvents(): Promise<CalendarEvent[]> {
  return eventsForDay(toISODate(new Date()))
}
