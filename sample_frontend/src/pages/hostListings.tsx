import React, { useEffect } from "react"
import Select from 'react-select'
export default function HostListings() {
  const [amenities, setAmenities] = React.useState([])
  const [listings, setListings] = React.useState([])
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
      <form className="flex flex-col items-center gap-2 mb-10">
        <input className="border-solid border-2 rounded-md" placeholder='Street Address'/>
        <input className="border-solid border-2 rounded-md" placeholder='City'/>
        <input className="border-solid border-2 rounded-md" placeholder='Country'/>
        <input className="border-solid border-2 rounded-md" placeholder='Postal Code'/>
        <input className="border-solid border-2 rounded-md" placeholder='Longitude'/>
        <input className="border-solid border-2 rounded-md" placeholder='Latitude'/>
        <input className="border-solid border-2 rounded-md" placeholder='Price'/>
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