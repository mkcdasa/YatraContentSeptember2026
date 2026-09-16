import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { BookOpen, Compass, Route as RouteIcon, Search, Store } from 'lucide-react'
import { Badge, Empty, ErrorNote, Input, SkeletonList } from '@/components/ui'
import { searchAll } from '@/data/search'
import { useDebounced } from '@/hooks/useDebounced'
import type { SearchHit } from '@/types/db'

const META: Record<SearchHit['kind'], { icon: React.ReactNode; label: string; href: (h: SearchHit) => string }> = {
  yatra: { icon: <RouteIcon size={16} />, label: 'Yatra', href: (h) => `/yatras/${h.slug}` },
  destination: { icon: <Compass size={16} />, label: 'Place', href: (h) => `/explore/${h.slug}` },
  article: { icon: <BookOpen size={16} />, label: 'Handbook', href: (h) => `/library/${h.slug}` },
  vendor: { icon: <Store size={16} />, label: 'Vendor', href: () => '/vendors' },
}

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const debounced = useDebounced(query)

  const q = useQuery({
    queryKey: ['search', debounced],
    queryFn: () => searchAll(debounced),
    enabled: debounced.trim().length >= 2,
  })

  return (
    <div className="space-y-4">
      <Input
        autoFocus
        placeholder="Yatras, temples, vendors, handbooks…"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        aria-label="Search everything"
      />

      {q.isError && <ErrorNote error={q.error} />}

      {debounced.trim().length < 2 ? (
        <Empty
          icon={<Search size={28} />}
          title="Search everything"
          hint="Type at least two characters. Vendors appear for staff only."
        />
      ) : q.isLoading ? (
        <SkeletonList rows={5} />
      ) : q.data?.length ? (
        <ul className="space-y-2">
          {q.data.map((hit) => {
            const meta = META[hit.kind]
            return (
              <li key={`${hit.kind}-${hit.id}`}>
                <Link to={meta.href(hit)} className="card flex items-center gap-3 p-3">
                  <span className="text-primary">{meta.icon}</span>
                  <div className="min-w-0 flex-1">
                    <p className="truncate font-medium leading-snug">{hit.title}</p>
                    {hit.subtitle && <p className="truncate text-xs text-muted">{hit.subtitle}</p>}
                  </div>
                  <Badge>{meta.label}</Badge>
                </Link>
              </li>
            )
          })}
        </ul>
      ) : (
        <Empty title={`Nothing found for "${debounced}"`} />
      )}
    </div>
  )
}
