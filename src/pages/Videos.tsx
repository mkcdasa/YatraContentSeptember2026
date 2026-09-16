import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { PlayCircle, Youtube } from 'lucide-react'
import { Card, Chip, ChipRow, Empty, ErrorNote, SkeletonList } from '@/components/ui'
import { listVideos } from '@/data/library'
import type { VideoKind } from '@/types/db'

const KINDS: { id: VideoKind; label: string }[] = [
  { id: 'expert', label: 'Industry experts' },
  { id: 'destination', label: 'Destinations' },
  { id: 'training', label: 'Training' },
  { id: 'testimonial', label: 'Testimonials' },
  { id: 'promo', label: 'Promos' },
]

export default function Videos() {
  const [kind, setKind] = useState<VideoKind>()
  const q = useQuery({ queryKey: ['videos', kind], queryFn: () => listVideos(kind) })

  return (
    <div className="space-y-4">
      <div>
        <h1 className="font-display text-2xl font-semibold">Video library</h1>
        <p className="text-sm text-muted">Talks from industry experts and destination footage.</p>
      </div>

      <ChipRow>
        <Chip active={!kind} onClick={() => setKind(undefined)}>All</Chip>
        {KINDS.map((k) => (
          <Chip key={k.id} active={kind === k.id} onClick={() => setKind(kind === k.id ? undefined : k.id)}>
            {k.label}
          </Chip>
        ))}
      </ChipRow>

      {q.isError && <ErrorNote error={q.error} />}

      {q.isLoading ? (
        <SkeletonList rows={4} />
      ) : q.data?.length ? (
        <ul className="grid gap-3 sm:grid-cols-2">
          {q.data.map((v) => (
            <li key={v.id}>
              <a href={v.url} target="_blank" rel="noreferrer" className="block">
                <Card className="overflow-hidden p-0">
                  {v.youtube_id ? (
                    <img
                      src={`https://i.ytimg.com/vi/${v.youtube_id}/hqdefault.jpg`}
                      alt=""
                      loading="lazy"
                      className="aspect-video w-full object-cover"
                    />
                  ) : (
                    <div className="grid aspect-video w-full place-items-center bg-surface-2 text-muted">
                      <PlayCircle size={32} />
                    </div>
                  )}
                  <div className="p-3">
                    <p className="line-clamp-2 text-sm font-medium leading-snug">{v.title}</p>
                    {v.channel && <p className="mt-0.5 text-xs text-muted">{v.channel}</p>}
                  </div>
                </Card>
              </a>
            </li>
          ))}
        </ul>
      ) : (
        <Empty
          icon={<Youtube size={28} />}
          title="No videos yet"
          hint="Paste a YouTube link and it is saved with its thumbnail."
        />
      )}
    </div>
  )
}
