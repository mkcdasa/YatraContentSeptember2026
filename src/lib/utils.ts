import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export const cn = (...inputs: ClassValue[]) => twMerge(clsx(inputs))

export const MONTHS = [
  'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
] as const

export const MONTHS_LONG = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
] as const

/** ₹1,57,950 — Indian digit grouping, no decimals. Prices here are never paise. */
export function inr(value: number | null | undefined): string {
  if (value == null) return '—'
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(value)
}

/** 15.7 L / 2.3 Cr — how the finance team actually reads these numbers. */
export function inrCompact(value: number | null | undefined): string {
  if (value == null) return '—'
  const abs = Math.abs(value)
  if (abs >= 1e7) return `₹${(value / 1e7).toFixed(2)} Cr`
  if (abs >= 1e5) return `₹${(value / 1e5).toFixed(2)} L`
  return inr(value)
}

export function formatDate(iso: string | null | undefined, opts?: Intl.DateTimeFormatOptions) {
  if (!iso) return '—'
  return new Date(`${iso}T00:00:00`).toLocaleDateString('en-IN', {
    day: 'numeric', month: 'short', year: 'numeric', ...opts,
  })
}

export function formatRange(start: string, end: string | null | undefined) {
  if (!end) return formatDate(start)
  const a = new Date(`${start}T00:00:00`)
  const b = new Date(`${end}T00:00:00`)
  const sameMonth = a.getMonth() === b.getMonth() && a.getFullYear() === b.getFullYear()
  if (sameMonth) {
    return `${a.getDate()}–${b.getDate()} ${MONTHS[b.getMonth()]} ${b.getFullYear()}`
  }
  return `${formatDate(start, { year: undefined })} – ${formatDate(end)}`
}

export function duration(nights: number | null, days: number | null) {
  if (nights == null && days == null) return null
  if (nights != null && days != null) return `${nights}N / ${days}D`
  return days != null ? `${days} days` : `${nights} nights`
}

/** "in 12 days" / "next week" / "tomorrow" — cards read better than raw dates. */
export function relativeDays(days: number): string {
  if (days < 0) return 'departed'
  if (days === 0) return 'today'
  if (days === 1) return 'tomorrow'
  if (days < 14) return `in ${days} days`
  if (days < 60) return `in ${Math.round(days / 7)} weeks`
  return `in ${Math.round(days / 30)} months`
}

export const toISODate = (d: Date) =>
  `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`

export function initials(name: string | null | undefined) {
  if (!name) return '?'
  return name.trim().split(/\s+/).slice(0, 2).map((w) => w[0]?.toUpperCase() ?? '').join('')
}

/** Kailash is a 5. A day trip is a 1. Used for the difficulty pip row. */
export const DIFFICULTY_LABELS = ['', 'Easy', 'Relaxed', 'Moderate', 'Strenuous', 'Extreme'] as const

export const SCOPE_LABELS: Record<string, string> = {
  domestic: 'Domestic', national: 'National', international: 'International',
}

export const NATURE_LABELS: Record<string, string> = {
  seasonal: 'Seasonal', evergreen: 'Evergreen', risky: 'High altitude', special: 'Special event',
}

export const PLACE_KIND_LABELS: Record<string, string> = {
  jyotirlinga: 'Jyotirlinga', shakti_peetha: 'Shakti Peetha', divya_desam: 'Divya Desam',
  char_dham: 'Char Dham', iskcon: 'ISKCON', unesco: 'UNESCO', river: 'Holy river',
  temple: 'Temple', other: 'Other',
}

export const VENDOR_KIND_LABELS: Record<string, string> = {
  hotel: 'Hotel', dmc: 'DMC', helicopter: 'Helicopter', airline: 'Airline',
  transport: 'Transport', insurance: 'Insurance', catering: 'Catering',
  guide: 'Guide', permit: 'Permits', other: 'Other',
}

export const EVENT_KIND_LABELS: Record<string, string> = {
  iskcon_festival: 'ISKCON festival', hindu_festival: 'Festival',
  public_holiday: 'Public holiday', special_occasion: 'Occasion',
  departure: 'Departure', marriage_season: 'Marriage season',
}
