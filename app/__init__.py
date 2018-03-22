# app/__init__.py
"""Initializes the app module"""

import os

# third-party imports
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flasgger import Swagger

# local imports
from config import app_config
from app.db import db

from app.api.v2.resources.hello import HelloWorld
from app.api.v2.resources.auth import RegisterUser, LoginUser, ResetPassword, LogoutUser
from app.api.v2.resources.business import BusinessCollection# , BusinessResource, BusinessReviews

app = Flask(__name__)
app.config.from_object(app_config[os.environ['FLASK_CONFIG']])

app.config['SWAGGER'] = {
    'swagger': '2.0',
    'title': 'WeConnect API',
    'description': "This API allows users to create and review businesses",
    'basePath': '',
    'version': '2',
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

# db = SQLAlchemy(app)
db.init_app(app)

# Add Blueprint; how to construct or extend the app
api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix="/api/v2")


# Add the resource to the API.
api.add_resource(HelloWorld, '/')
api.add_resource(BusinessCollection, '/businesses')
# api.add_resource(BusinessResource, '/businesses/<int:business_id>')
# api.add_resource(BusinessReviews, '/businesses/<int:business_id>/reviews')
api.add_resource(RegisterUser, '/auth/register')
api.add_resource(LoginUser, '/auth/login')
api.add_resource(ResetPassword, '/auth/reset-password')
api.add_resource(LogoutUser, '/auth/logout')

app.register_blueprint(api_bp)
