import { supabase } from '@/lib/supabase'
import type { FinanceReport, KnowledgeArticle, Video, VideoKind } from '@/types/db'

export async function listArticles(category?: string): Promise<KnowledgeArticle[]> {
  let q = supabase.from('knowledge_articles').select('*').order('title')
  if (category) q = q.eq('category', category)
  const { data, error } = await q
  if (error) throw error
  return data ?? []
}

export async function getArticle(slug: string): Promise<KnowledgeArticle | null> {
  const { data, error } = await supabase
    .from('knowledge_articles').select('*').eq('slug', slug).maybeSingle()
  if (error) throw error
  return data
}

export async function listVideos(kind?: VideoKind): Promise<Video[]> {
  let q = supabase.from('videos').select('*').order('title')
  if (kind) q = q.eq('kind', kind)
  const { data, error } = await q
  if (error) throw error
  return data ?? []
}

export async function addVideo(input: { title: string; url: string; kind: VideoKind; channel?: string; notes?: string }) {
  const youtube_id = extractYoutubeId(input.url)
  const { error } = await supabase.from('videos').insert({ ...input, youtube_id })
  if (error) throw error
}

export async function deleteVideo(id: string) {
  const { error } = await supabase.from('videos').delete().eq('id', id)
  if (error) throw error
}

export function extractYoutubeId(url: string): string | null {
  const m = url.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|shorts\/))([\w-]{6,})/)
  return m ? m[1] : null
}

/* --- staff tier ----------------------------------------------------------- */

export async function listFinanceReports(): Promise<FinanceReport[]> {
  const { data, error } = await supabase
    .from('finance_reports').select('*').order('created_at', { ascending: false })
  if (error) throw error
  return data ?? []
}

/** Signed URL, because the finance bucket is private. */
export async function financeReportUrl(path: string): Promise<string | null> {
  const { data, error } = await supabase.storage.from('finance').createSignedUrl(path, 300)
  if (error) return null
  return data.signedUrl
}
