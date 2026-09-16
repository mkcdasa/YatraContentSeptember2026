import { Suspense, lazy, type ReactNode } from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import { AppShell } from '@/components/app/AppShell'
import { useAuth } from '@/hooks/useAuth'
import { Skeleton, SkeletonList } from '@/components/ui'

// Home and the shell load eagerly; everything else splits. On a 3G connection
// in a hill station this is the difference between a usable app and a spinner.
import Home from '@/pages/Home'

const Login = lazy(() => import('@/pages/Login'))
const Yatras = lazy(() => import('@/pages/Yatras'))
const YatraDetail = lazy(() => import('@/pages/YatraDetail'))
const CalendarPage = lazy(() => import('@/pages/CalendarPage'))
const Explore = lazy(() => import('@/pages/Explore'))
const DestinationDetail = lazy(() => import('@/pages/DestinationDetail'))
const More = lazy(() => import('@/pages/More'))
const Vendors = lazy(() => import('@/pages/Vendors'))
const Finance = lazy(() => import('@/pages/Finance'))
const Library = lazy(() => import('@/pages/Library'))
const ArticlePage = lazy(() => import('@/pages/Library').then((m) => ({ default: m.ArticlePage })))
const Videos = lazy(() => import('@/pages/Videos'))
const Profile = lazy(() => import('@/pages/Profile'))
const People = lazy(() => import('@/pages/People'))
const SearchPage = lazy(() => import('@/pages/SearchPage'))
const NotFound = lazy(() => import('@/pages/NotFound'))

const Loading = () => (
  <div className="space-y-3">
    <Skeleton className="h-10" />
    <SkeletonList rows={3} />
  </div>
)

export function AppRoutes() {
  const { session, initializing } = useAuth()

  // Wait for the stored session before deciding. Redirecting first and
  // correcting later would drop the path a shared link was pointing at.
  if (initializing) {
    return (
      <div className="mx-auto max-w-2xl space-y-3 p-4">
        <Skeleton className="h-10" />
        <Skeleton className="h-40" />
        <Skeleton className="h-40" />
      </div>
    )
  }

  if (!session) {
    return (
      <Suspense fallback={<Loading />}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Suspense>
    )
  }

  return (
    <Routes>
      <Route path="/login" element={<Navigate to="/" replace />} />
      <Route element={<AppShell />}>
        <Route index element={<Home />} />
        <Route path="yatras" element={<Lazy><Yatras /></Lazy>} />
        <Route path="yatras/:slug" element={<Lazy><YatraDetail /></Lazy>} />
        <Route path="calendar" element={<Lazy><CalendarPage /></Lazy>} />
        <Route path="explore" element={<Lazy><Explore /></Lazy>} />
        <Route path="explore/:slug" element={<Lazy><DestinationDetail /></Lazy>} />
        <Route path="search" element={<Lazy><SearchPage /></Lazy>} />
        <Route path="more" element={<Lazy><More /></Lazy>} />
        <Route path="library" element={<Lazy><Library /></Lazy>} />
        <Route path="library/:slug" element={<Lazy><ArticlePage /></Lazy>} />
        <Route path="videos" element={<Lazy><Videos /></Lazy>} />
        {/* Staff and admin screens are also protected by RLS; these guards only
            keep the UI tidy for a yatri who guesses the URL. */}
        <Route path="vendors" element={<StaffRoute><Vendors /></StaffRoute>} />
        <Route path="finance" element={<StaffRoute><Finance /></StaffRoute>} />
        <Route path="admin/people" element={<AdminRoute><People /></AdminRoute>} />
        <Route path="profile" element={<Lazy><Profile /></Lazy>} />
        <Route path="*" element={<Lazy><NotFound /></Lazy>} />
      </Route>
    </Routes>
  )
}

const Lazy = ({ children }: { children: ReactNode }) => (
  <Suspense fallback={<Loading />}>{children}</Suspense>
)

function StaffRoute({ children }: { children: ReactNode }) {
  const { isStaff, loading } = useAuth()
  if (loading) return <Loading />
  return isStaff ? <Lazy>{children}</Lazy> : <Navigate to="/" replace />
}

function AdminRoute({ children }: { children: ReactNode }) {
  const { isAdmin, loading } = useAuth()
  if (loading) return <Loading />
  return isAdmin ? <Lazy>{children}</Lazy> : <Navigate to="/" replace />
}
