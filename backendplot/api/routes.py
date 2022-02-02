from flask import jsonify
from flask_restful import Resource, Api
from .models import db, User

api = Api()
class BackendTest(Resource):
    def get(self):
        return jsonify(users=[i.serialize for i in User.query.all()])

class ApiTest(Resource):
    def get(self):
        return {'Api': True}

# class TestPost(Resource):
#     def get(self, title):
#         dataTest = Test(title=title,date="2021-03-24")
#         db.session.add(dataTest)
#         db.session.commit()
#         return {'in':'Yes'}

api.add_resource(BackendTest, '/')
api.add_resource(ApiTest, '/api/')
# api.add_resource(TestPost, '/post/<string:title>')
