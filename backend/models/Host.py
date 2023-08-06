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

  """
  Insert a new listing into the listing table
  """
  @staticmethod
  def insert_one_listing (host_id, address, city, country, postalCode, long, lat, price):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor()
    query = '''
      INSERT INTO Listings (hostId, address, city, country, postalCode, longitude, latitude, price)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    values = (host_id, address, city, country, postalCode, long, lat, price)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()

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
  def insert_one_availability (listing_id, date):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor()
    query = '''
      INSERT INTO Availability (listing_id, date)
      VALUES (%s, %s)
    '''
    values = (listing_id, date)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()

  """
  Remove an availability from the availability table
  """
  @staticmethod
  def remove_one_availability(listing_id, date):
    mysqlConn = Host.get_mysql_connection()
    cursor = mysqlConn.cursor()
    query = '''
      DELETE FROM Availability
      WHERE listing_id = %s AND date = %s
    '''
    values = (listing_id, date)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()
  
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
      raise Exception("Booking does not exist or has already passed")
    
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
      raise Exception("Host does not own this listing")
    
    # insert into cancelled bookings
    query = '''
      INSERT INTO Cancellations (booking_id, host_id)
      VALUES (%s, %s)
    '''
    values = (booking_id, host_id)
    cursor.execute(query, values)
    cursor.close()
    mysqlConn.commit()
    mysqlConn.close()