import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { BookOpen, ChevronRight, Lock } from 'lucide-react'
import { Badge, Card, Chip, ChipRow, Empty, ErrorNote, SkeletonList } from '@/components/ui'
import { getArticle, listArticles } from '@/data/library'

const CATEGORY_LABELS: Record<string, string> = {
  packing: 'Packing', orientation: 'Orientation', planning: 'Planning',
  hospitality: 'Hospitality', marketing: 'Marketing', sos: 'Safety',
}

export default function Library() {
  const [category, setCategory] = useState<string>()
  const q = useQuery({ queryKey: ['articles', category], queryFn: () => listArticles(category) })
  const all = useQuery({ queryKey: ['articles'], queryFn: () => listArticles() })

  const categories = [...new Set((all.data ?? []).map((a) => a.category))].sort()

  return (
    <div className="space-y-4">
      <div>
        <h1 className="font-display text-2xl font-semibold">Handbooks</h1>
        <p className="text-sm text-muted">Checklists, orientation notes and departmental playbooks.</p>
      </div>

      {categories.length > 0 && (
        <ChipRow>
          <Chip active={!category} onClick={() => setCategory(undefined)}>All</Chip>
          {categories.map((c) => (
            <Chip key={c} active={category === c} onClick={() => setCategory(category === c ? undefined : c)}>
              {CATEGORY_LABELS[c] ?? c}
            </Chip>
          ))}
        </ChipRow>
      )}

      {q.isError && <ErrorNote error={q.error} />}

      {q.isLoading ? (
        <SkeletonList rows={4} />
      ) : q.data?.length ? (
        <ul className="space-y-2">
          {q.data.map((a) => (
            <li key={a.id}>
              <Link to={`/library/${a.slug}`} className="card flex items-center gap-3 p-3">
                <BookOpen size={17} className="shrink-0 text-primary" />
                <div className="min-w-0 flex-1">
                  <p className="truncate font-medium leading-snug">{a.title}</p>
                  <p className="text-xs text-muted">{CATEGORY_LABELS[a.category] ?? a.category}</p>
                </div>
                {a.visibility === 'staff' && <Badge tone="primary"><Lock size={10} /> Staff</Badge>}
                <ChevronRight size={17} className="shrink-0 text-muted" />
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <Empty icon={<BookOpen size={28} />} title="No handbooks yet" />
      )}
    </div>
  )
}

export function ArticlePage() {
  const { slug = '' } = useParams()
  const q = useQuery({ queryKey: ['article', slug], queryFn: () => getArticle(slug), enabled: !!slug })

  if (q.isLoading) return <SkeletonList rows={3} />
  if (q.isError) return <ErrorNote error={q.error} />
  if (!q.data) return <Empty title="Not found" hint="This handbook may be staff-only." />

  return (
    <article className="space-y-4">
      <header>
        <h1 className="font-display text-2xl font-semibold leading-tight">{q.data.title}</h1>
        <div className="mt-2 flex gap-1.5">
          <Badge>{CATEGORY_LABELS[q.data.category] ?? q.data.category}</Badge>
          {q.data.visibility === 'staff' && <Badge tone="primary"><Lock size={10} /> Staff only</Badge>}
        </div>
      </header>
      <Card>
        <Markdown source={q.data.body_md} />
      </Card>
    </article>
  )
}

/**
 * Deliberately tiny. Content here is a bulleted list exported from Evernote, not
 * arbitrary rich text, so a full markdown pipeline would be weight without
 * benefit. Everything is rendered as text — nothing is injected as HTML.
 */
function Markdown({ source }: { source: string }) {
  const lines = source.split('\n')
  return (
    <div className="space-y-2 text-sm leading-relaxed">
      {lines.map((line, i) => {
        const trimmed = line.trim()
        if (!trimmed) return null
        if (trimmed.startsWith('## ')) {
          return <h2 key={i} className="pt-2 text-base font-semibold">{trimmed.slice(3)}</h2>
        }
        if (/^[-*♦]\s/.test(trimmed)) {
          return (
            <p key={i} className="flex gap-2">
              <span className="text-primary">•</span>
              <span className="flex-1">{trimmed.replace(/^[-*♦]\s/, '')}</span>
            </p>
          )
        }
        return <p key={i}>{trimmed}</p>
      })}
    </div>
  )
}
