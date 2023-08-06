import React, { useEffect, useState } from 'react'
export default function HostDashboard(){
    const [username, setUsername] = useState('')
    useEffect(() => {
      
    }, [])
    function handleLogout () {
      localStorage.removeItem('userId')
      localStorage.removeItem('role')
      window.location.href = '/login'
    }
    return (
      <div className='w-full flex flex-col items-center gap-2 p-10'>
      <h1>Welcome {username}</h1>
        <a href="/hostListings"
          className="border-solid border-2 rounded-md p-1">My Listings</a>
        <a href="/hostBookings"
          className="border-solid border-2 rounded-md p-1">My Bookings</a>
        <a className="border-solid border-2 rounded-md p-1">My Reviews</a>
        <button onClick={() => {handleLogout()}}
          className="border-solid border-2 rounded-md p-1">Logout</button>
        <button onClick={() => {handleLogout()}}
          className="border-solid border-2 rounded-md p-1">Delete Profile</button>
      </div>
    )
}