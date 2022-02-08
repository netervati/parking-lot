from flask import jsonify, request
from flask_restful import Resource, Api
from .models import db, call_fernet_key, User, Parking, Entrance, Spot, Distance
from werkzeug.security import check_password_hash, generate_password_hash
from cryptography.fernet import Fernet
from operator import itemgetter
from functools import wraps
import datetime
import uuid
import math
import pytz
import jwt
import os

api = Api()
limit = 10
USRDATA = {}
without_timezone = datetime.datetime(2019, 2, 3, 6, 30, 15, 0)
timezone = pytz.timezone("Asia/Hong_Kong")
with_timezone = timezone.localize(without_timezone)

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

# RESTFUL HELPERS
def to_decrypt(value):
    f = Fernet( call_fernet_key())
    return f.decrypt(value.encode('UTF-8')).decode('UTF-8')

def get_nearest_spot(entrance, size):
    spot = db.session.query(Distance.distance, Spot.id, Spot.size).filter(Distance.spot == Spot.id).filter(Distance.entrance == entrance).filter(Spot.open == True).filter(Spot.size >= size).order_by(Distance.distance.asc()).first()
    return spot

def diff_dates(start_date, end_date):
    date_format_str = '%Y-%m-%d %H:%M:%S'
    start = datetime.datetime.strptime(str(start_date), date_format_str)
    end =   datetime.datetime.strptime(str(end_date), date_format_str)
    diff = end - start
    return diff.total_seconds() / 3600
# ----------------------------------
# ----------------------------------

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

class Dashboard(Resource):
    method_decorators = [token_required]
    def get(self):
        curDate = str(datetime.datetime.now().date())
        stats = {}
        currentParked = Parking.query.filter(Parking.parked_on.between(curDate + ' 00:00:00', curDate + ' 23:59:00'),Parking.total_fee == 0).count()
        freeSpots = Spot.query.filter(Spot.open == True).count()
        todayProfit = Parking.query.with_entities(db.func.sum(Parking.total_fee).label('total')).filter(Parking.parked_on.between(curDate + ' 00:00:00', curDate + ' 23:59:00')).first().total
        stats['todayProfit'] = str(todayProfit)
        stats['freeSpots'] = str(freeSpots)
        stats['currentParked'] = str(currentParked)
        return {'stats': stats}

class ParkingRegistry(Resource):
    method_decorators = [token_required]
    def get(self):
        page = int(request.args.get('page'))
        sort = int(request.args.get('sort'))
        search = request.args.get('search')
        model = Parking
        sortSwitch = {
            1: model.created_on.desc(),
            2: model.created_on.asc(),
            3: model.parked_on.desc(),
            4: model.parked_on.asc(),
            5: model.unparked_on.desc(),
            6: model.unparked_on.asc(),
        }
        offset = page * limit
        if not search:
            sql_query = model.query.order_by(sortSwitch.get(sort,model.created_on.desc())).offset(offset).limit(limit+1).all()
        else:
            formatSearch = "%{}%".format(search)
            sql_query = model.query.filter(model.vehicle_plateno.like(formatSearch)).order_by(sortSwitch.get(sort,model.created_on.desc())).offset(offset).limit(limit+1)
        return jsonify(records=[i.serialize for i in sql_query],limit=limit)

class ParkingForm(Resource):
    method_decorators = [token_required]
    def get(self):
        id = to_decrypt(request.args.get('id'))
        match_data = [i.serialize for i in Parking.query.filter_by(id=id)]
        if len(match_data) > 0:
            return jsonify(record=match_data)
        return {'response': 400}

    def post(self):
        post_data = request.json
        model = Parking
        get_spot = None
        if post_data['action'] == '1':
            try:
                if not post_data['entrance_id'] and not post_data['parked_on'] and not post_data['vehicle_plateno'] and not post_data['vehicle_size']: return {'response': 400}
                get_spot = get_nearest_spot(post_data['entrance_id'],post_data['vehicle_size'])
                prev_id = ''
                get_prev = model.query.filter_by(vehicle_plateno=post_data['vehicle_plateno']).order_by(model.unparked_on.desc()).first().serialize
                if get_prev:
                    diff_in_hours = diff_dates(get_prev['unparked_on'],post_data['parked_on'])
                    if diff_in_hours < 0: 
                        return {'response': 400}
                    if diff_in_hours <= 1:
                        prev_id = to_decrypt(get_prev['id'])
                insert_data = model(
                    id=uuid.uuid4(),
                    entrance_id=post_data['entrance_id'],
                    vehicle_plateno=post_data['vehicle_plateno'],
                    vehicle_size=int(post_data['vehicle_size']),
                    parked_on=post_data['parked_on'],
                    spot_id=get_spot[1],
                    spot_size=get_spot[2],
                    total_fee=0,
                    prev_id=prev_id,
                    distance_distance=get_spot[0],
                    created_on=datetime.datetime.now(),
                    updated_on=datetime.datetime.now(),
                    created_by=to_decrypt(USRDATA['user']),
                    updated_by=to_decrypt(USRDATA['user']))
                db.session.add(insert_data)
            except:
                db.session.rollback()
                return {'response': 400}
            
            match_data = Spot.query.get(get_spot[1])
            try:
                match_data.open = False
                match_data.updated_on = datetime.datetime.now()
                match_data.updated_by = to_decrypt(USRDATA['user'])
                db.session.commit()
            except:
                db.session.rollback()
                return {'response': 400}
        elif post_data['action'] == '2':
            match_data = model.query.get(to_decrypt(post_data['id']))
            try:
                diff_in_hours = diff_dates(match_data.parked_on,post_data['unparked_on'])
                counted_hours = int(math.ceil(diff_in_hours))
                remaining_hours = counted_hours
                rateSwitch = {
                    1: 20,
                    2: 60,
                    3: 100,
                }
                if match_data.prev_id:
                    targetprev = match_data.prev_id
                    while targetprev is not None:
                        get_prev = model.query.filter(model.id==targetprev).first()
                        diff_in_hours_prev = diff_dates(get_prev.parked_on,get_prev.unparked_on)
                        counted_hours_prev = int(math.ceil(diff_in_hours_prev))
                        remaining_hours += counted_hours_prev
                        targetprev = None
                        if get_prev.prev_id: targetprev = get_prev.prev_id
                total_fee = 0
                full_chunk = False
                while remaining_hours >= 24:
                    remaining_hours -= 24
                    total_fee += 5000
                    full_chunk = True
                if remaining_hours > 0:
                    if full_chunk == False: 
                        total_fee += 40 
                        remaining_hours -= 3
                    while remaining_hours > 0:  
                        total_fee += rateSwitch.get(int(match_data.spot_size),20)
                        remaining_hours -= 1

                match_data.unparked_on = post_data['unparked_on']
                match_data.total_fee = total_fee
                match_data.updated_on = datetime.datetime.now()
                match_data.updated_by = to_decrypt(USRDATA['user'])
                
            except:
                db.session.rollback()
                return {'response': 400}
            match_data = Spot.query.get(match_data.spot_id)
            try:
                match_data.open = True
                match_data.updated_on = datetime.datetime.now()
                match_data.updated_by = to_decrypt(USRDATA['user'])
                db.session.commit()
            except:
                db.session.rollback()
                return {'response': 400}
        elif post_data['action'] == '3':
            match_data = model.query.get(to_decrypt(post_data['id']))
            spot_id = match_data.spot_id
            try:
                db.session.delete(match_data)
            except:
                db.session.rollback()
                return {'response': 400}
            match_subdata = Spot.query.get(spot_id)
            try:
                match_subdata.open = True
                match_subdata.updated_on = datetime.datetime.now()
                match_subdata.updated_by = to_decrypt(USRDATA['user'])
                db.session.commit()
            except:
                db.session.rollback()
                return {'response': 400}
        else: 
            return {'response': 400}
        return {'response': 200}

class ParkingEntrance(Resource):
    method_decorators = [token_required]
    def get(self):
        return jsonify(entrance=[i.serialize_subrecord for i in Entrance.query.order_by(Entrance.label.asc()).all()])

class EntranceRegistry(Resource):
    method_decorators = [token_required]
    def get(self):
        page = int(request.args.get('page'))
        sort = int(request.args.get('sort'))
        search = request.args.get('search')
        model = Entrance
        sortSwitch = {
            1: model.created_on.desc(),
            2: model.created_on.asc(),
            3: model.label.desc(),
            4: model.label.asc(),
        }
        offset = page * limit
        if not search:
            sql_query = model.query.order_by(sortSwitch.get(sort,model.created_on.desc())).offset(offset).limit(limit+1).all()
        else:
            formatSearch = "%{}%".format(search)
            sql_query = model.query.filter(model.label.like(formatSearch)).order_by(sortSwitch.get(sort,model.created_on.desc())).offset(offset).limit(limit+1)
        return jsonify(records=[i.serialize for i in sql_query],limit=limit)

class EntranceForm(Resource):
    method_decorators = [token_required]
    def get(self):
        id = to_decrypt(request.args.get('id'))
        match_data = [i.serialize for i in Entrance.query.filter_by(id=id)]
        if len(match_data) > 0:
            return jsonify(record=match_data)
        return {'response': 400}

    def post(self):
        post_data = request.json
        model = Entrance
        if post_data['action'] == '1':
            try:
                if not post_data['label']: return {'response': 400}
                insert_data = model(
                    id=uuid.uuid4(),
                    label=post_data['label'],
                    created_on=datetime.datetime.now(),
                    updated_on=datetime.datetime.now(),
                    created_by=to_decrypt(USRDATA['user']),
                    updated_by=to_decrypt(USRDATA['user']))
                db.session.add(insert_data)
                db.session.commit()
            except:
                db.session.rollback()
                return {'response': 400}
        elif post_data['action'] == '2':
            match_data = model.query.get(to_decrypt(post_data['id']))
            try:
                match_data.label = post_data['label']
                match_data.updated_on = datetime.datetime.now()
                match_data.updated_by = to_decrypt(USRDATA['user'])
                db.session.commit()
            except:
                db.session.rollback()
                return {'response': 400}
        elif post_data['action'] == '3':
            curLeft = model.query.count()
            if curLeft <= 3 : return {'response': 400}
            match_data = model.query.get(to_decrypt(post_data['id']))
            try:
                db.session.delete(match_data)
                db.session.commit()
            except:
                db.session.rollback()
                return {'response': 400}
        else: 
            return {'response': 400}
        return {'response': 200}

class SpotRegistry(Resource):
    method_decorators = [token_required]
    def get(self):
        page = int(request.args.get('page'))
        sort = int(request.args.get('sort'))
        search = request.args.get('search')
        model = Spot
        sortSwitch = {
            1: model.created_on.desc(),
            2: model.created_on.asc(),
            3: model.label.desc(),
            4: model.label.asc(),
        }
        offset = page * limit
        if not search:
            sql_query = model.query.order_by(sortSwitch.get(sort,model.created_on.desc())).offset(offset).limit(limit+1).all()
        else:
            formatSearch = "%{}%".format(search)
            sql_query = model.query.filter(model.label.like(formatSearch)).order_by(sortSwitch.get(sort,model.created_on.desc())).offset(offset).limit(limit+1)
        return jsonify(records=[i.serialize for i in sql_query],limit=limit)

class SpotForm(Resource):
    method_decorators = [token_required]
    def get(self):
        id = to_decrypt(request.args.get('id'))
        match_data = [i.serialize for i in Spot.query.filter_by(id=id)]
        distance = sorted([i.serialize for i in Distance.query.filter_by(spot=id)], key=itemgetter('entrance_name'))
        match_subdata = distance
        entrance=[i.serialize_subrecord for i in Entrance.query.order_by(Entrance.label.asc()).all()]
        
        for entry in entrance:
            to_new = False
            for subdata in distance:
                if subdata['entrance'] == entry['entrance']:
                    to_new = True
                    continue
            if to_new == False: distance.append(entry)
        if len(match_data) > 0:
            return jsonify(record=match_data,subrecord=match_subdata)
        return {'response': 400}

    def post(self):
        post_data = request.json
        model = Spot
        if post_data['action'] == '1':
            inserted_id = None
            try:
                if not post_data['label'] and not post_data['size']: return {'response': 400}
                jwtuser = to_decrypt(USRDATA['user'])
                insert_data = model(
                    id = uuid.uuid4(),
                    label=post_data['label'],
                    size=post_data['size'],
                    created_on=datetime.datetime.now(),
                    updated_on=datetime.datetime.now(),
                    created_by=jwtuser,
                    updated_by=jwtuser)
                db.session.add(insert_data)
                db.session.commit()
                inserted_id = insert_data.id
            except:
                db.session.rollback()
                return {'response': 400}
            
            try:
                objects = []
                for value in post_data['subdata']:
                    objects.append(
                        Distance(
                            id=uuid.uuid4(),
                            entrance=value['entrance'],
                            distance=int(value['distance']),
                            spot = inserted_id,
                            created_on=datetime.datetime.now(),
                            updated_on=datetime.datetime.now(),
                            created_by=jwtuser,
                            updated_by=jwtuser)
                    )
                db.session.bulk_save_objects(objects)
            except:
                db.session.rollback()
                match_data = model.query.get(inserted_id)
                db.session.delete(match_data)
                db.session.commit()
                return {'response': 400}
        elif post_data['action'] == '2':
            match_data = model.query.get(to_decrypt(post_data['id']))
            objects = []
            jwtuser = to_decrypt(USRDATA['user'])
            try:
                if not post_data['label'] and not post_data['size']: return {'response': 400}
                match_data.label = post_data['label']
                match_data.size = post_data['size']
                match_data.updated_on = datetime.datetime.now()
                match_data.updated_by = jwtuser
                objects.append(match_data)
            except:
                db.session.rollback()
                return {'response': 400}
            
            try:
                for value in post_data['subdata']:
                    if 'id' in value.keys():
                        match_subdata = Distance.query.get(value['id'])
                        match_subdata.distance = int(value['distance'])
                        match_subdata.updated_on = datetime.datetime.now()
                        match_subdata.updated_by = jwtuser
                        objects.append(match_subdata)
                    else:
                        objects.append(
                            Distance(
                                id=uuid.uuid4(),
                                entrance=value['entrance'],
                                distance=int(value['distance']),
                                spot = match_data.id,
                                created_on=datetime.datetime.now(),
                                updated_on=datetime.datetime.now(),
                                created_by=jwtuser,
                                updated_by=jwtuser)
                        )
                db.session.bulk_save_objects(objects)
            except:
                db.session.rollback()
                return {'response': 400}
        elif post_data['action'] == '3':
            try:
                Distance.query.filter_by(spot=to_decrypt(post_data['id'])).delete()
            except:
                db.session.rollback()
                return {'response': 400}

            match_data = model.query.get(to_decrypt(post_data['id']))
            try:
                db.session.delete(match_data)
                db.session.commit()
            except:
                db.session.rollback()
                return {'response': 400}
        else: 
            return {'response': 400}
        return {'response': 200}

class SpotEntrance(Resource):
    method_decorators = [token_required]
    def get(self):
        return jsonify(entrance=[i.serialize_subrecord for i in Entrance.query.order_by(Entrance.label.asc()).all()])

class UserRegistry(Resource):
    method_decorators = [token_required]
    def get(self):
        page = int(request.args.get('page'))
        sort = int(request.args.get('sort'))
        search = request.args.get('search')
        model = User
        sortSwitch = {
            1: model.created_on.desc(),
            2: model.created_on.asc(),
            3: model.username.desc(),
            4: model.username.asc(),
            5: model.fullname.desc(),
            6: model.fullname.asc(),
        }
        offset = page * limit
        if not search:
            sql_query = model.query.order_by(sortSwitch.get(sort,model.created_on.desc())).offset(offset).limit(limit+1).all()
        else:
            formatSearch = "%{}%".format(search)
            sql_query = model.query.filter((model.username.like(formatSearch)) | (model.fullname.like(formatSearch))).order_by(sortSwitch.get(sort,model.created_on.desc())).offset(offset).limit(limit+1)
        return jsonify(records=[i.serialize_excludepass for i in sql_query],limit=limit)

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
        model = User
        if post_data['action'] == '1':
            try:
                if not post_data['username'] or not post_data['password'] or not post_data['fullname']: return {'response': 400}
                insert_data = model(
                    id=uuid.uuid4(),
                    username=post_data['username'],
                    password=generate_password_hash(post_data['password']),
                    fullname=post_data['fullname'],
                    created_on=datetime.datetime.now(),
                    updated_on=datetime.datetime.now())
                db.session.add(insert_data)
                db.session.commit()
            except:
                db.session.rollback()
                return {'response': 400}
        elif post_data['action'] == '2':
            match_data = model.query.get(to_decrypt(post_data['id']))
            try:
                if "password" in post_data.keys():
                    if not post_data["password"]: 
                        return {'response': 400}
                    match_data.password = generate_password_hash(post_data['password'])
                match_data.username = post_data['username']
                match_data.fullname = post_data['fullname']
                match_data.updated_on = datetime.datetime.now()
                db.session.commit()
            except:
                db.session.rollback()
                return {'response': 400}
        elif post_data['action'] == '3':
            match_data = model.query.get(to_decrypt(post_data['id']))
            if to_decrypt(USRDATA['user']) == match_data.id: return {'response': 400}
            try:
                db.session.delete(match_data)
                db.session.commit()
            except:
                db.session.rollback()
                return {'response': 400}
        else: 
            return {'response': 400}
        return {'response': 200}
# ----------------------------------
# ----------------------------------

# RESTFUL REGISTRATION
api.add_resource(BackendTest, '/')
api.add_resource(ApiTest, '/api/')
api.add_resource(Auth, '/api/auth/')
api.add_resource(Dashboard, '/api/dashboard/')
api.add_resource(ParkingRegistry, '/api/parking/registry/')
api.add_resource(ParkingForm, '/api/parking/form/')
api.add_resource(ParkingEntrance, '/api/parking/entrances/')
api.add_resource(EntranceRegistry, '/api/entrance/registry/')
api.add_resource(EntranceForm, '/api/entrance/form/')
api.add_resource(SpotRegistry, '/api/spot/registry/')
api.add_resource(SpotForm, '/api/spot/form/')
api.add_resource(SpotEntrance, '/api/spot/entrances/')
api.add_resource(UserRegistry, '/api/user/registry/')
api.add_resource(UserForm, '/api/user/form/')
# ----------------------------------
# ----------------------------------

