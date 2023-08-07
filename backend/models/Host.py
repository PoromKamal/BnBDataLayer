import mysql.connector

from .Auth import Auth
class Host:
  def get_mysql_connection():
    return mysql.connector.connect(
      host="localhost",
      user='root',
      password='admin',
      database='BnBDb'
    )

  """
  Inserts a new host into the host table
  """
  @staticmethod
  def insert_one_host(name, username, password, dateOfBirth, SIN, address, occupation):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor()
    if(not Auth.register_user(username, password)):
      cursor.close()
      return None
    query = '''
      INSERT INTO Hosts (name, username, dateOfBirth, SIN, address, occupation)
      VALUES (%s, %s, %s, %s, %s, %s)
    '''
    values = (name, username, dateOfBirth, SIN, address, occupation)
    cursor.execute(query, values)

    # Get the id of the newly inserted host
    query = '''
      SELECT id FROM Hosts
      WHERE SIN = %s
    '''
    values = (SIN,)
    cursor.execute(query, values)
    resultId = cursor.fetchone()[0]
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()
    return resultId

  @staticmethod
  def find_host_by_auth(username, password):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor(dictionary=True)
    query = '''
      SELECT Hosts.id
      FROM Hosts
      INNER JOIN Authentication ON Hosts.username = Authentication.username
      WHERE Hosts.username = %s AND Authentication.password = %s
    '''
    values = (username, password)
    cursor.execute(query, values)
    result = cursor.fetchone()
    cursor.close()
    mysqlConn.close()
    return result

  @staticmethod
  def get_all_bookings_by_id (hostId):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor(dictionary=True)
    query = '''
      SELECT B.id, B.renter_id
      FROM Bookings B
      INNER JOIN Listings L ON B.listing_id = L.id AND L.hostId = %s
    '''
    values = (hostId,)
    cursor.execute(query, values)
    result = cursor.fetchall()
    cursor.close()
    mysqlConn.close()
    return result

  """
  Returns a host from the host table
  by SIN
  """
  @staticmethod
  def get_one_host_by_sin (SIN):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor()
    query = '''
      SELECT * FROM Hosts
      WHERE SIN = %s
    '''
    values = (SIN,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    cursor.close()
    mysqlConn.close()
    return result[0]

  """
  Remove host from the host table
  """
  @staticmethod
  def remove_one_host(host_id):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor()
    query = '''
      DELETE FROM Hosts
      WHERE id = %s
    '''
    values = (host_id,)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()
    return True

  """
  Insert a new listing into the listing table
  """
  @staticmethod
  def insert_one_listing (host_id, address, city, country, postalCode, long, lat, price):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor()
    # Check if listing exists at address, long, lat
    query = '''
      SELECT * FROM Listings
      WHERE address = %s AND longitude = %s AND latitude = %s
    '''
    values = (address, long, lat)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result is not None:
      cursor.close()
      mysqlConn.close()
      return False

    query = '''
      INSERT INTO Listings (hostId, address, city, country, postalCode, longitude, latitude, price)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    values = (host_id, address, city, country, postalCode, long, lat, price)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()
    return True

  @staticmethod
  def get_all_listings_by_host_id(host_id):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor(dictionary=True)
    query = '''
      SELECT * FROM Listings
      WHERE hostId = %s
    '''
    values = (host_id,)
    cursor.execute(query, values)
    result = cursor.fetchall()
    cursor.close()
    mysqlConn.close()
    return result
  
  @staticmethod
  def get_reviews_by_listing_id(listing_id):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor(dictionary=True)
    query = '''
      SELECT R.username, LR.rating, LR.comment, LR.date
      FROM ListingRatings LR
      INNER JOIN Renters R ON LR.renter_id = R.id AND LR.listing_id = %s
    '''
    values = (listing_id,)
    cursor.execute(query, values)
    result = cursor.fetchall()
    cursor.close()
    mysqlConn.close()
    return result
  
  @staticmethod
  def get_recent_renters(hostId, days):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor(dictionary=True)
    query = '''
      SELECT R.username, L.*, B.*
      FROM Listings L
      INNER JOIN Bookings B ON L.id = B.listing_id AND L.hostId = %s
      INNER JOIN Renters R ON B.renter_id = R.id 
      AND B.end_date >= CURDATE() - INTERVAL %s DAY
      AND B.end_date < CURDATE()
    '''
    values = (hostId, days)
    cursor.execute(query, values)
    result = cursor.fetchall()
    cursor.close()
    mysqlConn.close()
    return result
  
  @staticmethod
  def get_listing_by_id (listing_id):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor(dictionary=True)
    query = '''
      SELECT * FROM Listings
      WHERE id = %s
    '''
    values = (listing_id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    cursor.close()
    mysqlConn.close()
    return result
  
  @staticmethod
  def get_listing_amenities (listing_id):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor(dictionary=True)
    query = '''
      SELECT A.*
      FROM ListingAmenities LA
      INNER JOIN Amenities A ON LA.amenity_id = A.id AND LA.listing_id = %s
    '''
    values = (listing_id,)
    cursor.execute(query, values)
    result = cursor.fetchall()
    cursor.close()
    mysqlConn.close()
    return result

  """
  Remove a listing from the listing table
  """
  @staticmethod
  def remove_one_listing(listing_id):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor()
    query = '''
      DELETE FROM Listings
      WHERE id = %s
    '''
    values = (listing_id,)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()

  """
  Insert a new availability into the availability table
  """
  @staticmethod
  def insert_one_availability (mysqlConn, listing_id, date):
    cursor = mysqlConn.cursor()
    query = '''
      INSERT INTO Availability (listing_id, date)
      VALUES (%s, %s)
    '''
    values = (listing_id, date)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()

  """
  Remove an availability from the availability table
  """
  @staticmethod
  def remove_one_availability(listing_id, date):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor()
    # Check if the availability is already booked
    query = '''
      SELECT * FROM Bookings
      WHERE listing_id = %s AND start_date <= %s AND end_date >= %s
    '''
    values = (listing_id, date, date)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result is not None:
      cursor.close()
      mysqlConn.close()
      return False
    
    # Delete the availability
    query = '''
      DELETE FROM Availability
      WHERE listing_id = %s AND date = %s
    '''
    values = (listing_id, date)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()
    return True
  
  """
    Insert a renter rating made by a host 
    into the renter ratings table
  """
  @staticmethod
  def insert_one_renter_rating (renter_id, host_id, rating, comment):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor()
    query = '''
      INSERT INTO RenterRatings (renter_id, host_id, rating, comment)
      VALUES (%s, %s, %s, %s)
    '''
    values = (renter_id, host_id, rating, comment)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()
    return True

  """
    Insert an amenity into the amenities table
  """
  @staticmethod
  def insert_one_amenity (name):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor()
    query = '''
      INSERT INTO Amenities (name)
      VALUES (%s)
    '''
    values = (name,)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()

  @staticmethod
  def get_reviews_made_by_host (hostId):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor(dictionary=True)
    query = '''
      SELECT R.username, LR.rating, LR.comment, LR.date
      FROM ListingRatings LR
      INNER JOIN Renters R ON LR.renter_id = R.id AND LR.host_id = %s
    '''
    values = (hostId,)
    cursor.execute(query, values)
    result = cursor.fetchall()
    cursor.close()
    mysqlConn.close()
    return result
  """
    Insert a listing amenity into the listing amenities table
  """
  @staticmethod
  def insert_one_listing_amenity (listing_id, amenity_id):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor()
    query = '''
      INSERT INTO ListingAmenities (listing_id, amenity_id)
      VALUES (%s, %s)
    '''
    values = (listing_id, amenity_id)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()
    return True
  
  @staticmethod
  def remove_one_listing_amenity (listing_id, amenity_id):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor()
    query = '''
      DELETE FROM ListingAmenities
      WHERE listing_id = %s AND amenity_id = %s
    '''
    values = (listing_id, amenity_id)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()
    return True

  @staticmethod
  def get_amenity_id_by_name(name):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor()
    query = '''
      SELECT id FROM Amenities
      WHERE name = %s
    '''
    values = (name,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    cursor.close()
    mysqlConn.close()
    return result[0]
  
  @staticmethod
  def get_all_availabilities(listing_id):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor(dictionary=True)
    query = '''
      SELECT * FROM Availability
      WHERE listing_id = %s
    '''
    values = (listing_id,)
    cursor.execute(query, values)
    result = cursor.fetchall()
    cursor.close()
    mysqlConn.close()
    return result

  @staticmethod
  def get_all_amenities ():
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor(dictionary=True)
    query = '''
      SELECT * FROM Amenities
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    mysqlConn.close()
    return result
  
  @staticmethod
  def get_bookings_by_listing_id (listing_id):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor(dictionary=True)
    query = '''
      SELECT Renters.username, Bookings.* 
      FROM Bookings
      INNER JOIN Renters ON Bookings.renter_id = Renters.id AND Bookings.listing_id = %s
    '''
    values = (listing_id,)
    cursor.execute(query, values)
    result = cursor.fetchall()
    cursor.close()
    mysqlConn.close()
    return result

  @staticmethod
  def get_all_listings ():
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor(dictionary=True)
    query = '''
      SELECT *
      FROM Listings;
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    mysqlConn.close()
    return result
  
  @staticmethod
  def cancel_booking (booking_id, host_id):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor()
    #Check if the booking exists and has not already passed
    query = '''
      SELECT * FROM Bookings
      WHERE id = %s AND end_date >= CURDATE() 
    '''
    values = (booking_id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result is None:
      cursor.close()
      mysqlConn.close()
      return False
    
    #Check if the host is the owner of the listing
    query = '''
      SELECT * FROM Listings
      WHERE id = %s AND hostId = %s
    '''
    values = (result[1], host_id)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result is None:
      cursor.close()
      mysqlConn.close()
      return False
    
    # insert into cancelled bookings
    query = '''
      INSERT INTO Cancellations (booking_id, host_id, cancellation_date)
      VALUES (%s, %s, CURDATE())
    '''
    values = (booking_id, host_id)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()
    return True
  
  def get_listings_with_revenue_generated ():
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor(dictionary=True)
    query = '''
      SELECT L.*, SUM(B.price_paid) AS revenue
      FROM Listings L
      INNER JOIN Bookings B ON L.id = B.listing_id
      GROUP BY L.id
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    mysqlConn.close()
    return result
  
  def get_amenity_name_by_id (amenity_id):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor()
    query = '''
      SELECT name FROM Amenities
      WHERE id = %s
    '''
    values = (amenity_id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    cursor.close()
    mysqlConn.close()
    return result[0]

  def get_recommended_amenities (listing_id):
    currAmenities = Host.get_listing_amenities(listing_id)
    currAmenities = set([amenity['id'] for amenity in currAmenities])
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor(dictionary=True)
    allListingsWithRevenue = Host.get_listings_with_revenue_generated()
    currListingRevenue = 0
    for listing in allListingsWithRevenue:
      if listing['id'] == listing_id:
        currListingRevenue = listing['revenue']
        break
    # Remove the current listing from the list, and all listings that have less revenue than the current listing
    betterPerformingListings = []
    for listing in allListingsWithRevenue:
      if listing['id'] != listing_id and listing['revenue'] > currListingRevenue:
        betterPerformingListings.append(listing)
      
    # Check the amenities of the better performing listings, which are not in the current listing
    recommendedAmenities = []
    uniqueAmenities = set()
    for listing in betterPerformingListings:
      amenities = Host.get_listing_amenities(listing['id'])
      diffAmenities = set()
      for amenity in amenities:
        if amenity['id'] not in currAmenities:
          diffAmenities.add(amenity['id'])
        # Projected increase per amenity 
        # = (revenue better listing - revenue curr listing) / (number of amenities)
        if(len(diffAmenities) == 0):
          continue
        projectedIncrease = (listing['revenue'] - currListingRevenue) / len(diffAmenities)
        for amenity in diffAmenities:
          if amenity not in uniqueAmenities:
            recommendedAmenities.append({
              'id': amenity,
              "name": Host.get_amenity_name_by_id(amenity),
              'projectedIncrease': projectedIncrease
            })
            uniqueAmenities.add(amenity)
    recommendedAmenities.sort(key=lambda x: x['projectedIncrease'], reverse=True)
    cursor.close()
    mysqlConn.close()
    recommendedPrice = 0
    if(len(betterPerformingListings) > 0):
      averagePrice = 0
      for listing in betterPerformingListings:
        averagePrice += listing['revenue']
      averagePrice /= len(betterPerformingListings)
      recommendedPrice = averagePrice

    return [recommendedAmenities, recommendedPrice]
    