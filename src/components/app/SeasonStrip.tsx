import { cn, MONTHS } from '@/lib/utils'

type Verdict = 'best' | 'shoulder' | 'avoid' | 'unknown'

function verdictFor(m: number, best: number[], shoulder: number[], avoid: number[]): Verdict {
  // Deliberate precedence: a month the team marked "avoid" wins over one that
  // also appears in "best". The source sheets contradict themselves in places
  // (Char Dham lists the same months in both columns) and the safe reading is
  // to warn rather than to invite.
  if (avoid.includes(m)) return 'avoid'
  if (best.includes(m)) return 'best'
  if (shoulder.includes(m)) return 'shoulder'
  return 'unknown'
}

const STYLES: Record<Verdict, string> = {
  best: 'bg-ok/85 text-white',
  shoulder: 'bg-accent/80 text-accent-fg',
  avoid: 'bg-danger/80 text-white',
  unknown: 'bg-surface-2 text-muted',
}

const LABELS: Record<Verdict, string> = {
  best: 'best season', shoulder: 'shoulder season', avoid: 'avoid', unknown: 'no guidance',
}

/**
 * Twelve months at a glance. This is the component features 6, 7 and 13 collapse
 * into: perfect weather, extreme weather and seasonality answered in one row a
 * coordinator can read while standing in a queue.
 */
export function SeasonStrip({
  best = [], shoulder = [], avoid = [], highlightMonth, compact,
}: {
  best?: number[]; shoulder?: number[]; avoid?: number[]
  highlightMonth?: number; compact?: boolean
}) {
  return (
    <div>
      <div className="grid grid-cols-12 gap-1" role="list" aria-label="Season by month">
        {MONTHS.map((label, i) => {
          const m = i + 1
          const v = verdictFor(m, best, shoulder, avoid)
          return (
            <div
              key={label}
              role="listitem"
              title={`${label}: ${LABELS[v]}`}
              className={cn(
                'grid place-items-center rounded-md text-[10px] font-semibold uppercase',
                compact ? 'h-5' : 'h-7',
                STYLES[v],
                highlightMonth === m && 'ring-2 ring-primary ring-offset-1 ring-offset-bg',
              )}
            >
              {label[0]}
              <span className="sr-only">{`${label}: ${LABELS[v]}`}</span>
            </div>
          )
        })}
      </div>
      {!compact && (
        <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-[11px] text-muted">
          <Legend className="bg-ok/85" label="Best" />
          <Legend className="bg-accent/80" label="Shoulder" />
          <Legend className="bg-danger/80" label="Avoid" />
        </div>
      )}
    </div>
  )
}

const Legend = ({ className, label }: { className: string; label: string }) => (
  <span className="inline-flex items-center gap-1.5">
    <span className={cn('h-2.5 w-2.5 rounded-sm', className)} />
    {label}
  </span>
)
