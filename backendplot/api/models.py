from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d")+" "+value.strftime("%H:%M:%S")


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256), unique=True)
    salt = db.Column(db.String(256), unique=True)
    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    @property
    def serialize(self):
        return {
           'id'         : self.id,
           'username'      : self.username,
           'created_on'       : dump_datetime(self.created_on),
           'updated_on'       : dump_datetime(self.updated_on),
        }

    def __repr__(self):
        return self.title

# class Entrance(db.Model):
#     __tablename__ = 'entrance'
#     id = db.Column(db.Integer, primary_key=True)
#     label = db.Column(db.String(255), unique=True)
#     created_on = db.Column(db.DateTime)
#     updated_on = db.Column(db.DateTime, default=datetime.datetime.utcnow())

#     def __repr__(self):
#         return self.title