from flask import Flask
from flask_cors import CORS
import os

def AppConfig():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['ALLOWED_ORIGIN'] = os.environ.get('ALLOWED_ORIGIN')
    cors = CORS(app, resources={r'/api/*': {'origins': os.environ.get('ALLOWED_ORIGIN')}})

    return app