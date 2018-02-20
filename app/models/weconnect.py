# app/models/weconnect.py
"""Script for creating WeConnect app and managing classes"""

# Third party imports
from werkzeug.security import check_password_hash

# local imports
# from app.models.business import Business
from app.models.category import Category
from app.models.location import Location
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
# Begin categories

    def create_category(self, username, name, description):
        """Create Category.
        Add an instance of the Category class to the categories dictionary
        of unique names as keys, if username exists in users dictionary.

        :param username:    A string: username of the active user
        :param name:        A string: name of the category to edit
        :param description: A string: Some details on the category
        :return:            categories dictionary
        """

        if username in self.users.keys():
            if not all(isinstance(i, str) for i in [name, description]):
                raise TypeError("Input should be a string!")

            if name not in self.categories:
                category = Category(name, description)

                # Update categories in WeConnect
                self.categories[name] = category

                # Update user categories
                self.users[username].categories[name] = category

                return self.categories
            return "This category already exists!"
        return "Username does not exist!"

    def view_category(self, username, name):
        """Display a Category
        Display a Category if it exists in the categories dictionary,
        and if username exists in users dictionary.

        :param username: A string: username of the active user
        :param name:     A string: name of the category to view
        :return:         The value of key matching the category name
        """
        if username in self.users.keys():
            if name in self.categories:
                return self.categories[name]
            return "Category does not exist!"
        return "Username does not exist!"

    def edit_category(self, username, name, description):
        """Edit a Category
        Edit a Category if username exists in users dictionary.

        :param username:    A string: username of the active user
        :param name:        A string: name of the category to edit
        :param description: A string: Some details on the category
        :return:            categories dictionary
        """

        # Update the description
        if self.users[username].categories[name]:
            if not all(isinstance(i, str) for i in [name, description]):
                raise TypeError("Input should be a string!")

            updated_category = Category(name, description)

            # Update categories in WeConnect
            self.categories[name] = updated_category

            # Update user categories
            self.users[username].categories[name] = updated_category

            return self.categories
        return "User did not create the category!"

    def delete_category(self, username, name):
        """Delete a Category
        Delete a Category if username exists in users dictionary.

        :param username: A string: username of the active user
        :param name:     A string: name of the category to delete
        :return:         categories dictionary
        """

        if self.users[username].categories[name]:
            if not isinstance(name, str):
                raise TypeError("Input should be a string!")

            # Delete this category from WeConnect
            del self.categories[name]

            # Delete this category from the categories of this user
            del self.users[username].categories[name]

            return self.categories
        return "User did not create the category!"

        # Begin locations
    def create_location(self, username, name, description):
        """Create Location.
        Add an instance of the Location class to the locations dictionary
        of unique names as keys, if username exists in users dictionary.

        :param username:    A string: username of the active user
        :param name:        A string: name of the location to edit
        :param description: A string: Some details on the location
        :return:            locations dictionary
        """

        if username in self.users.keys():
            if not all(isinstance(i, str) for i in [name, description]):
                raise TypeError("Input should be a string!")

            if name not in self.locations:
                location = Location(name, description)

                # Update locations in WeConnect
                self.locations[name] = location

                # Update locations of this user
                self.users[username].locations[name] = location

                return self.locations
            return "This location already exists!"
        return "Username does not exist!"

    def view_location(self, username, name):
        """Display a Location
        Display a Location if it exists in the locations dictionary,
        and if username exists in users dictionary.

        :param username: A string: username of the active user
        :param name:     A string: name of the location to view
        :return:         The value of key matching the location name
        """
        if username in self.users.keys():
            if name in self.locations:
                return self.locations[name]
            return "Location does not exist!"
        return "Username does not exist!"

    def edit_location(self, username, name, description):
        """Edit a Location
        Edit a Location if username exists in users dictionary.

        :param username:    A string: username of the active user
        :param name:        A string: name of the location to edit
        :param description: A string: Some details on the location
        :return:            locations dictionary
        """

        # Update the description
        if self.users[username].locations[name]:
            if not all(isinstance(i, str) for i in [name, description]):
                raise TypeError("Input should be a string!")

            updated_location = Location(name, description)

            # Update locations in WeConnect
            self.locations[name] = updated_location

            # Update locations of this user
            self.users[username].locations[name] = updated_location

            return self.locations
        return "User did not create the location!"

    def delete_location(self, username, name):
        """Delete a Location
        Delete a Location if username exists in users dictionary.

        :param username: A string: username of the active user
        :param name:     A string: name of the location to delete
        :return:         locations dictionary
        """

        if self.users[username].locations[name]:
            if not isinstance(name, str):
                raise TypeError("Input should be a string!")

            # Delete this location from WeConnect
            del self.locations[name]

            # Delete this location from the locations of this user
            del self.users[username].locations[name]

            return self.locations
        return "User did not create the location!"
