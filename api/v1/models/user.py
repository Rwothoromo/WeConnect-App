# app/models/user.py

# Third party imports
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


class User(UserMixin):
    """Class to create a User class object"""

    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.businesses = {}
        self.reviews = {}
        self.categories = {}
        self.locations = {}
