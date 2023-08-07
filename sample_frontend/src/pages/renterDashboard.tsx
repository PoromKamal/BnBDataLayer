import React, { useEffect, useState } from 'react'
import Select from 'react-select'
export default function RenterDashboard(){
    const [username, setUsername] = useState('')
    const [searchType, setSearchType] = useState('')
    const [longitude, setLongitude] = useState('')
    const [latitude, setLatitude] = useState('')
    const [postalCode, setPostalCode] = useState('')
    const [streetAddress, setStreetAddress] = useState('')
    const [city, setCity] = useState('')
    const [country, setCountry] = useState('')
    const searchTypes = [
      {value: "LongLat", label: "Longitude, Latitude"},
      {value: "PostalCode", label: "Postal Code"},
      {value:"Address", label: "Address"}
    ]
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

    function handleChangeSearchType(newValue: any, actionMeta: any) {
      if(newValue) {
        setSearchType(newValue.value)
      }
    }

    function handleSearchLongLat(){
      console.log('searching')
    }

    function handleSearchPostal(){
      console.log('searching')
    }

    function handleSearchAddress(){
      console.log('searching')
    }

    function renderSearch(){
      if(searchType == 'LongLat'){
        return (
          <div className='flex flex-col gap-1'>
            <label htmlFor="longitude">Longitude: </label>
            <input onChange={e => setLongitude(e.target.value)}
              required className="border-solid border-2 rounded-md" placeholder='Longitude'/>
            <label htmlFor="latitude">Latitude: </label>
            <input onChange={e => setLatitude(e.target.value)}
              required className="border-solid border-2 rounded-md" placeholder='Latitude'/>
            <button className="border-solid border-2 rounded-md p-1 bg-gray-500"
              onClick={() => {handleSearchLongLat()}}>Search</button>
          </div>
        )
      }
      else if(searchType == 'PostalCode'){
        return (<div className='flex flex-col gap-1'>
          <label htmlFor="postalCode">Postal Code: </label>
          <input onChange={e => setPostalCode(e.target.value)}
            required className="border-solid border-2 rounded-md" placeholder='Postal Code'/>
          <button className="border-solid border-2 rounded-md p-1 bg-gray-500"
            onClick={() => {handleSearchPostal()}}>Search</button>
        </div>)
      }
      else if(searchType == 'Address'){
        return(<div className='flex flex-col gap-1'>
          <label htmlFor="address">Street Addres: </label>
          <input onChange={e => setStreetAddress(e.target.value)}
            className="border-solid border-2 rounded-md"/>
          <label htmlFor="city">City: </label>
          <input onChange={e => setCity(e.target.value)}
            className="border-solid border-2 rounded-md"/>
          <label htmlFor="country">Country: </label>
          <input onChange={e => setCountry(e.target.value)}
            className="border-solid border-2 rounded-md" />
          <button className="border-solid border-2 rounded-md p-1 bg-gray-500"
            onClick={() => {handleSearchAddress()}}>Search</button>
        </div>)
      }
    }

    function renderFilters(){
      return(
        <div className='flex flex-col items-center gap-1 border-solid 
                      border-black border-2 rounded-md p-3'>
          <div>
            Filters
          </div>
          <div className='flex flex-col gap-1'>
            <label htmlFor="price">Price Range: </label>
            <div className="flex flex-col gap-1">
              <label htmlFor="minPrice">Min: </label>
              <input className="border-solid border-2 rounded-md" placeholder='Min Price'/>
              <label htmlFor="maxPrice">Max: </label>
              <input className="border-solid border-2 rounded-md" placeholder='Max Price'/>
            </div>
          </div>
          <div>
            <label htmlFor="rating">Rating: </label>
          </div>
          <div>
            <label htmlFor="amenities">Amenities: </label>
          </div>
          <div>
            <label>Date Range: </label>
            <div className='className="flex flex-col gap-1"'>
              <div>
                <label htmlFor="startDate">Start: </label>
                <input type="date" className="border-solid border-2 rounded-md" placeholder='Start Date'/>
              </div>
              <div>
                <label htmlFor="endDate">End: </label>
                <input type="date" className="border-solid border-2 rounded-md" placeholder='End Date'/>
              </div>
            </div>
          </div>
        </div>
      )
    }


    return (
      <div className='w-full flex flex-col items-center gap-2 p-10'>
        <h1>Welcome {username}</h1>
        <div className='flex justify-center gap-10'>
          <div className="flex flex-col gap-1 border-solid 
          border-black border-2 rounded-md p-2">
            Search:
            <div>
              <Select onChange={handleChangeSearchType}
              options={searchTypes}/>
              {
                renderSearch()
              }
            </div>
          </div>

          <div>
            {
              renderFilters()
            }
          </div>
        </div>


        Results:
        <div>

        </div>

        <button onClick={() => {handleLogout()}}
          className="border-solid border-2 rounded-md p-1">Logout</button>
        <button onClick={() => {handleDeleteAccount()}}
          className="border-solid border-2 rounded-md p-1">Delete Profile</button>
      </div>
    )
}