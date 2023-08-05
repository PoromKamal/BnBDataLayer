from flask import Flask
import mysql.connector
from queries import setup_queries
from models import Renter, Host, Reports
from utils.SearchFilters import SearchFilters

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

mysql = mysql.connector.connect(
  host=app.config['MYSQL_HOST'],
  user=app.config['MYSQL_USER'],
  password=app.config['MYSQL_PASSWORD'],
  database=app.config['MYSQL_DB']
)

@app.route('/test')
def login():
  return "Hello World!"

@app.route("/register")
def register():
  

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
  app.run(host="localhost", port=5000)