import mysql.connector
class Renter:
  mysql = mysql.connector.connect(
    host="localhost",
    user='root',
    password='admin',
    database='BnBDb'
  )

  """
  Inserts a new renter into the renter table
  """
  @staticmethod
  def insert_one_renter(name, dateOfBirth, SIN, address, occupation):
    cursor = Renter.mysql.cursor()
    query = '''
      INSERT INTO Renters (name, dateOfBirth, SIN, address, occupation)
      VALUES (%s, %s, %s, %s, %s)
    '''
    values = (name, dateOfBirth, SIN, address, occupation)
    cursor.execute(query, values)
    cursor.close()
    Renter.mysql.commit()

  """
  Removes a renter from the renter table
  """
  @staticmethod
  def remove_one_renter(renter_id):
    cursor = Renter.mysql.cursor()
    query = '''
      DELETE FROM Renters
      WHERE id = %s
    '''
    values = (renter_id,)
    cursor.execute(query, values)
    cursor.close()
    Renter.mysql.commit()

  """
  Returns a renter from the renter table
  by SIN
  """
  @staticmethod
  def get_one_renter_by_sin (SIN):
    cursor = Renter.mysql.cursor()
    query = '''
      SELECT * FROM Renters
      WHERE SIN = %s
    '''
    values = (SIN,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    cursor.close()
    return result
  
  """
    Inserts a booking into the booking table
    for renter with renter_id
  """
  @staticmethod
  def insert_one_booking (listing_id, renter_id, start_date, end_date):
    cursor = Renter.mysql.cursor()
    # TODO: Check if already booked
    # TODO: Check if dates in {start_date, end_date} is available
    query = '''
      INSERT INTO Bookings (listing_id, renter_id, start_date, end_date)
      VALUES (%s, %s, %s, %s)
    '''
    values = (listing_id, renter_id, start_date, end_date)
    cursor.execute(query, values)
    cursor.close()
    Renter.mysql.commit()

  """
    Removes a booking from the booking table
  """
  @staticmethod
  def remove_one_booking (booking_id):
    cursor = Renter.mysql.cursor()
    query = '''
      DELETE FROM Bookings
      WHERE id = %s
    '''
    values = (booking_id)
    cursor.execute(query, values)
    cursor.close()
    Renter.mysql.commit()

  """
  Inserts a listing rating into the listing rating table
  made by renter with renter_id
  """
  @staticmethod
  def insert_one_listing_rating(renter_id, listing_id, rating, comment):
    cursor = Renter.mysql.cursor()
    query = '''
      INSERT INTO ListingRatings (renter_id, listing_id, rating, comment)
      VALUES (%s, %s, %s, %s)
    '''
    values = (renter_id, listing_id, rating, comment)
    cursor.execute(query, values)
    cursor.close()
    Renter.mysql.commit()

  """
  Removes a listing rating from the listing rating table
  """
  @staticmethod
  def delete_one_listing_rating (rating_id):
    cursor = Renter.mysql.cursor()
    query = '''
      DELETE FROM ListingRatings
      WHERE id = %s
    '''
    values = (rating_id)
    cursor.execute(query, values)
    cursor.close()
    Renter.mysql.commit()
  
  @staticmethod
  def get_all_listings():
    cursor = Renter.mysql.cursor()
    query = '''
      SELECT * FROM Listings
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result
  
  LONG_LAT_PROXIMITY_SEARCH_QUERY = '''
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
    );
  '''
  @staticmethod
  def search_listings_by_proximity (longitude, latitude, km_radius):
    cursor = Renter.mysql.cursor()
    values = (latitude, latitude, longitude, latitude, latitude, longitude, km_radius)
    cursor.execute(Renter.LONG_LAT_PROXIMITY_SEARCH_QUERY, values)
    result = cursor.fetchall()
    # print out the results
    for row in result:
      print(row)
    cursor.close()
    return result
