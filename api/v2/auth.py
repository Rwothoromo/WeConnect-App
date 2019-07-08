# app/api/resources/auth.py

import os
import sys
import inspect
import random
import datetime
import json

from functools import wraps

import jwt

from flask import jsonify, request, make_response, session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flasgger import swag_from
from werkzeug.security import check_password_hash, generate_password_hash


# solution to python 3 relative import messages
# use the inspect module because for os.path.abspath(__file__),
# the __file__ attribute is not always given
auth_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
resources_dir = os.path.dirname(auth_dir)
v2_dir = os.path.dirname(resources_dir)
api_dir = os.path.dirname(v2_dir)
app_dir = os.path.dirname(api_dir)
sys.path.insert(0, app_dir)

from api.db import db
from api.v2.models.blacklist import Blacklist
from api.v2.models.user import User
from api.v2.models.log import Log


secret_key = os.environ.get('SECRET_KEY', 'MEGAtron35648')


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


def validate_inputs(args):
    """Return error message if input is invalid"""

    fifty_character_limit = ['first_name', 'last_name', 'username', 'password', 'name', 'category', 'location']
    for key, value in args.items():
        valid_length = 50 if key in fifty_character_limit else 256
        arg_is_invalid = (len(value) > valid_length or not isinstance(value, str) or not value.strip(), \
                            valid_length, key)
        if arg_is_invalid[0]:
            return arg_is_invalid


def token_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        access_token = None

        if "Authorization" in request.headers:
            authorization = request.headers.get("Authorization", None)
            if authorization:
                authorization_list = authorization.split(" ")
                if len(authorization_list) > 1:
                    access_token = authorization_list[1]

            if not access_token:
                return {"message": "No token provided"}, 401

            if Blacklist.query.filter_by(token=access_token).first():
                return {"message": "Invalid token provided"}, 401

            try:
                decoded_token = jwt.decode(
                    access_token, secret_key, algorithms=["HS256"])
                sub = decoded_token.get("sub", None)
                user = User.query.get(sub)
            except (jwt.InvalidTokenError, IndexError, db.NoResultFound):
                return {"message": "Invalid token provided"}, 401
            else:
                request.data = json.loads(request.data.decode()) if request.data else {}
                request.data["user"] = user

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
        
        invalid_input = validate_inputs(args)
        if invalid_input:
            return make_response(jsonify({"message": "{} must be a string of maximum {} characters".format(invalid_input[2], invalid_input[1])}), 400)

        first_name = args.get("first_name", None)
        last_name = args.get("last_name", None)
        username = args.get("username", None)
        password = args.get("password", None)

        if username:
            username = username.lower()

        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(first_name, last_name, username, password)
            db.session.add(user)
            db.session.commit()

            user = User.query.filter_by(username=username).first()
            log = Log(
                "Insert", "Added user: {}".format(username), "users", user.id)
            db.session.add(log)
            db.session.commit()

            return make_response(jsonify({"message": "User added"}), 201)

        return make_response(jsonify({"message": "User already exists"}), 409)


class LoginUser(Resource):
    """Login a user"""

    @swag_from('docs/login_user.yml')
    def post(self):
        """Logs in a user and create a token for them"""

        response_data = {"message": "Login failed"}

        args = request.get_json()

        invalid_input = validate_inputs(args)
        if invalid_input:
            return make_response(jsonify({"message": "{} must be a string of maximum {} characters".format(invalid_input[2], invalid_input[1])}), 400)

        username = args.get("username", None)
        password = args.get("password", None)

        if username:
            username = username.lower()

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password_hash, password):
                access_token = jwt.encode(
                    {
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                        "iat": datetime.datetime.utcnow(),
                        "sub": user.id
                    }, secret_key, algorithm="HS256")

                session["user_id"] = user.id

                log = Log(
                    "Login", "Logged in user: {}".format(username), "users", user.id)
                db.session.add(log)
                db.session.commit()

                response_data["message"] = "User logged in"
                response_data["username"] = user.username
                response_data["first_name"] = user.first_name
                response_data["last_name"] = user.last_name
                response_data["access_token"] = access_token.decode()
                response = jsonify(response_data)
                response.status_code = 200
                return response

            response_data["message"] = "Incorrect username and password combination!"
            response = jsonify(response_data)
            response.status_code = 401
            return response

        response_data["message"] = "Incorrect username and password combination!"
        response = jsonify(response_data)
        response.status_code = 401
        return response


class ResetPassword(Resource):
    """Password reset"""

    @token_required
    @swag_from('docs/reset_password.yml')
    def post(self):
        """Reset a password if token is valid"""

        response_data = {"message": "fail"}

        user_data = request.data["user"]
        user = User.query.filter_by(id=user_data.id).first()

        password = "Chang3m3" + str(random.randrange(10000))
        user.password_hash = generate_password_hash(password)
        db.session.commit()

        log1 = Log("Update", "Updated password for user: {}".format(
            user.username), "users", user_data.id)
        db.session.add(log1)
        db.session.commit()

        response_data["message"] = "User password reset"
        response_data["new_password"] = password
        response = jsonify(response_data)
        response.status_code = 200

        authorization = request.headers.get("Authorization", None)
        if authorization:
            token = authorization.split(" ")[1]
        token_blacklist = Blacklist(token)
        db.session.add(token_blacklist)
        db.session.commit()

        log2 = Log("Insert", "Revoked token for user: {}".format(
            user.username), "blacklists", user_data.id)
        db.session.add(log2)
        db.session.commit()

        session["user_id"] = None

        return response


class LogoutUser(Resource):
    """Logs out a user if token is valid"""

    @token_required
    @swag_from('docs/logout.yml')
    def post(self):
        """Logs out a user"""

        authorization = request.headers.get("Authorization", None)
        if authorization:
            token = authorization.split(" ")[1]
        token_blacklist = Blacklist(token)

        db.session.add(token_blacklist)
        db.session.commit()

        user_data = request.data["user"]
        log = Log("Insert", "Revoked token for user: {}".format(
            user_data.username), "blacklists", user_data.id)
        db.session.add(log)
        db.session.commit()

        session["user_id"] = None

        return make_response(jsonify({"message": "Logged out successfully"}), 200)
