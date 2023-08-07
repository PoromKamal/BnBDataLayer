import React, { FormEventHandler, useEffect, useState } from 'react'
import Select from 'react-select'
export default function RenterProfile() {
  const [renter, setRenter] = useState({
    username: '',
    name: '',
    SIN: '',
    dateOfBirth: '',
    address: '',
    occupation: ''
  })

  const [cardNumber, setCardNumber] = useState('123456789')
  const [expiryDate, setExpiryDate] = useState('')
  const [cvv, setCvv] = useState('343')
  const [paymentMethods, setPaymentMethods] = useState([])
  const [reviews, setReviews] = useState([])

  useEffect(() => {
    const userId = localStorage.getItem('userId')
    const fetchData = async () => {
      const renterData = await fetch('http://localhost:5000/getRenterById?id=' + userId)
      const renterJson = await renterData.json()
      setRenter(renterJson.renter)
    }
    fetchData()
    fetchPaymentMethods()
    fetchHostReviews()
  }, [])

  const fetchPaymentMethods = async () => {
    const paymentMethods = 
    await fetch('http://localhost:5000/getAllPaymentMethods?renterId=' 
    + localStorage.getItem('userId'))

    const paymentMethodsJson = await paymentMethods.json()
    console.log(paymentMethodsJson.paymentMethods)
    setPaymentMethods(paymentMethodsJson.paymentMethods)
  }

  const fetchHostReviews = async () =>{
    const userId = localStorage.getItem('userId')
    const reviewData = await fetch('http://localhost:5000/getReviewsOfRenter?id=' 
    + userId)
    const reviewJson = await reviewData.json()
    setReviews(reviewJson.reviews)
  }

  const renderRenterInfo = () => {
    return(
      <div className="w-fit flex flex-col items-center gap-2 p-10 
          border-solid border-black border-2 rounded-md">
        <h1>Username: {renter.username}</h1>
        <h1>Name: {renter.name}</h1>
        <h1>SIN: {renter.SIN}</h1>
        <h1>Date of Birth: {renter.dateOfBirth}</h1>
        <h1>Address: {renter.address}</h1>
        <h1>Occupation: {renter.occupation}</h1>
      </div>
    )
  }

  const renderRenterReviews = () => {
    return(
      <div className="w-fit flex flex-col items-center gap-2 p-10
      overflow-scroll h-1/3">
        <h1>Reviews</h1>
        {
          reviews.length == 0 ? <h1>No Reviews</h1> :
          reviews.map((review: any) => {
            return(
              <div className="flex flex-col items-center gap-2 p-10 
                  border-solid border-black border-2 rounded-md">
                <h1>Host Username: {review.username}</h1>
                <h1>Rating: {review.rating}</h1>
                <h1>Comment: {review.comment}</h1>
              </div>
            )
          })
        }
      </div>
    )
  }

  const handleSubmitPaymentMethod = async () => {
    const userId = localStorage.getItem('userId')
    const paymentMethodData = await fetch('http://localhost:5000/insertPaymentMethod', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        renterId: userId,
        cardNumber: cardNumber,
        expiryDate: expiryDate,
        cvv: cvv
      })
    })
    const paymentMethodJson = await paymentMethodData.json()
    if(paymentMethodJson.success) {
      alert('Payment method added successfully')
      fetchPaymentMethods()
    }
    else {
      alert('Error adding payment method')
    }
  }

  const renderPaymentMethods = () => {
    return(
      <div className="w-fit flex flex-col items-center gap-2 p-10
        h-56 overflow-scroll">
        <h1>Payment Methods</h1>
        {
          paymentMethods.map((paymentMethod: any) => {
            return(
              <div className="flex flex-col items-center gap-2 p-10 
                  border-solid border-black border-2 rounded-md">
                <h1>Card Number: {paymentMethod.card_number}</h1>
                <h1>Expiry Date: {paymentMethod.expiry_date}</h1>
                <h1>CVV: {paymentMethod.cvv}</h1>
              </div>
            )
          })
        }
      </div>
    )
  }


  return(
    <div className="w-full flex flex-col justify-center items-center gap-2">
      <h1>Renter Profile</h1>
      {
        renderRenterInfo()
      }
      <div className="flex">
        <form onSubmit={(e) => {e.preventDefault(); handleSubmitPaymentMethod()}}
        className="border-solid border-black border-2 rounded-md
          flex flex-col gap-2 p-2">
          <label htmlFor="username">Insert Payment Method </label>
          <input required value = {cardNumber} onChange = {e => setCardNumber(e.target.value)}
            type="text" id="cardNumber" name="cardNumber" placeholder="Card Number"
            className="border-solid border-2 rounded-md"/>
          <input required type="date"
            value = {expiryDate} onChange = {e => setExpiryDate(e.target.value)} 
             id="expiryDate" name="expiryDate" placeholder="Expiry Date"
            className="border-solid border-2 rounded-md"/>
          <input required value = {cvv} onChange = {e => setCvv(e.target.value)}
            type="text" id="cvv" name="cvv" placeholder="CVV"
            className="border-solid border-2 rounded-md"/>
          <button
            type="submit" className="border-solid border-2 rounded-md">
            Submit
          </button>
        </form>
        {
          renderPaymentMethods()
        }
      </div>
      {
        renderRenterReviews()
      }
    </div>
  )
}