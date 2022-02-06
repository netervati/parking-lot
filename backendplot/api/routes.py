from flask import jsonify, request
from flask_restful import Resource, Api
from functools import wraps
import jwt
import os
from .models import db, call_fernet_key, User, Entrance
import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from cryptography.fernet import Fernet

api = Api()
limit = 1
USRDATA = {}

def to_decrypt(value):
    f = Fernet( call_fernet_key())
    return f.decrypt(value.encode('UTF-8')).decode('UTF-8')

def registry_query():
    return sql_query

# VERIFICATION OF JWT FROM FRONT END (DECORATOR)
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        secret_key = os.environ.get('SECRET_KEY')
        token = str(request.headers.get('Authorization'))
        if not token:
            return jsonify({'message': 'Token is missing.', 'response': 401})
        try:
            data = jwt.decode(token, secret_key)
            USRDATA['user'] = data['user']
        except:
            return jsonify({'message': 'Token is invalid.', 'response': 401})

        return f(*args, **kwargs)
    return decorated
# ----------------------------------
# ----------------------------------

class BackendTest(Resource):
    def get(self):
        return jsonify(entrances=[i.serialize for i in Entrance.query.filter_by(created_by='3b0b5e66-28e7-4c3e-8ee4-8a9134df76cd')])

class ApiTest(Resource):
    method_decorators = [token_required]
    def get(self):
        return jsonify(users=[i.serialize_excludepass for i in User.query.order_by(User.created_on.desc()).all()])

# RESTFUL ENDPOINTS
class Auth(Resource):
    def post(self):
        secret_key = os.environ.get('SECRET_KEY')
        post_data = request.json
        match_data = [i.serialize for i in User.query.filter_by(username=post_data['username'])]
        if len(match_data) > 0:
            if check_password_hash(match_data[0]['password'], post_data['password']):
                token = jwt.encode({'user': match_data[0]['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15) }, secret_key)
                return jsonify({'token': token.decode('utf-8')})
        return {'message': 'Authentication Failed. Could not match the provided user credentials.'}

class UserRegistry(Resource):
    method_decorators = [token_required]
    def get(self):
        page = int(request.args.get('page'))
        sort = int(request.args.get('sort'))
        search = request.args.get('search')
        sortSwitch = {
            1: User.created_on.desc(),
            2: User.created_on.asc(),
            3: User.username.desc(),
            4: User.username.asc(),
            5: User.fullname.desc(),
            6: User.fullname.asc(),
        }
        if not search:
            sql_query = User.query.order_by(sortSwitch.get(sort,User.created_on.desc())).offset(page).limit(limit+1).all()
        else:
            formatSearch = "%{}%".format(search)
            sql_query = User.query.filter((User.username.like(formatSearch)) | (User.fullname.like(formatSearch))).order_by(sortSwitch.get(sort,User.created_on.desc())).offset(page).limit(limit+1)
        return jsonify(users=[i.serialize_excludepass for i in sql_query],limit=limit)

class UserForm(Resource):
    method_decorators = [token_required]
    def get(self):
        id = to_decrypt(request.args.get('id'))
        match_data = [i.serialize for i in User.query.filter_by(id=id)]
        if len(match_data) > 0:
            return jsonify(record=match_data)
        return {'response': 400}

    def post(self):
        post_data = request.json
        if post_data['action'] == '1':
            try:
                if not post_data['username'] or not post_data['password'] or not post_data['fullname']: return {'response': 400}
                insert_data = User(
                    username=post_data['username'],
                    password=generate_password_hash(post_data['password']),
                    fullname=post_data['fullname'],
                    created_on=datetime.datetime.utcnow(),
                    updated_on=datetime.datetime.utcnow())
                db.session.add(insert_data)
                db.session.commit()
            except:
                return {'response': 400}
        elif post_data['action'] == '2':
            match_data = User.query.get(to_decrypt(post_data['id']))
            try:
                if "password" in post_data.keys():
                    if not post_data["password"]: 
                        return {'response': 400}
                    match_data.password = generate_password_hash(post_data['password'])
                match_data.username = post_data['username']
                match_data.fullname = post_data['fullname']
                match_data.updated_on = datetime.datetime.utcnow()
                db.session.commit()
            except:
                return {'response': 400}
        elif post_data['action'] == '3':
            match_data = User.query.get(to_decrypt(post_data['id']))
            if to_decrypt(USRDATA['user']) == match_data.id: return {'response': 400}
            try:
                db.session.delete(match_data)
                db.session.commit()
            except:
                return {'response': 400}
        else: 
            return {'response': 400}
        return {'response': 200}
# ----------------------------------
# ----------------------------------

# for attr, value in match_data.__dict__.items():
#     key = str(attr)
#     if key in post_data.keys():
#         attr = post_data[key] 

# RESTFUL REGISTRATION
api.add_resource(BackendTest, '/')
api.add_resource(ApiTest, '/api/')
api.add_resource(Auth, '/api/auth/')
api.add_resource(UserRegistry, '/api/user/registry/')
api.add_resource(UserForm, '/api/user/form/')
# ----------------------------------
# ----------------------------------

