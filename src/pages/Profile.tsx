import { useEffect, useState, type FormEvent } from 'react'
import { Button, Card, ErrorNote, Input, SectionTitle } from '@/components/ui'
import { useAuth } from '@/hooks/useAuth'
import { updateProfile } from '@/data/profile'

const ROLE_LABELS: Record<string, string> = {
  admin: 'Administrator', staff: 'Staff', tour_leader: 'Tour leader', yatri: 'Yatri',
}

export default function Profile() {
  const { profile, session, signOut, refreshProfile } = useAuth()
  const [fullName, setFullName] = useState('')
  const [phone, setPhone] = useState('')
  const [city, setCity] = useState('')
  const [saved, setSaved] = useState(false)
  const [error, setError] = useState<unknown>(null)
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    setFullName(profile?.full_name ?? '')
    setPhone(profile?.phone ?? '')
    setCity(profile?.city ?? '')
  }, [profile])

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    if (!session) return
    setBusy(true)
    setError(null)
    setSaved(false)
    try {
      await updateProfile(session.user.id, { full_name: fullName, phone, city })
      await refreshProfile()
      setSaved(true)
    } catch (err) {
      setError(err)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="space-y-5">
      <h1 className="font-display text-2xl font-semibold">Profile</h1>

      <Card>
        <p className="text-sm text-muted">{profile?.email}</p>
        <p className="mt-1 text-sm">
          Role: <span className="font-medium">{ROLE_LABELS[profile?.role ?? 'yatri']}</span>
        </p>
        <p className="mt-2 text-xs text-muted">
          Roles are set by an administrator. Vendor rates and margins are visible to staff only.
        </p>
      </Card>

      <section>
        <SectionTitle>Your details</SectionTitle>
        <form onSubmit={onSubmit} className="space-y-3">
          <Input placeholder="Full name" value={fullName} onChange={(e) => setFullName(e.target.value)} />
          <Input placeholder="Phone" inputMode="tel" value={phone} onChange={(e) => setPhone(e.target.value)} />
          <Input placeholder="City" value={city} onChange={(e) => setCity(e.target.value)} />
          <Button type="submit" disabled={busy} className="w-full">
            {busy ? 'Saving…' : saved ? 'Saved' : 'Save'}
          </Button>
        </form>
        {error != null && <ErrorNote error={error} />}
      </section>

      <Button variant="outline" className="w-full" onClick={() => signOut()}>
        Sign out
      </Button>
    </div>
  )
}
