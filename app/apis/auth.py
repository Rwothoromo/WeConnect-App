# app/apis/auth.py
"""Weconnect entry point"""

from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser

app = Flask(__name__)               # Create Flask WSGI appliction
api_v1 = Api(app, prefix="/api/v1")  # Wrap the app in Api

@app.route('/api/auth/register', methods=['POST'])
def register(self):
    """Creates a user account"""

    # request parsing code checks if the request is valid,
    # and returns the validated data, and an error otherwise
    args = user_request_parser.parse_args()
    users.append(args)

    return jsonify({"msg": "User added", "user_data": args})

@app.route('/api/auth/login', methods=['POST'])
def login(self):
    """Logs in a user"""
    
    return jsonify({"msg": "User logged in", "user_data": args})

@app.route('/api/auth/logout', methods=['POST'])
def logout(self):
    """Logs out a user"""
    
    return jsonify({"msg": "User logged in", "user_data": args})

@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password(self):
    """Password reset"""
    
    return jsonify({"msg": "User logged in", "user_data": args})


if __name__ == '__main__':
    app.run(debug=True)
