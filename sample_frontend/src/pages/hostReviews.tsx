import React, { useEffect } from "react"
import Select from 'react-select'
export default function HostReviews() {
  const [reviews, setReviews] = React.useState([])
  const [recentRenters, setRecentRenters] = React.useState([])
  const [rentersLoaded, setRentersLoaded] = React.useState(false)
  const [rating, setRating] = React.useState('')
  const [comment, setComment] = React.useState('')
  const [renter, setRenter] = React.useState({listing_id: '', renter_id: ''})
  useEffect(() => {
    // Fetch recent renters
    const fetchData = async () => {
      const userId = localStorage.getItem('userId')
      const recentRenterData = await fetch('http://localhost:5000/getRecentRenters?id='
                                + userId)
      const recentRenterJson = await recentRenterData.json()
      const formattedRenters = recentRenterJson.renters.map((renter: any) => {
        return {
          value: renter,
          label: renter.username
        }
      })

      setRecentRenters(formattedRenters)
      setRentersLoaded(true)
    }

    fetchData()
  }, [])

  const handleChangeRenter = async (newValue: any, actionMeta: any) => {
    if(newValue) {
      setRenter(newValue.value)
    }
  }

  const handleChangeRating = (e: { target: { value: React.SetStateAction<string> } }) => {
    setRating(e.target.value)
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    // Check if rating has been selected
    console.log(rating)
    if(rating == '' || rating == undefined) {
      alert('Please select a rating')
      return
    }

    const hostId = localStorage.getItem('userId')
    const renterId = renter.renter_id
    const listingId = renter.listing_id
    const reviewData = await fetch('http://localhost:5000/insertRenterRating', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          hostId: hostId,
          renterId: renterId,
          rating: rating,
          comment: comment
          })
        })
    const reviewJson = await reviewData.json()
    if(reviewJson.success) {
      alert('Review submitted successfully')
    } else {
      alert('Error submitting review')
    }
  }

  return (
    <div className='w-full flex flex-col items-center gap-2 p-10'>
      <h1>Review a Renter</h1>
      <a href="/hostDashboard"
        className="border-solid border-2 rounded-md p-1">Back to Dashboard</a>

      <div>
        Review a Recent Renter:
      </div>
      <form onSubmit={handleSubmit}
        className="flex flex-col items-center gap-2 border-solid border-black border-2 rounded-md p-2">
        {
            rentersLoaded &&
            <Select required onChange={handleChangeRenter}
              options={recentRenters}/>
          }
        Rating:
        <div className="flex gap-1">
          <input onChange = {handleChangeRating}
          type="radio" id="1" name="rating" value="1"/>
          <label htmlFor="1">1</label>
          <input onChange = {handleChangeRating}
           type="radio" id="2" name="rating" value="2"/>
          <label htmlFor="2">2</label>
          <input onChange = {handleChangeRating}
           type="radio" id="3" name="rating" value="3"/>
          <label htmlFor="3">3</label>
          <input onChange = {handleChangeRating}
            type="radio" id="4" name="rating" value="4"/>
          <label htmlFor="4">4</label>
          <input onChange = {handleChangeRating}
            type="radio" id="5" name="rating" value="5"/>
          <label htmlFor="5">5</label>
        </div>
        <textarea required value={comment} onChange={e => setComment(e.target.value) }
        className="border-solid border-2 rounded-md max-h-56" placeholder='Comment'/>
        <button type="submit" className="border-solid border-2 rounded-md p-1">Submit</button>
      </form>
    </div>
  )
}