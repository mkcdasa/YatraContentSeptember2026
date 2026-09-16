import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { CalendarDays, Compass, Home, MoreHorizontal, Route, Search } from 'lucide-react'
import { cn, initials } from '@/lib/utils'
import { useAuth } from '@/hooks/useAuth'

const TABS = [
  { to: '/', label: 'Home', icon: Home, end: true },
  { to: '/yatras', label: 'Yatras', icon: Route },
  { to: '/calendar', label: 'Calendar', icon: CalendarDays },
  { to: '/explore', label: 'Explore', icon: Compass },
  { to: '/more', label: 'More', icon: MoreHorizontal },
]

export function AppShell() {
  const { profile } = useAuth()
  const navigate = useNavigate()

  return (
    <div className="mx-auto flex min-h-screen w-full max-w-2xl flex-col">
      <header
        className="sticky top-0 z-30 border-b border-border bg-bg/85 backdrop-blur-md"
        style={{ paddingTop: 'env(safe-area-inset-top)' }}
      >
        <div className="flex h-14 items-center gap-2 px-4">
          <NavLink to="/" className="flex items-center gap-2">
            <span className="grid h-8 w-8 place-items-center rounded-lg bg-primary font-display text-sm font-semibold text-primary-fg">
              य
            </span>
            <span className="font-display text-base font-semibold">Yatra KB</span>
          </NavLink>

          <div className="flex-1" />

          <button
            onClick={() => navigate('/search')}
            aria-label="Search"
            className="tap grid place-items-center rounded-full text-muted hover:text-fg"
          >
            <Search size={20} />
          </button>
          <NavLink
            to="/profile"
            aria-label="Profile"
            className="grid h-9 w-9 place-items-center rounded-full bg-surface-2 text-xs font-semibold"
          >
            {initials(profile?.full_name ?? profile?.email)}
          </NavLink>
        </div>
      </header>

      <main className="flex-1 px-4 pb-28 pt-4">
        <Outlet />
      </main>

      <nav
        className="fixed inset-x-0 bottom-0 z-30 mx-auto max-w-2xl border-t border-border bg-bg/95 backdrop-blur-md"
        style={{ paddingBottom: 'env(safe-area-inset-bottom)' }}
        aria-label="Primary"
      >
        <ul className="grid grid-cols-5">
          {TABS.map(({ to, label, icon: Icon, end }) => (
            <li key={to}>
              <NavLink
                to={to}
                end={end}
                className={({ isActive }) =>
                  cn(
                    'flex h-14 flex-col items-center justify-center gap-0.5 text-[11px] font-medium transition-colors',
                    isActive ? 'text-primary' : 'text-muted',
                  )
                }
              >
                {({ isActive }) => (
                  <>
                    <Icon size={20} strokeWidth={isActive ? 2.4 : 1.8} />
                    {label}
                  </>
                )}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  )
}
