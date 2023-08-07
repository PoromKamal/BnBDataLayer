import Image from 'next/image'
import { Inter } from 'next/font/google'
import { useEffect } from 'react'

const inter = Inter({ subsets: ['latin'] })

export default function Home() {
  useEffect(() => {
    const userId = localStorage.getItem('userId')
    const role = localStorage.getItem('role')
    if (!(userId || role))
      window.location.href = '/login'
    else if (role === 'host')
      window.location.href = '/hostDashboard'
    else if (role === 'renter')
      window.location.href = '/renterDashboard'
  }, [])

  return (
    <div>
    </div>
  )
}
