# OOP Parking Lot
![System Demo](https://raw.githubusercontent.com/netervati/parking-lot/main/demo/demo.gif)

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

## Hosting the Application Locally
To use OOP Parking Lot, you will need [python 3.9](https://www.python.org/downloads/release/python-390/). Also, you need to make sure that you have a hosting application for MySQL database (e.g. [Wamp](https://www.wampserver.com/en/)).
### Installation
Follow the step-by-step installation below:
1. Clone this repository
```
$ git clone https://github.com/netervati/parking-lot
```
2. Start your virtual environment
```
$ pipenv shell
```
3. Install the packages located in the requirements.txt
4. Open the backendplot sub-folder and create the following files: ```.env```, ```.flaskenv```, ```pass.key```
5. In the ```.env```, add the following with the correct values:
```
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = mysql://[USER]:[PASSWORD]@[HOST]/[DATABASE]
ALLOWED_ORIGIN = [YOUR VUE ADDRESS PREFERRABLY YOUR IP]
SECRET_KEY = [JWT SECRET KEY]
```
6. In the ```.flaskenv```, add the following:
```
FLASK_APP=app.py
FLASK_ENV=development
DEBUG=true
```
7. Then, using the  [Cryptography](https://www.geeksforgeeks.org/fernet-symmetric-encryption-using-cryptography-module-in-python/#:~:text=Python%20supports%20a%20cryptography%20package,encrypt%20and%20decrypt%20methods%20respectively.) package, generate a Fernet key and save it in ```pass.key```
8. Open the api folder, and check config.py
9. Replace the ```r'/api/*'``` with the preferred allowed end point for your RESTful backend (remember to make sure that the end point matches the ALLOWED_ORIGIN)
```
CORS(app, resources={r'/api/*': {'origins': os.environ.get('ALLOWED_ORIGIN')}})
```
10. Open the frontendplot sub-folder and install the packages from the ```package.json```
11. Create another ```.env```
12. In the ```.env``` (front end),  add this with the correct value:
```
VUE_APP_API_URL=[YOUR FLASK URL SPECIFICALLY THE ALLOWED ENTRY POINT IN THE CORS]
```
13. Re-open backendplot
14. Run the following:
```
$ flask db upgrade
```
15. Run both apps in their respective sub-folders
```
$ flask run # for the backend
$ npm run serve # for the frontend
```