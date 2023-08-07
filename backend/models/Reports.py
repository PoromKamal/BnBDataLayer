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
    cursor = Reports.mysql.cursor(dictionary=True)
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
  def get_total_bookings_by_postal (dateRange:tuple):
    cursor = Reports.mysql.cursor(dictionary=True)
    query = '''
      SELECT postalCode, COUNT(*) as bookingsCount
      FROM Bookings
      INNER JOIN Listings ON Listings.id = Bookings.listing_id
      WHERE start_date >= %s AND end_date <= %s
      GROUP BY postalCode
    '''
    values = dateRange
    cursor.execute(query, values)
    result = cursor.fetchall()
    for row in result:
      print(row)
    cursor.close()
    return result

  @staticmethod
  def get_total_listings_by_country ():
    cursor = Reports.mysql.cursor(dictionary=True)
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
    cursor = Reports.mysql.cursor(dictionary=True)
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
    cursor = Reports.mysql.cursor(dictionary=True)
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

  def get_all_distinct_countries ():
    cursor = Reports.mysql.cursor()
    query = '''
      SELECT DISTINCT country
      FROM Listings
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

  def get_all_cities():
    cursor = Reports.mysql.cursor()
    query = '''
      SELECT DISTINCT city, country
      FROM Listings
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

  @staticmethod
  def get_hosts_ranking_by_listing_count_by_country (refineByCity=False):
    cursor = Reports.mysql.cursor(dictionary=True)
    response = {}
    if(refineByCity):
      allCities = Reports.get_all_cities()
      for city in allCities:
        query = '''
          SELECT H.*, COUNT(*) as listingCount
          FROM Listings L
          INNER JOIN Hosts H ON H.id = L.hostId
          WHERE L.city = %s
          GROUP BY H.id
          ORDER BY listingCount DESC
        '''
        values = (city[0],)
        cursor.execute(query, values)
        result = cursor.fetchall()
        responseKey = f'{city[0]}, {city[1]}'
        response[responseKey] = []
        for row in result:
          response[responseKey].append(row)
        print(f'City, Country: {city[0], city[1]}')
        print('=============')
    else:
      allCountries = Reports.get_all_distinct_countries()
      for country in allCountries:
        query = '''
          SELECT H.*, COUNT(*) as listingCount
          FROM Listings L
          INNER JOIN Hosts H ON H.id = L.hostId
          WHERE L.country = %s
          GROUP BY H.id
          ORDER BY listingCount DESC
        '''
        values = (country[0],)
        cursor.execute(query, values)
        result = cursor.fetchall()
        response[country[0]] = []
        print(f'Country: {country[0]}')
        for row in result:
          response[country[0]].append(row)
          print(row)
        print('=============')
    cursor.close()
    return response
  
  @staticmethod
  def report_host_monopoly (refineByCity=False):
    cursor = Reports.mysql.cursor(dictionary=True)
    result = None
    response = {}
    if (refineByCity):
      allCities = Reports.get_all_cities()
      for city in allCities:
        query = '''
          SELECT H.*, COUNT(*) as listingCount,
          COUNT(*) / (SELECT COUNT(*) From Listings WHERE city = %s) * 100 
                                                          as percentage
          FROM Listings L
          INNER JOIN Hosts H ON H.id = L.hostId
          WHERE L.city = %s
          GROUP BY H.id
          HAVING percentage > 10
          ORDER BY listingCount DESC
        '''
        values = (city[0],city[0])
        cursor.execute(query, values)
        result = cursor.fetchall()
        responseKey = f'{city[0]}, {city[1]}'
        response[responseKey] = []
        print(f'City, Country: {city[0], city[1]}')
        for row in result:
          response[responseKey].append(row)
          print(row)
        print('=============')
    else:
      allCountries = Reports.get_all_distinct_countries()
      for country in allCountries:
        query = '''
          SELECT H.*, COUNT(*) as listingCount,
          COUNT(*) / (SELECT COUNT(*) From Listings WHERE country = %s) * 100 
                                                          as percentage
          FROM Listings L
          INNER JOIN Hosts H ON H.id = L.hostId
          WHERE L.country = %s
          GROUP BY H.id
          HAVING percentage > 10
          ORDER BY listingCount DESC
        '''
        values = (country[0], country[0])
        cursor.execute(query, values)
        result = cursor.fetchall()
        response[country[0]] = []
        print(f'Country: {country[0]}')
        for row in result:
          response[country[0]].append(row)
          print(row)
        print('=============')
    cursor.close()
    return response
  
  @staticmethod
  def get_rank_renter_by_bookings (timeRange: tuple, refineByCity=False):
    cursor = Reports.mysql.cursor(dictionary=True)
    result = None
    response = {}
    if refineByCity:
      allCities = Reports.get_all_cities()
      for city in allCities:
        query = '''
          SELECT R.*, COUNT(*) as bookingCount
          FROM Bookings B
          INNER JOIN Renters R ON R.id = B.renter_id
          INNER JOIN Listings L ON L.id = B.listing_id
          WHERE B.start_date >= %s AND B.end_date <= %s AND L.city = %s
          GROUP BY R.id
          ORDER BY bookingCount DESC
        '''
        values = (timeRange[0], timeRange[1], city[0])
        cursor.execute(query, values)
        result = cursor.fetchall()
        print(f'City, Country: {city[0], city[1]}')
        for row in result:
          responseKey = f'{city[0]}, {city[1]}'
          response[responseKey] = []
          response[responseKey].append(row)
          print(row)
        print('=============')
    else:
      query = '''
        SELECT R.*, COUNT(*) as bookingCount
        FROM Bookings B
        INNER JOIN Renters R ON R.id = B.renter_id
        WHERE B.start_date >= %s AND B.end_date <= %s
        GROUP BY R.id
        ORDER BY bookingCount DESC
      '''
      values = timeRange
      cursor.execute(query, values)
      result = cursor.fetchall()
      response = result
      for row in result:
        print(row)
    cursor.close()
    return response

  @staticmethod
  def get_renter_with_most_cancellations_ytd ():
    cursor = Reports.mysql.cursor(dictionary=True)
    query = '''
      SELECT R.*, COUNT(*) as cancellationCount
      FROM Cancellations C
      INNER JOIN Renters R ON R.id = C.renter_id
      WHERE C.cancellation_date >= (CURDATE() - INTERVAL 1 YEAR)
      GROUP BY R.id
      ORDER BY cancellationCount DESC
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
      print(row)
    cursor.close()
    return result
  
  @staticmethod
  def get_host_with_most_cancellations_ytd ():
    cursor = Reports.mysql.cursor(dictionary=True)
    query = '''
      SELECT H.*, COUNT(*) as cancellationCount
      FROM Cancellations C
      INNER JOIN Hosts H ON H.id = C.host_id
      WHERE C.cancellation_date >= (CURDATE() - INTERVAL 1 YEAR)
      GROUP BY H.id
      ORDER BY cancellationCount DESC
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
      print(row)
    cursor.close()
    return result
