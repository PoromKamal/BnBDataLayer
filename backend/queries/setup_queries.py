bnb_amenities = [
    "Toilet paper",
    "Soap",
    "Bed sheets",
    "Towels",
    "Shampoo",
    "Free parking on premises",
    "Hot water",
    "Elevator",
    "Pool",
    "Gym",
    "Kitchen facilities",
    "Breakfast",
    "Coffee maker",
    "Tea",
    "Fire extinguisher",
    "Smoke detector",
    "Carbon monoxide detector",
    "First aid kit",
    "Wi-Fi",
    "TV",
    "Cable TV",
    "Netflix",
    "Air conditioning",
    "Heating",
    "High chair",
    "Baby bath",
    "Crib",
    "Outlet covers",
    "Changing table",
    "Patio or balcony",
    "Garden or backyard",
    "BBQ grill",
    "Step-free access to the property",
    "Wide doorway",
    "Well-lit path to entrance",
    "Pet-friendly listing"
]

restart_database = '''
  DROP DATABASE IF EXISTS BnBDb;
  CREATE DATABASE BnBDb;
  USE BnBDb;
'''

create_authentication_table = '''
  CREATE TABLE IF NOT EXISTS Authentication (
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    PRIMARY KEY (username)
  );
'''

create_renter_table = '''
  CREATE TABLE IF NOT EXISTS Renters (
    id INT AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    dateOfBirth DATE NOT NULL,
    SIN VARCHAR(9) UNIQUE NOT NULL,
    address VARCHAR(100) NOT NULL,
    occupation VARCHAR(100) NOT NULL,
    FOREIGN KEY (username) REFERENCES Authentication(username)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    UNIQUE (SIN),
    PRIMARY KEY (id)
  );
'''

create_host_table = '''
  CREATE TABLE IF NOT EXISTS Hosts (
    id INT AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    dateOfBirth DATE NOT NULL,
    SIN VARCHAR(9) UNIQUE NOT NULL,
    address VARCHAR(100) NOT NULL,
    occupation VARCHAR(100) NOT NULL,
    FOREIGN KEY (username) REFERENCES Authentication(username)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    UNIQUE (SIN),
    PRIMARY KEY (id)
  );
'''

create_listing_table = '''
  CREATE TABLE IF NOT EXISTS Listings (
    id INT AUTO_INCREMENT,
    hostId INT NOT NULL,
    address VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    postalCode VARCHAR(6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL,
    latitude DECIMAL(8, 6) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    averageRating DECIMAL(2, 1) DEFAULT 0,
    UNIQUE (longitude, latitude, address),
    PRIMARY KEY (id),
    FOREIGN KEY (hostId) REFERENCES Hosts(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    CHECK (price > 0),
    CHECK (longitude >= -180 AND longitude <= 180),
    CHECK (latitude >= -90 AND latitude <= 90)
  );
'''

create_availability_table = '''
  CREATE TABLE IF NOT EXISTS Availability (
      listing_id INT NOT NULL,
      date DATE NOT NULL,
      PRIMARY KEY (listing_id, date)
  );
'''

create_booking_table = '''
  CREATE TABLE IF NOT EXISTS Bookings (
    id INT AUTO_INCREMENT,
    listing_id INT NOT NULL,
    renter_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    price_paid DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (listing_id) REFERENCES Listings(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (renter_id) REFERENCES Renters(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    CHECK (start_date < end_date)
  );
  CREATE TRIGGER calculate_price_paid
    BEFORE INSERT ON Bookings
    FOR EACH ROW
    BEGIN
      SET NEW.price_paid = (SELECT price FROM Listings WHERE id = NEW.listing_id) * (DATEDIFF(NEW.end_date, NEW.start_date) + 1);
    END;
'''

create_listing_rating_table = '''
  CREATE TABLE IF NOT EXISTS ListingRatings (
    id INT AUTO_INCREMENT,
    renter_id INT NOT NULL,
    listing_id INT NOT NULL,
    rating INT NOT NULL,
    comment VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (renter_id) REFERENCES Renters(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (listing_id) REFERENCES Listings(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    CHECK (rating >= 1 AND rating <= 5)
  );
  CREATE TRIGGER check_renter_can_rate
    BEFORE INSERT ON ListingRatings
    FOR EACH ROW
    BEGIN
      IF NOT EXISTS(
        SELECT 1
        FROM Bookings
        WHERE renter_id = NEW.renter_id AND listing_id = NEW.listing_id AND end_date < CURDATE()
        AND DATEDIFF(CURDATE(), end_date) <= 180
        ) THEN
        SIGNAL SQLSTATE '45000'
          SET MESSAGE_TEXT = 'Renter cannot rate this listing';
      END IF;
    END;
  CREATE TRIGGER update_listing_average_rating
    AFTER INSERT ON ListingRatings
    FOR EACH ROW
    BEGIN
      UPDATE Listings
      SET averageRating = (
        SELECT AVG(rating)
        FROM ListingRatings
        WHERE listing_id = NEW.listing_id
      )
      WHERE id = NEW.listing_id;
    END;
'''

create_renter_rating_table = '''
  CREATE TABLE IF NOT EXISTS RenterRatings (
    id INT AUTO_INCREMENT,
    renter_id INT NOT NULL,
    host_id INT NOT NULL,
    rating INT NOT NULL,
    comment VARCHAR(100) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (renter_id) REFERENCES Renters(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (host_id) REFERENCES Hosts(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    CHECK (rating >= 1 AND rating <= 5)
  );
  CREATE TRIGGER check_host_can_rate
    BEFORE INSERT ON RenterRatings
    FOR EACH ROW
    BEGIN
      IF NOT EXISTS(
        SELECT 1
        FROM Bookings
        WHERE renter_id = NEW.renter_id AND end_date < CURDATE()
        AND DATEDIFF(CURDATE(), end_date) <= 180
        ) THEN
        SIGNAL SQLSTATE '45000'
          SET MESSAGE_TEXT = 'Host cannot rate this renter';
      END IF;
    END;
'''

create_renter_payment_info_table = '''
  CREATE TABLE IF NOT EXISTS PaymentInformation (
    id INT AUTO_INCREMENT,
    renter_id INT NOT NULL,
    card_number VARCHAR(16) NOT NULL,
    security_code VARCHAR(3) NOT NULL,
    expiry_date DATE NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (renter_id) REFERENCES Renters(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
  );
'''

create_amenities_table = '''
  CREATE TABLE IF NOT EXISTS Amenities (
    id INT AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    PRIMARY KEY (id)
  );
'''

create_listing_amenities_table = '''
  CREATE TABLE IF NOT EXISTS ListingAmenities (
    listing_id INT NOT NULL,
    amenity_id INT NOT NULL,
    PRIMARY KEY (listing_id, amenity_id),
    FOREIGN KEY (listing_id) REFERENCES Listings(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES Amenities(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
  );
'''

create_cancellation_table = '''
  CREATE TABLE IF NOT EXISTS Cancellations (
    id INT AUTO_INCREMENT,
    booking_id INT NOT NULL,
    host_id INT NULL,
    renter_id INT NULL,
    cancellation_date DATE NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (booking_id) REFERENCES Bookings(id)
      ON DELETE NO ACTION
      ON UPDATE CASCADE,
    FOREIGN KEY (host_id) REFERENCES Hosts(id)
      ON DELETE NO ACTION
      ON UPDATE CASCADE,
    FOREIGN KEY (renter_id) REFERENCES Renters(id)
      ON DELETE NO ACTION
      ON UPDATE CASCADE
  );
'''

setup_queries = [
  restart_database,
  create_authentication_table,
  create_renter_table,
  create_host_table,
  create_listing_table,
  create_availability_table,
  create_booking_table,
  create_listing_rating_table,
  create_renter_rating_table,
  create_renter_payment_info_table,
  create_amenities_table,
  create_amenities_table,
  create_listing_amenities_table,
  create_cancellation_table
]