# run.py
"""Weconnect entry point"""

from flask import Flask, jsonify, request
from flask_restful import Resource, Api

from app import app

app = Flask(__name__)               # Create Flask WSGI appliction
api = Api(app, prefix="/api/v1")    # Wrap the app in Api

# users list of user dictionary objects
users = [
    {"first_name": "john", "last_name": "doe", "username": "johndoe", "password_hash": "password_hash"},
    {"first_name": "jane", "last_name": "len", "username": "janelen", "password_hash": "password_hash"},
    {"first_name": "jack", "last_name": "dan", "username": "jackdan", "password_hash": "password_hash"}
]

# When we write our Resources, Flask-RESTful generates the routes
# and the view handlers necessary to represent the resource over RESTful HTTP


class HelloWorld(Resource):
    """HelloWorld resource which extends Resource"""

    # define what the get http verb will do
    def get(self):
        return jsonify({'hello': 'world'})


class UserCollection(Resource):
    """User collection resource"""

    def get(self):
        """Return all users"""

        return jsonify({"msg": "All users "})

    def post(self):
        """Create users"""

        return jsonify({"msg": "We will create new users here"})


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
