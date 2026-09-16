import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { ChevronLeft, ChevronRight, Sparkles } from 'lucide-react'
import { Badge, Button, Card, Empty, ErrorNote, SectionTitle, Skeleton } from '@/components/ui'
import { departuresInMonth, eventsForDay, monthSummary, panchangaForDay } from '@/data/calendar'
import { MonthGrid } from '@/components/app/MonthGrid'
import { EVENT_KIND_LABELS, MONTHS_LONG, formatDate, formatRange, toISODate } from '@/lib/utils'

export default function CalendarPage() {
  const today = new Date()
  const [year, setYear] = useState(today.getFullYear())
  const [month1, setMonth1] = useState(today.getMonth() + 1)
  const [selected, setSelected] = useState<string>(toISODate(today))

  const summaries = useQuery({
    queryKey: ['calendar', year, month1],
    queryFn: () => monthSummary(year, month1),
  })
  const departures = useQuery({
    queryKey: ['calendar-departures', year, month1],
    queryFn: () => departuresInMonth(year, month1),
  })
  const dayEvents = useQuery({
    queryKey: ['day-events', selected],
    queryFn: () => eventsForDay(selected),
  })
  const dayPanchanga = useQuery({
    queryKey: ['day-panchanga', selected],
    queryFn: () => panchangaForDay(selected),
  })

  const step = (delta: number) => {
    const d = new Date(year, month1 - 1 + delta, 1)
    setYear(d.getFullYear())
    setMonth1(d.getMonth() + 1)
  }

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <h1 className="font-display text-2xl font-semibold">
          {MONTHS_LONG[month1 - 1]} <span className="text-muted">{year}</span>
        </h1>
        <div className="flex gap-1">
          <Button variant="ghost" size="icon" aria-label="Previous month" onClick={() => step(-1)}>
            <ChevronLeft size={20} />
          </Button>
          <Button variant="ghost" size="icon" aria-label="Next month" onClick={() => step(1)}>
            <ChevronRight size={20} />
          </Button>
        </div>
      </div>

      {summaries.isError && <ErrorNote error={summaries.error} />}

      <Card className="p-3">
        {summaries.isLoading ? (
          <Skeleton className="h-64" />
        ) : (
          <MonthGrid
            year={year}
            month1={month1}
            summaries={summaries.data ?? []}
            selected={selected}
            onSelect={setSelected}
          />
        )}
        <div className="mt-3 flex flex-wrap gap-x-4 gap-y-1 border-t border-border pt-3 text-[11px] text-muted">
          <Legend className="bg-primary" label="ISKCON festival" />
          <Legend className="bg-accent" label="Festival" />
          <Legend className="bg-ok" label="Departure" />
        </div>
      </Card>

      <section>
        <SectionTitle>{formatDate(selected, { weekday: 'long' })}</SectionTitle>

        {dayPanchanga.data && (
          <Card className="mb-3">
            <dl className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm sm:grid-cols-3">
              {(
                [
                  ['Tithi', dayPanchanga.data.tithi],
                  ['Masam', dayPanchanga.data.masam],
                  ['Paksha', dayPanchanga.data.paksha],
                  ['Nakshatra', dayPanchanga.data.nakshatra],
                  ['Yoga', dayPanchanga.data.yoga],
                  ['Karana', dayPanchanga.data.karana],
                ] as const
              )
                .filter(([, v]) => v)
                .map(([k, v]) => (
                  <div key={k}>
                    <dt className="text-xs text-muted">{k}</dt>
                    <dd className="font-medium">{v}</dd>
                  </div>
                ))}
            </dl>
          </Card>
        )}

        {dayEvents.isLoading ? (
          <Skeleton className="h-20" />
        ) : dayEvents.data?.length ? (
          <ul className="space-y-2">
            {dayEvents.data.map((e) => (
              <li key={e.id}>
                <Card className="p-3">
                  <div className="flex items-start gap-2">
                    <Sparkles size={15} className="mt-0.5 shrink-0 text-accent" />
                    <div className="flex-1">
                      <p className="text-sm font-medium">{e.title}</p>
                      {(e.temple || e.deity) && (
                        <p className="text-xs text-muted">
                          {[e.temple, e.deity].filter(Boolean).join(' · ')}
                        </p>
                      )}
                      {e.significance && <p className="mt-1 text-xs text-muted">{e.significance}</p>}
                    </div>
                    <Badge>{EVENT_KIND_LABELS[e.kind]}</Badge>
                  </div>
                </Card>
              </li>
            ))}
          </ul>
        ) : (
          <Empty title="Nothing recorded for this day" />
        )}
      </section>

      {!!departures.data?.length && (
        <section>
          <SectionTitle>Departures this month</SectionTitle>
          <ul className="space-y-2">
            {departures.data.map((d) => (
              <li key={d.batch_id}>
                <Link to={`/yatras/${d.slug}`} className="card flex items-center justify-between gap-3 p-3">
                  <div>
                    <p className="font-medium leading-snug">{d.title}</p>
                    <p className="text-xs text-muted">{formatRange(d.start_date, d.end_date)}</p>
                  </div>
                  <ChevronRight size={18} className="shrink-0 text-muted" />
                </Link>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  )
}

const Legend = ({ className, label }: { className: string; label: string }) => (
  <span className="inline-flex items-center gap-1.5">
    <span className={`h-2 w-2 rounded-full ${className}`} />
    {label}
  </span>
)
