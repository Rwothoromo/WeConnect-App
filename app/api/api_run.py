# app/api/api_run.py
"""Weconnect api setup"""

import os
import sys
import inspect

from flask import Flask, Blueprint, redirect
from flask_restful import Api

from v1.resources.hello import HelloWorld
from v1.resources.auth import RegisterUser, LoginUser, ResetPassword, LogoutUser
from v1.resources.business import BusinessResource, BusinessCollection, BusinessReviews

# solution to python 3 relative import errors
# use the inspect module because for os.path.abspath(__file__),
# the __file__ attribute is not always given
api_run_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
api_dir = os.path.dirname(api_run_dir)
app_dir = os.path.dirname(api_dir)
sys.path.insert(0, app_dir)
# sys.path.append(os.path.dirname)


app = Flask(__name__)                   # Create Flask WSGI appliction
api_bp = Blueprint('api', __name__)     # Add Blueprint; how to construct or extend the app
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

if __name__ == '__main__':
    app.run(debug=True)
