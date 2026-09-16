import { cn, MONTHS_LONG } from '@/lib/utils'
import type { CalendarDaySummary } from '@/types/db'

const WEEKDAYS = ['S', 'M', 'T', 'W', 'T', 'F', 'S']

/**
 * A month grid that shows why a date matters, not just that it exists: one dot
 * per signal (ISKCON festival, Hindu festival, departure) so the shape of a
 * busy month is legible before anything is tapped.
 */
export function MonthGrid({
  year, month1, summaries, selected, onSelect,
}: {
  year: number
  month1: number
  summaries: CalendarDaySummary[]
  selected: string | null
  onSelect: (date: string) => void
}) {
  const byDate = new Map(summaries.map((s) => [s.on_date, s]))
  const first = new Date(year, month1 - 1, 1)
  const daysInMonth = new Date(year, month1, 0).getDate()
  const leading = first.getDay()
  const today = new Date()
  const isThisMonth = today.getFullYear() === year && today.getMonth() === month1 - 1

  return (
    <div>
      <div className="mb-1 grid grid-cols-7 gap-1">
        {WEEKDAYS.map((d, i) => (
          <div key={i} className="py-1 text-center text-[11px] font-medium text-muted">
            {d}
          </div>
        ))}
      </div>
      <div className="grid grid-cols-7 gap-1" role="grid" aria-label={`${MONTHS_LONG[month1 - 1]} ${year}`}>
        {Array.from({ length: leading }, (_, i) => <div key={`pad-${i}`} />)}
        {Array.from({ length: daysInMonth }, (_, i) => {
          const day = i + 1
          const iso = `${year}-${String(month1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
          const s = byDate.get(iso)
          const isToday = isThisMonth && today.getDate() === day
          const isSelected = selected === iso
          return (
            <button
              key={iso}
              onClick={() => onSelect(iso)}
              aria-label={`${day} ${MONTHS_LONG[month1 - 1]}`}
              aria-current={isToday ? 'date' : undefined}
              className={cn(
                'flex aspect-square flex-col items-center justify-center gap-1 rounded-lg text-sm transition-colors',
                isSelected ? 'bg-primary text-primary-fg' : 'hover:bg-surface-2',
                isToday && !isSelected && 'ring-1 ring-primary',
              )}
            >
              <span className={cn('tabular-nums', isToday && !isSelected && 'font-semibold text-primary')}>
                {day}
              </span>
              <span className="flex h-1.5 items-center gap-0.5">
                {!!s?.iskcon_count && <Dot className="bg-primary" inverted={isSelected} />}
                {!!s?.hindu_count && <Dot className="bg-accent" inverted={isSelected} />}
                {!!s?.departure_count && <Dot className="bg-ok" inverted={isSelected} />}
              </span>
            </button>
          )
        })}
      </div>
    </div>
  )
}

const Dot = ({ className, inverted }: { className: string; inverted?: boolean }) => (
  <span className={cn('h-1.5 w-1.5 rounded-full', inverted ? 'bg-primary-fg' : className)} />
)
