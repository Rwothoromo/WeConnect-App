# app/api/resources/user.py
"""Contains user logic"""

from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser

app = Flask(__name__)               # Create Flask WSGI appliction
api_v1 = Api(app, prefix="/api/v1")  # Wrap the app in Api

# users list of user dictionary objects
users = [
    {"first_name": "john", "last_name": "doe",
     "username": "johndoe", "password_hash": "password_hash"},
    {"first_name": "jane", "last_name": "len",
     "username": "janelen", "password_hash": "password_hash"},
    {"first_name": "jack", "last_name": "dan",
     "username": "jackdan", "password_hash": "password_hash"}
]


def get_user(username):
    """Return user if username matches"""

    for user in users:
        if user.get("username") == username:
            return user
    return None


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


class UserCollection(Resource):
    """User collection resource"""

    def get(self):
        """Return all users"""

        return jsonify(users)

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

        user = get_user(username)
        if not user:
            return jsonify({"error": "User not found"})

        return jsonify(user)

    def put(self, username):
        """Update a user's details"""

        args = user_request_parser.parse_args()
        user = get_user(username)
        if user:
            users.remove(user)
            users.append(args)

        return jsonify(args)

    def delete(self, username):
        """Delete a user"""

        user = get_user(username)
        if user:
            users.remove(user)

        return jsonify({"message": "Deleted"})


# Add the resource to the API.
api_v1.add_resource(UserCollection, '/users')
api_v1.add_resource(User, '/users/<string:username>')

if __name__ == '__main__':
    app.run(debug=True)
