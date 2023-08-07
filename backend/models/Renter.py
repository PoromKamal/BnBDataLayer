import datetime
import mysql.connector

from .Auth import Auth
class Renter:

  def get_mysql_connection():
    return mysql.connector.connect(
      host="localhost",
      user='root',
      password='admin',
      database='BnBDb'
    )

  """
  Inserts a new renter into the renter table
  """
  @staticmethod
  def insert_one_renter(name, username, password, dateOfBirth, SIN, address, occupation):
    mysqlConn = Renter.get_mysql_connection()
    cursor = mysqlConn.cursor()
    if(not Auth.register_user(username, password)):
      cursor.close()
      return None
    
    query = '''
      INSERT INTO Renters (name, username, dateOfBirth, SIN, address, occupation)
      VALUES (%s, %s, %s, %s, %s, %s)
    '''
    values = (name, username, dateOfBirth, SIN, address, occupation)
    cursor.execute(query, values)

    # Get the newly created renter's id
    query = '''
      SELECT id FROM Renters
      WHERE SIN = %s
    '''
    values = (SIN,)
    cursor.execute(query, values)
    renter_id = cursor.fetchone()[0]
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()
    return renter_id

  @staticmethod
  def get_reviews_of_renter (renterId):
    mysqlConn = Renter.get_mysql_connection()
    cursor = mysqlConn.cursor(dictionary=True)
    query = '''
      SELECT Hosts.username, RenterRatings.*
      FROM RenterRatings
      INNER JOIN Hosts ON Hosts.id = RenterRatings.host_id
      AND renter_id = %s
    '''
    values = (renterId,)
    cursor.execute(query, values)
    result = cursor.fetchall()
    cursor.close()
    mysqlConn.close()
    return result

  """
  Removes a renter from the renter table
  """
  @staticmethod
  def remove_one_renter(renter_id):
    mysqlConn = Renter.get_mysql_connection()
    cursor = mysqlConn.cursor()
    query = '''
      DELETE FROM Renters
      WHERE id = %s
    '''
    values = (renter_id,)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()

  """
  Returns a renter from the renter table
  by SIN
  """
  @staticmethod
  def get_one_renter_by_sin (SIN):
    mysqlConn = Renter.get_mysql_connection()
    cursor = mysqlConn.cursor()
    query = '''
      SELECT * FROM Renters
      WHERE SIN = %s
    '''
    values = (SIN,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    cursor.close()
    mysqlConn.close()
    return result[0]
  
  @staticmethod
  def get_one_renter_by_id (id):
    mysqlConn = Renter.get_mysql_connection()
    cursor = mysqlConn.cursor(dictionary=True)
    query = '''
      SELECT * FROM Renters
      WHERE id = %s
    '''
    values = (id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    cursor.close()
    mysqlConn.close()
    return result
  
  @staticmethod
  def insert_one_payment_method(renterId, cardNumber, expiry, cvv):
    mysqlConn = Renter.get_mysql_connection()
    cursor = mysqlConn.cursor()
    query = '''
      INSERT INTO PaymentInformation (renter_id, card_number, security_code, expiry_date)
      VALUES (%s, %s, %s, %s)
    '''
    values = (renterId, cardNumber, cvv, expiry)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()
    return True

  @staticmethod
  def get_all_payment_method_by_id (renterId):
    mysqlConn = Renter.get_mysql_connection()
    cursor = mysqlConn.cursor(dictionary=True)
    query = '''
      SELECT * FROM PaymentInformation
      WHERE renter_id = %s
    '''
    values = (renterId,)
    cursor.execute(query, values)
    result = cursor.fetchall()
    cursor.close()
    mysqlConn.close()
    return result


  """
    Inserts a booking into the booking table
    for renter with renter_id
  """
  @staticmethod
  def insert_one_booking (listing_id, renter_id, start_date, end_date):
    mysqlConn = Renter.get_mysql_connection()
    cursor = mysqlConn.cursor()
    # Check if there are available dates
    query = '''
      SELECT * FROM Availability
      WHERE listing_id = %s AND date BETWEEN %s AND %s
    '''
    values = (listing_id, start_date, end_date)
    cursor.execute(query, values)
    result = cursor.fetchall()
    if len(result) == 0:
      cursor.close()
      return False
    
    print(start_date, end_date)
    startDate = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    endDate = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    print(abs((endDate - startDate).days) + 1)
    
    # TODO: Check if conflicts with other bookings
    query = '''
      SELECT * FROM Bookings
      WHERE listing_id = %s AND (start_date <= %s AND end_date >= %s)
      OR (start_date >= %s AND end_date >= %s)
      OR (start_date >= %s AND end_date <= %s)
    '''
    values = (listing_id, start_date, start_date, start_date, end_date, 
              start_date, end_date)
    cursor.execute(query, values)
    result = cursor.fetchall()
    if len(result) > 0:
      cursor.close()
      return False
    # TODO: Check if dates in {start_date, end_date} is available
    query = '''
      INSERT INTO Bookings (listing_id, renter_id, start_date, end_date)
      VALUES (%s, %s, %s, %s)
    '''
    values = (listing_id, renter_id, start_date, end_date)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()
    return True

  """
    Removes a booking from the booking table
  """
  @staticmethod
  def remove_one_booking (booking_id):
    mysqlConn = Renter.get_mysql_connection()
    cursor = mysqlConn.cursor()
    query = '''
      DELETE FROM Bookings
      WHERE id = %s
    '''
    values = (booking_id)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()

  """
  Inserts a listing rating into the listing rating table
  made by renter with renter_id
  """
  @staticmethod
  def insert_one_listing_rating(renter_id, listing_id, rating, comment):
    mysqlConn = Renter.get_mysql_connection()
    cursor = mysqlConn.cursor()
    query = '''
      INSERT INTO ListingRatings (renter_id, listing_id, rating, comment, date)
      VALUES (%s, %s, %s, %s, CURDATE())
    '''
    values = (renter_id, listing_id, rating, comment)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()
  
  """
  Removes a listing rating from the listing rating table
  """
  @staticmethod
  def delete_one_listing_rating (rating_id):
    mysqlConn = Renter.get_mysql_connection()
    cursor = mysqlConn.cursor()
    query = '''
      DELETE FROM ListingRatings
      WHERE id = %s
    '''
    values = (rating_id)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()
  
  @staticmethod
  def get_all_listings():
    mysqlConn = Renter.get_mysql_connection()
    cursor = mysqlConn.cursor()
    query = '''
      SELECT * FROM Listings
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    mysqlConn.close()
    return result
  
  LONG_LAT_PROXIMITY_SEARCH_QUERY_BASE = '''
    SELECT *, 6371 * 2 * ASIN(SQRT(
          POWER(SIN(RADIANS((latitude - %s) / 2)), 2) +
          COS(RADIANS(%s)) * COS(RADIANS(latitude)) *
          POWER(SIN(RADIANS((longitude - %s) / 2)), 2)
      )) AS distance
    FROM Listings
    WHERE (
      6371 * 2 * ASIN(SQRT(
          POWER(SIN(RADIANS((latitude - %s) / 2)), 2) +
          COS(RADIANS(%s)) * COS(RADIANS(latitude)) *
          POWER(SIN(RADIANS((longitude - %s) / 2)), 2)
      )) <= %s
    )
  '''
  
  POSTAL_CODE_PROXIMITY_SEARCH_QUERY_BASE = '''
    SELECT * FROM Listings
    WHERE postalCode LIKE (CONCAT(SUBSTRING(%s, 1, 3) , '%'))
    '''
  
  AVAILABLE_WITHIN_WINDOW_QUERY_BASE = '''
    SELECT SearchResults.*
    FROM ({}) AS SearchResults
    JOIN Availability A ON SearchResults.id = A.listing_id
    WHERE A.date BETWEEN %s AND %s
    GROUP BY id
    HAVING COUNT(DISTINCT A.date) >= DATEDIFF(%s, %s) + 1
  '''

  AMENITY_SEARCH_QUERY_BASE = '''
    SELECT SearchResults.*
    FROM ({}) AS SearchResults
    JOIN ListingAmenities LA ON SearchResults.id = LA.listing_id
    JOIN Amenities A ON LA.amenity_id = A.id
    WHERE A.name IN ({})
    GROUP BY id
    HAVING COUNT(DISTINCT LA.amenity_id) = {}
  '''
  
  def build_proximity_search_query (longitude, latitude,
                                    km_radius, filters, order_by) -> [str, tuple]:
    values = (latitude, latitude, longitude, latitude, latitude, longitude, km_radius)
    base_query = Renter.LONG_LAT_PROXIMITY_SEARCH_QUERY_BASE

    if filters['postalCode'] != None:
      base_query += " AND postalCode=%s"
      values += (filters['postalCode'],)

    if len(filters['price_range']) == 2 \
      and filters['price_range'][0] != None \
      and filters['price_range'][1] != None \
      and filters['price_range'][0] <= filters['price_range'][1]:
      base_query += " AND price >= %s AND price <= %s"
      values += (filters['price_range'][0], filters['price_range'][1])

    if(filters['price_range'][0] != None and filters['price_range'][1] == None):
      base_query += " AND price >= %s"
      baseValues += (filters['price_range'][0],)
    
    if(filters['price_range'][0] == None and filters['price_range'][1] != None):
      base_query += " AND price <= %s"
      baseValues += (filters['price_range'][1],)

    if filters['minRating'] != 1:
      base_query += " AND averageRating >= %s"
      values += (filters['minRating'],)
    
    if len(filters['availabilityWindow']) == 2 \
      and filters['availabilityWindow'][0] != None \
      and filters['availabilityWindow'][1] != None \
      and filters['availabilityWindow'][0] <= filters['availabilityWindow'][1]:
      base_query = Renter.AVAILABLE_WITHIN_WINDOW_QUERY_BASE \
              .format (base_query)
      values += (filters['availabilityWindow'][0], filters['availabilityWindow'][1],
                filters['availabilityWindow'][1], filters['availabilityWindow'][0])
    
    if len(filters['amenities']) > 0:
      base_query = Renter.AMENITY_SEARCH_QUERY_BASE \
              .format (base_query, "%s" + ", %s" * (len(filters['amenities']) - 1),
                      len(filters['amenities']))
      values += tuple(filters['amenities'])
    if filters['ascending']:
      base_query += f'\n ORDER BY {order_by} ASC '
    else:
      base_query += f'\nORDER BY {order_by} DESC'
    return (base_query, values)

  @staticmethod
  def search_listings_by_proximity (longitude, latitude, 
                                    km_radius, filters, order_by = "distance"):
    [query, values] = \
    Renter.build_proximity_search_query(longitude, latitude, km_radius, 
                                        filters, order_by)                
    print(query)
    print(values)
    mysqlConn = Renter.get_mysql_connection()
    cursor = mysqlConn.cursor(dictionary=True)
    cursor.execute(query, values)
    result = cursor.fetchall()
    # print out the results
    for row in result:
      print(row)
    cursor.close()
    mysqlConn.close()
    return result

  def build_search_query(base_query, baseValues, filters):

    if len(filters['price_range']) == 2 \
      and filters['price_range'][0] != None \
      and filters['price_range'][1] != None \
      and filters['price_range'][0] <= filters['price_range'][1]:
      base_query += " AND price >= %s AND price <= %s"
      baseValues += (filters['price_range'][0], filters['price_range'][1])

    if(filters['price_range'][0] != None and filters['price_range'][1] == None):
      base_query += " AND price >= %s"
      baseValues += (filters['price_range'][0],)
    
    if(filters['price_range'][0] == None and filters['price_range'][1] != None):
      base_query += " AND price <= %s"
      baseValues += (filters['price_range'][1],)

    if filters['minRating'] != 1:
      base_query += " AND averageRating >= %s"
      baseValues += (filters['minRating'],)
    
    if filters["postalCode"] != None \
    and len(filters["postalCode"]) == 6:
      base_query += " AND postalCode=%s"
      baseValues += (filters['postalCode'],)
    
    if len(filters['availabilityWindow']) == 2 \
      and filters['availabilityWindow'][0] != None \
      and filters['availabilityWindow'][1] != None \
      and filters['availabilityWindow'][0] <= filters['availabilityWindow'][1]:
      base_query = Renter.AVAILABLE_WITHIN_WINDOW_QUERY_BASE \
              .format (base_query)
      baseValues += (filters['availabilityWindow'][0], filters['availabilityWindow'][1],
                filters['availabilityWindow'][1], filters['availabilityWindow'][0])
    
    if len(filters['amenities']) > 0:
      base_query = Renter.AMENITY_SEARCH_QUERY_BASE \
              .format (base_query, "%s" + ", %s" * (len(filters['amenities']) - 1),
                      len(filters['amenities']))
      baseValues += tuple(filters['amenities'])
    
    if filters['ascending']:
      base_query += f'ORDER BY price ASC'
    else:
      base_query += f'ORDER BY price DESC'
    return (base_query, baseValues)

  @staticmethod
  def search_listings_by_postal_code (postal_code,
    filters: dict ({ 'postalCode' : None, 'price_range': (None, None),
      'amenities' :  [], 'availabilityWindow' :  (None, None),
      'minRating' :  1, 'ascending' :  True })):
    
    base_query = '''
      SELECT * FROM Listings
      WHERE postalCode LIKE (CONCAT(SUBSTRING(%s, 1, 3) , '%'))
    '''
    baseValues = (postal_code,)
    
    [query, values] = \
      Renter.build_search_query(base_query, baseValues, filters)
    print(query)
    mysqlConn = Renter.get_mysql_connection()
    cursor = mysqlConn.cursor(dictionary=True)
    cursor.execute(query, values)
    result = cursor.fetchall()
    cursor.close()
    mysqlConn.close()
    return result

  @staticmethod
  def search_listings_by_address (address, city, country, filters):
    base_query = '''
      SELECT * FROM Listings
      WHERE address = %s
      AND city = %s
      AND country = %s
    '''
    base_values = (address, city, country)
    [query, values] = \
      Renter.build_search_query(base_query, base_values, filters)
    mysqlConn = Renter.get_mysql_connection()
    cursor = mysqlConn.cursor(dictionary=True)
    cursor.execute(query, values)
    result = cursor.fetchall()
    for row in result:
      print(row)
    cursor.close()
    mysqlConn.close()
    return result


  @staticmethod
  def cancel_booking (booking_id, renter_id):
    mysqlConn = Renter.get_mysql_connection()
    cursor = mysqlConn.cursor()
    # Check if booking exists
    query = '''
      SELECT * FROM Bookings
      WHERE id = %s AND renter_id = %s AND end_date >= CURDATE()
    '''
    values = (booking_id, renter_id)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result == None:
      return False

    # Add booking to cancellations table
    query = '''
      INSERT INTO Cancellations (booking_id, renter_id, cancellation_date)
      VALUES (%s, %s, CURDATE())
    '''
    values = (booking_id, renter_id)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()
    return True