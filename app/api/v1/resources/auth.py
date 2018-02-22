# app/api/resources/auth.py
"""Contains auth logic"""

from flask import Flask, Blueprint, jsonify
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser

auth_blueprint = Blueprint('auth', __name__)

# users list of user dictionary objects
users = []


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


@auth_blueprint.route('/api/auth/register', methods=['POST'])
def register():
    """Creates a user account"""

    # request parsing code checks if the request is valid,
    # and returns the validated data, and an error otherwise
    args = user_request_parser.parse_args()
    users.append(args)

    return jsonify({"msg": "User added", "user_data": args}), 201 # Post success

@auth_blueprint.route('/api/auth/login', methods=['POST'])
def login():
    """Logs in a user"""
    
    return jsonify(users), 201 # Post success

@auth_blueprint.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logs out a user"""
    
    return jsonify(users), 201 # Post success

@auth_blueprint.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    """Password reset"""
    
    return jsonify(users), 201 # Post success
