from flask import jsonify, request
from flask_restful import Resource, Api
from werkzeug.security import check_password_hash
from functools import wraps
from .models import db, User
import datetime
import jwt
import os

api = Api()
secret_key = os.environ.get('SECRET_KEY')

# Token Verification from Front End
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
        return jsonify(users=[i.serialize for i in User.query.all()])

# RESTful Endpoints
class Auth(Resource):
    def get(self):
        match_data = [i.serialize for i in User.query.filter_by(username='admin')]
        if check_password_hash(match_data[0]['password'], 'plot2020'):
            token = jwt.encode({'user': match_data[0]['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15) }, secret_key)
            return jsonify({'token': token.decode('utf-8')})

        return {'Api': False}

    def post(self):
        post_data = request.json
        match_data = [i.serialize for i in User.query.filter_by(username=post_data['username'])]
        if len(match_data) > 0:
            if check_password_hash(match_data[0]['password'], post_data['password']):
                token = jwt.encode({'user': match_data[0]['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15) }, secret_key)
                return jsonify({'token': token.decode('utf-8')})
        return {'message': 'Authentication Failed. Could not match the provided user credentials.'}

# class TestPost(Resource):
#     def get(self, title):
#         dataTest = Test(title=title,date="2021-03-24")
#         db.session.add(dataTest)
#         db.session.commit()
#         return {'in':'Yes'}

# RESTful registration
api.add_resource(BackendTest, '/')
api.add_resource(ApiTest, '/api/')
api.add_resource(Auth, '/api/auth/')
# api.add_resource(TestPost, '/post/<string:title>')
