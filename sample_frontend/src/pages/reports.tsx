import React from 'react'
import Select from 'react-select'
export default function ReportsPage(){
  const [selectedReport, setSelectedReport] = React.useState(0)
  const [listingCountByCountry, setListingCountByCountry] = React.useState([] as any)
  const [listingCountByCountryByCity, setListingCountByCountryByCity] = React.useState([] as any)
  const [listingCountByCountryByCityByPostalCode, setListingCountByCountryByCityByPostalCode] = React.useState([] as any)
  const [dataLoaded, setDataLoaded] = React.useState(false)
  const [dateRange, setDateRange] = React.useState({startDate: '', endDate: ''} as any)
  const [totalBookingsByCity, setTotalBookingsByCity] = React.useState([] as any)
  const [totalBookingsByPostalCode, setTotalBookingsByPostalCode] = React.useState([] as any)
  const [hostRankPerCountry, setHostRankPerCountry] = React.useState([] as any)
  const [hostRankPerCountryPerCity, setHostRankPerCountryPerCity] = React.useState([] as any)
  const [hostsWith10PercentListings, setHostsWith10PercentListings] = React.useState([] as any)
  const [hostsWith10PercentListingsByCity, setHostsWith10PercentListingsByCity] = React.useState([] as any)
  const [rankRenters, setRankRenters] = React.useState([] as any)
  const [rankRentersByCity, setRankRentersByCity] = React.useState([] as any)
  const [rankRentersCancellations, setRankRentersCancellations] = React.useState([] as any)
  const [rankHostsCancellations, setRankHostsCancellations] = React.useState([] as any)

  const reports = [
    {"label": "Total number of Listings By Country", 
    "value": 1},
    {"label": "Total number of Listings By Country By City ", 
    "value": 2},
    {"label": "Total number of Listings By Country By City By PostalCode",
    "value": 3},
    {"label": "Total number of Bookings in Date Range By City",
    "value": 4},
    {"label": "Total number of Bookings in Date Range By Postal Code",
    "value": 5},
    {"label": "Ranking of Hosts per Country",
    "value": 6},
    {"label": "Ranking of Hosts per Country per City",
    "value": 7},
    {"label": "Hosts with 10%+ listings owner ship by Country",
    "value": 8},
    {"label": "Hosts with 10%+ listings owner ship by Country by City",
    "value": 9},
    {"label": "Ranking of Renters by Bookings in Date Range",
    "value": 10},
    {"label": "Ranking of Renters by Bookings in Date Range by City",
    "value": 11},
    {"label": "Ranking of Renters by # Cancellations",
    "value": 12},
    {"label": "Ranking of Hosts by # Cancellations",
    "value": 13},
    {"label": "Common Listing Noun Phrases",
    "value": 14},
  ]

  const fetchListingDataByCountry = async (city:boolean, cityAndPostal:boolean) => {
    let url = 'http://localhost:5000/getTotalListingsByCountry?'
    if(city && !cityAndPostal){
      url += "city=true"
    }

    if(cityAndPostal){
      url += "city=true&postalCode=true"
    }

    const listingData = await fetch(url)
    const listingDataJson = await listingData.json()
    if(!listingDataJson.success){
      alert("Failed to fetch data")
      return;
    }

    if(!city && !cityAndPostal){
      setListingCountByCountry(listingDataJson.listings)
      setDataLoaded(true)
    }

    if(city && !cityAndPostal){
      setListingCountByCountryByCity(listingDataJson.listings)
      setDataLoaded(true)
    }

    if(cityAndPostal){
      setListingCountByCountryByCityByPostalCode(listingDataJson.listings)
      setDataLoaded(true)
    }
  }

  const fetchHostsWith10PercentListings = async (city:boolean) => {
    let url = 'http://localhost:5000/getHostsWith10PercentListings?'
    if(city){
      url += "city=true"
    }
    const hostData = await fetch(url)
    const hostDataJson = await hostData.json()
    if(!hostDataJson.success){
      alert("Failed to fetch data")
      return;
    }
    
    if(city){
      setHostsWith10PercentListingsByCity(hostDataJson.hosts)
      setDataLoaded(true)
    }else {
      setHostsWith10PercentListings(hostDataJson.hosts)
      setDataLoaded(true)
    }
  }


  const fetchBookingDataBy = async (fetchByCity: boolean) => {
    if(dateRange.startDate === '' || dateRange.endDate === ''){
      alert("Please select a start and end date")
      return;
    }

    let url = 'http://localhost:5000/getTotalBookingsBy?'
    if(fetchByCity){
      url += "city=true"
    } else {
      url += "postal=true"
    }
    url += `&startDate=${dateRange.startDate}&endDate=${dateRange.endDate}`
    const bookingData = await fetch(url)
    const bookingDataJson = await bookingData.json()
    if(!bookingDataJson.success){
      alert("Failed to fetch data")
      return;
    }

    console.log(selectedReport)

    if(fetchByCity){
      setTotalBookingsByCity(bookingDataJson.bookings)
      setDataLoaded(true)
    }else {
      setTotalBookingsByPostalCode(bookingDataJson.bookings)
      setDataLoaded(true)
    }
  }

  const fetchHostsRankPerCountry = async (fetchByCity: boolean) => {
    let url = 'http://localhost:5000/getHostRankPerCountry?'
    if(fetchByCity){
      url += "city=true"
    }
    const hostRankData = await fetch(url)
    const hostRankDataJson = await hostRankData.json()
    if(!hostRankDataJson.success){
      alert("Failed to fetch data")
      return;
    }

    console.log(hostRankDataJson)
    
    if(fetchByCity){
      setHostRankPerCountryPerCity(hostRankDataJson.hosts)
      setDataLoaded(true)
    }else {
      setHostRankPerCountry(hostRankDataJson.hosts)
      setDataLoaded(true)
    }
  }

  const fetchRankRenters = async (fetchByCity: boolean) => {
    let url = 'http://localhost:5000/rankRentersByBookings?'
    
    if(dateRange.startDate === '' || dateRange.endDate === ''){
      alert("Please select a start and end date")
      return;
    }

    if(fetchByCity){
      url += "city=true"
    }

    url += `&startDate=${dateRange.startDate}&endDate=${dateRange.endDate}`
    
    const rankRentersData = await fetch(url)
    const rankRentersDataJson = await rankRentersData.json()
    if(!rankRentersDataJson.success){
      alert("Failed to fetch data")
      return;
    }

    if(fetchByCity){
      setRankRentersByCity(rankRentersDataJson.renters)
      setDataLoaded(true)
    }else {
      setRankRenters(rankRentersDataJson.renters)
      setDataLoaded(true)
    }
  }

  const fetchRankRentersCancellations = async () => {
    let url = 'http://localhost:5000/rankRentersByCancellations?'
    const rankRentersCancellationsData = await fetch(url)
    const rankRentersCancellationsDataJson = await rankRentersCancellationsData.json()
    if(!rankRentersCancellationsDataJson.success){
      alert("Failed to fetch data")
      return;
    }
    
    setRankRentersCancellations(rankRentersCancellationsDataJson.renters)
    setDataLoaded(true)
  }

  const fetchRankHostsCancellations = async () => {
    let url = 'http://localhost:5000/rankHostsByCancellations?'
    const rankHostsCancellationsData = await fetch(url)
    const rankHostsCancellationsDataJson = await rankHostsCancellationsData.json()
    if(!rankHostsCancellationsDataJson.success){
      alert("Failed to fetch data")
      return;
    }

    setRankHostsCancellations(rankHostsCancellationsDataJson.hosts)
    setDataLoaded(true)
  }


  const renderTotalBookingsByCity = () => {
    console.log('here');
    return totalBookingsByCity.map((city:any) => {
      return(
        <div className='flex flex-row gap-5 justify-between
        border-solid border-black border-2 rounded-sm'>
          <h1>{city.city}</h1>
          <h1>{city.bookingsCount}</h1>
        </div>
      )
    })
  }

  const renderTotalBookingsByPostalCode = () => {
    return totalBookingsByPostalCode.map((postalCode:any) => {
      return(
        <div className='flex flex-row gap-5 justify-between
        border-solid border-black border-2 rounded-sm'>
          <h1>{postalCode.postalCode}</h1>
          <h1>{postalCode.bookingsCount}</h1>
        </div>
      )
    })
  }


  const renderListingsByCountry = () => {
    return listingCountByCountry.map((country:any) => {
      return(
        <div className='flex flex-row gap-5 justify-between
        border-solid border-black border-2 rounded-sm'>
          <h1>{country.country}</h1>
          <h1>{country.listingCount}</h1>
        </div>
      )
    })
  }

  const renderListingsByCountryByCity = () => {
    return listingCountByCountryByCity.map((country:any) => {
      return(
        <div className='flex flex-row gap-5 justify-between border-solid
         border-black border-2 rounded-sm'>
          <h1>{country.country}</h1>
          <h1>{country.city}</h1>
          <h1>{country.listingCount}</h1>
        </div>
      )
    })
  }

  const renderListingsByCountryByCityByPostalCode = () => {
    return listingCountByCountryByCityByPostalCode.map((country:any) => {
      return(
        <div className='flex flex-row gap-5  justify-between
        border-solid border-black border-2 rounded-sm'>
          <h1>{country.country}</h1>
          <h1>{country.city}</h1>
          <h1>{country.postalCode}</h1>
          <h1>{country.listingCount}</h1>
        </div>
      )
    })
  }

  const renderHostRankPerCountry = () => {
    console.log(hostRankPerCountry)
    return Object.keys(hostRankPerCountry).map((country:any) => {
      console.log(country);
      return (<div>
        <h1>{country}</h1>
        <h1>Username, listingCount</h1>
        {
          hostRankPerCountry[country].map((host: any) => { 
            return (
              <div className='flex flex-row gap-5 justify-between
              border-solid border-black border-2 rounded-sm'>
                <h1>{host.username}</h1>
                <h1>{host.listingCount}</h1>
              </div>
            )
          })
        }
      </div>)

    });
  }

  const renderHostRankPerCountryPerCity = () => {
    return Object.keys(hostRankPerCountryPerCity).map((city:any) => {
      console.log(city);
      return (<div>
        <h1>{city}</h1>
        <h1>Username, listingCount</h1>
        {
          hostRankPerCountryPerCity[city].map((host: any) => { 
            return (
              <div className='flex flex-row gap-5 justify-between
              border-solid border-black border-2 rounded-sm'>
                <h1>{host.username}</h1>
                <h1>{host.listingCount}</h1>
              </div>
            )
          })
        }
      </div>)

    });
  }

  const renderHostsWith10PercentListings = () => {
    return Object.keys(hostsWith10PercentListings).map((country:any) => {
      return (<div>
        <h1>{country}</h1>
        <h1>Username, Percentage</h1>
        {
          hostsWith10PercentListings[country].map((host: any) => { 
            return (
              <div className='flex flex-row gap-5 justify-between
              border-solid border-black border-2 rounded-sm'>
                <h1>{host.username}</h1>
                <h1>{host.percentage}</h1>
              </div>
            )
          })
        }
      </div>)
    });
  }

  const renderHostsWith10PercentListingsByCity = () => {
    return Object.keys(hostsWith10PercentListingsByCity).map((city:any) => {
      return (<div>
        <h1>{city}</h1>
        <h1>Username, Percentage</h1>
        {
          hostsWith10PercentListingsByCity[city].map((host: any) => { 
            return (
              <div className='flex flex-row gap-5 justify-between
              border-solid border-black border-2 rounded-sm'>
                <h1>{host.username}</h1>
                <h1>{host.percentage}</h1>
              </div>
            )
          })
        }
      </div>)
    });
  }

  const renderRankRenters = () => {
    return rankRenters.map((renter:any) => {
      return(
        <div className='flex flex-row gap-5 justify-between
        border-solid border-black border-2 rounded-sm'>
          <h1>{renter.username}</h1>
          <h1>{renter.bookingCount}</h1>
        </div>
      )
    })
  }

  const renderRankRentersByCity = () =>{
    return Object.keys (rankRentersByCity).map((city:any) => {
      return (<div>
        <h1>{city}</h1>
        <h1>Username, bookingCount</h1>
        {
          rankRentersByCity[city].map((renter: any) => { 
            return (
              <div className='flex flex-row gap-5 justify-between
              border-solid border-black border-2 rounded-sm'>
                <h1>{renter.username}</h1>
                <h1>{renter.bookingCount}</h1>
              </div>
            )
          })
        }
      </div>)
    });
  }

  const renderRankRentersCancellations = () => {
    return rankRentersCancellations.map((renter:any) => {
      return(
        <div className='flex flex-row gap-5 justify-between
        border-solid border-black border-2 rounded-sm'>
          <h1>{renter.username}</h1>
          <h1>{renter.cancellationCount}</h1>
        </div>
      )
    })
  }

  const renderRankHostsCancellations = () => {
    return rankHostsCancellations.map((host:any) => {
      return(
        <div className='flex flex-row gap-5 justify-between
        border-solid border-black border-2 rounded-sm'>
          <h1>{host.username}</h1>
          <h1>{host.cancellationCount}</h1>
        </div>
      )
    })
  }

  const renderReport =  () => {
    switch(selectedReport){
      case 1:
        return (
          <div className='flex flex-col gap-1'>
            Country, Listing Count
            {
              renderListingsByCountry()
            }

          </div>
        )
      case 2:
        return (
          <div className='flex flex-col gap-1'>
            Country, City, Listing Count
            {
              renderListingsByCountryByCity()
            }

          </div>
        )
      case 3:
        return (
          <div className='flex flex-col gap-1'>
            Country, City, Postal Code, Listing Count
            {
              renderListingsByCountryByCityByPostalCode()
            }

          </div>
        )
      case 4:
        return(
          <div className='flex flex-col gap-1'>
            City, Booking Count
            {
              renderTotalBookingsByCity()
            }
          </div>
        )

      case 5:
        return(
          <div className='flex flex-col gap-1'>
            Postal Code, Booking Count
            {
              renderTotalBookingsByPostalCode()
            }
          </div>
        )
      case 6:
        return(
          <div className='flex flex-col gap-1'>
            {
              renderHostRankPerCountry()
            }
          </div>
        )
      case 7:
        return(
          <div className='flex flex-col gap-1'>
            {
              renderHostRankPerCountryPerCity()
            }
          </div>
        )
      case 8:
        return(
          <div className='flex flex-col gap-1'>
            {
              renderHostsWith10PercentListings()
            }
          </div>
        )
      case 9:
        return(
          <div className='flex flex-col gap-1'>
            Username, Percent
            {
              renderHostsWith10PercentListingsByCity()
            }
          </div>
        )
      case 10:
        return(
          <div className='flex flex-col gap-1'>
            Username, Booking Count
            {
              renderRankRenters()
            }
          </div>
        )
      case 11:
        return(
          <div className='flex flex-col gap-1'>
            {
              renderRankRentersByCity()
            }
          </div>
        )
      case 12:
        return(
          <div className='flex flex-col gap-1'>
            Username, Cancellation Count
            {
              renderRankRentersCancellations()
            }
          </div>
        )
      case 13:
        return(
          <div className='flex flex-col gap-1'>
            Username, Cancellation Count
            {
              renderRankHostsCancellations()
            }
          </div>
        )
      default:
        return <div></div>
    }
  }

  const handleSelectionChange = (newValue: any, actionMeta: any) => {
    setSelectedReport(newValue.value)
    setDataLoaded(false)
    switch(newValue.value){
      case 1:
        fetchListingDataByCountry(false, false)
        break;
      case 2:
        fetchListingDataByCountry(true, false)
        break;
      case 3:
        fetchListingDataByCountry(true, true)
        break;
      case 4:
        fetchBookingDataBy(true)
        break;
      case 5:
        fetchBookingDataBy(false)
        break;
      case 6:
        fetchHostsRankPerCountry(false)
        break;
      case 7:
        fetchHostsRankPerCountry(true)
        break;
      case 8:
        fetchHostsWith10PercentListings(false)
        break;
      case 9:
        fetchHostsWith10PercentListings(true)
        break;
      case 10:
        fetchRankRenters(false)
        break;
      case 11:
        fetchRankRenters(true)
        break;
      case 12:
        fetchRankRentersCancellations()
        break;
      case 13:
        fetchRankHostsCancellations()
        break;
      default:
        break;
    }
  }


  return(
    <div className="w-full items-center justify-center flex flex-col pt-10">
      <Select
        onChange={handleSelectionChange}
        className='w-56'
        options={reports}
      />
      <div className="flex flex-col">
        (Only for some reports)
        <h1>Start Date: </h1>
        <input type="date" onChange={(e) => setDateRange({...dateRange, startDate: e.target.value})}/>
        <h2>End Date: </h2>
        <input type="date" onChange={(e) => setDateRange({...dateRange, endDate: e.target.value})}/>
      </div>
      <div className='h-2/3'>
        <h1>Report Results</h1>
        {
          dataLoaded && renderReport()
        }
      </div>
    </div>
  )
} 