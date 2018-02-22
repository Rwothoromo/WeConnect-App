# app/api/app.py
"""Weconnect api setup"""

from flask import Flask, Blueprint
from flask_restful import Api

from api.v1.resources.hello import HelloWorld
# from api.v1.resources.auth import Foo
from api.v1.resources.user import User, UserCollection
from api.v1.resources.business import Business, BusinessCollection

app = Flask(__name__)                   # Create Flask WSGI appliction
api_bp = Blueprint('api', __name__)     # Add Blueprint; how to construct or extend the app
api = Api(api_bp)


# Add the resource to the API.
api.add_resource(HelloWorld, '/')
api.add_resource(UserCollection, '/users')
api.add_resource(User, '/users/<string:username>')
api.add_resource(BusinessCollection, '/businesses')
api.add_resource(Business, '/businesses/<string:name>')

app.register_blueprint(api, url_prefix="/api/v1")
