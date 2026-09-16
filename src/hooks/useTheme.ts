import { useCallback, useEffect, useState } from 'react'

type Theme = 'light' | 'dark' | 'system'
const KEY = 'yatra-theme'

function read(): Theme {
  try {
    const v = localStorage.getItem(KEY)
    return v === 'light' || v === 'dark' ? v : 'system'
  } catch {
    // private browsing, blocked storage — 'system' is a fine answer
    return 'system'
  }
}

export function useTheme() {
  const [theme, setThemeState] = useState<Theme>(read)

  useEffect(() => {
    const root = document.documentElement
    if (theme === 'system') root.removeAttribute('data-theme')
    else root.setAttribute('data-theme', theme)
    try {
      if (theme === 'system') localStorage.removeItem(KEY)
      else localStorage.setItem(KEY, theme)
    } catch {
      /* not worth surfacing */
    }
  }, [theme])

  const setTheme = useCallback((next: Theme) => setThemeState(next), [])
  return { theme, setTheme }
}
