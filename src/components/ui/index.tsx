import { cva, type VariantProps } from 'class-variance-authority'
import { X } from 'lucide-react'
import {
  forwardRef, useEffect, type ButtonHTMLAttributes, type HTMLAttributes,
  type InputHTMLAttributes, type ReactNode,
} from 'react'
import { cn } from '@/lib/utils'

/* ------------------------------------------------------------------ Button */

const buttonStyles = cva(
  'tap inline-flex items-center justify-center gap-2 rounded-xl font-medium transition-colors disabled:opacity-50 disabled:pointer-events-none',
  {
    variants: {
      variant: {
        primary: 'bg-primary text-primary-fg hover:opacity-90 active:opacity-80',
        secondary: 'bg-surface-2 text-fg hover:bg-border',
        outline: 'border border-border bg-surface text-fg hover:bg-surface-2',
        ghost: 'text-fg hover:bg-surface-2',
        danger: 'bg-danger text-white hover:opacity-90',
      },
      size: {
        sm: 'h-9 px-3 text-sm min-h-0',
        md: 'h-11 px-4 text-sm',
        lg: 'h-12 px-5 text-base',
        icon: 'h-11 w-11 p-0',
      },
    },
    defaultVariants: { variant: 'primary', size: 'md' },
  },
)

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonStyles> {}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => (
    <button ref={ref} className={cn(buttonStyles({ variant, size }), className)} {...props} />
  ),
)
Button.displayName = 'Button'

/* -------------------------------------------------------------------- Card */

export const Card = ({ className, ...props }: HTMLAttributes<HTMLDivElement>) => (
  <div className={cn('card p-4', className)} {...props} />
)

export const SectionTitle = ({ children, action }: { children: ReactNode; action?: ReactNode }) => (
  <div className="flex items-baseline justify-between gap-3 mb-3">
    <h2 className="text-lg font-semibold">{children}</h2>
    {action}
  </div>
)

/* ------------------------------------------------------------------- Badge */

const badgeStyles = cva('inline-flex items-center gap-1 rounded-full font-medium', {
  variants: {
    tone: {
      neutral: 'bg-surface-2 text-muted',
      primary: 'bg-primary/10 text-primary',
      accent: 'bg-accent/15 text-accent-fg dark:text-accent',
      ok: 'bg-ok/12 text-ok',
      warn: 'bg-warn/15 text-warn',
      danger: 'bg-danger/12 text-danger',
    },
    size: { sm: 'px-2 py-0.5 text-[11px]', md: 'px-2.5 py-1 text-xs' },
  },
  defaultVariants: { tone: 'neutral', size: 'sm' },
})

export interface BadgeProps
  extends HTMLAttributes<HTMLSpanElement>, VariantProps<typeof badgeStyles> {}

export const Badge = ({ className, tone, size, ...props }: BadgeProps) => (
  <span className={cn(badgeStyles({ tone, size }), className)} {...props} />
)

/* -------------------------------------------------------------------- Chip */

export function Chip({
  active, children, onClick, className,
}: {
  active?: boolean; children: ReactNode; onClick?: () => void; className?: string
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      className={cn(
        'shrink-0 rounded-full border px-3 py-1.5 text-sm font-medium transition-colors',
        active
          ? 'border-primary bg-primary text-primary-fg'
          : 'border-border bg-surface text-muted hover:text-fg',
        className,
      )}
    >
      {children}
    </button>
  )
}

/** Horizontally scrolling filter row — the pattern every travel app converges on. */
export const ChipRow = ({ children, className }: { children: ReactNode; className?: string }) => (
  <div className={cn('hide-scrollbar -mx-4 flex gap-2 overflow-x-auto px-4 pb-1', className)}>
    {children}
  </div>
)

/* ------------------------------------------------------------------- Input */

export const Input = forwardRef<HTMLInputElement, InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => (
    <input
      ref={ref}
      className={cn(
        'h-11 w-full rounded-xl border border-border bg-surface px-3.5 text-base',
        'placeholder:text-muted focus:border-primary focus:outline-none',
        className,
      )}
      {...props}
    />
  ),
)
Input.displayName = 'Input'

/* ---------------------------------------------------------------- Skeleton */

export const Skeleton = ({ className }: { className?: string }) => (
  <div className={cn('relative overflow-hidden rounded-xl bg-surface-2', className)}>
    <div className="absolute inset-0 -translate-x-full animate-shimmer bg-gradient-to-r from-transparent via-black/5 to-transparent dark:via-white/5" />
  </div>
)

export const SkeletonList = ({ rows = 4 }: { rows?: number }) => (
  <div className="space-y-3">
    {Array.from({ length: rows }, (_, i) => (
      <Skeleton key={i} className="h-24" />
    ))}
  </div>
)

/* ------------------------------------------------------------------- Empty */

export function Empty({ icon, title, hint }: { icon?: ReactNode; title: string; hint?: string }) {
  return (
    <div className="flex flex-col items-center justify-center gap-2 px-6 py-14 text-center">
      {icon && <div className="text-muted">{icon}</div>}
      <p className="font-medium">{title}</p>
      {hint && <p className="max-w-xs text-sm text-muted">{hint}</p>}
    </div>
  )
}

/* ------------------------------------------------------------------- Sheet */

/** Bottom sheet. Phones reach up, not across — details open from the bottom. */
export function Sheet({
  open, onClose, title, children,
}: {
  open: boolean; onClose: () => void; title?: string; children: ReactNode
}) {
  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && onClose()
    document.addEventListener('keydown', onKey)
    const prev = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => {
      document.removeEventListener('keydown', onKey)
      document.body.style.overflow = prev
    }
  }, [open, onClose])

  if (!open) return null
  return (
    <div className="fixed inset-0 z-50 flex items-end justify-center sm:items-center">
      <div
        className="absolute inset-0 bg-black/40"
        onClick={onClose}
        role="presentation"
      />
      <div
        role="dialog"
        aria-modal="true"
        aria-label={title}
        className="relative w-full max-w-lg animate-fade-up rounded-t-3xl bg-surface shadow-pop sm:rounded-3xl"
        style={{ maxHeight: '85vh' }}
      >
        <div className="flex items-center justify-between border-b border-border px-4 py-3">
          <h3 className="font-semibold">{title}</h3>
          <button onClick={onClose} aria-label="Close" className="tap -mr-2 grid place-items-center rounded-full">
            <X size={20} />
          </button>
        </div>
        <div
          className="overflow-y-auto px-4 py-4"
          style={{ maxHeight: 'calc(85vh - 56px)', paddingBottom: 'calc(1rem + env(safe-area-inset-bottom))' }}
        >
          {children}
        </div>
      </div>
    </div>
  )
}

/* -------------------------------------------------------------------- Tabs */

export function Tabs<T extends string>({
  tabs, value, onChange,
}: {
  tabs: { id: T; label: string; hidden?: boolean }[]
  value: T
  onChange: (id: T) => void
}) {
  const visible = tabs.filter((t) => !t.hidden)
  return (
    <div role="tablist" className="hide-scrollbar -mx-4 flex gap-1 overflow-x-auto border-b border-border px-4">
      {visible.map((t) => (
        <button
          key={t.id}
          role="tab"
          aria-selected={value === t.id}
          onClick={() => onChange(t.id)}
          className={cn(
            'shrink-0 border-b-2 px-3 py-3 text-sm font-medium transition-colors',
            value === t.id
              ? 'border-primary text-primary'
              : 'border-transparent text-muted hover:text-fg',
          )}
        >
          {t.label}
        </button>
      ))}
    </div>
  )
}

/* --------------------------------------------------------------- Stat tile */

export function Stat({
  label, value, hint, tone = 'neutral',
}: {
  label: string; value: ReactNode; hint?: string; tone?: 'neutral' | 'ok' | 'warn' | 'danger'
}) {
  const toneClass = {
    neutral: 'text-fg', ok: 'text-ok', warn: 'text-warn', danger: 'text-danger',
  }[tone]
  return (
    <div className="card p-3">
      <p className="text-xs text-muted">{label}</p>
      <p className={cn('mt-0.5 font-display text-xl font-semibold tabular-nums', toneClass)}>{value}</p>
      {hint && <p className="mt-0.5 text-[11px] text-muted">{hint}</p>}
    </div>
  )
}

/**
 * Supabase rejects with a plain `PostgrestError` object, not an `Error`, so an
 * `instanceof` check alone throws away the only useful part of a failure.
 */
export function errorMessage(error: unknown): string {
  if (error == null) return 'Something went wrong.'
  if (error instanceof Error) return error.message
  if (typeof error === 'string') return error
  if (typeof error === 'object') {
    const e = error as { message?: unknown; details?: unknown; hint?: unknown }
    const parts = [e.message, e.details, e.hint].filter(
      (p): p is string => typeof p === 'string' && p.length > 0,
    )
    if (parts.length) return parts.join(' — ')
  }
  return 'Something went wrong.'
}

export function ErrorNote({ error }: { error: unknown }) {
  return (
    <div className="rounded-xl border border-danger/30 bg-danger/5 px-4 py-3 text-sm text-danger">
      {errorMessage(error)}
    </div>
  )
}
