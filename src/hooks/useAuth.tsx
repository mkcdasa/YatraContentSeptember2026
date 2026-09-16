import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react'
import type { Session } from '@supabase/supabase-js'
import { supabase } from '@/lib/supabase'
import { getProfile } from '@/data/profile'
import type { AppRole, Profile } from '@/types/db'

interface AuthValue {
  session: Session | null
  profile: Profile | null
  /** True until the stored session has been read from storage. */
  initializing: boolean
  /** True until the profile for the *current* session has been fetched. */
  loading: boolean
  /** admin, staff and tour_leader. The gate for vendors, pricing and margins. */
  isStaff: boolean
  isAdmin: boolean
  role: AppRole | null
  signInWithGoogle: () => Promise<void>
  signInWithEmail: (email: string) => Promise<void>
  signOut: () => Promise<void>
  refreshProfile: () => Promise<void>
}

const AuthContext = createContext<AuthValue | null>(null)

/**
 * The profile is tracked together with the user id it belongs to. Deriving
 * `loading` from that pair rather than from a free-standing boolean is what
 * stops a staff member who opens /vendors directly from being bounced to Home
 * in the instant between the session arriving and the profile landing.
 */
interface ProfileState {
  userId: string | null
  profile: Profile | null
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<Session | null>(null)
  const [initializing, setInitializing] = useState(true)
  const [profileState, setProfileState] = useState<ProfileState>({ userId: null, profile: null })

  useEffect(() => {
    let alive = true

    supabase.auth
      .getSession()
      .then(({ data }) => {
        if (alive) setSession(data.session)
      })
      .finally(() => {
        if (alive) setInitializing(false)
      })

    const { data: sub } = supabase.auth.onAuthStateChange((_event, next) => {
      setSession(next)
    })
    return () => {
      alive = false
      sub.subscription.unsubscribe()
    }
  }, [])

  const userId = session?.user.id ?? null

  useEffect(() => {
    let alive = true
    if (!userId) {
      setProfileState({ userId: null, profile: null })
      return
    }
    getProfile(userId)
      .then((profile) => alive && setProfileState({ userId, profile }))
      // A failed profile read still resolves the pair, otherwise the app hangs
      // on a skeleton forever. RLS always lets a user read their own row, so
      // this is a network failure, not an authorisation one.
      .catch(() => alive && setProfileState({ userId, profile: null }))
    return () => {
      alive = false
    }
  }, [userId])

  const value = useMemo<AuthValue>(() => {
    const resolved = profileState.userId === userId
    const profile = resolved ? profileState.profile : null
    const role = profile?.role ?? null
    return {
      session,
      profile,
      initializing,
      loading: initializing || (userId != null && !resolved),
      role,
      isStaff: role === 'admin' || role === 'staff' || role === 'tour_leader',
      isAdmin: role === 'admin',
      signInWithGoogle: async () => {
        const { error } = await supabase.auth.signInWithOAuth({
          provider: 'google',
          options: { redirectTo: window.location.origin },
        })
        if (error) throw error
      },
      signInWithEmail: async (email: string) => {
        const { error } = await supabase.auth.signInWithOtp({
          email,
          options: { emailRedirectTo: window.location.origin },
        })
        if (error) throw error
      },
      signOut: async () => {
        await supabase.auth.signOut()
        setProfileState({ userId: null, profile: null })
      },
      refreshProfile: async () => {
        if (!userId) return
        setProfileState({ userId, profile: await getProfile(userId) })
      },
    }
  }, [session, userId, profileState, initializing])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside <AuthProvider>')
  return ctx
}
