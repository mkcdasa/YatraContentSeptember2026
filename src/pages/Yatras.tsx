import { useMemo, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Route as RouteIcon, SlidersHorizontal } from 'lucide-react'
import {
  Button, Chip, ChipRow, Empty, ErrorNote, Input, Sheet, SkeletonList,
} from '@/components/ui'
import { YatraCard } from '@/components/app/YatraCard'
import { listThemes, listYatras, listYatrasForMonth } from '@/data/yatras'
import { useDebounced } from '@/hooks/useDebounced'
import { MONTHS, NATURE_LABELS, SCOPE_LABELS } from '@/lib/utils'
import type { Yatra } from '@/types/db'

const SCOPES = ['domestic', 'national', 'international'] as const
const NATURES = ['seasonal', 'evergreen', 'risky', 'special'] as const

export default function Yatras() {
  const [search, setSearch] = useState('')
  const [scope, setScope] = useState<string[]>([])
  const [nature, setNature] = useState<string[]>([])
  const [theme, setTheme] = useState<string>()
  const [month, setMonth] = useState<number>()
  const [seniorOnly, setSeniorOnly] = useState(false)
  const [filtersOpen, setFiltersOpen] = useState(false)

  const debounced = useDebounced(search)

  const list = useQuery({
    queryKey: ['yatras', debounced, scope, nature, theme, seniorOnly],
    queryFn: () =>
      listYatras({
        search: debounced || undefined,
        scope: scope.length ? scope : undefined,
        nature: nature.length ? nature : undefined,
        theme,
        seniorFriendly: seniorOnly || undefined,
      }),
  })

  // The month filter needs travel_windows, so it is a separate query whose
  // result intersects the main list rather than a fifth argument to it.
  const monthList = useQuery({
    queryKey: ['yatras', 'month', month],
    queryFn: () => listYatrasForMonth(month!),
    enabled: month != null,
  })

  const themes = useQuery({ queryKey: ['themes'], queryFn: listThemes })

  const results: Yatra[] = useMemo(() => {
    const base = list.data ?? []
    if (month == null || !monthList.data) return base
    const allowed = new Set(monthList.data.map((y) => y.id))
    return base.filter((y) => allowed.has(y.id))
  }, [list.data, monthList.data, month])

  const activeCount =
    scope.length + nature.length + (theme ? 1 : 0) + (month != null ? 1 : 0) + (seniorOnly ? 1 : 0)

  const toggle = (arr: string[], set: (v: string[]) => void, value: string) =>
    set(arr.includes(value) ? arr.filter((v) => v !== value) : [...arr, value])

  return (
    <div className="space-y-4">
      <h1 className="font-display text-2xl font-semibold">Yatras</h1>

      <div className="flex gap-2">
        <Input
          placeholder="Search yatras"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          aria-label="Search yatras"
        />
        <Button variant="outline" size="icon" aria-label="Filters" onClick={() => setFiltersOpen(true)}>
          <span className="relative">
            <SlidersHorizontal size={18} />
            {activeCount > 0 && (
              <span className="absolute -right-2 -top-2 grid h-4 w-4 place-items-center rounded-full bg-primary text-[10px] font-bold text-primary-fg">
                {activeCount}
              </span>
            )}
          </span>
        </Button>
      </div>

      <ChipRow>
        {SCOPES.map((s) => (
          <Chip key={s} active={scope.includes(s)} onClick={() => toggle(scope, setScope, s)}>
            {SCOPE_LABELS[s]}
          </Chip>
        ))}
        {NATURES.map((n) => (
          <Chip key={n} active={nature.includes(n)} onClick={() => toggle(nature, setNature, n)}>
            {NATURE_LABELS[n]}
          </Chip>
        ))}
      </ChipRow>

      {list.isError && <ErrorNote error={list.error} />}

      {list.isLoading || (month != null && monthList.isLoading) ? (
        <SkeletonList rows={5} />
      ) : results.length ? (
        <>
          <p className="text-sm text-muted">{results.length} yatras</p>
          <div className="space-y-3">
            {results.map((y) => (
              <YatraCard key={y.id} yatra={y} />
            ))}
          </div>
        </>
      ) : (
        <Empty
          icon={<RouteIcon size={28} />}
          title="No yatras match these filters"
          hint="Try clearing a filter, or search by a different name."
        />
      )}

      <Sheet open={filtersOpen} onClose={() => setFiltersOpen(false)} title="Filters">
        <div className="space-y-6">
          <div>
            <p className="mb-2 text-sm font-medium">Travelling in</p>
            <div className="grid grid-cols-6 gap-1.5">
              {MONTHS.map((label, i) => (
                <Chip
                  key={label}
                  active={month === i + 1}
                  onClick={() => setMonth(month === i + 1 ? undefined : i + 1)}
                  className="justify-center px-0 text-center"
                >
                  {label}
                </Chip>
              ))}
            </div>
            <p className="mt-2 text-xs text-muted">
              Matches yatras whose best or shoulder season includes this month.
            </p>
          </div>

          <div>
            <p className="mb-2 text-sm font-medium">Theme</p>
            <div className="flex flex-wrap gap-2">
              {(themes.data ?? []).map((t) => (
                <Chip key={t} active={theme === t} onClick={() => setTheme(theme === t ? undefined : t)}>
                  {t}
                </Chip>
              ))}
              {!themes.data?.length && <p className="text-sm text-muted">No themes tagged yet.</p>}
            </div>
          </div>

          <div>
            <p className="mb-2 text-sm font-medium">Suitability</p>
            <Chip active={seniorOnly} onClick={() => setSeniorOnly(!seniorOnly)}>
              Senior friendly only
            </Chip>
          </div>

          <div className="flex gap-2 pt-2">
            <Button
              variant="outline"
              className="flex-1"
              onClick={() => {
                setScope([]); setNature([]); setTheme(undefined)
                setMonth(undefined); setSeniorOnly(false)
              }}
            >
              Clear all
            </Button>
            <Button className="flex-1" onClick={() => setFiltersOpen(false)}>
              Show {results.length} results
            </Button>
          </div>
        </div>
      </Sheet>
    </div>
  )
}
