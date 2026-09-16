import type { ReactNode } from 'react'
import { useAuth } from '@/hooks/useAuth'

/**
 * Presentation-layer gate. It is not the security boundary — RLS is — but it
 * stops the UI from rendering empty "Negotiated rates" panels to a yatri who
 * would otherwise wonder what they are missing.
 */
export function StaffOnly({ children, fallback = null }: { children: ReactNode; fallback?: ReactNode }) {
  const { isStaff } = useAuth()
  return <>{isStaff ? children : fallback}</>
}

export function AdminOnly({ children, fallback = null }: { children: ReactNode; fallback?: ReactNode }) {
  const { isAdmin } = useAuth()
  return <>{isAdmin ? children : fallback}</>
}
