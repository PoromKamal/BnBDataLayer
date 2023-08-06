import React, { useEffect } from "react"
import Select from 'react-select'
export default function HostListings() {
  const [listings, setListings] = React.useState([])
  const [streetAddress, setStreetAddress] = React.useState('')
  const [city, setCity] = React.useState('')
  const [country, setCountry] = React.useState('')
  const [postalCode, setPostalCode] = React.useState('')
  const [longitude, setLongitude] = React.useState('')
  const [latitude, setLatitude] = React.useState('')
  const [price, setPrice] = React.useState('')
  
  useEffect(() => {
    // Fetch all the listings
    const fetchData = async () => {
      const userId = localStorage.getItem('userId')
      const listingData = await fetch('http://localhost:5000/getAllListings?hostId=' 
                                + userId)
      const listingJson = await listingData.json()
      setListings(listingJson.listings)
    }
    fetchData()
  }, [])

  const handleNavigateToListing = async (listingId: string) => {
    localStorage.setItem('listingId', listingId)
    // Pass in amenities here
    const amenityData = await fetch('http://localhost:5000/getAmenitiesByListingId?id='
                              + listingId)
    const amenityJson = await amenityData.json()
    localStorage.setItem('amenities', JSON.stringify(amenityJson.amenities))
    window.location.href = '/listing'
  }

  const handleAddListing = async () => {
    const userId = localStorage.getItem('userId')
    const listingData = await fetch('http://localhost:5000/insertListing', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          hostId: userId,
          address: streetAddress,
          city: city,
          country: country,
          postalCode: postalCode,
          longitude: longitude,
          latitude: latitude,
          price: price
          })
        })
    const listingJson = await listingData.json()
    console.log(listingJson)
    if(!listingJson.success){
      alert('Error adding listing')
      return
    }
    alert('Listing added successfully')
    setStreetAddress('')
    setCity('')
    setCountry('')
    setPostalCode('')
    setLongitude('')
    setLatitude('')
    setPrice('')

    // Refetch listings
    const listings = await fetch('http://localhost:5000/getAllListings?hostId='
                              + userId)
    const listingsJson = await listings.json()
    setListings(listingsJson.listings)
  }

  const listingCard = (listingId: string, address: string,
    city: string, country: string, postalCode: string, longitude: string,
    latitude: string, price: string) =>
    (
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
      </div>
      )
  
  return (
    <div className='w-full flex flex-col items-center gap-2 p-10'>
      <h1>Your Listings</h1>
      <a href="/hostDashboard"
        className="border-solid border-2 rounded-md p-1">Back to Dashboard</a>
      
      <div>
        Add a new listing:
      </div>
      <form onSubmit={(e) => {e.preventDefault(); handleAddListing()}}
        className="flex flex-col items-center gap-2 mb-10">
        <input value={streetAddress} onChange={(e) => setStreetAddress(e.target.value)}
          className="border-solid border-2 rounded-md" placeholder='Street Address'/>
        <input value={city} onChange={(e) => setCity(e.target.value)}
          className="border-solid border-2 rounded-md" placeholder='City'/>
        <input value={country} onChange={(e) => setCountry(e.target.value)}
          className="border-solid border-2 rounded-md" placeholder='Country'/>
        <input value={postalCode} onChange={(e) => setPostalCode(e.target.value)}
          className="border-solid border-2 rounded-md" placeholder='Postal Code'/>
        <input value={longitude} onChange={(e) => setLongitude(e.target.value)}
          className="border-solid border-2 rounded-md" placeholder='Longitude'/>
        <input value={latitude} onChange={(e) => setLatitude(e.target.value)}
          className="border-solid border-2 rounded-md" placeholder='Latitude'/>
        <input value={price} onChange={(e) => setPrice(e.target.value)}
          className="border-solid border-2 rounded-md" placeholder='Price'/>
        <button type="submit" className="border-solid border-2 rounded-md p-1">Add Listing</button>
      </form>

      <div className="flex flex-col gap-2">
        Your listings (Click to view and edit):
        {listings.map((listing: any) => listingCard(listing.id, listing.address,
          listing.city, listing.country, listing.postalCode, listing.longitude,
          listing.latitude, listing.price))}
      </div>
    </div>
  )
}