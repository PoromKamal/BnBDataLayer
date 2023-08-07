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
    const [radius, setRadius] = useState('')
    const [order, setOrder] = useState('ascending')
    const [filters, setFilter] = useState({ minPrice: '', maxPrice: '', 
    rating: '', amenities: '', startDate: '', endDate: '', postalCode: '' })
    const [orderBy, setOrderBy] = useState('')
    const [searchResults, setSearchResults] = useState([])


    useEffect(() => {
      //TODO: Initialize search results with every listing

    }, [])

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
      const renterId = localStorage.getItem('userId')
      localStorage.removeItem('userId')
      localStorage.removeItem('role')
      fetch("http://localhost:5000/deleteRenter", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({renterId}),
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

    function generate_filters(){
      let url = ''

      if(filters.postalCode != '' && searchType != 'PostalCode'){
        url += '&postalCode=' + filters.postalCode
      }

      if(filters.minPrice != ''){
        url += '&minPrice=' + filters.minPrice
      }

      if(filters.maxPrice != ''){
        url += '&maxPrice=' + filters.maxPrice
      }

      if(filters.rating != ''){
        url += '&minRating=' + filters.rating
      }

      if(filters.amenities != ''){
        url += '&amenities='
        for(let i = 0; i < filters.amenities.length; i++){
          url += filters.amenities[i] + ','
        }
        url = url.substring(0, url.length - 1)
      }

      if(filters.startDate != ''){
        url += '&startDate=' + filters.startDate
      }

      if(filters.endDate != ''){
        url += '&endDate=' + filters.endDate
      }
      
      if(order != ''){
        url += '&order=' + order
      }

      if(searchType == "LongLat" && orderBy != ''){
        url += '&orderBy=' + orderBy
      }

      return url
    }

    async function handleSearchByPostal(){
      // Check if all fields are filled
      if(postalCode == '') {
        alert('Please fill in all fields')
        return
      }

      let url = 'http://localhost:5000/searchByPostalCode?postalCode=' + postalCode
      + generate_filters()
      
      const searchResults = await fetch(url)
      const searchResultsJson = await searchResults.json()
      console.log(searchResultsJson)
      setSearchResults(searchResultsJson.results)
    }

    async function handleSearchLongLat(){
      // Check if all fields are filled
      if(longitude == '' || latitude == '' || radius == ''){
        alert('Please fill in all fields')
        return
      }

      let url = 'http://localhost:5000/searchByLongLat?longitude=' 
      + longitude + '&latitude=' + latitude + '&radius=' + radius
      + generate_filters()
      
      const searchResults = await fetch(url)
      const searchResultsJson = await searchResults.json()
      setSearchResults(searchResultsJson.results)
    }

    async function handleSearchByAddress(){

      let url = 'http://localhost:5000/searchByAddress?streetAddress='
      + streetAddress + '&city=' + city + '&country=' + country
      + generate_filters()

      const searchResults = await fetch(url)
      const searchResultsJson = await searchResults.json()
      setSearchResults(searchResultsJson.results)
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
            <label htmlFor="radius">Radius: </label>
            <input onChange={e => setRadius(e.target.value)}
              required className="border-solid border-2 rounded-md" placeholder='Radius KM'/>
            <button className="border-solid border-2 rounded-md p-1 bg-gray-500"
              onClick={() => {handleSearchLongLat()}}>Search</button>
          </div>
        )
      }
      else if(searchType == 'PostalCode'){
        return (<div className='flex flex-col gap-1'>
          <label htmlFor="postalCode">Postal Code: </label>
          <input  value = {postalCode}
            onChange={e => setPostalCode(e.target.value)}
            required className="border-solid border-2 rounded-md" placeholder='Postal Code'/>
          <button className="border-solid border-2 rounded-md p-1 bg-gray-500"
            onClick={() => {handleSearchByPostal()}}>Search</button>
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
            onClick={() => {handleSearchByAddress()}}>Search</button>
        </div>)
      }
    }

    const handleNavigateToListing = (listingId: string) => {
      // TODO: Navigate to listing page
    }

    const ListingCard = (address: string , city: string, country: string, 
      postalCode:string, longitude: string, latitude: string, 
      price:string, listingId:string, distance: string) => (
      <div className="flex flex-col border-solid 
                      rounded-md border-black border-2
                      cursor-pointer"
          onClick={()=>{handleNavigateToListing(listingId)}}>
        <div>
          Address: {address}
        </div>
        <div className="flex gap-2 p-1">
          <div>
            City: {city}
          </div>
          <div>
            Country: {country}
          </div>
          <div>
            Postal Code: {postalCode}
          </div>
        </div>
        <div className="flex gap-2 p-1">
            <div>
              Longitude: {longitude}
            </div>
            <div>
              Latitude: {latitude}
            </div>
            <div>
              Price: {price}
            </div>
        </div>
        {
          searchType == "LongLat" &&
            <div>
            Distance: {distance} km
            </div>
        }
      </div>
    )
      

    function handleClearFilters(){
      setFilter({ minPrice: '', maxPrice: '',
      rating: '', amenities: '', startDate: '', endDate: '', postalCode: '' })
    }

    function renderFilters(){
      return(
        <div className='flex flex-col items-center gap-1 border-solid 
                      border-black border-2 rounded-md p-3'>
          <div>
            Filters
          </div>
          {
            searchType != "PostalCode" &&
            (
            <div className="flex flex-col">
              <label htmlFor="postalCode">Postal: </label>
              <input value = {filters.postalCode} onChange={e => setFilter({...filters, postalCode: e.target.value})}
                className="border-solid border-2 rounded-md" placeholder='Postal Code'/>
            </div>
            )
          }
          <div className='flex flex-col gap-1'>
            <div className="flex flex-col gap-1">
              <label htmlFor="minPrice">Min: </label>
              <input value = {filters.minPrice} onChange={e => setFilter({...filters, minPrice: e.target.value})}
                className="border-solid border-2 rounded-md" placeholder='Min Price'/>
              <label htmlFor="maxPrice">Max: </label>
              <input value = {filters.maxPrice} onChange={e => setFilter({...filters, maxPrice: e.target.value})}
                className="border-solid border-2 rounded-md" placeholder='Max Price'/>
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
                <input value = {filters.startDate} onChange={e => setFilter({...filters, startDate: e.target.value})}
                  type="date" className="border-solid border-2 rounded-md" placeholder='Start Date'/>
              </div>
              <div>
                <label htmlFor="endDate">End: </label>
                <input value = {filters.endDate} onChange={e => setFilter({...filters, endDate: e.target.value})}
                  type="date" className="border-solid border-2 rounded-md" placeholder='End Date'/>
              </div>
            </div>
          </div>
            {
              searchType == "LongLat" &&
              (
                <div>
                  <label htmlFor="order">Order By </label>
                  <div className="flex gap-2">
                    <input onChange = {e => setOrderBy(e.target.value)}
                    type="radio" id="distance" name="orderBy" value="distance"/>
                    <label htmlFor="distance">distance</label>
                    <input onChange = {e => setOrderBy(e.target.value)}
                      type="radio" id="price" name="orderBy" value="price"/>
                    <label htmlFor="price">price</label>
                  </div>
                </div>
              )
            }
          <div>
            <label htmlFor="order">Order </label>
            <div className="flex gap-2">
              <input onChange = {e => setOrder(e.target.value)}
              type="radio" id="ascending" name="order" value="ascending"/>
              <label htmlFor="ascending">ascending</label>
              <input onChange = {e => setOrder(e.target.value)}
                type="radio" id="descending" name="order" value="descending"/>
              <label htmlFor="descending">descending</label>
            </div>
          </div>
          <div>
            <button onClick={() => {handleClearFilters()}}
              className="border-solid border-2 rounded-md p-1 bg-gray-500">
              Clear Filters
            </button>
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
        <div className="flex flex-col gap-2 h-1/3 overflow-scroll">
            {
              searchResults.map((listing: any) => {
                const distance = searchType == "LongLat" ? 
                                      listing.distance.toFixed(2) : 0
                console.log(listing)
                return ListingCard(listing.address, listing.city, listing.country, 
                  listing.postalCode, listing.longitude, listing.latitude, 
                  listing.price, listing.listingId, distance)
              })
            }
        </div>

        <button onClick={() => {handleLogout()}}
          className="border-solid border-2 rounded-md p-1">Logout</button>
        <button onClick={() => {handleDeleteAccount()}}
          className="border-solid border-2 rounded-md p-1">Delete Profile</button>
      </div>
    )
}