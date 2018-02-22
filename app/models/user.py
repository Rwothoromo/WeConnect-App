# app/models/user.py
"""Script for creating User class objects"""

# Third party imports
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from app import app
import datetime, jwt

class User(UserMixin):
    """User class"""

    def __init__(self, first_name, last_name, username, password_hash):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password_hash = generate_password_hash(password_hash)
        self.businesses = {}
        self.reviews = {}
        self.categories = {}
        self.locations = {}

    def encode_auth_token(self, username):
        """
        Generates the Auth Token, given a user id, 
        Token is created from the payload and the secret key set in the config.py file
        :return: string
        """

        # exp: expiration date of the token
        # iat: the time the token is generated
        # sub: the subject of the token (the user whom it identifies)

        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': username
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # This means the time specified in the payload’s exp field has expired.
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            # When the token supplied is not correct or malformed
            return 'Invalid token. Please log in again.'
