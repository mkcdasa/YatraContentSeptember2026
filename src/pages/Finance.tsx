import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { FileText, Repeat, TrendingUp } from 'lucide-react'
import { Badge, Card, Empty, ErrorNote, SectionTitle, SkeletonList, Stat } from '@/components/ui'
import { profitability } from '@/data/yatras'
import { listFinanceReports } from '@/data/library'
import { NATURE_LABELS, inrCompact } from '@/lib/utils'

export default function Finance() {
  const rows = useQuery({ queryKey: ['profitability'], queryFn: profitability })
  const reports = useQuery({ queryKey: ['finance-reports'], queryFn: listFinanceReports })

  const withMargin = (rows.data ?? []).filter((r) => r.avg_margin_pct != null)
  const totalSurplus = withMargin.reduce((sum, r) => sum + (r.total_expected_surplus ?? 0), 0)
  const repeatable = (rows.data ?? []).filter((r) => (r.batches_this_year ?? 0) >= 4)

  return (
    <div className="space-y-5">
      <div>
        <h1 className="font-display text-2xl font-semibold">Profitability</h1>
        <p className="text-sm text-muted">Margins, repeatability and finance reports. Staff only.</p>
      </div>

      {rows.isError && <ErrorNote error={rows.error} />}

      {rows.isLoading ? (
        <SkeletonList rows={5} />
      ) : (
        <>
          <div className="grid grid-cols-3 gap-2">
            <Stat label="Yatras costed" value={withMargin.length} />
            <Stat label="Expected surplus" value={inrCompact(totalSurplus)} tone="ok" />
            <Stat label="Repeats 4×+" value={repeatable.length} hint="this year" />
          </div>

          <section>
            <SectionTitle>Ranked by margin</SectionTitle>
            {withMargin.length ? (
              <ul className="space-y-2">
                {withMargin.map((r) => (
                  <li key={r.yatra_id}>
                    <Link to={`/yatras/${r.slug}`} className="block">
                      <Card className="p-3">
                        <div className="flex items-start justify-between gap-3">
                          <div className="min-w-0">
                            <p className="truncate font-medium leading-snug">{r.title}</p>
                            <p className="mt-0.5 flex flex-wrap items-center gap-1.5 text-xs text-muted">
                              <Badge>{NATURE_LABELS[r.nature]}</Badge>
                              {!!r.batches_this_year && (
                                <Badge tone={r.batches_this_year >= 4 ? 'ok' : 'neutral'}>
                                  <Repeat size={10} /> {r.batches_this_year}× this year
                                </Badge>
                              )}
                            </p>
                          </div>
                          <div className="shrink-0 text-right">
                            <p className="flex items-center gap-1 font-semibold tabular-nums text-ok">
                              <TrendingUp size={14} />
                              {r.avg_margin_pct!.toFixed(1)}%
                            </p>
                            <p className="text-[11px] text-muted">
                              {inrCompact(r.total_expected_surplus)}
                            </p>
                          </div>
                        </div>
                        <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-surface-2">
                          <div
                            className="h-full rounded-full bg-ok"
                            style={{ width: `${Math.min(100, Math.max(2, r.avg_margin_pct!))}%` }}
                          />
                        </div>
                      </Card>
                    </Link>
                  </li>
                ))}
              </ul>
            ) : (
              <Empty
                title="No costings yet"
                hint="Economics rows drive this ranking. Add them per yatra or per batch."
              />
            )}
          </section>
        </>
      )}

      <section>
        <SectionTitle>Finance team reports</SectionTitle>
        {reports.data?.length ? (
          <ul className="space-y-2">
            {reports.data.map((r) => (
              <li key={r.id}>
                <Card className="flex items-start gap-3 p-3">
                  <FileText size={16} className="mt-0.5 shrink-0 text-muted" />
                  <div className="min-w-0 flex-1">
                    <p className="font-medium leading-snug">{r.title}</p>
                    {r.period && <p className="text-xs text-muted">{r.period}</p>}
                    {r.summary && <p className="mt-1 text-sm text-muted">{r.summary}</p>}
                  </div>
                </Card>
              </li>
            ))}
          </ul>
        ) : (
          <Empty title="No reports uploaded" hint="Finance uploads land in the private 'finance' bucket." />
        )}
      </section>
    </div>
  )
}
