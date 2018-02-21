# run.py
"""Weconnect entry point"""

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser

from app import app

app = Flask(__name__)               # Create Flask WSGI appliction
api = Api(app, prefix="/api/v1")    # Wrap the app in Api

# users list of user dictionary objects
users = [
    {"first_name": "john", "last_name": "doe",
        "username": "johndoe", "password_hash": "password_hash"},
    {"first_name": "jane", "last_name": "len",
        "username": "janelen", "password_hash": "password_hash"},
    {"first_name": "jack", "last_name": "dan",
        "username": "jackdan", "password_hash": "password_hash"}
]

# RequestParser and added arguments will know which fields to accept and how to validate those
user_request_parser = RequestParser(bundle_errors=True)
user_request_parser.add_argument(
    "first_name", type=str, required=True, help="First name must be a valid string")
user_request_parser.add_argument(
    "last_name", type=str, required=True, help="Last name must be a valid string")
user_request_parser.add_argument(
    "username", type=str, required=True, help="Username must be a valid string")
user_request_parser.add_argument("password_hash", required=True)


# When we write our Resources, Flask-RESTful generates the routes
# and the view handlers necessary to represent the resource over RESTful HTTP


class HelloWorld(Resource):
    """HelloWorld resource which extends Resource"""

    # define what the get http verb will do
    def get(self):
        """Return greeting"""

        return jsonify({'WeConnect': 'WeConnect brings businesses and users together, and allows users to review businesses.'})


class UserCollection(Resource):
    """User collection resource"""

    def get(self):
        """Return all users"""

        return jsonify({"msg": "All users "})

    def post(self):
        """Create users"""

        # request parsing code checks if the request is valid,
        # and returns the validated data, and an error otherwise
        args = user_request_parser.parse_args()
        users.append(args)

        return jsonify({"msg": "User added", "user_data": args})


class User(Resource):
    """User resource"""

    def get(self, username):
        """Return a user's details"""

        return jsonify({"msg": "Details about user : {}".format(username)})

    def put(self, username):
        """Update a user's details"""

        return jsonify({"msg": "Update user user : {}".format(username)})

    def delete(self, username):
        """Delete a user"""

        return jsonify({"msg": "Delete user user : {}".format(username)})


# Add the resource to the API.
api.add_resource(HelloWorld, '/')
api.add_resource(UserCollection, '/users')
api.add_resource(User, '/users/<string:username>')

if __name__ == '__main__':
    app.run(debug=True)
