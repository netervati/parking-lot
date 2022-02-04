from flask_sqlalchemy import SQLAlchemy
import datetime
import uuid

db = SQLAlchemy()

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d")+" "+value.strftime("%H:%M:%S")


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(256), default=uuid.uuid4(), primary_key=True, autoincrement=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False, unique=True)
    salt = db.Column(db.String(256), unique=True)
    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    @property
    def serialize(self):
        return {
           'id'         : self.id,
           'username'      : self.username,
           'password'      : self.password,
           'created_on'       : dump_datetime(self.created_on),
           'updated_on'       : dump_datetime(self.updated_on),
        }
    
    @property
    def serialize_excludepass(self):
        return {
           'id'         : self.id,
           'username'      : self.username,
           'created_on'       : dump_datetime(self.created_on),
           'updated_on'       : dump_datetime(self.updated_on),
        }

    def __repr__(self):
        return self.title

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
        return self.title