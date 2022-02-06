from cryptography.fernet import Fernet
from flask_sqlalchemy import SQLAlchemy
import datetime
import uuid

db = SQLAlchemy()

def dump_datetime(value):
    if value is None:
        return None
    return value.strftime("%Y-%m-%d")+" "+value.strftime("%H:%M:%S")

def call_fernet_key():
    return open("pass.key", "rb").read()

def to_encrypt(value):
    f = Fernet( call_fernet_key())
    return f.encrypt(value.encode('UTF-8')).decode('UTF-8')

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(256), default=uuid.uuid4(), primary_key=True, autoincrement=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False, unique=True)
    fullname = db.Column(db.String(20), nullable=True, unique=True)
    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)

    @property
    def serialize(self):
        return {
           'id'         : to_encrypt(self.id),
           'username'      : self.username,
           'fullname'      : self.fullname,
           'password'      : self.password,
           'created_on'       : dump_datetime(self.created_on),
           'updated_on'       : dump_datetime(self.updated_on),
        }
    
    @property
    def serialize_excludepass(self):
        return {
           'id'         : to_encrypt(self.id),
           'username'      : self.username,
           'fullname'      : self.fullname,
           'created_on'       : dump_datetime(self.created_on),
           'updated_on'       : dump_datetime(self.updated_on),
        }

    def __repr__(self):
        return self.username

class Entrance(db.Model):
    __tablename__ = 'entrance'

    id = db.Column(db.String(256), default=uuid.uuid4(), primary_key=True, autoincrement=False)
    label = db.Column(db.String(20), nullable=False, unique=True)
    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    created_by = db.Column(db.String(256), db.ForeignKey('user.id'), nullable=False)
    updated_by = db.Column(db.String(256), db.ForeignKey('user.id'), nullable=False)
    
    author = db.relationship('User', foreign_keys=[created_by])
    rewriter = db.relationship('User', foreign_keys=[updated_by])

    @property
    def serialize(self):
        return {
           'id'         : self.id,
           'username'      : self.username,
           'password'      : self.password,
           'created_on'       : dump_datetime(self.created_on),
           'updated_on'       : dump_datetime(self.updated_on),
        }

    def __repr__(self):
        return self.label