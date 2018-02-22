# app/api/app.py
"""Weconnect api setup"""

from flask import Flask, Blueprint
from flask_restful import Api

from v1.resources.hello import HelloWorld
from v1.resources.user import User, UserCollection
from v1.resources.business import Business, BusinessCollection, BusinessReviews
from v1.resources.auth import auth_blueprint

app = Flask(__name__)                   # Create Flask WSGI appliction
api_bp = Blueprint('api', __name__)     # Add Blueprint; how to construct or extend the app
api = Api(api_bp, prefix="/api/v1")


# Add the resource to the API.
api.add_resource(HelloWorld, '/')
api.add_resource(UserCollection, '/users')
api.add_resource(User, '/users/<string:username>')
api.add_resource(BusinessCollection, '/businesses')
api.add_resource(Business, '/businesses/<string:name>')
api.add_resource(BusinessReviews, '/businesses/<string:name>/reviews')

app.register_blueprint(api_bp)
app.register_blueprint(auth_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
