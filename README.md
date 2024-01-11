# BnBDataLayer
Backend API for an application similar to AirBnB 🏠

# Features
- Core AirBnB functionality such as posting listings (with amenities, location, etc), and bookings. 
- Search feature, with search by proximity, postal-code, and exact.
- Analytics dashboard which contains:
    - Regional rankings for hosts, and guests
    - Recommended pricing for listings
    - Amenities suggestions for listing, along with projected revenue increase
    - Word clouds for listing reviews
 
# Build Instructions

Comes with a sample frontend.
To build the frontend, you need to have the following tools installed:
 - Node

Then to build, and run the frontend cd into the sample_frontend folder and run:
```
npm i
npm run dev
```
This will open the front end application on port 5000.

To build the backend, you need to have the following tools installed:
- pip
- python
- mysql
To build the backend first run:

```
PROJECT_ROOT/backend % pip install -r requirements.txt
```
Then to run the application:

```
PROJECT_ROOT/backend % python Launcher.py
```
