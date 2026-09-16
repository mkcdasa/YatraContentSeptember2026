/**
 * Generates the PWA icons from the brand colour at build time.
 *
 * They are generated rather than committed so the repository stays text-only,
 * which keeps it reviewable in a diff and portable across every transport we
 * push through. Swap this for real artwork by dropping pwa-192.png and
 * pwa-512.png into public/ — this script leaves existing files alone.
 */
import { writeFileSync, existsSync, mkdirSync } from 'node:fs'
import { deflateSync } from 'node:zlib'

const BRAND = [0x7c, 0x2d, 0x12] // hsl(16 72% 28%), the --primary token

function crc32(buf) {
  let c, table = []
  for (let n = 0; n < 256; n++) {
    c = n
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1
    table[n] = c >>> 0
  }
  let crc = 0xffffffff
  for (const b of buf) crc = table[(crc ^ b) & 0xff] ^ (crc >>> 8)
  return (crc ^ 0xffffffff) >>> 0
}

function chunk(type, data) {
  const len = Buffer.alloc(4)
  len.writeUInt32BE(data.length)
  const body = Buffer.concat([Buffer.from(type, 'ascii'), data])
  const crc = Buffer.alloc(4)
  crc.writeUInt32BE(crc32(body))
  return Buffer.concat([len, body, crc])
}

function png(size) {
  const row = Buffer.concat([Buffer.from([0]), Buffer.from(Array(size).fill(BRAND).flat())])
  const raw = Buffer.concat(Array(size).fill(row))
  const ihdr = Buffer.alloc(13)
  ihdr.writeUInt32BE(size, 0)
  ihdr.writeUInt32BE(size, 4)
  ihdr[8] = 8    // bit depth
  ihdr[9] = 2    // colour type: truecolour
  return Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    chunk('IHDR', ihdr),
    chunk('IDAT', deflateSync(raw, { level: 9 })),
    chunk('IEND', Buffer.alloc(0)),
  ])
}

mkdirSync('public', { recursive: true })
for (const size of [192, 512]) {
  const path = `public/pwa-${size}.png`
  if (existsSync(path)) {
    console.log(`kept existing ${path}`)
    continue
  }
  writeFileSync(path, png(size))
  console.log(`generated ${path}`)
}
