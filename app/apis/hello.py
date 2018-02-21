# run.py
"""Weconnect greeting"""

from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser


app = Flask(__name__)               # Create Flask WSGI appliction
api_v1 = Api(app, prefix="/api/v1") # Wrap the app in Api


# When we write our Resources, Flask-RESTful generates the routes
# and the view handlers necessary to represent the resource over RESTful HTTP


class HelloWorld(Resource):
    """HelloWorld resource which extends Resource"""

    # define what the get http verb will do
    def get(self):
        """Return greeting"""

        return jsonify({'WeConnect': 'WeConnect brings businesses and users together, and allows users to review businesses.'})


# Add the resource to the API.
api_v1.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
