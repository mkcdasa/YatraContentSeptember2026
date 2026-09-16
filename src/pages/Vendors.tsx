import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Check, Mail, MapPin, Phone, Store } from 'lucide-react'
import { Badge, Card, Chip, ChipRow, Empty, ErrorNote, Input, Sheet, SkeletonList } from '@/components/ui'
import { getVendor, listRates, listVendors } from '@/data/vendors'
import { useDebounced } from '@/hooks/useDebounced'
import { VENDOR_KIND_LABELS, inr } from '@/lib/utils'
import type { VendorKind } from '@/types/db'

const KINDS: VendorKind[] = ['hotel', 'dmc', 'helicopter', 'airline', 'transport', 'permit', 'insurance']

export default function Vendors() {
  const [search, setSearch] = useState('')
  const [kind, setKind] = useState<VendorKind>()
  const [openId, setOpenId] = useState<string>()
  const debounced = useDebounced(search)

  const q = useQuery({
    queryKey: ['vendors', debounced, kind],
    queryFn: () => listVendors({ search: debounced || undefined, kind }),
  })

  return (
    <div className="space-y-4">
      <div>
        <h1 className="font-display text-2xl font-semibold">Vendors</h1>
        <p className="text-sm text-muted">Contacts and negotiated rates. Staff only.</p>
      </div>

      <Input
        placeholder="Search vendors"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        aria-label="Search vendors"
      />

      <ChipRow>
        <Chip active={!kind} onClick={() => setKind(undefined)}>All</Chip>
        {KINDS.map((k) => (
          <Chip key={k} active={kind === k} onClick={() => setKind(kind === k ? undefined : k)}>
            {VENDOR_KIND_LABELS[k]}
          </Chip>
        ))}
      </ChipRow>

      {q.isError && <ErrorNote error={q.error} />}

      {q.isLoading ? (
        <SkeletonList rows={5} />
      ) : q.data?.length ? (
        <ul className="space-y-2">
          {q.data.map((v) => (
            <li key={v.id}>
              <button onClick={() => setOpenId(v.id)} className="w-full text-left">
                <Card className="p-3">
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                      <p className="truncate font-medium">{v.name}</p>
                      <p className="truncate text-xs text-muted">
                        {[VENDOR_KIND_LABELS[v.kind], v.city].filter(Boolean).join(' · ')}
                      </p>
                    </div>
                    {v.is_preferred && <Badge tone="ok">Preferred</Badge>}
                  </div>
                </Card>
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <Empty
          icon={<Store size={28} />}
          title="No vendors yet"
          hint="Add hotels, DMCs and helicopter operators with their negotiated rates."
        />
      )}

      <VendorSheet id={openId} onClose={() => setOpenId(undefined)} />
    </div>
  )
}

function VendorSheet({ id, onClose }: { id?: string; onClose: () => void }) {
  const vendor = useQuery({ queryKey: ['vendor', id], queryFn: () => getVendor(id!), enabled: !!id })
  const rates = useQuery({ queryKey: ['rates', id], queryFn: () => listRates(id!), enabled: !!id })
  const v = vendor.data

  return (
    <Sheet open={!!id} onClose={onClose} title={v?.name ?? 'Vendor'}>
      {!v ? (
        <SkeletonList rows={2} />
      ) : (
        <div className="space-y-4">
          <div className="flex flex-wrap gap-1.5">
            <Badge tone="primary">{VENDOR_KIND_LABELS[v.kind]}</Badge>
            {v.is_preferred && <Badge tone="ok">Preferred</Badge>}
            {v.rating != null && <Badge tone="accent">{v.rating}★</Badge>}
          </div>

          {v.contact_person && <p className="text-sm">{v.contact_person}</p>}

          <div className="grid gap-2">
            {v.phone && <ContactRow icon={<Phone size={15} />} href={`tel:${v.phone}`} text={v.phone} />}
            {v.alt_phone && <ContactRow icon={<Phone size={15} />} href={`tel:${v.alt_phone}`} text={v.alt_phone} />}
            {v.email && <ContactRow icon={<Mail size={15} />} href={`mailto:${v.email}`} text={v.email} />}
            {v.map_url && <ContactRow icon={<MapPin size={15} />} href={v.map_url} text="Open in Maps" external />}
          </div>

          {v.notes && <p className="whitespace-pre-line text-sm text-muted">{v.notes}</p>}

          <div>
            <h4 className="mb-2 font-semibold">Rates</h4>
            {rates.data?.length ? (
              <ul className="space-y-2">
                {rates.data.map((r) => (
                  <li key={r.id}>
                    <Card className="p-3">
                      <div className="flex items-start justify-between gap-3">
                        <p className="flex-1 text-sm">{r.service}</p>
                        <div className="text-right">
                          <p className="font-semibold tabular-nums">{inr(r.rate)}</p>
                          <p className="text-[11px] text-muted">{r.unit}</p>
                        </div>
                      </div>
                      <div className="mt-2 flex flex-wrap items-center gap-2">
                        {r.is_final && <Badge tone="ok"><Check size={11} /> Negotiated</Badge>}
                        {r.valid_to && <Badge>valid to {r.valid_to}</Badge>}
                      </div>
                      {r.terms && <p className="mt-2 text-xs text-muted">{r.terms}</p>}
                    </Card>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-muted">No rates recorded.</p>
            )}
          </div>
        </div>
      )}
    </Sheet>
  )
}

function ContactRow({
  icon, href, text, external,
}: {
  icon: React.ReactNode; href: string; text: string; external?: boolean
}) {
  return (
    <a
      href={href}
      {...(external ? { target: '_blank', rel: 'noreferrer' } : {})}
      className="tap flex items-center gap-2 rounded-xl bg-surface-2 px-3 text-sm font-medium text-primary"
    >
      {icon} {text}
    </a>
  )
}
