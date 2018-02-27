# app/api/v1/resources/hello.py
"""Contains simple greeting logic"""

from flask import jsonify
from flask_restful import Resource


# When we write our Resources, Flask-RESTful generates the routes
# and the view handlers necessary to represent the resource over RESTful HTTP


class HelloWorld(Resource):
    """HelloWorld resource which extends Resource"""

    # define what the get http verb will do
    def get(self):
        """Return greeting"""

        return jsonify({'WeConnect': 'WeConnect brings businesses and users together, and allows users to review businesses.'})