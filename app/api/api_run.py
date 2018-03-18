# app/api/api_run.py
"""Weconnect api setup"""

import os
import sys
import inspect

from flask import Flask, Blueprint, redirect
from flask_restful import Api
from flasgger import Swagger


# solution to python 3 relative import errors
# use the inspect module because for os.path.abspath(__file__),
# the __file__ attribute is not always given
api_run_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
api_dir = os.path.dirname(api_run_dir)
app_dir = os.path.dirname(api_dir)
sys.path.insert(0, app_dir)
# sys.path.append(os.path.dirname)

from app.api.v1.resources.hello import HelloWorld
from app.api.v1.resources.auth import RegisterUser, LoginUser, ResetPassword, LogoutUser
from app.api.v1.resources.business import BusinessResource, BusinessCollection, BusinessReviews

app = Flask(__name__)                   # Create Flask WSGI appliction

app.config['SWAGGER'] = {
    'swagger': '2.0',
    'title': 'WeConnect API',
    'description': "This API allows users to create and review businesses",
    'basePath': '',
    'version': '1',
    'contact': {
        'Developer': 'Elijah Rwothoromo',
        'Profile': 'https://github.com/Rwothoromo'
    },
    'license': {
    },
    'tags': [
        {
            'name': 'User',
            'description': 'The API user'
        },
        {
            'name': 'Business',
            'description': 'A business can be added, updated, reviewed or deleted by a user'
        },
        {
            'name': 'WeConnect',
            'description': 'WeConnect brings businesses and users together, and allows users to review businesses'
        },
    ]
}

swagger = Swagger(app)

# Add Blueprint; how to construct or extend the app
api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix="/api/v1")


# Add the resource to the API.
api.add_resource(HelloWorld, '/')
api.add_resource(BusinessCollection, '/businesses')
api.add_resource(BusinessResource, '/businesses/<int:business_id>')
api.add_resource(BusinessReviews, '/businesses/<int:business_id>/reviews')
api.add_resource(RegisterUser, '/auth/register')
api.add_resource(LoginUser, '/auth/login')
api.add_resource(ResetPassword, '/auth/reset-password')
api.add_resource(LogoutUser, '/auth/logout')

app.register_blueprint(api_bp)


@app.route('/')
def main():
    """Redirect to api endpoints"""

    return redirect('/api/v1/')


if __name__ == '__main__': # pragma: no cover
    app.run()
