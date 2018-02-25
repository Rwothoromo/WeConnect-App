# app/api/resources/auth.py
"""Contains user logic"""

import random
import os
import sys
import inspect

from flask import jsonify
from flask_restful import Resource, fields
from flask_restful.reqparse import RequestParser


# solution to python 3 relative import errors
# use the inspect module because for os.path.abspath(__file__), 
# the __file__ attribute is not always given
auth_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
resources_dir = os.path.dirname(auth_dir)
v1_dir = os.path.dirname(resources_dir)
api_dir = os.path.dirname(v1_dir)
app_dir = os.path.dirname(api_dir)
sys.path.insert(0, app_dir)
# sys.path.append(os.path.dirname)

from app.models.weconnect import WeConnect
from app.models.user import User


weconnect = WeConnect()

# users list of user dictionary objects
users = [
    {"first_name": "john", "last_name": "doe",
     "username": "johndoe", "password_hash": "password_hash"}
]

# create initial user
init_user = User("john", "doe", "johndoe", "password_hash")
weconnect.register(init_user)

# RequestParser and added arguments will know which fields to accept and how to validate those
user_request_parser = RequestParser(bundle_errors=True)

user_request_parser.add_argument(
    "first_name", type=str, required=True,
    help="First name must be a valid string")

user_request_parser.add_argument(
    "last_name", type=str, required=True,
    help="Last name must be a valid string")

user_request_parser.add_argument(
    "username", type=str, required=True,
    help="Username must be a valid string")

user_request_parser.add_argument(
    "password_hash", type=str, required=True,
    help="Password is required")


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

    def get(self):
        """Return all users"""

        return jsonify(users)

    def post(self):
        """Create users"""

        # request parsing code checks if the request is valid,
        # and returns the validated data, and an error otherwise
        args = user_request_parser.parse_args()

        user = get_user(args.username)
        if not user:
            user_object = User(args.first_name, args.last_name,
                        args.username, args.password_hash)
            reg_user = weconnect.register(user_object)

            if isinstance(reg_user, User):
                users.append(args)
                # Post success
                return jsonify({"message": "User added", "user_data": args})
            else:
                # Unprocessable entity
                return jsonify({"message": reg_user, "user_data": args})

        return jsonify({"error": "User already exists"})


class UserResource(Resource):
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
            user_object = User(args.first_name, args.last_name,
                        args.username, args.password_hash)
            updated_user = weconnect.edit_user(user_object)

            if isinstance(updated_user, User):
                users.remove(user)
                users.append(args)
                # Post success
                return jsonify({"message": "User updated", "user_data": args})
            else:
                # Unprocessable entity
                return jsonify({"message": updated_user, "user_data": args})

        return jsonify({"error": "User not found"})

    def delete(self, username):
        """Delete a user"""

        user = get_user(username)
        if user:
            users.remove(user)

        return jsonify({"message": "User deleted"})


class RegisterUser(Resource):
    """Register a user"""

    def post(self):
        """Creates a user account"""

        # request parsing code checks if the request is valid,
        # and returns the validated data, and an error otherwise
        args = user_request_parser.parse_args()
        user = User(args.first_name, args.last_name,
                    args.username, args.password_hash)
        reg_user = weconnect.register(user)

        if isinstance(reg_user, User):
            users.append(args)
            # Post success
            return jsonify({"message": "User added", "user_data": args})
        else:
            # Unprocessable entity
            return jsonify({"message": reg_user, "user_data": args})


class LoginUser(Resource):
    """Login a user"""

    def post(self):
        """Logs in a user"""

        args = user_request_parser.parse_args()

        logged_in_user = weconnect.login(args.username, args.password_hash)

        if isinstance(logged_in_user, User):
            # Post success
            return jsonify({"message": "User logged in", "user_data": args})
        else:
            # Unprocessable entity
            return jsonify({"message": logged_in_user, "user_data": args})


class ResetPassword(Resource):
    """Password reset"""

    def post(self):
        """Password reset"""

        args = user_request_parser.parse_args()
        user = get_user(args.username)
        if user:
            args.password_hash = 'Chang3m3'+str(random.randrange(10000))
            user_object = User(args.first_name, args.last_name,
                        args.username, args.password_hash)
            updated_user = weconnect.edit_user(user_object)

            if isinstance(updated_user, User):
                users.remove(user)
                users.append(args)
                # Post success
                return jsonify({"message": "User password reset", "user_data": args})
            else:
                # Unprocessable entity
                return jsonify({"message": updated_user, "user_data": args})

        return jsonify({"error": "User not found"})


class LogoutUser(Resource):
    """Logs out a user"""

    def post(self):
        """Logs out a user"""

        args = user_request_parser.parse_args()

        # Post success
        return jsonify({"message": "User logged out", "user_data": args})
