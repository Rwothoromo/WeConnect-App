# run.py
"""Weconnect entry point"""

from flask import Flask
from flask_restful import Resource, Api

from app import app

app = Flask(__name__)               # Create Flask WSGI appliction
api = Api(app)    # Wrap the app in Api , prefix="/api/v1"


class HelloWorld(Resource):
    """HelloWorld resource which extends Resource"""

    # define what the get http verb will do
    def get(self):
        return {'hello': 'world'}

# When we write our Resources, Flask-RESTful generates the routes
# and the view handlers necessary to represent the resource over RESTful HTTP


# Add the resource to the API.
api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
