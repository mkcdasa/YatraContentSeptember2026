import { useState, type FormEvent } from 'react'
import { Button, Card, ErrorNote, Input } from '@/components/ui'
import { useAuth } from '@/hooks/useAuth'

export default function Login() {
  const { signInWithGoogle, signInWithEmail } = useAuth()
  const [email, setEmail] = useState('')
  const [sent, setSent] = useState(false)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<unknown>(null)

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    setBusy(true)
    setError(null)
    try {
      await signInWithEmail(email.trim())
      setSent(true)
    } catch (err) {
      setError(err)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="mx-auto flex min-h-screen w-full max-w-md flex-col justify-center px-6 py-10">
      <div className="mb-8 text-center">
        <span className="mx-auto grid h-14 w-14 place-items-center rounded-2xl bg-primary font-display text-xl font-semibold text-primary-fg">
          य
        </span>
        <h1 className="mt-4 font-display text-2xl font-semibold">Yatra Knowledge Base</h1>
        <p className="mt-1 text-sm text-muted">
          Itineraries, calendar, temples and vendor rates for the Yatra Department
        </p>
      </div>

      <Card className="space-y-4">
        <Button className="w-full" size="lg" variant="outline" onClick={() => signInWithGoogle().catch(setError)}>
          Continue with Google
        </Button>

        <div className="flex items-center gap-3 text-xs text-muted">
          <span className="h-px flex-1 bg-border" /> or <span className="h-px flex-1 bg-border" />
        </div>

        {sent ? (
          <p className="rounded-xl bg-ok/10 px-4 py-3 text-sm text-ok">
            Check {email} for a sign-in link.
          </p>
        ) : (
          <form onSubmit={onSubmit} className="space-y-3">
            <Input
              type="email"
              required
              autoComplete="email"
              inputMode="email"
              placeholder="you@hkmhyderabad.org"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <Button type="submit" className="w-full" size="lg" disabled={busy}>
              {busy ? 'Sending…' : 'Email me a sign-in link'}
            </Button>
          </form>
        )}

        {error != null && <ErrorNote error={error} />}
      </Card>

      <p className="mt-6 text-center text-xs text-muted">
        New accounts start as Yatri. An administrator grants staff access.
      </p>
    </div>
  )
}
