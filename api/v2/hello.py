# app/api/v2/resources/hello.py

from flask import jsonify, make_response
from flask_restful import Resource
from flasgger import swag_from


# When we write our Resources, Flask-RESTful generates the routes
# and the view handlers necessary to represent the resource over RESTful HTTP


class HelloWorld(Resource):
    """HelloWorld resource which extends Resource"""

    # define what the get http verb will do
    @swag_from('docs/hello.yml')
    def get(self):
        """Return greeting"""

        return make_response(jsonify({'WeConnect': 'WeConnect brings businesses and users together, and allows users to review businesses'}), 200)
