# app/api/resources/user.py
"""Contains user logic"""

from flask import Flask, jsonify
from flask_restful import Resource, fields, marshal_with
from flask_restful.reqparse import RequestParser

import sys
# from .user import User
# from app.models.weconnect import WeConnect

# weconnect = WeConnect()

# marshal_with Takes raw data (in the form of a dict, list, object) 
# and a dict of fields to output and filters the data based on those fields.

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
    "first_name", dest="first_name", location="form", type=str, required=True, help="First name must be a valid string")
user_request_parser.add_argument(
    "last_name", dest="last_name", location="form", type=str, required=True, help="Last name must be a valid string")
user_request_parser.add_argument(
    "username", dest="username", location="form", type=str, required=True, help="Username must be a valid string")
user_request_parser.add_argument(
    "password_hash", dest="password_hash", location="form", type=str, required=True, help="Password is required")

user_fields = {
    'first_name': fields.String,
    'last_name': fields.String,
    'username': fields.String,
    'password_hash': fields.String,
}


def get_user(username):
    """Return user if username matches"""

    for user in users:
        if user.get("username") == username:
            return user
    return None


# When we write our Resources, Flask-RESTful generates the routes
# and the view handlers necessary to represent the resource over RESTful HTTP


class UserCollection(Resource):
    """User collection resource"""

    @marshal_with(user_fields)
    def get(self):
        """Return all users"""

        return jsonify(users)

    @marshal_with(user_fields)
    def post(self):
        """Create users"""

        # request parsing code checks if the request is valid,
        # and returns the validated data, and an error otherwise
        args = user_request_parser.parse_args()
        # users.append(args)
        # user = create_user(args.first_name, args.last_name, args.username, args.password_hash)

        return jsonify({"msg": "User added", "user_data": args})


class UserResource(Resource):
    """User resource"""

    @marshal_with(user_fields)
    def get(self, username):
        """Return a user's details"""

        user = get_user(username)
        if not user:
            return jsonify({"error": "User not found"})

        return jsonify(user)

    @marshal_with(user_fields)
    def put(self, username):
        """Update a user's details"""

        args = user_request_parser.parse_args()
        user = get_user(username)
        if user:
            users.remove(user)
            users.append(args)

        return jsonify(args)

    @marshal_with(user_fields)
    def delete(self, username):
        """Delete a user"""

        user = get_user(username)
        if user:
            users.remove(user)

        return jsonify({"message": "Deleted"})

class RegisterUser(Resource):
    """Register a user"""

    @marshal_with(user_fields)
    def post(self):
        """Creates a user account"""

        # request parsing code checks if the request is valid,
        # and returns the validated data, and an error otherwise
        args = user_request_parser.parse_args()
        users.append(args)
        user_object = User(args.first_name, args.last_name, args.username, args.password_hash)
        user = weconnect.register(user_object)
        if isinstance(user, User):
            return jsonify({"message": "User added", "user_data": args}), 201 # Post success

class LoginUser(Resource):
    """Login a user"""

    @marshal_with(user_fields)
    def post(self):
        """Logs in a user"""

        args = user_request_parser.parse_args()

        return jsonify({"message": "User logged in", "user_data": args}), 201 # Post success

class ResetPassword(Resource):
    """Password reset"""

    @marshal_with(user_fields)
    def post(self):
        """Password reset"""

        args = user_request_parser.parse_args()
    
        return jsonify({"message": "Password reset", "user_data": args}), 201 # Post success

class LogoutUser(Resource):
    """Logs out a user"""

    @marshal_with(user_fields)
    def post(self):
        """Logs out a user"""

        args = user_request_parser.parse_args()
    
        return jsonify({"message": "User logged out", "user_data": args}), 201 # Post success
