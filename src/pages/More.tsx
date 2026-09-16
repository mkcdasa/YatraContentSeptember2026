import { Link } from 'react-router-dom'
import {
  BookOpen, ChevronRight, IndianRupee, Moon, Store, Sun, SunMoon, User, Users, Youtube,
} from 'lucide-react'
import { Badge, Card, SectionTitle } from '@/components/ui'
import { AdminOnly, StaffOnly } from '@/components/app/RoleGate'
import { useTheme } from '@/hooks/useTheme'
import { useAuth } from '@/hooks/useAuth'

export default function More() {
  const { theme, setTheme } = useTheme()
  const { profile } = useAuth()

  return (
    <div className="space-y-6">
      <h1 className="font-display text-2xl font-semibold">More</h1>

      <section>
        <SectionTitle>Library</SectionTitle>
        <div className="space-y-2">
          <Row to="/library" icon={<BookOpen size={17} />} label="Handbooks & checklists" />
          <Row to="/videos" icon={<Youtube size={17} />} label="Video library" />
        </div>
      </section>

      <StaffOnly>
        <section>
          <SectionTitle>Department</SectionTitle>
          <div className="space-y-2">
            <Row to="/vendors" icon={<Store size={17} />} label="Vendors & negotiated rates" staff />
            <Row to="/finance" icon={<IndianRupee size={17} />} label="Profitability & reports" staff />
            <AdminOnly>
              <Row to="/admin/people" icon={<Users size={17} />} label="People & roles" staff />
            </AdminOnly>
          </div>
        </section>
      </StaffOnly>

      <section>
        <SectionTitle>Appearance</SectionTitle>
        <Card className="flex gap-2 p-2">
          {([
            ['light', 'Light', <Sun key="l" size={16} />],
            ['dark', 'Dark', <Moon key="d" size={16} />],
            ['system', 'Auto', <SunMoon key="s" size={16} />],
          ] as const).map(([id, label, icon]) => (
            <button
              key={id}
              onClick={() => setTheme(id)}
              aria-pressed={theme === id}
              className={`tap flex flex-1 items-center justify-center gap-1.5 rounded-lg text-sm font-medium transition-colors ${
                theme === id ? 'bg-primary text-primary-fg' : 'text-muted hover:bg-surface-2'
              }`}
            >
              {icon} {label}
            </button>
          ))}
        </Card>
      </section>

      <section>
        <SectionTitle>Account</SectionTitle>
        <Row
          to="/profile"
          icon={<User size={17} />}
          label={profile?.full_name ?? profile?.email ?? 'Profile'}
        />
      </section>
    </div>
  )
}

function Row({
  to, icon, label, staff,
}: {
  to: string; icon: React.ReactNode; label: string; staff?: boolean
}) {
  return (
    <Link to={to} className="card flex items-center gap-3 p-3">
      <span className="text-primary">{icon}</span>
      <span className="flex-1 text-sm font-medium">{label}</span>
      {staff && <Badge tone="primary">Staff</Badge>}
      <ChevronRight size={17} className="text-muted" />
    </Link>
  )
}
