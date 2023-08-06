import { type } from "os"
import React, { useEffect } from "react"
import Select, { ActionMeta, MultiValue } from 'react-select'
import { ValueType } from "tailwindcss/types/config"

export default function Listing() {
  const [listing, setListing] = React.useState({address: '', city: '', 
  country: '', postalCode: '', longitude: '', latitude: '', price: ''})
  const [amenities, setAmenities] = React.useState([] as { value: any; label: any }[])
  const [allAmenities, setAllAmenities] = React.useState([] as { value: any; label: any }[])
  const [amenitiesLoaded, setAmenitiesLoaded] = React.useState(false)
  const [listingId, setListingId] = React.useState('')
  const [reviews, setReviews] = React.useState([])
  const [bookings, setBookings] = React.useState([])
  const [availabilities, setAvailabilities] = React.useState([])
  const [newAvailability, setNewAvailability] = React.useState({startDate: '', endDate: ''})

  const handleChangeAmenities = (newValue: MultiValue<{ value: any; label: any; }>, 
      actionMeta: ActionMeta<{ value: any; label: any; }>) => {
    // TODO: Update amenities for the listing
  }

  useEffect(() => {

    const fetchData = async () => {
      // Fetch listing data
      const listingId = localStorage.getItem('listingId')
      if(listingId)
        setListingId(listingId)
      const listingData = await fetch('http://localhost:5000/getListingById?id=' 
                                + listingId)
      const listingJson = await listingData.json()
      setListing(listingJson.listing)

      //Fetch amenities
      const amenityData = await fetch('http://localhost:5000/getAmenitiesByListingId?id='
                                + listingId)
      const amenityJson = await amenityData.json()

      //Format amenities for react-select options format
      const currAmenities: { value: any; label: any }[] = []
      
      amenityJson.amenities.forEach((amenity: any) => {
        currAmenities.push({value: amenity.name, label: amenity.name})
      })

      // Get all amenities
      const allAmenityData = await fetch('http://localhost:5000/getAllAmenities')
      const allAmenityJson = await allAmenityData.json()
      console.log(allAmenityJson)
      const newAllAmens: { value: any; label: any }[] = []
      allAmenityJson.amenities.forEach((amenity: any) => {
        newAllAmens.push({value: amenity.name, label: amenity.name}) 
      })
      setAllAmenities(newAllAmens)
      setAmenities(currAmenities)
      setAmenitiesLoaded(true)
    }
    fetchData()
  }, [])

  const renderAmenityDropDown = () => {
    return (
      <div className="m-5">
        <Select
          isMulti
          name="amenities"
          defaultValue={amenities}
          options={allAmenities}
          onChange={handleChangeAmenities}
          className="basic-multi-select"
          classNamePrefix="select"
        />
      </div>
      
    )
  }

  function cancelBooking(bookingId: string) {
    // Process booking cancellation
    
    // Update the bookings state
    const new_bookings = bookings.filter((booking: any) => booking.id !== bookingId)
    setBookings(new_bookings)
  }

  const bookingCard = (bookingId: string, renterUsername: string, 
                    startDate: string, endDate: string, pricePaid: string) => 
  (
    <div className="flex flex-col">
      <div>
        Renter: {renterUsername}
      </div>

      <div className="flex gap-2 p-1">
        <div>
          Start Date: {startDate}
        </div>
        <div>
          End Date: {endDate}
        </div>
      </div>
      <div>
        Price Paid: {pricePaid}
      </div>
      <button onClick={()=>{cancelBooking(bookingId)}} >
        Cancel Booking
      </button>
    </div>
  )

  const handleAddAvailability = async () => {
    // Check start date is before end date
    console.log(newAvailability)
    if(newAvailability.startDate > newAvailability.endDate) {
      alert('Start date must be before end date')
      return
    }

    const sendData = fetch('http://localhost:5000/insertAvailabilities', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({listingId: listingId, 
        startDate: newAvailability.startDate, 
        endDate: newAvailability.endDate})
    })
  }

  return(
    <div className="flex flex-col justify-center items-center">
      Listing details:
      <div className="flex flex-col border-solid 
                      rounded-md border-black border-2 items-center
                      w-2/3">
        <div>
          Address: {listing.address}
        </div>
        <div className="flex gap-2 p-1">
          <div>
            City: {listing.city}
          </div>
          <div>
            Country: {listing.country}
          </div>
          <div>
            Postal Code: {listing.postalCode}
          </div>
        </div>
        <div className="flex gap-2 p-1">
            <div>
              Longitude: {listing.longitude}
            </div>
            <div>
              Latitude: {listing.latitude}
            </div>
            <div>
              Price: {listing.price}
            </div>
        </div>
      </div>

      <div>
        {amenitiesLoaded ? renderAmenityDropDown() : <div>Loading...</div>}
      </div>

      <div>
        Reviews:
      </div>

      <div className="flex flex-col items-center">
        <div className="flex flex-col border-solid border-black 
                        border-2 rounded-md p-2">
          Start Date:
          <input value={newAvailability.startDate}
            onChange={(e) => {setNewAvailability({...newAvailability, startDate: e.target.value})}}
            type="date"/>
          End Date:
          <input value={newAvailability.endDate}
            onChange={(e) => {setNewAvailability({...newAvailability, endDate: e.target.value})}}
            type="date"/>
          <button onClick={handleAddAvailability}
            className="border-solid border-black border-2 rounded-md">
            Add Availability
          </button>
        </div>
        <div>
          All Availabilities
        </div>
      </div>

      <div>
        Bookings:
      </div>

    </div>)

}
