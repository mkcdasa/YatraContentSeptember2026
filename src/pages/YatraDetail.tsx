import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  AlertTriangle, CalendarDays, Check, Mountain, Phone, Plus, ThumbsDown, ThumbsUp, Trash2,
} from 'lucide-react'
import {
  Badge, Button, Card, Empty, ErrorNote, SectionTitle, Sheet, Skeleton, Stat, Tabs,
} from '@/components/ui'
import { SeasonStrip } from '@/components/app/SeasonStrip'
import { StaffOnly } from '@/components/app/RoleGate'
import {
  addNote, deleteNote, getEconomics, getItinerary, getTravelWindow, getYatra,
  listBatches, listNotes, listPricing,
} from '@/data/yatras'
import { ratesForYatra } from '@/data/vendors'
import { useAuth } from '@/hooks/useAuth'
import {
  DIFFICULTY_LABELS, MONTHS, NATURE_LABELS, SCOPE_LABELS, duration,
  formatRange, inr, inrCompact, VENDOR_KIND_LABELS,
} from '@/lib/utils'

type TabId = 'overview' | 'itinerary' | 'dates' | 'season' | 'notes' | 'vendors' | 'economics'

export default function YatraDetail() {
  const { slug = '' } = useParams()
  const { isStaff } = useAuth()
  const [tab, setTab] = useState<TabId>('overview')

  const yatra = useQuery({ queryKey: ['yatra', slug], queryFn: () => getYatra(slug), enabled: !!slug })
  const id = yatra.data?.id

  if (yatra.isLoading) return <Skeleton className="h-64" />
  if (yatra.isError) return <ErrorNote error={yatra.error} />
  if (!yatra.data) return <Empty title="Yatra not found" hint="It may have been renamed or unpublished." />

  const y = yatra.data
  const dur = duration(y.nights, y.days)

  return (
    <div className="space-y-4">
      <header>
        <h1 className="font-display text-2xl font-semibold leading-tight">{y.title}</h1>
        <div className="mt-2 flex flex-wrap gap-1.5">
          <Badge tone="primary">{SCOPE_LABELS[y.scope]}</Badge>
          <Badge>{NATURE_LABELS[y.nature]}</Badge>
          {dur && <Badge>{dur}</Badge>}
          {y.difficulty != null && (
            <Badge tone={y.difficulty >= 4 ? 'warn' : 'neutral'}>
              <Mountain size={11} /> {DIFFICULTY_LABELS[y.difficulty]}
            </Badge>
          )}
          {y.visa_required && <Badge tone="accent">Visa required</Badge>}
          {y.senior_friendly && <Badge tone="ok">Senior friendly</Badge>}
        </div>
        {y.themes.length > 0 && <p className="mt-2 text-sm text-muted">{y.themes.join(' · ')}</p>}
      </header>

      <Tabs<TabId>
        value={tab}
        onChange={setTab}
        tabs={[
          { id: 'overview', label: 'Overview' },
          { id: 'itinerary', label: 'Itinerary' },
          { id: 'dates', label: 'Dates' },
          { id: 'season', label: 'Season' },
          { id: 'notes', label: 'Pros & cons' },
          { id: 'vendors', label: 'Vendors', hidden: !isStaff },
          { id: 'economics', label: 'Economics', hidden: !isStaff },
        ]}
      />

      {tab === 'overview' && <Overview yatra={y} />}
      {tab === 'itinerary' && id && <ItineraryTab yatraId={id} />}
      {tab === 'dates' && id && <DatesTab yatraId={id} />}
      {tab === 'season' && id && <SeasonTab yatraId={id} />}
      {tab === 'notes' && id && <NotesTab yatraId={id} />}
      {tab === 'vendors' && id && <StaffOnly><VendorsTab yatraId={id} /></StaffOnly>}
      {tab === 'economics' && id && <StaffOnly><EconomicsTab yatraId={id} /></StaffOnly>}
    </div>
  )
}

/* ------------------------------------------------------------------------ */

function Overview({ yatra }: { yatra: NonNullable<Awaited<ReturnType<typeof getYatra>>> }) {
  return (
    <div className="space-y-4">
      {yatra.summary && <p className="text-sm leading-relaxed">{yatra.summary}</p>}

      <div className="grid grid-cols-3 gap-2">
        <Stat label="Duration" value={duration(yatra.nights, yatra.days) ?? '—'} />
        <Stat label="Min group" value={yatra.min_pax ?? '—'} />
        <Stat
          label="Repeats"
          value={yatra.repeatable_per_year ? `${yatra.repeatable_per_year}×/yr` : '—'}
          hint="per year"
        />
      </div>

      {yatra.visa_required && (
        <Card className="border-accent/40 bg-accent/5">
          <p className="flex items-center gap-2 text-sm font-medium">
            <AlertTriangle size={15} className="text-warn" /> Visa required
          </p>
          {yatra.visa_notes && <p className="mt-1 text-sm text-muted">{yatra.visa_notes}</p>}
        </Card>
      )}

      {yatra.highlights.length > 0 && (
        <section>
          <SectionTitle>Highlights</SectionTitle>
          <ul className="space-y-1.5">
            {yatra.highlights.map((h, i) => (
              <li key={i} className="flex gap-2 text-sm">
                <Check size={15} className="mt-0.5 shrink-0 text-ok" />
                {h}
              </li>
            ))}
          </ul>
        </section>
      )}

      {yatra.inclusions.length > 0 && (
        <section>
          <SectionTitle>Inclusions</SectionTitle>
          <ul className="list-inside list-disc space-y-1 text-sm text-muted">
            {yatra.inclusions.map((h, i) => <li key={i}>{h}</li>)}
          </ul>
        </section>
      )}
    </div>
  )
}

function ItineraryTab({ yatraId }: { yatraId: string }) {
  const q = useQuery({ queryKey: ['itinerary', yatraId], queryFn: () => getItinerary(yatraId) })
  if (q.isLoading) return <Skeleton className="h-48" />
  if (q.isError) return <ErrorNote error={q.error} />
  if (!q.data?.days.length) {
    return <Empty title="No itinerary yet" hint="Day-by-day details have not been added for this yatra." />
  }

  return (
    <div className="space-y-3">
      {q.data.itinerary.intro && (
        <p className="text-sm leading-relaxed text-muted">{q.data.itinerary.intro}</p>
      )}
      <ol className="relative space-y-3 border-l border-border pl-5">
        {q.data.days.map((d) => (
          <li key={d.id} className="relative">
            <span className="absolute -left-[26px] grid h-5 w-5 place-items-center rounded-full bg-primary text-[10px] font-bold text-primary-fg">
              {d.day_number}
            </span>
            <Card className="p-3">
              {d.title && <p className="font-medium leading-snug">{d.title}</p>}
              {d.body && (
                <p className="mt-1 whitespace-pre-line text-sm leading-relaxed text-muted">{d.body}</p>
              )}
              {(d.stay || d.meals) && (
                <p className="mt-2 flex flex-wrap gap-2 text-xs text-muted">
                  {d.stay && <Badge>Stay: {d.stay}</Badge>}
                  {d.meals && <Badge>Meals: {d.meals}</Badge>}
                </p>
              )}
            </Card>
          </li>
        ))}
      </ol>
    </div>
  )
}

function DatesTab({ yatraId }: { yatraId: string }) {
  const batches = useQuery({ queryKey: ['batches', yatraId], queryFn: () => listBatches(yatraId) })
  const pricing = useQuery({ queryKey: ['pricing', yatraId], queryFn: () => listPricing(yatraId) })

  if (batches.isLoading) return <Skeleton className="h-40" />
  if (batches.isError) return <ErrorNote error={batches.error} />
  if (!batches.data?.length) return <Empty title="No dates scheduled" />

  const byTier = new Map(pricing.data?.map((p) => [p.tier, p]))

  return (
    <div className="space-y-4">
      <ul className="space-y-2">
        {batches.data.map((b) => (
          <li key={b.id}>
            <Card className="flex items-center justify-between gap-3 p-3">
              <div>
                <p className="font-medium">{formatRange(b.start_date, b.end_date)}</p>
                {b.departure_city && <p className="text-xs text-muted">from {b.departure_city}</p>}
              </div>
              <div className="flex items-center gap-2">
                {b.seats_left != null && (
                  <Badge tone={b.seats_left <= 5 ? 'danger' : 'neutral'}>{b.seats_left} left</Badge>
                )}
                <Badge tone={b.status === 'open' ? 'ok' : 'neutral'}>{b.status}</Badge>
              </div>
            </Card>
          </li>
        ))}
      </ul>

      {/* Pricing is staff-tier: RLS returns nothing to a yatri, so this simply
          does not render for them. */}
      <StaffOnly>
        {!!pricing.data?.length && (
          <section>
            <SectionTitle>Package pricing</SectionTitle>
            <div className="grid grid-cols-2 gap-2">
              {(['general', 'premium'] as const).map((tier) => {
                const p = byTier.get(tier)
                if (!p) return null
                return (
                  <Card key={tier} className="p-3">
                    <p className="text-xs uppercase tracking-wide text-muted">{tier}</p>
                    <p className="mt-1 font-display text-xl font-semibold tabular-nums">{inr(p.total)}</p>
                    <p className="mt-1 text-[11px] text-muted">
                      {inr(p.amount)} + GST {inr(p.gst)}
                      {p.tcs > 0 && ` + TCS ${inr(p.tcs)}`}
                    </p>
                  </Card>
                )
              })}
            </div>
          </section>
        )}
      </StaffOnly>
    </div>
  )
}

function SeasonTab({ yatraId }: { yatraId: string }) {
  const q = useQuery({ queryKey: ['window', yatraId], queryFn: () => getTravelWindow(yatraId) })
  if (q.isLoading) return <Skeleton className="h-40" />
  if (q.isError) return <ErrorNote error={q.error} />
  if (!q.data) {
    return <Empty title="No season guidance yet" hint="Best, shoulder and avoid months have not been recorded." />
  }

  const w = q.data
  const named = (months: number[]) => months.map((m) => MONTHS[m - 1]).join(', ') || '—'

  return (
    <div className="space-y-4">
      <Card>
        <SeasonStrip best={w.best_months} shoulder={w.shoulder_months} avoid={w.avoid_months} />
      </Card>

      <div className="grid grid-cols-3 gap-2">
        <Stat label="Open" value={w.open_months ? `${w.open_months} mo` : '—'} />
        <Stat label="Best" value={w.best_months.length} hint={named(w.best_months)} tone="ok" />
        <Stat label="Avoid" value={w.avoid_months.length} hint={named(w.avoid_months)} tone="danger" />
      </div>

      {w.caution && (
        <Card className="border-warn/40 bg-warn/5">
          <p className="flex items-center gap-2 text-sm font-medium">
            <AlertTriangle size={15} className="text-warn" /> Caution
          </p>
          <p className="mt-1 whitespace-pre-line text-sm text-muted">{w.caution}</p>
        </Card>
      )}

      {w.weather_note && (
        <Card>
          <p className="text-sm font-medium">Shoulder season</p>
          <p className="mt-1 whitespace-pre-line text-sm text-muted">{w.weather_note}</p>
        </Card>
      )}
    </div>
  )
}

function NotesTab({ yatraId }: { yatraId: string }) {
  const qc = useQueryClient()
  const { isStaff } = useAuth()
  const [open, setOpen] = useState(false)
  const [verdict, setVerdict] = useState<'pro' | 'con'>('pro')
  const [body, setBody] = useState('')

  const q = useQuery({ queryKey: ['notes', yatraId], queryFn: () => listNotes(yatraId) })
  const invalidate = () => qc.invalidateQueries({ queryKey: ['notes', yatraId] })

  const create = useMutation({
    mutationFn: () => addNote({ yatra_id: yatraId, verdict, body: body.trim(), weight: 3 }),
    onSuccess: () => { setBody(''); setOpen(false); invalidate() },
  })
  const remove = useMutation({ mutationFn: deleteNote, onSuccess: invalidate })

  const pros = q.data?.filter((n) => n.verdict === 'pro') ?? []
  const cons = q.data?.filter((n) => n.verdict === 'con') ?? []

  return (
    <div className="space-y-4">
      {isStaff && (
        <Button variant="outline" className="w-full" onClick={() => setOpen(true)}>
          <Plus size={16} /> Add a note
        </Button>
      )}

      {q.isLoading && <Skeleton className="h-32" />}
      {create.isError && <ErrorNote error={create.error} />}

      {!q.isLoading && !pros.length && !cons.length && (
        <Empty
          title="Nothing recorded yet"
          hint="Capture what worked and what did not, while the yatra is fresh."
        />
      )}

      {[
        { rows: pros, label: 'Pros', icon: <ThumbsUp size={15} className="text-ok" /> },
        { rows: cons, label: 'Cons', icon: <ThumbsDown size={15} className="text-danger" /> },
      ].map(({ rows, label, icon }) =>
        rows.length ? (
          <section key={label}>
            <SectionTitle>{label}</SectionTitle>
            <ul className="space-y-2">
              {rows.map((n) => (
                <li key={n.id}>
                  <Card className="flex items-start gap-2 p-3">
                    <span className="mt-0.5">{icon}</span>
                    <p className="flex-1 text-sm">{n.body}</p>
                    {isStaff && (
                      <button
                        aria-label="Delete note"
                        onClick={() => remove.mutate(n.id)}
                        className="text-muted hover:text-danger"
                      >
                        <Trash2 size={15} />
                      </button>
                    )}
                  </Card>
                </li>
              ))}
            </ul>
          </section>
        ) : null,
      )}

      <Sheet open={open} onClose={() => setOpen(false)} title="Add a note">
        <div className="space-y-4">
          <div className="flex gap-2">
            <Button
              variant={verdict === 'pro' ? 'primary' : 'outline'}
              className="flex-1"
              onClick={() => setVerdict('pro')}
            >
              <ThumbsUp size={16} /> Pro
            </Button>
            <Button
              variant={verdict === 'con' ? 'primary' : 'outline'}
              className="flex-1"
              onClick={() => setVerdict('con')}
            >
              <ThumbsDown size={16} /> Con
            </Button>
          </div>
          <textarea
            value={body}
            onChange={(e) => setBody(e.target.value)}
            rows={4}
            placeholder="Helicopter slots were confirmed only 48 hours before departure…"
            className="w-full rounded-xl border border-border bg-surface p-3 text-base focus:border-primary focus:outline-none"
          />
          <Button
            className="w-full"
            disabled={!body.trim() || create.isPending}
            onClick={() => create.mutate()}
          >
            {create.isPending ? 'Saving…' : 'Save note'}
          </Button>
        </div>
      </Sheet>
    </div>
  )
}

function VendorsTab({ yatraId }: { yatraId: string }) {
  const q = useQuery({ queryKey: ['yatra-rates', yatraId], queryFn: () => ratesForYatra(yatraId) })
  if (q.isLoading) return <Skeleton className="h-40" />
  if (q.isError) return <ErrorNote error={q.error} />
  if (!q.data?.length) {
    return <Empty title="No rates linked" hint="Link vendor rates to this yatra to see them here." />
  }

  return (
    <ul className="space-y-2">
      {q.data.map((r) => (
        <li key={r.id}>
          <Card className="p-3">
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="font-medium">{r.vendors?.name ?? 'Vendor'}</p>
                <p className="text-xs text-muted">
                  {r.vendors?.kind ? VENDOR_KIND_LABELS[r.vendors.kind] : ''}
                  {r.vendors?.city ? ` · ${r.vendors.city}` : ''}
                </p>
              </div>
              <div className="text-right">
                <p className="font-semibold tabular-nums">{inr(r.rate)}</p>
                <p className="text-[11px] text-muted">{r.unit}</p>
              </div>
            </div>
            <p className="mt-2 text-sm">{r.service}</p>
            <div className="mt-2 flex items-center gap-2">
              {r.is_final && <Badge tone="ok"><Check size={11} /> Negotiated</Badge>}
              {r.vendors?.phone && (
                <a href={`tel:${r.vendors.phone}`} className="inline-flex items-center gap-1 text-xs text-primary">
                  <Phone size={12} /> {r.vendors.phone}
                </a>
              )}
            </div>
          </Card>
        </li>
      ))}
    </ul>
  )
}

function EconomicsTab({ yatraId }: { yatraId: string }) {
  const q = useQuery({ queryKey: ['economics', yatraId], queryFn: () => getEconomics(yatraId) })
  if (q.isLoading) return <Skeleton className="h-40" />
  if (q.isError) return <ErrorNote error={q.error} />
  if (!q.data?.length) return <Empty title="No economics recorded" />

  return (
    <div className="space-y-3">
      {q.data.map((e) => (
        <Card key={e.id} className="space-y-3">
          <div className="grid grid-cols-2 gap-2">
            <Stat label="Expected pax" value={e.expected_pax ?? '—'} />
            <Stat label="Avg ticket" value={inr(e.ticket_avg)} />
            <Stat label="Expected revenue" value={inrCompact(e.expected_revenue)} />
            <Stat
              label="Expected surplus"
              value={inrCompact(e.expected_surplus)}
              tone={(e.expected_surplus ?? 0) > 0 ? 'ok' : 'danger'}
            />
          </div>
          {e.margin_pct != null && (
            <div>
              <div className="flex items-baseline justify-between text-sm">
                <span className="text-muted">Margin</span>
                <span className="font-semibold tabular-nums">{e.margin_pct.toFixed(1)}%</span>
              </div>
              <div className="mt-1.5 h-2 overflow-hidden rounded-full bg-surface-2">
                <div
                  className="h-full rounded-full bg-ok"
                  style={{ width: `${Math.min(100, Math.max(0, e.margin_pct))}%` }}
                />
              </div>
            </div>
          )}
          {e.notes && (
            <p className="flex items-start gap-2 text-xs text-muted">
              <CalendarDays size={13} className="mt-0.5 shrink-0" />
              {e.notes}
            </p>
          )}
        </Card>
      ))}
    </div>
  )
}
