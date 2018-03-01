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
from flasgger import swag_from


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

secret_key = os.environ.get('SECRET_KEY') if os.environ.get('SECRET_KEY') else 'MEGAtron35648'

# users list of user dictionary objects
users = []

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
    "password", type=str, required=True,
    help="Password is required")

def string_empty(string_var):
    """Return true if string is empty"""

    if not isinstance(string_var, str) or string_var in [' ', '']:
        return True
    return False

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

        if "Authorization" in request.headers:
            access_token = request.headers["Authorization"].split(" ")[1]

            if not access_token:
                return {"message": "No token provided"}, 401

            if access_token in weconnect.token_blacklist:
                return {"message": "Invalid token provided"}, 401

            try:
                decoded_token = jwt.decode(
                    access_token, secret_key, algorithms=["HS256"])

                user = get_user_by_id(decoded_token["sub"])
                if user:
                    request.data = json.loads(
                        request.data) if len(request.data) else {}
                    request.data["user"] = user

            except:
                return {"message": "Invalid token provided"}, 401

            return function(*args, **kwargs)
        else:
            return {"message": "No token provided"}, 401

    return decorated_function


# When we write our Resources, Flask-RESTful generates the routes
# and the view handlers necessary to represent the resource over RESTful HTTP


class RegisterUser(Resource):
    """Register a user"""

    @swag_from('docs/post_user.yml')
    def post(self):
        """Creates a user account"""

        args = user_request_parser.parse_args()
        for key, value in args.items():
            if string_empty(value):
                return make_response(jsonify({"message": key+" must be supplied"}), 400)

        user = get_user_by_username(args["username"])
        if not user:
            user_id = len(users) + 1
            user_object = User(args["first_name"], args["last_name"],
                               args["username"], args["password"])
            weconnect.register(user_object)

            user = {"user_id": user_id, "user_data": args}
            users.append(user)
            # Post create success
            return make_response(jsonify({"message": "User added"}), 201)

        # Bad request
        return make_response(jsonify({"message": "User already exists"}), 409)


class LoginUser(Resource):
    """Login a user"""

    @swag_from('docs/login_user.yml')
    def post(self):
        """Logs in a user and create a token for them"""

        args = request.get_json()
        for key, value in args.items():
            if string_empty(value):
                return make_response(jsonify({"message": key+" must be supplied"}), 400)

        response_data = {"message": "Login failed"}

        logged_in_user = weconnect.login(
            args["username"], args["password"])

        if isinstance(logged_in_user, User):
            user = get_user_by_username(args["username"])

            access_token = jwt.encode(
                {
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    "iat": datetime.datetime.utcnow(),
                    "sub": user.get("user_id")
                }, secret_key, algorithm="HS256")

            response_data["message"] = "User logged in"
            response_data["access_token"] = access_token.decode()
            response = jsonify(response_data)
            response.status_code = 200  # Post success
            return response

        response_data["message"] = logged_in_user
        response = jsonify(response_data)
        response.status_code = 400  # Bad request
        return response


class ResetPassword(Resource):
    """Password reset"""

    @token_required
    def post(self):
        """Reset a password if token is valid"""

        response_data = {"message": "fail"}

        user = request.data["user"]

        if user:
            user_data = user.get("user_data")

            password = "Chang3m3" + str(random.randrange(10000))
            user_object = User(
                user_data["first_name"], user_data["last_name"], user_data["username"], password)
            weconnect.edit_user(user_object)

            users.remove(user)
            args = {
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "username": user_data["username"],
                "password": password
            }
            user_data = {"user_id": user.get("user_id"), "user_data": args}
            users.append(user_data)

            response_data["message"] = "User password reset"
            response_data["user"] = user_data
            response = jsonify(response_data)
            response.status_code = 200  # Post update success
            return response

        response_data["message"] = "User not found"
        response = jsonify(response_data)
        response.status_code = 400  # Bad request
        return response


class LogoutUser(Resource):
    """Logs out a user if token is valid"""

    @token_required
    def post(self):
        """Logs out a user"""

        try:
            token = request.headers["Authorization"].split(" ")[1]
            weconnect.token_blacklist.append(token)
            return make_response(jsonify({"message": "Access token revoked"}), 200)

        except:
            return make_response(jsonify({"message": "Something went wrong"}), 500)
