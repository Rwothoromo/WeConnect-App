# app/models/weconnect.py

# Third party imports
from werkzeug.security import check_password_hash

# local imports
from app.models.business import Business
from app.models.category import Category
from app.models.location import Location
from app.models.review import Review
from app.models.user import User


class WeConnect:
    """Class for WeConnect app functionality"""

    def __init__(self):
        self.businesses = {}
        self.categories = {}
        self.locations = {}
        self.reviews = {}
        self.users = {}
        self.token_blacklist = []

    def register(self, user):
        """Register user
        Add an instance of the User class to the users dictionary of unique usernames as keys.

        :param user: class instance:
        """

        if isinstance(user, User):
            if user.username not in self.users:
                self.users[user.username] = user
                return user
            return "User already exists!"
        return "Not a User instance!"

    def edit_user(self, user):
        """Update a User
        Update an instance of the User class if username exists in users dictionary.

        :param user: class instance:
        :return:     user object
        """

        if isinstance(user, User):
            if user.username in self.users:
                self.users[user.username] = user
                return user
            return "User does not exist!"
        return "Not a User instance!"

    def delete_user(self, username):
        """Delete a User
        Delete a User class if username exists in users dictionary.

        :param user: class instance:
        :return:     users dictionary
        """

        if username in self.users.keys():
            del self.users[username]
            return self.users
        return "User does not exist!"

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

    # Begin businesses
    def create_business(self, username, name, description, category, location, photo):
        """Create Business.
        Add an instance of the Business class to the businesses dictionary
        of unique names as keys, if username exists in users dictionary.

        :param username:    A string: userusername of the active user
        :param name:        A string: name of the business to create
        :param description: A string: Some details on the review
        :param category:    A string: name of the category
        :param location:    A string: name of the location
        :param photo:       A string: path to the business photo
        :return:         businesses dictionary
        """

        if username in self.users.keys():
            if not all(isinstance(i, str) for i in [name, description, category, location, photo]):
                raise TypeError("Input should be a string!")

            if name not in self.businesses:
                business = Business(name, description,
                                    category, location, photo)

                # Update businesses in WeConnect
                self.businesses[name] = business

                # Update businesses of this user
                self.users[username].businesses[name] = business

                # Update businesses in this category
                self.categories[category].businesses[name] = business

                # Update businesses in this location
                self.locations[location].businesses[name] = business

                return business
            return "This business already exists!"
        return "Username does not exist!"

    def view_business(self, username, name):
        """Display a Business
        Display a Business if it exists in the businesses dictionary,
        and if username exists in users dictionary.

        :param username: A string: username of the active user
        :param name:     A string: name of the business to view
        :return:         The value of key matching the business name
        """
        if username in self.users.keys():
            if name in self.businesses:
                return self.businesses[name]
            return "Business does not exist!"
        return "Username does not exist!"

    def edit_business(self, username, name, description, category, location, photo):
        """Edit a Business
        Edit a Business if username exists in users dictionary.

        :param username:    A string: username of the active user
        :param name:        A string: name of the business to edit
        :param description: A string: Some details on the business
        :return:            businesses dictionary
        """

        # Update all except the name
        if username in self.users.keys():
            if not all(isinstance(i, str) for i in [name, description, category, location, photo]):
                raise TypeError("Input should be a string!")

            if self.users[username].businesses[name]:
                updated_business = Business(
                    name, description, category, location, photo)

                this_business = self.users[username].businesses[name]
                old_category = this_business.category
                old_location = this_business.location

                # Update businesses in WeConnect
                self.businesses[name] = updated_business

                # Update businesses of this user
                self.users[username].businesses[name] = updated_business

                # Update businesses in this category
                self.categories[category].businesses[name] = updated_business

                # Delete this business from the previous category
                if old_category != category:
                    del self.categories[old_category].businesses[name]

                # Update businesses in this location
                self.locations[location].businesses[name] = updated_business

                # Delete this business from the previous location
                if old_location != location:
                    del self.locations[old_location].businesses[name]

            return updated_business
        return "User did not create the business!"

    def delete_business(self, username, name):
        """Delete a Business
        Delete a Business if username exists in users dictionary.

        :param username: A string: username of the active user
        :param name:     A string: name of the business to delete
        :return:         businesses dictionary
        """

        if username in self.users.keys():
            if not isinstance(name, str):
                raise TypeError("Input should be a string!")

            if self.users[username].businesses[name]:

                this_business = self.users[username].businesses[name]
                old_category = this_business.category
                old_location = this_business.location

                # Delete this business from WeConnect
                del self.businesses[name]

                # Delete this business from the businesses of this user
                del self.users[username].businesses[name]

                # Delete this business from the previous category
                del self.categories[old_category].businesses[name]

                # Delete this business from the previous location
                del self.locations[old_location].businesses[name]

            return self.businesses
        return "User did not create the business!"

    # Begin reviews
    def create_review(self, username, name, description, business):
        """Create Review.
        Add an instance of the Review class to the reviews dictionary
        of unique names as keys, if username exists in users dictionary.

        :param username:    A string: userusername of the active user
        :param name:        A string: name of the review to create
        :param description: A string: Some details on the review
        :param business:    A string: name of the business
        :return:            reviews dictionary
        """

        if username in self.users.keys():
            if not all(isinstance(i, str) for i in [name, description, business]):
                raise TypeError("Input should be a string!")

            if name not in self.reviews:
                review = Review(name, description, business)

                # Update reviews in WeConnect
                self.reviews[name] = review

                # Update reviews of this user
                self.users[username].reviews[name] = review

                # Update reviews in this business
                self.businesses[business].reviews[name] = review

                return review
            return "This review already exists!"
        return "Username does not exist!"

    def view_review(self, username, name):
        """Display a Review
        Display a Review if it exists in the reviews dictionary,
        and if username exists in users dictionary.

        :param username: A string: username of the active user
        :param name:     A string: name of the review to view
        :return:         The value of key matching the review name
        """
        if username in self.users.keys():
            if name in self.reviews:
                return self.reviews[name]
            return "Review does not exist!"
        return "Username does not exist!"

    def edit_review(self, username, name, description, business):
        """Edit a Review
        Edit a Review if username exists in users dictionary.

        :param username:    A string: userusername of the active user
        :param name:        A string: name of the review to create
        :param description: A string: Some details on the review
        :param business:    A string: name of the business
        :return:            reviews dictionary
        """

        # Update the description
        if self.users[username].reviews[name]:
            if not all(isinstance(i, str) for i in [name, description]):
                raise TypeError("Input should be a string!")

            updated_review = Review(name, description, business)

            # Update reviews in WeConnect
            self.reviews[name] = updated_review

            # Update reviews of this user
            self.users[username].reviews[name] = updated_review

            # Update reviews in this business
            self.businesses[business].reviews[name] = updated_review

            return self.reviews
        return "User did not create the review!"

    def delete_review(self, username, name):
        """Delete a Review
        Delete a Review if username exists in users dictionary.

        :param username: A string: username of the active user
        :param name:     A string: name of the review to delete
        :return:         reviews dictionary
        """

        if self.users[username].reviews[name]:
            if not isinstance(name, str):
                raise TypeError("Input should be a string!")

            old_business = self.reviews[name].business

            # Delete this review from WeConnect
            del self.reviews[name]

            # Delete this review from the reviews of this user
            del self.users[username].reviews[name]

            # Delete this review from the previous business
            del self.businesses[old_business].reviews[name]

            return self.reviews
        return "User did not create the review!"
