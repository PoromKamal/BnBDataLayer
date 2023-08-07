import React, { useEffect, useState } from 'react'
export default function HostDashboard(){
    const [username, setUsername] = useState('')
    function handleLogout () {
      localStorage.removeItem('userId')
      localStorage.removeItem('role')
      window.location.href = '/login'
    }
    
    function handleDeleteAccount(){
      const hostId = localStorage.getItem('userId')
      localStorage.removeItem('userId')
      localStorage.removeItem('role')
      fetch("http://localhost:5000/deleteHost", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          hostId: hostId,
        }),
      }).then((res) => {
        if (res.status === 200) {
          alert("Account deleted successfully");
          window.location.href = "/login";
        } else {
          alert("Error deleting account");
        }
      });
    }

    return (
      <div className='w-full flex flex-col items-center gap-2 p-10'>
      <h1>Welcome {username}</h1>
        <a href="/hostListings"
          className="border-solid border-2 rounded-md p-1">My Listings</a>
        <a href="/hostReviews"
          className="border-solid border-2 rounded-md p-1">My Reviews</a>
        <button onClick={() => {handleLogout()}}
          className="border-solid border-2 rounded-md p-1">Logout</button>
        <button onClick={() => {handleDeleteAccount()}}
          className="border-solid border-2 rounded-md p-1">Delete Profile</button>
      </div>
    )
}