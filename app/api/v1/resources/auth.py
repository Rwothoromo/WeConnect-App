# app/api/resources/auth.py
"""Contains user logic"""

import os
import sys
import inspect
import random
import datetime
import json

from functools import wraps

import jwt

from flask import jsonify, request, make_response
from flask_restful import Resource
from flask_restful.reqparse import RequestParser


# solution to python 3 relative import messages
# use the inspect module because for os.path.abspath(__file__),
# the __file__ attribute is not always given
auth_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
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
    {
        "user_id": 1,
        "user_data": {
            "first_name": "john", "last_name": "doe", "username": "johndoe",
            "password_hash": "password_hash"
        }
    }
]

# create initial user
init_user = User("john", "doe", "johndoe", "password_hash")
weconnect.register(init_user)

# RequestParser and added arguments will know which fields to accept and how to validate those
user_request_parser = RequestParser(bundle_errors=True)

user_request_parser.add_argument(
    "first_name", type=str, help="First name must be a valid string")

user_request_parser.add_argument(
    "last_name", type=str, help="Last name must be a valid string")

user_request_parser.add_argument(
    "username", type=str, required=True,
    help="Username must be a valid string")

user_request_parser.add_argument(
    "password_hash", type=str, required=True,
    help="Password is required")


def get_user_by_id(user_id):
    """Return user if user id matches"""

    for user in users:
        if user.get("user_id") == user_id:
            return user
    return None


def get_user_by_username(username):
    """Return user id if username matches"""

    for user in users:
        user_data = user.get("user_data")
        if user_data["username"] == username:
            return user
    return None


def token_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        access_token = None

        if 'Authorization' in request.headers:
            access_token = request.headers['Authorization'].split(' ')[1]

            if not access_token:
                # return jsonify({"message": "No token provided"}), 401
                return {"message": "No token provided"}, 401

            try:
                decoded_token = jwt.decode(
                    access_token, 'WECONNECTSECRET', algorithms=['HS256'])
                import ipdb
                ipdb.set_trace()
                user = get_user_by_id(decoded_token["sub"])
                request.data = json.loads(request.data)
                request.data['user'] = user
                
            except:
                # return jsonify({"message": "Invalid token provided"}), 401
                return {"message": "Invalid token provided"}, 401

            return function(*args, **kwargs)

    return decorated_function


# When we write our Resources, Flask-RESTful generates the routes
# and the view handlers necessary to represent the resource over RESTful HTTP


class UserCollection(Resource):
    """Retrieve all users or create them"""

    @token_required
    def get(self):
        """Return all users"""

        # return jsonify(users)
        return jsonify(users)

    @token_required
    def post(self):
        """Create users"""

        # request parsing code checks if the request is valid,
        # and returns the validated data, and an message otherwise
        args = user_request_parser.parse_args()

        user = get_user_by_username(args.username)
        if not user:
            user_id = len(users) + 1
            user_object = User(args.first_name, args.last_name,
                               args.username, args.password_hash)
            weconnect.register(user_object)

            user = {"user_id": user_id, "user_data": args}
            users.append(user)
            # Post success
            # return jsonify({"message": "User added", "user": user}), 200
            return {"message": "User added", "user": user}, 200

        # return jsonify({"message": "User already exists"}), 400
        return {"message": "User already exists"}, 400


class UserResource(Resource):
    """Retrieve, update or delete a single user"""

    @token_required
    def get(self, user_id):
        """Return a user's details"""

        user = get_user_by_id(user_id)
        if not user:
            # return jsonify({"message": "User not found"}), 404
            return {"message": "User not found"}, 404

        # return jsonify({"user": user}), 200
        return {"user": user}, 200

    @token_required
    def put(self, user_id):
        """Update a user's details"""

        args = user_request_parser.parse_args()
        user = get_user_by_id(user_id)
        if user:
            user_object = User(args.first_name, args.last_name,
                               args.username, args.password_hash)
            weconnect.edit_user(user_object)
            users.remove(user)
            user_data = {"user_id": user_id, "user_data": args}
            users.append(user_data)
            # Post success
            # return jsonify({"message": "User updated", "user_data": user_data}), 200
            return {"message": "User updated", "user_data": user_data}, 200

        # return jsonify({"message": "User not found"}), 404
        return {"message": "User not found"}, 404

    @token_required
    def delete(self, user_id):
        """Delete a user"""

        user = get_user_by_id(user_id)
        if user:
            data = user.get("user_data")
            username = data["username"]
            weconnect.delete_user(username)
            users.remove(user)
            # return jsonify({"message": "User deleted"}), 200
            return {"message": "User deleted"}, 200

        # return jsonify({"message": "User not found"}), 404
        return {"message": "User not found"}, 404


class RegisterUser(Resource):
    """Register a user"""

    def post(self):
        """Creates a user account"""

        args = user_request_parser.parse_args()

        user = get_user_by_username(args.username)
        if not user:
            user_id = len(users) + 1
            user_object = User(args.first_name, args.last_name,
                               args.username, args.password_hash)
            weconnect.register(user_object)

            user = {"user_id": user_id, "user_data": args}
            users.append(user)
            # Post success
            # return jsonify({"message": "User added", "user": user}), 200
            return {"message": "User added", "user": user}, 200

        # return jsonify({"message": "User already exists"}), 400
        return {"message": "User already exists"}, 400


class LoginUser(Resource):
    """Login a user"""

    def post(self):
        """Logs in a user and create a token for them"""

        args = request.get_json()

        response_data = {"message": "fail", "user": args}

        logged_in_user = weconnect.login(args["username"], args["password_hash"])

        if isinstance(logged_in_user, User):
            user = get_user_by_username(args["username"])

            access_token = jwt.encode(
                {
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=60),
                    "iat": datetime.datetime.utcnow(),
                    "sub": user.get("user_id")
                }, 'WECONNECTSECRET', algorithm='HS256')

            response_data["message"] = "User logged in"
            response_data["user"] = user
            response_data["access_token"] = access_token.decode()
            response = jsonify(response_data)
            response.status_code = 200 # Post success
            return response

        response_data["message"] = logged_in_user
        response = jsonify(response_data)
        response.status_code = 400 # Bad request
        return response


class ResetPassword(Resource):
    """Password reset"""

    @token_required
    def post(self):
        """Reset a password if token is valid"""

        args = request.get_json()     

        response_data = {"message": "fail", "user": args}

        user = request.data['user']

        if user:
            user_data = user.get("user_data")

            if args["password_hash"] == user_data["password_hash"]:
                password_hash = 'Chang3m3' + str(random.randrange(10000))
                user_object = User(user_data["first_name"], user_data["last_name"], user_data["username"], password_hash)
                weconnect.edit_user(user_object)

                users.remove(user)
                args = {"username": "johndoe", "password_hash": password_hash}
                user_data = {"user_id": user.get("user_id"), "user_data": args}
                users.append(user_data)

                response_data["message"] = "User password reset"
                response_data["user"] = user_data
                response = jsonify(response_data)
                response.status_code = 200 # Post update success

            response = jsonify(response_data)
            response.status_code = 400 # Bad request
            return response

        response_data["message"] = "User not found"
        response = jsonify(response_data)
        response.status_code = 400 # Bad request
        return response


class LogoutUser(Resource):
    """Logs out a user if token is valid"""

    @token_required
    def post(self):
        """Logs out a user"""

        try:
            if 'access_token' in request.headers:
                request.headers['access_token'] = None
                # return jsonify({'message':"Successfully logged out"}), 200
                return {'message':"Access token revoked"}, 200

        except:
            # return jsonify({'message': 'Something went wrong'}), 500
            return {'message': 'Something went wrong'}, 500
