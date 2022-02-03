from datetime import datetime
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, Api
from functools import wraps
from .models import db, User
import datetime
import jwt
import os

api = Api()
secret_key = os.environ.get('SECRET_KEY')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = str(request.headers.get('Authorization'))
        if not token:
            return jsonify({'message': 'Token is missing.'})

        try:
            data = jwt.decode(token, secret_key)
        except:
            return jsonify({'message': 'Token is invalid.'})

        return f(*args, **kwargs)
    return decorated

class BackendTest(Resource):
    def get(self):
        return jsonify(users=[i.serialize for i in User.query.all()])

class ApiTest(Resource):
    method_decorators = [token_required]
    def get(self):
        return {'Api': True}

class Auth(Resource):
    def get(self):
        return {'Api': False}
    def post(self):
        post_data = request.json

        if post_data['username'] == 'test' and post_data['password'] == 'test':
            token = jwt.encode({'user': post_data['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60) }, secret_key)
            return jsonify({'token': token.decode('utf-8')})
        return {'Api': post_data}

# class TestPost(Resource):
#     def get(self, title):
#         dataTest = Test(title=title,date="2021-03-24")
#         db.session.add(dataTest)
#         db.session.commit()
#         return {'in':'Yes'}

api.add_resource(BackendTest, '/')
api.add_resource(ApiTest, '/api/')

api.add_resource(Auth, '/api/auth/')
# api.add_resource(TestPost, '/post/<string:title>')
