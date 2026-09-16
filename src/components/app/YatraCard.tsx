import { Link } from 'react-router-dom'
import { CalendarDays, Mountain, Plane } from 'lucide-react'
import { Badge } from '@/components/ui'
import { DIFFICULTY_LABELS, NATURE_LABELS, duration, formatRange, relativeDays } from '@/lib/utils'
import type { UpcomingDeparture, Yatra } from '@/types/db'

const natureTone = (nature: string) =>
  nature === 'risky' ? 'warn' : nature === 'special' ? 'accent' : nature === 'seasonal' ? 'primary' : 'neutral'

export function YatraCard({ yatra }: { yatra: Yatra }) {
  const dur = duration(yatra.nights, yatra.days)
  return (
    <Link to={`/yatras/${yatra.slug}`} className="card block p-4 transition-colors active:bg-surface-2">
      <div className="flex items-start justify-between gap-3">
        <h3 className="font-display text-base font-semibold leading-snug">{yatra.title}</h3>
        {yatra.scope === 'international' && <Plane size={16} className="mt-1 shrink-0 text-muted" />}
      </div>

      <div className="mt-2 flex flex-wrap items-center gap-1.5">
        <Badge tone={natureTone(yatra.nature)}>{NATURE_LABELS[yatra.nature]}</Badge>
        {dur && <Badge>{dur}</Badge>}
        {yatra.difficulty != null && yatra.difficulty >= 4 && (
          <Badge tone="warn">
            <Mountain size={11} /> {DIFFICULTY_LABELS[yatra.difficulty]}
          </Badge>
        )}
        {yatra.visa_required && <Badge tone="primary">Visa</Badge>}
      </div>

      {yatra.themes.length > 0 && (
        <p className="mt-2 line-clamp-1 text-xs text-muted">{yatra.themes.join(' · ')}</p>
      )}
    </Link>
  )
}

export function DepartureCard({ departure }: { departure: UpcomingDeparture }) {
  const seatsTight = departure.seats_left != null && departure.seats_left <= 5
  return (
    <Link
      to={`/yatras/${departure.slug}`}
      className="card block w-64 shrink-0 p-4 transition-colors active:bg-surface-2"
    >
      <p className="text-xs font-medium text-primary">{relativeDays(departure.days_away)}</p>
      <h3 className="mt-1 line-clamp-2 font-display text-base font-semibold leading-snug">
        {departure.title}
      </h3>
      <p className="mt-2 flex items-center gap-1.5 text-xs text-muted">
        <CalendarDays size={13} />
        {formatRange(departure.start_date, departure.end_date)}
      </p>
      {seatsTight && (
        <Badge tone="danger" className="mt-2">
          {departure.seats_left} seats left
        </Badge>
      )}
    </Link>
  )
}
