import { useQuery } from '@tanstack/react-query'
import { useParams } from 'react-router-dom'
import { MapPin } from 'lucide-react'
import { Badge, Card, Empty, ErrorNote, SectionTitle, Skeleton } from '@/components/ui'
import { SeasonStrip } from '@/components/app/SeasonStrip'
import { getDestination, listPastimes } from '@/data/destinations'
import { PLACE_KIND_LABELS } from '@/lib/utils'

export default function DestinationDetail() {
  const { slug = '' } = useParams()
  const q = useQuery({ queryKey: ['destination', slug], queryFn: () => getDestination(slug), enabled: !!slug })
  const pastimes = useQuery({
    queryKey: ['pastimes', q.data?.id],
    queryFn: () => listPastimes(q.data!.id),
    enabled: !!q.data?.id,
  })

  if (q.isLoading) return <Skeleton className="h-48" />
  if (q.isError) return <ErrorNote error={q.error} />
  if (!q.data) return <Empty title="Place not found" />

  const d = q.data

  return (
    <div className="space-y-4">
      <header>
        <h1 className="font-display text-2xl font-semibold leading-tight">{d.name}</h1>
        <p className="mt-1 text-sm text-muted">
          {[d.deity, d.city, d.state, d.country !== 'India' ? d.country : null].filter(Boolean).join(' · ')}
        </p>
        <div className="mt-2 flex flex-wrap gap-1.5">
          {d.kinds.map((k) => (
            <Badge key={k} tone="primary">{PLACE_KIND_LABELS[k]}</Badge>
          ))}
        </div>
      </header>

      {d.speciality && (
        <Card className="border-accent/40 bg-accent/5">
          <p className="text-sm">{d.speciality}</p>
        </Card>
      )}

      {(d.best_months.length > 0 || d.avoid_months.length > 0) && (
        <section>
          <SectionTitle>When to visit</SectionTitle>
          <Card>
            <SeasonStrip best={d.best_months} avoid={d.avoid_months} />
            {d.best_time_note && <p className="mt-3 text-sm text-muted">{d.best_time_note}</p>}
          </Card>
        </section>
      )}

      {d.sevas.length > 0 && (
        <section>
          <SectionTitle>Darshans & sevas</SectionTitle>
          <div className="flex flex-wrap gap-1.5">
            {d.sevas.map((s) => <Badge key={s} size="md">{s}</Badge>)}
          </div>
        </section>
      )}

      {d.description && (
        <section>
          <SectionTitle>About</SectionTitle>
          <p className="whitespace-pre-line text-sm leading-relaxed">{d.description}</p>
        </section>
      )}

      {!!pastimes.data?.length && (
        <section>
          <SectionTitle>Pastimes</SectionTitle>
          <div className="space-y-2">
            {pastimes.data.map((p) => (
              <Card key={p.id}>
                <p className="font-medium">{p.title}</p>
                {p.source && <p className="text-xs text-muted">{p.source}</p>}
                <p className="mt-2 whitespace-pre-line text-sm leading-relaxed">{p.body}</p>
              </Card>
            ))}
          </div>
        </section>
      )}

      {d.map_url && (
        <a
          href={d.map_url}
          target="_blank"
          rel="noreferrer"
          className="card flex items-center gap-2 p-3 text-sm font-medium text-primary"
        >
          <MapPin size={16} /> Open in Maps
        </a>
      )}
    </div>
  )
}
