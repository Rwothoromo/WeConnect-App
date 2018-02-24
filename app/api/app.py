# app/api/app.py
"""Weconnect api setup"""

from flask import Flask, Blueprint
from flask_restful import Api

from v1.resources.hello import HelloWorld
from v1.resources.user import UserResource, UserCollection, RegisterUser, LoginUser, ResetPassword, LogoutUser
from v1.resources.business import BusinessResource, BusinessCollection, BusinessReviews

app = Flask(__name__)                   # Create Flask WSGI appliction
api_bp = Blueprint('api', __name__)     # Add Blueprint; how to construct or extend the app
api = Api(api_bp, prefix="/api/v1")


# Add the resource to the API.
api.add_resource(HelloWorld, '/')
api.add_resource(UserCollection, '/users')
api.add_resource(UserResource, '/users/<string:username>')
api.add_resource(BusinessCollection, '/businesses')
api.add_resource(BusinessResource, '/businesses/<string:name>')
api.add_resource(BusinessReviews, '/businesses/<string:name>/reviews')
api.add_resource(RegisterUser, '/auth/register')
api.add_resource(LoginUser, '/auth/login')
api.add_resource(ResetPassword, '/auth/reset-password')
api.add_resource(LogoutUser, '/auth/logout')

app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)
