import React, { useEffect } from "react"
import Select from 'react-select'
export default function HostReviews() {
  const [reviews, setReviews] = React.useState([])
  const [recentRenters, setRecentRenters] = React.useState([])
  useEffect(() => {
    // Fetch all the reviews
  }, [])

  return (
    <div className='w-full flex flex-col items-center gap-2 p-10'>
      <h1>Review a Renter</h1>
      <a href="/hostDashboard"
        className="border-solid border-2 rounded-md p-1">Back to Dashboard</a>
      
      <div>
        Review a Recent Renter:
      </div>
      <form className="flex flex-col items-center gap-2 p-10">
        <input className="border-solid border-2 rounded-md" placeholder='Rating'/>
        <input className="border-solid border-2 rounded-md" placeholder='Comment'/>
      </form>

      <div>
        {}
      </div>
    </div>
  )
}