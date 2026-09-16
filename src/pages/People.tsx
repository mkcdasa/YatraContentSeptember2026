import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Card, Empty, ErrorNote, SkeletonList } from '@/components/ui'
import { listProfiles, setRole } from '@/data/profile'
import { initials } from '@/lib/utils'
import type { AppRole } from '@/types/db'

const ROLES: AppRole[] = ['yatri', 'tour_leader', 'staff', 'admin']
const ROLE_LABELS: Record<AppRole, string> = {
  yatri: 'Yatri', tour_leader: 'Tour leader', staff: 'Staff', admin: 'Admin',
}

/**
 * Admin-only. RLS already rejects a role change from anyone else, so this screen
 * is a convenience, not the control.
 */
export default function People() {
  const qc = useQueryClient()
  const q = useQuery({ queryKey: ['profiles'], queryFn: listProfiles })
  const mutate = useMutation({
    mutationFn: ({ id, role }: { id: string; role: AppRole }) => setRole(id, role),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['profiles'] }),
  })

  return (
    <div className="space-y-4">
      <div>
        <h1 className="font-display text-2xl font-semibold">People & roles</h1>
        <p className="text-sm text-muted">
          Staff and tour leaders see vendors, negotiated rates and margins. Yatris do not.
        </p>
      </div>

      {q.isError && <ErrorNote error={q.error} />}
      {mutate.isError && <ErrorNote error={mutate.error} />}

      {q.isLoading ? (
        <SkeletonList rows={5} />
      ) : q.data?.length ? (
        <ul className="space-y-2">
          {q.data.map((p) => (
            <li key={p.id}>
              <Card className="p-3">
                <div className="flex items-center gap-3">
                  <span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-surface-2 text-xs font-semibold">
                    {initials(p.full_name ?? p.email)}
                  </span>
                  <div className="min-w-0 flex-1">
                    <p className="truncate font-medium">{p.full_name ?? '—'}</p>
                    <p className="truncate text-xs text-muted">{p.email}</p>
                  </div>
                </div>
                <div className="mt-3 flex gap-1">
                  {ROLES.map((r) => (
                    <button
                      key={r}
                      disabled={mutate.isPending}
                      onClick={() => mutate.mutate({ id: p.id, role: r })}
                      aria-pressed={p.role === r}
                      className={`flex-1 rounded-lg py-2 text-xs font-medium transition-colors ${
                        p.role === r ? 'bg-primary text-primary-fg' : 'bg-surface-2 text-muted'
                      }`}
                    >
                      {ROLE_LABELS[r]}
                    </button>
                  ))}
                </div>
              </Card>
            </li>
          ))}
        </ul>
      ) : (
        <Empty title="No people yet" />
      )}
    </div>
  )
}
