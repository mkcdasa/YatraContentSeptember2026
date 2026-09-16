import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import {
  BookOpen, CalendarDays, Compass, IndianRupee, Search, Sparkles, Store, Youtube,
} from 'lucide-react'
import { Badge, Card, Empty, SectionTitle, Skeleton } from '@/components/ui'
import { DepartureCard } from '@/components/app/YatraCard'
import { StaffOnly } from '@/components/app/RoleGate'
import { todayEvents, todayPanchanga } from '@/data/calendar'
import { upcomingDepartures } from '@/data/yatras'
import { EVENT_KIND_LABELS, MONTHS_LONG } from '@/lib/utils'
import { useAuth } from '@/hooks/useAuth'

export default function Home() {
  const { profile } = useAuth()
  const departures = useQuery({ queryKey: ['departures'], queryFn: () => upcomingDepartures(10) })
  const panchanga = useQuery({ queryKey: ['panchanga', 'today'], queryFn: todayPanchanga })
  const events = useQuery({ queryKey: ['events', 'today'], queryFn: todayEvents })

  const today = new Date()
  const firstName = profile?.full_name?.split(' ')[0]

  return (
    <div className="space-y-7">
      <section>
        <p className="text-sm text-muted">
          {today.toLocaleDateString('en-IN', { weekday: 'long' })}, {today.getDate()}{' '}
          {MONTHS_LONG[today.getMonth()]}
        </p>
        <h1 className="mt-0.5 font-display text-2xl font-semibold">
          {firstName ? `Hare Krishna, ${firstName}` : 'Hare Krishna'}
        </h1>
      </section>

      <Link
        to="/search"
        className="card flex items-center gap-3 px-4 py-3 text-muted transition-colors active:bg-surface-2"
      >
        <Search size={18} />
        <span className="text-sm">Search yatras, temples, vendors…</span>
      </Link>

      {/* Today's panchanga and festivals — the first thing a coordinator checks */}
      <section>
        <SectionTitle
          action={<Link to="/calendar" className="text-sm font-medium text-primary">Calendar</Link>}
        >
          Today
        </SectionTitle>
        {panchanga.isLoading ? (
          <Skeleton className="h-24" />
        ) : (
          <Card>
            {panchanga.data ? (
              <dl className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm sm:grid-cols-4">
                {(
                  [
                    ['Tithi', panchanga.data.tithi],
                    ['Masam', panchanga.data.masam],
                    ['Paksha', panchanga.data.paksha],
                    ['Nakshatra', panchanga.data.nakshatra],
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
            ) : (
              <p className="text-sm text-muted">No panchanga recorded for today.</p>
            )}

            {!!events.data?.length && (
              <ul className="mt-3 space-y-1.5 border-t border-border pt-3">
                {events.data.slice(0, 4).map((e) => (
                  <li key={e.id} className="flex items-start gap-2 text-sm">
                    <Sparkles size={14} className="mt-0.5 shrink-0 text-accent" />
                    <span className="flex-1">{e.title}</span>
                    <Badge size="sm">{EVENT_KIND_LABELS[e.kind]}</Badge>
                  </li>
                ))}
              </ul>
            )}
          </Card>
        )}
      </section>

      <section>
        <SectionTitle
          action={<Link to="/yatras" className="text-sm font-medium text-primary">All yatras</Link>}
        >
          Next departures
        </SectionTitle>
        {departures.isLoading ? (
          <div className="flex gap-3">
            <Skeleton className="h-36 w-64 shrink-0" />
            <Skeleton className="h-36 w-64 shrink-0" />
          </div>
        ) : departures.data?.length ? (
          <div className="hide-scrollbar -mx-4 flex gap-3 overflow-x-auto px-4">
            {departures.data.map((d) => (
              <DepartureCard key={d.batch_id} departure={d} />
            ))}
          </div>
        ) : (
          <Empty
            icon={<CalendarDays size={28} />}
            title="No upcoming departures"
            hint="Add batch dates to a yatra and they will appear here."
          />
        )}
      </section>

      <section>
        <SectionTitle>Jump to</SectionTitle>
        <div className="grid grid-cols-2 gap-3">
          <Tile to="/explore" icon={<Compass size={20} />} label="Temples & holy places" />
          <Tile to="/library" icon={<BookOpen size={20} />} label="Handbooks & checklists" />
          <Tile to="/videos" icon={<Youtube size={20} />} label="Video library" />
          <StaffOnly>
            <Tile to="/vendors" icon={<Store size={20} />} label="Vendors & rates" staff />
          </StaffOnly>
          <StaffOnly>
            <Tile to="/finance" icon={<IndianRupee size={20} />} label="Profitability" staff />
          </StaffOnly>
        </div>
      </section>
    </div>
  )
}

function Tile({
  to, icon, label, staff,
}: {
  to: string; icon: React.ReactNode; label: string; staff?: boolean
}) {
  return (
    <Link to={to} className="card flex flex-col gap-2 p-4 transition-colors active:bg-surface-2">
      <span className="text-primary">{icon}</span>
      <span className="text-sm font-medium leading-snug">{label}</span>
      {staff && <Badge tone="primary" className="self-start">Staff</Badge>}
    </Link>
  )
}
