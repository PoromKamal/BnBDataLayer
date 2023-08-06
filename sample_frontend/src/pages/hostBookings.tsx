import React, { useEffect } from "react"
import Select from 'react-select'
export default function HostBooking(){

  return (
    <div className='w-full flex flex-col items-center gap-2 p-10'>
      <h1>Your Bookings</h1>
      <a href="/hostDashboard"
        className="border-solid border-2 rounded-md p-1">Back to Dashboard</a>
      <div>
        {}
      </div>
    </div>
  )
}