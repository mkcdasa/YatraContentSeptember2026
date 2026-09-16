import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { Compass } from 'lucide-react'
import { Badge, Button, Card, Chip, ChipRow, Empty, ErrorNote, Input, SkeletonList } from '@/components/ui'
import { listDestinations, listStates } from '@/data/destinations'
import { useDebounced } from '@/hooks/useDebounced'
import { MONTHS, PLACE_KIND_LABELS } from '@/lib/utils'
import type { PlaceKind } from '@/types/db'

const KINDS: PlaceKind[] = [
  'jyotirlinga', 'shakti_peetha', 'divya_desam', 'char_dham', 'unesco', 'river', 'temple',
]

export default function Explore() {
  const [search, setSearch] = useState('')
  const [kinds, setKinds] = useState<PlaceKind[]>([])
  const [state, setState] = useState<string>()
  const [month, setMonth] = useState<number>()
  const [page, setPage] = useState(0)

  const debounced = useDebounced(search)
  const filters = {
    search: debounced || undefined,
    kinds: kinds.length ? kinds : undefined,
    state,
    month,
  }

  const q = useQuery({
    queryKey: ['destinations', filters, page],
    queryFn: () => listDestinations(filters, page),
  })
  const states = useQuery({ queryKey: ['states'], queryFn: listStates })

  const reset = () => setPage(0)
  const toggleKind = (k: PlaceKind) => {
    setKinds(kinds.includes(k) ? kinds.filter((x) => x !== k) : [...kinds, k])
    reset()
  }

  return (
    <div className="space-y-4">
      <h1 className="font-display text-2xl font-semibold">Temples & holy places</h1>

      <Input
        placeholder="Search by name, deity or town"
        value={search}
        onChange={(e) => { setSearch(e.target.value); reset() }}
        aria-label="Search places"
      />

      <ChipRow>
        {KINDS.map((k) => (
          <Chip key={k} active={kinds.includes(k)} onClick={() => toggleKind(k)}>
            {PLACE_KIND_LABELS[k]}
          </Chip>
        ))}
      </ChipRow>

      <ChipRow>
        <Chip active={!month} onClick={() => { setMonth(undefined); reset() }}>Any month</Chip>
        {MONTHS.map((label, i) => (
          <Chip
            key={label}
            active={month === i + 1}
            onClick={() => { setMonth(month === i + 1 ? undefined : i + 1); reset() }}
          >
            {label}
          </Chip>
        ))}
      </ChipRow>

      {!!states.data?.length && (
        <ChipRow>
          <Chip active={!state} onClick={() => { setState(undefined); reset() }}>All states</Chip>
          {states.data.map((s) => (
            <Chip key={s} active={state === s} onClick={() => { setState(state === s ? undefined : s); reset() }}>
              {s}
            </Chip>
          ))}
        </ChipRow>
      )}

      {q.isError && <ErrorNote error={q.error} />}

      {q.isLoading ? (
        <SkeletonList rows={6} />
      ) : q.data?.rows.length ? (
        <>
          <div className="space-y-2">
            {q.data.rows.map((d) => (
              <Link key={d.id} to={`/explore/${d.slug}`} className="block">
                <Card className="p-3">
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                      <p className="truncate font-medium leading-snug">{d.name}</p>
                      <p className="truncate text-xs text-muted">
                        {[d.deity, d.city, d.state].filter(Boolean).join(' · ')}
                      </p>
                    </div>
                  </div>
                  {d.kinds.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-1">
                      {d.kinds.map((k) => (
                        <Badge key={k} tone={k === 'temple' ? 'neutral' : 'primary'}>
                          {PLACE_KIND_LABELS[k]}
                        </Badge>
                      ))}
                    </div>
                  )}
                </Card>
              </Link>
            ))}
          </div>

          <div className="flex items-center justify-between pt-2">
            <Button variant="outline" size="sm" disabled={page === 0} onClick={() => setPage(page - 1)}>
              Previous
            </Button>
            <span className="text-sm text-muted">Page {page + 1}</span>
            <Button variant="outline" size="sm" disabled={!q.data.hasMore} onClick={() => setPage(page + 1)}>
              Next
            </Button>
          </div>
        </>
      ) : (
        <Empty icon={<Compass size={28} />} title="No places match" hint="Try a different name or clear a filter." />
      )}
    </div>
  )
}
