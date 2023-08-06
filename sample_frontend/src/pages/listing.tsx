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

  const handleChangeAmenities = async (newValue: MultiValue<{ value: any; label: any; }>, 
      actionMeta: ActionMeta<{ value: any; label: any; }>) => {

    console.log(newValue[newValue.length-1].value)
    console.log(actionMeta.action)
    if(actionMeta.action === 'select-option') {
      const response = await fetch('http://localhost:5000/addListingAmenity', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({listingId: listingId,
                            amenityName: newValue[newValue.length-1].value})
      })
      const json = await response.json()
      if(!json.success) {
        alert('Failed to add amenity')
        return
      }
    } else if(actionMeta.action === 'remove-value') {
      const response = await fetch('http://localhost:5000/removeListingAmenity', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({listingId: listingId,
                            amenityName: newValue[newValue.length-1].value})
      })
    }
  }
  const handleRemoveAvail = async (listing_id: string, date: string) => {
    const dateObj = new Date(date)
    const processedDate = dateObj.toISOString().split('T')[0]
    // TODO: Handle removal of availability
    const removalResult =  await fetch('http://localhost:5000/removeAvailability', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({listingId: listing_id, date: processedDate})
    })

    if(!removalResult.ok) {
      alert('Failed to remove availability')
      return
    }

    // Update the availabilities state
    const new_availabilities = availabilities.filter((avail: any) => avail.date !== date)
    setAvailabilities(new_availabilities)
  }

  const AvailabilityCard = (listing_id: string, date: string) => {
    return(
      <div className="flex items-center 
                      gap-1 border-solid border-black border-2 p-2 rounded-md">
        <div>
          {date}
        </div>
        <div>
          <button onClick={()=>{handleRemoveAvail(listing_id, date)}}
            className="border-solid border-black border-2 rounded-md p-1">
            Delete
          </button>
        </div>
      </div>
    )
  }

  const BookingCard = (bookingId: string, renterUsername: string, 
                    startDate: string, endDate: string, pricePaid: string) => 
  (
    <div className="flex flex-col border-solid border-black 
                    border-2 rounded-md p-2 items-center gap-1">
      <div>
        Renter: {renterUsername}
      </div>
      
      <div className="flex gap-2 p-1 flex-col">
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
      <button className="border-solid border-black border-2 rounded-md p-1"
        onClick={()=>{cancelBooking(bookingId)}} >
        Cancel Booking
      </button>
    </div>
  )

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

      // Get all availabilities
      const availabilityData = await fetch('http://localhost:5000/getAvailabilitiesByListingId?id='
                                + listingId)
      const availabilityJson = await availabilityData.json()

      // Remove Time from date
      availabilityJson.availabilities.forEach((avail: any) => {
        avail.date = avail.date.replace('00:00:00 GMT', '')
      })

      const bookingData = await fetch('http://localhost:5000/getBookingsByListingId?id='
                                + listingId)
      const bookingJson = await bookingData.json()

      bookingJson.bookings.forEach((booking: any) => {
        booking.start_date = booking.start_date.replace('00:00:00 GMT', '')
        booking.end_date = booking.end_date.replace('00:00:00 GMT', '')
      })
      
      setBookings(bookingJson.bookings)
      setAvailabilities(availabilityJson.availabilities)
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

  async function cancelBooking(bookingId: string) {
    console.log(bookingId)
    // Process booking cancellation
    const cancellationResult = await fetch('http://localhost:5000/hostCancelBooking', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({bookingId: bookingId, hostId: localStorage.getItem('userId')})
    })

    if(!cancellationResult.ok) {
      alert('Failed to cancel booking')
      return
    }

    // Update the bookings state
    const new_bookings = bookings.filter((booking: any) => booking.id !== bookingId)
    setBookings(new_bookings)
  }

  const handleAddAvailability = async () => {
    // Check start date is before end date
    console.log(newAvailability)
    if(newAvailability.startDate > newAvailability.endDate) {
      alert('Start date must be before end date')
      return
    }

    const sendData = await fetch('http://localhost:5000/insertAvailabilities', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({listingId: listingId, 
        startDate: newAvailability.startDate, 
        endDate: newAvailability.endDate})
    })

    const json = await sendData.json()
    if(json.success) {
      // Update availabilities state
      // Refetch availabilities
      const availabilityData = await fetch('http://localhost:5000/getAvailabilitiesByListingId?id='
                                + listingId)
      const availabilityJson = await availabilityData.json()
      // Remove Time from date
      availabilityJson.availabilities.forEach((avail: any) => {
        avail.date = avail.date.replace('00:00:00 GMT', '')
      })
      setAvailabilities(availabilityJson.availabilities)
    }
  }

  return(
    <div className="flex flex-col justify-center items-center gap-1">
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

      <div className="flex flex-col items-center gap-5">
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
        <div className="flex flex-col gap-1 items-center max-h-56 overflow-scroll">
          All Availabilities:
          {availabilities.map((avail: any) => AvailabilityCard(avail.listing_id, avail.date))}
        </div>
      </div>

      <div className="flex flex-col gap-1 items-center max-h-56 overflow-scroll">
        Bookings:
        {
          bookings.map((booking: any) => BookingCard(booking.id, booking.username,
            booking.start_date, booking.end_date, booking.price_paid))
        }
      </div>

      <div>
        <button onClick={()=>{window.location.href = '/hostListings'}}
          className="border-solid border-black border-2 rounded-md p-1">
          Back
        </button>
      </div>

    </div>)

}
