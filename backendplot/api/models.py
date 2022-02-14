from cryptography.fernet import Fernet
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# MODEL HELPERS
def dump_datetime(value):
    if value is None:
        return None
    return value.strftime("%Y-%m-%d")+" "+value.strftime("%H:%M:%S")

def get_user(value):
    user_data = User.query.get(value)
    return user_data.username

def get_entrance(value):
    entrance_data = Entrance.query.get(value)
    return entrance_data.label

def get_spot(value):
    spot_data = Spot.query.get(value)
    return spot_data.label

def call_fernet_key():
    return open("pass.key", "rb").read()

def to_encrypt(value):
    f = Fernet( call_fernet_key())
    return f.encrypt(value.encode('UTF-8')).decode('UTF-8')
# ----------------------------------
# ----------------------------------

# DATABASE MODELS
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(256), primary_key=True, autoincrement=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False, unique=True)
    fullname = db.Column(db.String(20), nullable=True, unique=True)
    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)
    created_by = db.Column(db.String(256), db.ForeignKey('user.id'), nullable=True)

    entrance_author = db.relationship('Entrance', backref='author',lazy='dynamic')
    spot_author = db.relationship('Spot', backref='author',lazy='dynamic')
    distance_author = db.relationship('Distance', backref='author',lazy='dynamic')
    parking_author = db.relationship('Parking', backref='author',lazy='dynamic')

    @property
    def serialize(self):
        return {
           'id'         : to_encrypt(self.id),
           'username'      : self.username,
           'fullname'      : self.fullname,
           'password'      : self.password,
           'created_on'       : dump_datetime(self.created_on),
           'updated_on'       : dump_datetime(self.updated_on),
           'created_by'       : get_user(self.created_by) if self.created_by is not None else '' 
        }
    
    @property
    def serialize_excludepass(self):
        return {
           'id'         : to_encrypt(self.id),
           'username'      : self.username,
           'fullname'      : self.fullname,
           'created_on'       : dump_datetime(self.created_on),
           'updated_on'       : dump_datetime(self.updated_on),
           'created_by'       : get_user(self.created_by) if self.created_by is not None else ''
        }

    def __repr__(self):
        return self.username 

class Entrance(db.Model):
    __tablename__ = 'entrance'

    id = db.Column(db.String(256), primary_key=True, autoincrement=False)
    label = db.Column(db.String(20), nullable=False, unique=True)
    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)
    created_by = db.Column(db.String(256), db.ForeignKey('user.id'), nullable=False)

    distance_entrance = db.relationship('Distance', backref='entry',lazy='dynamic')
    parking_entrance = db.relationship('Parking', backref='entry',lazy='dynamic')

    @property
    def serialize(self):
        return {
           'id'         : to_encrypt(self.id),
           'label'      : self.label,
           'created_on'       : dump_datetime(self.created_on),
           'updated_on'       : dump_datetime(self.updated_on),
           'created_by'       : get_user(self.created_by) 
        }

    @property
    def serialize_subrecord(self):
        return {
           'entrance'         : self.id,
           'entrance_name'      : self.label,
        }

    def __repr__(self):
        return self.label

class Spot(db.Model):
    __tablename__ = 'spot'

    id = db.Column(db.String(256), primary_key=True, autoincrement=False)
    label = db.Column(db.String(20), nullable=False, unique=True)
    size = db.Column(db.Integer(), default=0, nullable=False)
    open = db.Column(db.Boolean, default=True, nullable=False)
    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)
    created_by = db.Column(db.String(256), db.ForeignKey('user.id'), nullable=False)

    distance_spot = db.relationship('Distance', backref='parkspot',lazy='dynamic')
    parking_spot = db.relationship('Parking', backref='parkspot',lazy='dynamic')

    @property
    def serialize(self):
        return {
           'id'         : to_encrypt(self.id),
           'label'      : self.label,
           'size'      : self.size,
           'open'      : self.open,
           'created_on'       : dump_datetime(self.created_on),
           'updated_on'       : dump_datetime(self.updated_on),
           'created_by'       : get_user(self.created_by)
        }

    def __repr__(self):
        return self.label

class Distance(db.Model):
    __tablename__ = 'distance'

    id = db.Column(db.String(256), primary_key=True, autoincrement=False)
    distance = db.Column(db.Integer(), nullable=False)
    entrance = db.Column(db.String(256), db.ForeignKey('entrance.id'), nullable=False)
    spot = db.Column(db.String(256), db.ForeignKey('spot.id'), nullable=False)
    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)
    created_by = db.Column(db.String(256), db.ForeignKey('user.id'), nullable=False)

    @property
    def serialize(self):
        return {
           'id'         : self.id,
           'distance'         : self.distance,
           'entrance'       : self.entrance,  
           'entrance_name'       : get_entrance(self.entrance),  
        }

    def __repr__(self):
        return str(self.distance)

class Parking(db.Model):
    __tablename__ = 'parking'

    id = db.Column(db.String(256), primary_key=True, autoincrement=False)
    vehicle_plateno = db.Column(db.String(20), nullable=False)
    vehicle_size = db.Column(db.Integer(), nullable=False)
    entrance_id = db.Column(db.String(256), db.ForeignKey('entrance.id'), nullable=False)
    spot_id = db.Column(db.String(256), db.ForeignKey('spot.id'), nullable=False)
    spot_size = db.Column(db.Integer(), nullable=False)
    distance_distance = db.Column(db.Integer(), nullable=False)
    parked_on = db.Column(db.DateTime)
    unparked_on = db.Column(db.DateTime)
    total_fee = db.Column(db.Integer(), nullable=False)
    prev_id = db.Column(db.String(256), nullable=True)
    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)
    created_by = db.Column(db.String(256), db.ForeignKey('user.id'), nullable=False)

    @property
    def serialize(self):
        return {
           'id'         : to_encrypt(self.id),
           'vehicle_plateno'         : self.vehicle_plateno,
           'vehicle_size'       : self.vehicle_size,  
           'entrance_id'       : self.entrance_id, 
           'entrance_label'       : get_entrance(self.entrance_id),  
           'spot_id'       : self.spot_id, 
           'spot_label'       : get_spot(self.spot_id),  
           'spot_size'       : self.spot_size,
           'distance_distance'       : self.distance_distance,  
           'parked_on'       : dump_datetime(self.parked_on),
           'unparked_on'       : dump_datetime(self.unparked_on), 
           'total_fee'       : self.total_fee, 
           'created_on'       : dump_datetime(self.created_on),
           'updated_on'       : dump_datetime(self.updated_on),
           'created_by'       : get_user(self.created_by)
        }

    def __repr__(self):
        return self.vehicle_plateno
# ----------------------------------
# ----------------------------------