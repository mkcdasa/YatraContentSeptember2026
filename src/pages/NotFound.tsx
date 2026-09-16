import { Link } from 'react-router-dom'
import { Button, Empty } from '@/components/ui'

export default function NotFound() {
  return (
    <div className="space-y-4">
      <Empty title="Page not found" hint="The link may be out of date." />
      <Link to="/">
        <Button className="w-full">Back to home</Button>
      </Link>
    </div>
  )
}
