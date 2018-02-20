# app/models/weconnect.py
"""Script for creating WeConnect app and managing classes"""

# Third party imports
from werkzeug.security import check_password_hash

# local imports
# from app.models.business import Business
# from app.models.category import Category
# from app.models.location import Location
# from app.models.review import Review
from app.models.user import User


class WeConnect(object):
    """WeConnect class"""

    def __init__(self):
        self.businesses = {}
        self.categories = {}
        self.locations = {}
        self.reviews = {}
        self.users = {}

    def register(self, user):
        """Register user.
        Add an instance of the User class to the users dictionary of unique usernames as keys.

        :param user: class instance:
        """

        if isinstance(user, User):
            if user.username not in self.users:
                self.users[user.username] = user
                return True
            return False
        return "Not a User instance!"

    def login(self, username, password):
        """Log in user.
        Log in if the username and password match in users dictionary.

        :param username: A string:
        :param password: A string:
        """

        if username in self.users.keys():
            # check if password matches the stored hash value
            password_hash = self.users[username].password_hash
            if check_password_hash(password_hash, password):
                # return this user instance
                return self.users[username]
            return "Incorrect username and password combination!"
        return "This username does not exist! Please register!"
