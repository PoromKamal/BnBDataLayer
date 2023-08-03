from flask import Flask
import mysql.connector
from queries import setup_queries
from models import Renter, Host

Host = Host.Host
Renter = Renter.Renter
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
  Host.insert_one_host ("Porom", "1999-01-01", "123456789", "1234 Main St", "Student")
  Renter.insert_one_renter ("Ryan", "2000-01-01", "234567899", "1234 Trail St", "Student")
  hostId = Host.get_one_host_by_sin("123456789")[0]
  renterId = Renter.get_one_renter_by_sin("234567899")[0]
  Host.insert_one_listing (hostId, "1234 Main St", "33", "-71", "100.00")
  Host.insert_one_listing(hostId, "1234 Secondary St", 
                          "33.06", "-71.06", "100.00") # ~ 8.71 km away
  Host.insert_one_listing(hostId, "1234 Third St", 
                          "33.065", "-71.065", "100.00") # ~ 9.42 km away
  Host.insert_one_availability (1, "2023-05-01")
  Host.insert_one_availability (1, "2023-05-02")
  Host.insert_one_availability (1, "2023-05-03")
  Host.insert_one_availability (1, "2023-05-04")
  Host.insert_one_availability (1, "2023-05-05")
  Renter.insert_one_booking (1, renterId, "2023-05-01", "2023-05-05")
  Renter.insert_one_listing_rating (renterId, 1, 5, "Great place!")
  Host.insert_one_renter_rating (renterId, hostId, 5, "Great renter!")
  Renter.search_listings_by_proximity ("33", "-71", "10.0")
  app.run(host="localhost", port=5000)