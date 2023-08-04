""""
  Module for various reports on the data
"""
import mysql.connector
class Reports:
  mysql = mysql.connector.connect(
    host="localhost",
    user='root',
    password='admin',
    database='BnBDb'
  )

  @staticmethod
  def get_total_bookings_by_city (dateRange:tuple):
    if(len(dateRange) != 2):
      raise Exception("Invalid date range")
    cursor = Reports.mysql.cursor()
    query = '''
      SELECT city, COUNT(*) as bookingsCount
      FROM Bookings
      INNER JOIN Listings ON Listings.id = Bookings.listing_id
      WHERE start_date >= %s AND end_date <= %s
      GROUP BY city
    '''
    values = dateRange
    cursor.execute(query, values)
    result = cursor.fetchall()
    for row in result:
      print(row)
    cursor.close()
    return result
  
  @staticmethod
  def get_total_bookings_by_postal ():
    cursor = Reports.mysql.cursor()
    query = '''
      SELECT postalCode, COUNT(*) as bookingsCount
      FROM Bookings
      INNER JOIN Listings ON Listings.id = Bookings.listing_id
      GROUP BY postalCode
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
      print(row)
    cursor.close()
    return result

  @staticmethod
  def get_total_listings_by_country ():
    cursor = Reports.mysql.cursor()
    query = '''
      SELECT country, COUNT(*) as listingCount
      FROM Listings
      GROUP BY Country
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
      print(row)
    cursor.close()
    return result

  @staticmethod
  def get_total_listings_by_country_and_city ():
    cursor = Reports.mysql.cursor()
    query = '''
      SELECT country, city, COUNT(*) as listingCount
      FROM Listings
      GROUP BY Country, city
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
      print(row)
    cursor.close()
    return result
  
  @staticmethod
  def get_total_listings_by_country_and_city_and_postal ():
    cursor = Reports.mysql.cursor()
    query = '''
      SELECT country, city, postalCode, COUNT(*) as listingCount
      FROM Listings
      GROUP BY country, city, postalCode
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
      print(row)
    cursor.close()
    return result