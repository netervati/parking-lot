# OOP Parking Lot
![alt text](https://raw.githubusercontent.com/netervati/ketodietlib/main/demo/demosite.gif)

OOP Parking Lot is a full-stack application designed to manage parking lots. The application implements specific rules on how vehicles are parked, un-parked, and rated. 

## Technologies
Below are the technologies that I used:

### Backend
- Flask
- Flask-CORS
- Flask-RESTful
- Flask-SQLAlchemy
- Flask-Migrate
- MySQL
- Cryptography
- PyJWT
- PyTz
- Python Dotenv

### Frontend
- Vue.js
- Vue-Routers
- vue-datetimepicker
- vue-chart-3
- Chart.js
- Sweet Alert 2
- Bootstrap
- Bootstrap Icons
- Axios

## Rules
Below are the rules that the system follows:

### General
- Vehicles are auto-assigned with a parking spot that is nearest to the entrance where the vehicle arrives
- A vehicle that re-enters the parking lot within 1 hour since it left is charged a continuous rate

### Vehicles and Parking Spots
Parking | Small Spot | Medium Spot | Large Spot |
--- | --- | --- | --- |
Small Vehicle | ✔ | ✔ | ✔ |
Medium Vehicle | - | ✔ | ✔ |
Large Vehicle | - | - | ✔ |

### Rates
- 40 - *for the first 3 hours regardless of the parking spot's and vehicle's size*
- Beyond initial hours:
	- 20 / hr - *vehicles parked at small spots*
	- 60 / hr - *vehicles parked at medium spots*
	- 100 / hr - *vehicles parked at large spots*
- 5000 - *vehicles exceeding 1 full 24 hours of parking (rate above will only apply on extra hours)*