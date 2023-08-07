from datetime import datetime
from flask import Flask, request
import mysql.connector
from queries import setup_queries
from models import Renter, Host, Reports
from utils.SearchFilters import SearchFilters
from flask_cors import CORS, cross_origin

Host = Host.Host
Renter = Renter.Renter
Reports = Reports.Reports
bnb_amenities = setup_queries.bnb_amenities
setup_queries = setup_queries.setup_queries


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'BnBDb'
CORS(app, resources={r"/*": {"origins": "*"}})
mysql = mysql.connector.connect(
  host=app.config['MYSQL_HOST'],
  user=app.config['MYSQL_USER'],
  password=app.config['MYSQL_PASSWORD'],
  database=app.config['MYSQL_DB']
)

@app.route('/test')
def login():
  return "Hello World!"

@app.route("/register", methods=['POST'])
@cross_origin(origin="*")
def register():
  print(request.json)
  username = request.json['username']
  password = request.json['password']
  name = request.json['name']
  dateOfBirth = request.json['dob']
  SIN = request.json['sin']
  address = request.json['address']
  occupation = request.json['occupation']
  role = request.json['role']
  if(role == "renter"):
    newId = Renter.insert_one_renter(name, username, password, 
                             dateOfBirth, SIN, address, occupation)
    
    hostId = Host.insert_one_host ("Porom", "asdf", "test", "2002-01-01", 
                          "312411111", "1234 Main St",  "Student")
                          
    Host.insert_one_listing (hostId, "1234 Main St", "Toronto", "Canada", 
                             "M1C2T2", "33", "-71", "354.00")
    Host.insert_one_listing(hostId, "1234 Secondary St", "Brampton", "Canada", "M1C3T2",
                            "33.06", "-71.06", "3434.00")
    Host.insert_one_listing(hostId, "1234 Third St", "Oshawa", "Canada", "M3C2T2",
                            "33.065", "-71.065", "23.00")
    
    Host.insert_one_availability (1, "2023-08-04")
    Host.insert_one_availability (1, "2023-08-05")
    Host.insert_one_availability (1, "2023-08-06")

    Host.insert_one_availability (1, "2023-08-07")
    Host.insert_one_availability (1, "2023-08-08")
    Host.insert_one_availability (1, "2023-08-09")
    Host.insert_one_availability (1, "2023-08-10")
    Host.insert_one_availability (1, "2023-08-11")
    Renter.insert_one_booking (1, newId, "2023-08-04", "2023-08-06") 
    Host.insert_one_renter_rating (newId, hostId, 3, "Great renter!")
    
    amenityId = Host.get_amenity_id_by_name("Air Conditioning")
    Host.insert_one_listing_amenity (1, amenityId)
  

    if(newId is None):
      return {"success": False, "message": "Username already exists"}, 400
    return {"success": True, "message": "Successfully registered", "id": newId}
  
  if(role == "host"):
    hostId = Host.insert_one_host(name, username, password, 
                             dateOfBirth, SIN, address, occupation)
    if(hostId is None):
      return {"success": False, "message": "Username already exists"}, 400
    Host.insert_one_listing (hostId, "1234 Main St", "Toronto", "Canada", 
                              "M1C2T2", "33", "-71", "354.00")
    Host.insert_one_listing(hostId, "1234 Secondary St", "Brampton", "Canada", "M1C3T2",
                            "33.06", "-71.06", "3434.00")
    Host.insert_one_listing(hostId, "1234 Third St", "Oshawa", "Bangladesh", "M3C2T2",
                            "33.063", "-71.065", "23.00")
    Host.insert_one_listing(hostId, "1234 Third St", "Oshawa", "China", "M3C2T2",
                          "33.062", "-71.065", "23.00")
    Host.insert_one_listing(hostId, "1234 Third St", "Oshawa", "Japan", "M3C2T2",
                          "33.061", "-71.065", "23.00")
    
    Host.insert_one_listing_amenity (2, 1)
    Host.insert_one_listing_amenity (2, 3)
    Host.insert_one_listing_amenity (2, 2)
    Host.insert_one_listing_amenity (1, 1)
    renterId = Renter.insert_one_renter ("Ryan", "Ryan2", "password", "2000-01-01", "234567899", "1234 Trail St", "Student")
    renter2Id = Renter.insert_one_renter ("Ryan", "Ryan3", "password", "2000-01-01", "255567899", "1234 Trail St", "Student")
    Host.insert_one_availability (1, "2023-07-04")
    Host.insert_one_availability (1, "2023-07-05")
    Host.insert_one_availability (1, "2023-07-06")
    Host.insert_one_availability (1, "2023-07-07")
    Host.insert_one_availability (1, "2023-07-08")

    Host.insert_one_availability (2, "2023-07-04")
    Host.insert_one_availability (2, "2023-07-05")
    Host.insert_one_availability (2, "2023-07-06")
    Host.insert_one_availability (2, "2023-07-07")
    Host.insert_one_availability (2, "2023-07-08")

    Host.insert_one_availability (3, "2023-08-04")
    Host.insert_one_availability (3, "2023-08-05")
    Host.insert_one_availability (3, "2023-08-06")
    Host.insert_one_availability (3, "2023-08-07")
    Host.insert_one_availability (3, "2023-08-08")

    Renter.insert_one_booking (1, renterId, "2023-07-04", "2023-07-06")
    Renter.insert_one_booking (2, renterId, "2023-07-05", "2023-07-06")
    Renter.insert_one_booking (1, renter2Id, "2023-07-07", "2023-07-08")

    Renter.insert_one_listing_rating (renterId, 1, 5, "Great place!")
    Renter.insert_one_listing_rating (renterId, 2, 2, "Decent place!")
    Renter.insert_one_listing_rating (renter2Id , 1, 3, "Great place!")

          
    return {"success": True, "message": "Successfully registered", "id": hostId}
  
  return {"success": False, "message": "Invalid role"}, 400


@app.route("/getAllListings", methods=['GET'])
@cross_origin(origin="*")
def getAllListings():
  hostId = request.args.get('hostId') or None
  result = []
  if(hostId):
    result = Host.get_all_listings_by_host_id(hostId)
  else:
    result = Host.get_all_listings()
  return {"success": True, "listings": result}

@app.route("/getListingById", methods=['GET'])
@cross_origin(origin="*")
def getListingById():
  listingId = request.args.get('id')
  return {"success": True, "listing": Host.get_listing_by_id(listingId)}

@app.route("/getAmenitiesByListingId", methods=['GET'])
@cross_origin(origin="*")
def getAmenitiesByListingId():
  listingId = request.args.get('id')
  return {"success": True, "amenities": Host.get_listing_amenities(listingId)}

@app.route("/getHostsWith10PercentListings", methods=['GET'])
@cross_origin(origin="*")
def getHostsWith10PercentListings():
  city = request.args.get('city') or False
  return {"success": True, "hosts": Reports.report_host_monopoly(city)}


@app.route("/getAllAmenities", methods=['GET'])
@cross_origin(origin="*")
def getAllAmenities():
  return {"success": True, "amenities": Host.get_all_amenities()}

@app.route("/insertAvailabilities", methods=['POST'])
@cross_origin(origin="*")
def insertAvailabilities():
  # Check if req contains start, and end dates
  listingId = request.json['listingId']
  start_date = request.json['startDate']
  end_date = request.json['endDate']
  if not start_date or not end_date or not listingId:
    return {"success": False, "message": "Start and end dates must be provided"}, 400
  
  # Aggregate list of dates to insert starting
  # from start_date to end_date
  dates = []
  cur_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
  end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
  while cur_date <= end_date:
    dates.append(cur_date.strftime("%Y-%m-%d"))
    cur_date += datetime.timedelta(days=1)
  
  # Insert dates
  for date in dates:
    Host.insert_one_availability(listingId, date)
  
  return {"success": True, "message": "Temp"}

@app.route("/rankRentersByBookings", methods=['GET'])
@cross_origin(origin="*")
def rankRentersByBookings():
  startDate = request.args.get('startDate')
  endDate = request.args.get('endDate')
  dateRange = (startDate, endDate)
  city = request.args.get('city') or False
  return {"success": True, 
          "renters": Reports.get_rank_renter_by_bookings(dateRange, city)}

@app.route("/rankRentersByCancellations", methods=['GET'])
@cross_origin(origin="*")
def rankRentersByCancellations():
  return {"success": True,
          "renters": Reports.get_renter_with_most_cancellations_ytd()}

@app.route("/rankHostsByCancellations", methods=['GET'])
@cross_origin(origin="*")
def rankHostsByCancellations():
  return {"success": True,
          "hosts": Reports.get_host_with_most_cancellations_ytd()}
          

@app.route("/insertListing", methods=['POST'])
@cross_origin(origin="*")
def insertListing():
  hostId = request.json['hostId']
  address = request.json['address']
  city = request.json['city']
  country = request.json['country']
  postalCode = request.json['postalCode']
  latitude = request.json['latitude']
  longitude = request.json['longitude']
  price = request.json['price']
  result = Host.insert_one_listing(hostId, address, city, country, 
                                   postalCode, latitude, longitude, price)
  if not result:
    return {"success": False, "message": "Listing already exists"}, 400
  return {"success": True, "message": "Listing added successfully"}

@app.route("/getAvailabilitiesByListingId", methods=['GET'])
@cross_origin(origin="*")
def getAvailabilitiesByListingId():
  listingId = request.args.get('id')
  return {"success": True, 
          "availabilities": Host.get_all_availabilities(listingId)}


@app.route("/getBookingsByListingId", methods=['GET'])
@cross_origin(origin="*")
def getBookingsByListingId():
  listingId = request.args.get('id')
  return {"success": True, 
          "bookings": Host.get_bookings_by_listing_id(listingId)}

@app.route("/renterCancelBooking", methods=['POST'])
@cross_origin(origin="*")
def renterCancelBooking():
  bookingId = request.json['bookingId']
  renterId = request.json['renterId']
  success = Renter.cancel_booking(bookingId, renterId)
  if(not success):
    return {"success": False, 
          "message": "Booking does not exist or has already passed"}, 400
  return {"message": "Booking cancelled successfully", "success": True}

@app.route("/hostCancelBooking", methods=['POST'])
@cross_origin(origin="*")
def hostCancelBooking():
  bookingId = request.json['bookingId']
  hostId = request.json['hostId']
  success = Host.cancel_booking(bookingId, hostId)
  if(not success):
    return {"success": False, 
          "message": "Booking does not exist or has already passed"}, 400
  return {"message": "Booking cancelled successfully", "success": True}

@app.route("/removeAvailability", methods=['POST'])
@cross_origin(origin="*")
def removeAvailability():
  listingId = request.json['listingId']
  date = request.json['date']
  success = Host.remove_one_availability(listingId, date)
  if(not success):
    return {"success": False, 
          "message": "Availability has been booked already"}, 400
  return {"message": "Availability removed successfully", "success": True}

@app.route("/addListingAmenity", methods=['POST'])
@cross_origin(origin="*")
def addListingAmenity():
  listingId = request.json['listingId']
  amenityName = request.json['amenityName']
  amenityId = Host.get_amenity_id_by_name(amenityName)
  if(amenityId is None):
    Host.insert_one_amenity(amenityName)
    amenityId = Host.get_amenity_id_by_name(amenityName)
  success = Host.insert_one_listing_amenity(listingId, amenityId)
  if(not success):
    return {"success": False, 
          "message": "Amenity already exists for this listing"}, 400
  return {"message": "Amenity added successfully", "success": True}

@app.route("/removeListingAmenity", methods=['POST'])
@cross_origin(origin="*")
def removeListingAmenity():
  listingId = request.json['listingId']
  amenityName = request.json['amenityName']
  amenityId = Host.get_amenity_id_by_name(amenityName)
  if(amenityId is None):
    return {"success": False, 
          "message": "Amenity does not exist"}, 400
  success = Host.remove_one_listing_amenity(listingId, amenityId)
  if(not success):
    return {"success": False, 
          "message": "Amenity does not exist for this listing"}, 400
  return {"message": "Amenity removed successfully", "success": True}

@app.route("/getReviewsOfRenter", methods=['GET'])
@cross_origin(origin="*")
def getReviewsOfRenter():
  renterId = request.args.get('id')
  return {"success": True, 
          "reviews": Renter.get_reviews_of_renter(renterId)}

@app.route("/getReviewsByListingId", methods=['GET'])
@cross_origin(origin="*")
def getReviewsByListingId():
  listingId = request.args.get('id')
  return {"success": True, 
          "reviews": Host.get_reviews_by_listing_id(listingId)}

@app.route("/getRenterById", methods=['GET'])
@cross_origin(origin="*")
def getRenterById():
  renterId = request.args.get('id')
  return {"success": True, 
          "renter": Renter.get_one_renter_by_id(renterId)}

@app.route("/getRecentRenters", methods=['GET'])
@cross_origin(origin="*")
def getRecentRenters():
  hostId = request.args.get('id')
  days = 180
  return {"success": True, 
          "renters": Host.get_recent_renters(hostId, days)}

@app.route("/insertPaymentMethod", methods=['POST'])
@cross_origin(origin="*")
def insertPaymentMethod():
  renterId = request.json['renterId']
  cardNumber = request.json['cardNumber']
  expiryDate = request.json['expiryDate']
  cvv = request.json['cvv']
  success = Renter.insert_one_payment_method(renterId, cardNumber, expiryDate, cvv)
  if(not success):
    return {"success": False, 
          "message": "Payment method already exists"}, 400
  return {"message": "Payment method added successfully", "success": True}

@app.route("/getAllPaymentMethods", methods=['GET'])
@cross_origin(origin="*")
def getAllPaymentMethods():
  renterId = request.args.get('renterId')
  return {"success": True, 
          "paymentMethods": Renter.get_all_payment_method_by_id(renterId)}

@app.route("/insertRenterRating", methods=['POST'])
@cross_origin(origin="*")
def insertRenterRating():
  renterId = request.json['renterId']
  hostId = request.json['hostId']
  rating = request.json['rating']
  comment = request.json['comment']
  print(renterId, hostId, rating, comment)
  if(not(renterId and hostId and rating and comment)):
    return {"success": False, 
          "message": "Missing required fields"}, 400

@app.route("/deleteHost", methods=['DELETE'])
@cross_origin(origin="*")
def deleteHost():
  hostId = request.json['hostId']
  success = Host.remove_one_host(hostId)
  if(not success):
    return {"success": False, 
          "message": "Host does not exist"}, 400
  return {"message": "Host deleted successfully", "success": True}

@app.route("/searchByLongLat", methods=['GET'])
@cross_origin(origin="*")
def searchLongLat():
  longitude = request.args.get('longitude')
  latitude = request.args.get('latitude')
  radius = request.args.get('radius')
  orderBy = request.args.get('orderBy')
  order = request.args.get('order') or "ascending"

  minPrice = request.args.get('minPrice') or None
  maxPrice = request.args.get('maxPrice') or None
  amenities = request.args.get('amenities') or []
  startDate = request.args.get('startDate') or None
  endDate = request.args.get('endDate') or None
  minRating = request.args.get('minRating') or 1
  postalCode = request.args.get('postalCode') or None

  filterDict = {
    'price_range': (minPrice, maxPrice),
    'amenities' : amenities,
    'availabilityWindow' :  (startDate, endDate),
    'minRating' :  minRating,
    'ascending' : order == "ascending",
    'postalCode' : postalCode
  }

  if(not orderBy):
    orderBy = "distance"
  
  if(not order):
    order = "ascending" # Default to ascending

  results = Renter.search_listings_by_proximity (longitude, latitude, radius, 
                                                 filterDict, orderBy)
  return {"success": True, "results": results}

@app.route("/getCommonNounPhrases", methods=['GET'])
@cross_origin(origin="*")
def getCommonNounPhrases():
  return {"success": True, 
          "phrases": Reports.get_common_noun_phrases_for_listings()}


@app.route("/getTotalListingsByCountry", methods=['GET'])
@cross_origin(origin="*")
def getTotalListings():
  city = request.args.get('city') or False
  postalCode = request.args.get('postalCode') or False
  
  if city and postalCode:
    return {"success": True, 
            "listings": 
            Reports.get_total_listings_by_country_and_city_and_postal ()}
  
  if city:
    return {"success": True, 
            "listings": Reports.get_total_listings_by_country_and_city()}

  return {"success": True,
          "listings": Reports.get_total_listings_by_country()}

@app.route("/getHostRankPerCountry", methods=['GET'])
@cross_origin(origin="*")
def getHostRankPerCountry():
  city = request.args.get('city') or False
  return {"success": True, 
          "hosts": Reports.get_hosts_ranking_by_listing_count_by_country(city)}


@app.route("/getTotalBookingsBy", methods=['GET'])
@cross_origin(origin="*")
def getTotalBookings():
  city = request.args.get('city') or False
  startDate = request.args.get('startDate')
  endDate = request.args.get('endDate')
  dateRange = (startDate, endDate)
  if city:
    return {"success": True, 
            "bookings": Reports.get_total_bookings_by_city(dateRange)}
  
  postal = request.args.get('postal') or False
  if postal:
    return {"success": True, 
            "bookings": Reports.get_total_bookings_by_postal(dateRange)}

  return {"success": True,
          "bookings": Reports.get_total_bookings_by_city(dateRange)}

@app.route("/searchByPostalCode", methods=['GET'])
@cross_origin(origin="*")
def searchByPostalCode():
  postalCode = request.args.get('postalCode')
  order = request.args.get('order') or "ascending"

  minPrice = request.args.get('minPrice') or None
  maxPrice = request.args.get('maxPrice') or None
  amenities = request.args.get('amenities') or []
  startDate = request.args.get('startDate') or None
  endDate = request.args.get('endDate') or None
  minRating = request.args.get('minRating') or 1
  amenities = amenities.split(",")
  print(amenities)
  filterDict = {
    'price_range': (minPrice, maxPrice),
    'amenities' : amenities,
    'availabilityWindow' :  (startDate, endDate),
    'minRating' :  minRating,
    'ascending' : order == "ascending",
    'postalCode' : ""
  }

  results = Renter.search_listings_by_postal_code(postalCode, filterDict)
  return {"success": True, "results": results}
  
@app.route("/searchByAddress", methods=['GET'])
@cross_origin(origin="*")
def searchByAddress():
  streetAddress = request.args.get('streetAddress')
  order = request.args.get('order') or "ascending"
  city = request.args.get('city') or None
  country = request.args.get('country') or None

  minPrice = request.args.get('minPrice') or None
  maxPrice = request.args.get('maxPrice') or None
  amenities = request.args.get('amenities') or []
  startDate = request.args.get('startDate') or None
  endDate = request.args.get('endDate') or None
  minRating = request.args.get('minRating') or 1
  postalCode = request.args.get('postalCode') or None

  filterDict = {
    'price_range': (minPrice, maxPrice),
    'amenities' : amenities,
    'availabilityWindow' :  (startDate, endDate),
    'minRating' :  minRating,
    'ascending' : order == "ascending",
    'postalCode' : postalCode
  }

  results = Renter.search_listings_by_address(streetAddress, city, country, filterDict)
  return {"success": True, "results": results}

@app.route("/insertBooking", methods=['POST'])
@cross_origin(origin="*")
def bookListing():
  renterId = request.json['renterId']
  listingId = request.json['listingId']
  startDate = request.json['startDate']
  endDate = request.json['endDate']
  success = Renter.insert_one_booking(listingId, renterId, startDate, endDate)
  if(not success):
    return {"success": False, 
          "message": "Could not book"}, 400
  return {"message": "Booking added successfully", "success": True}

@app.route("/getRecommendedAmenities", methods=['GET'])
@cross_origin(origin="*")
def getRecommendedAmenities():
  listingId = request.args.get('listingId')
  return {"success": True, 
          "amenities": Host.get_recommended_amenities(listingId)}


def setup_database():
  cusor = mysql.cursor()
  for query in setup_queries:
    # print(query)
    results = cusor.execute(query, multi=True)
    for cur in results:
      cur.fetchall()
  cusor.close()
  mysql.commit()

def setup_amenities():
  cursor = mysql.cursor()
  for amenity in bnb_amenities:
    query = '''
      INSERT INTO Amenities (name)
      VALUES (%s)
    '''
    values = (amenity,)
    cursor.execute(query, values)
  cursor.close()
  mysql.commit()


if __name__ == '__main__':
  setup_database()
  setup_amenities()
  """
  hostId = Host.insert_one_host ("Porom", "asdf", "test", "2002-01-01", 
                          "312411111", "1234 Main St",  "Student")
                          
  Host.insert_one_listing (hostId, "1234 Main St", "Toronto", "Canada", 
                            "M1C2T2", "33", "-71", "354.00")
  Host.insert_one_listing(hostId, "1234 Secondary St", "Brampton", "Canada", "M1C3T2",
                          "33.06", "-71.06", "3434.00")
  Host.insert_one_listing(hostId, "1234 Third St", "Oshawa", "Bangladesh", "M3C2T2",
                          "33.063", "-71.065", "23.00")
  Host.insert_one_listing(hostId, "1234 Third St", "Oshawa", "China", "M3C2T2",
                        "33.062", "-71.065", "23.00")
  Host.insert_one_listing(hostId, "1234 Third St", "Oshawa", "Japan", "M3C2T2",
                        "33.061", "-71.065", "23.00")
  
  Host.insert_one_listing_amenity (2, 1)
  Host.insert_one_listing_amenity (2, 3)
  Host.insert_one_listing_amenity (2, 2)
  Host.insert_one_listing_amenity (1, 1)
  renterId = Renter.insert_one_renter ("Ryan", "Ryan2", "password", "2000-01-01", "234567899", "1234 Trail St", "Student")
  renter2Id = Renter.insert_one_renter ("Ryan", "Ryan3", "password", "2000-01-01", "255567899", "1234 Trail St", "Student")
  Host.insert_one_availability (1, "2023-07-04")
  Host.insert_one_availability (1, "2023-07-05")
  Host.insert_one_availability (1, "2023-07-06")
  Host.insert_one_availability (1, "2023-07-07")
  Host.insert_one_availability (1, "2023-07-08")

  Host.insert_one_availability (2, "2023-07-04")
  Host.insert_one_availability (2, "2023-07-05")
  Host.insert_one_availability (2, "2023-07-06")
  Host.insert_one_availability (2, "2023-07-07")
  Host.insert_one_availability (2, "2023-07-08")

  Host.insert_one_availability (3, "2023-08-04")
  Host.insert_one_availability (3, "2023-08-05")
  Host.insert_one_availability (3, "2023-08-06")
  Host.insert_one_availability (3, "2023-08-07")
  Host.insert_one_availability (3, "2023-08-08")

  Renter.insert_one_booking (1, renterId, "2023-07-04", "2023-07-06")
  Renter.insert_one_booking (2, renterId, "2023-07-05", "2023-07-06")
  Renter.insert_one_booking (1, renter2Id, "2023-07-07", "2023-07-08")

  Renter.insert_one_listing_rating (renterId, 1, 5, "Great place!")
  Renter.insert_one_listing_rating (renterId, 2, 2, "Decent place!")
  Renter.insert_one_listing_rating (renter2Id , 1, 3, "Great place!")

  recommended = Host.get_recommended_amenities (1)
  print(recommended)

  Host.insert_one_host ("Porom", "1999-01-01", "123456789", "1234 Main St",  "Student")
  Host.insert_one_host ("Sarraf", "1999-01-01", "345678912", "79 Main St",  "Student")
  Renter.insert_one_renter ("Ryan", "2000-01-01", "234567899", "1234 Trail St", "Student")
  hostId = Host.get_one_host_by_sin("123456789")
  sarrafId = Host.get_one_host_by_sin("345678912")
  renterId = Renter.get_one_renter_by_sin("234567899")
  Host.insert_one_listing (hostId, "1234 Main St", "Toronto", "Canada", "M1C2T2", "33", "-71", "354.00")
  Host.insert_one_listing(hostId, "1234 Secondary St", "Brampton", "Canada", "M1C3T2",
                          "33.06", "-71.06", "3434.00") # ~ 8.71 km away
  Host.insert_one_listing(hostId, "1234 Third St", "Oshawa", "Canada", "M3C2T2",
                          "33.065", "-71.065", "23.00") # ~ 9.42 km away
  Host.insert_one_listing(sarrafId, "1234 Fourth St", "Bomanville", "Canada", "M3C7R4",
                          "33.067", "-71.067", "357.00")
  Host.insert_one_listing(sarrafId, "1234 Pyramid St", "Cairo", "Egypt", "M3C7R4",
                          "53.067", "-61.067", "35337.00")
  Host.insert_one_availability (1, "2023-08-05")
  Host.insert_one_availability (1, "2023-08-06")
  Host.insert_one_availability (1, "2023-08-07")
  Host.insert_one_availability (1, "2023-08-08")
  Host.insert_one_availability (1, "2023-08-09")

  Host.insert_one_availability (2, "2023-08-05")
  Host.insert_one_availability (2, "2023-08-06")
  Host.insert_one_availability (2, "2023-08-07")
  Host.insert_one_availability (2, "2023-08-08")
  Host.insert_one_availability (2, "2023-08-09")
  
  Host.insert_one_availability (3, "2023-05-01")
  Host.insert_one_availability (3, "2023-05-02")
  Host.insert_one_availability (3, "2023-05-03")
  Host.insert_one_availability (3, "2023-05-04")
  Host.insert_one_availability (3, "2023-05-05")

  Host.insert_one_listing_amenity (1, 1)
  Host.insert_one_listing_amenity (1, 3)
  Host.insert_one_listing_amenity (1, 2)

  Renter.insert_one_booking (1, renterId, "2023-08-05", "2023-08-09")
  Renter.insert_one_booking (2, renterId, "2023-08-05", "2023-08-09")
  Renter.insert_one_booking (3, renterId, "2023-05-01", "2023-05-05")
  
  #Renter.insert_one_listing_rating (renterId, 1, 5, "Great place!")
  #Renter.insert_one_listing_rating (renterId, 2, 2, "Great place!")
  #Host.insert_one_renter_rating (renterId, hostId, 3, "Great renter!")
  #Renter.search_listings_by_proximity ("33", "-71", "10.0", "price", False)
  filterDict = { 
    'postalCode' : None,
    'price_range': (),
    'amenities' : [],
    'availabilityWindow' :  (),
    'minRating' :  1,
    'ascending' :  True
  }

  shampoo_id = Host.get_amenity_id_by_name("Shampoo")
  netflix_id = Host.get_amenity_id_by_name("Netflix")
  Host.insert_one_listing_amenity (1, shampoo_id)
  Host.insert_one_listing_amenity (1, netflix_id)
  Host.insert_one_listing_amenity (2, shampoo_id)
  Host.insert_one_listing_amenity (2, netflix_id)

  Renter.cancel_booking (1,  renterId)
  Renter.cancel_booking (2,  renterId)

  print("Total Bookings By City: \n ===================")
  Reports.get_total_bookings_by_city(("2023-05-01", "2023-05-05"))
  print("Total Bookings By Postal: \n ===================")
  Reports.get_total_bookings_by_postal()
  print("Total Listings By Country: \n ===================")
  Reports.get_total_listings_by_country()
  print("Total Listings By Country and City: \n ===================")
  Reports.get_total_listings_by_country_and_city()
  print("Total Listings By Country and City And Postal: \n ===================")
  Reports.get_total_listings_by_country_and_city_and_postal()
  print("Hosts ranking by listing count, per country \n ===================")
  Reports.get_hosts_ranking_by_listing_count_by_country(True)
  print("Hosts with 10%%+ listings owned by country")
  Reports.report_host_monopoly(True)
  print("Renter Ranking in a time period:")
  Reports.get_rank_renter_by_bookings(("2023-05-01", "2023-05-05"), True)
  print("Renters with most cancellations (year-to-date):")
  Reports.get_renter_with_most_cancellations_ytd()
  #Renter.search_listings_by_proximity ("33", "-71", "15.0", filterDict, "distance")
  #Renter.search_listings_by_postal_code("M1C2T2", filterDict)
  #Renter.search_listings_by_address("1234 Main St", filterDict)
  """
  app.run(host="localhost", port=5000, threaded=True)