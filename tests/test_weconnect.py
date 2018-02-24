# app/tests/test_weconnect.py
"""This script tests the functionality of WeConnect class"""

# third party imports
from unittest import TestCase

# local imports
from app.models.weconnect import WeConnect
from app.models.user import User


class WeConnectTestCase(TestCase):
    """Test user registration and login"""

    def setUp(self):
        self.weconnect = WeConnect()
        self.users = self.weconnect.users
        self.user = User("john", "doe", "johndoe", "password to hash one")
        self.a_user = User("jane", "doe", "johndoe", "password to hash two")

    def test_weconnect_instance(self):
        """Test if WeConnect instance is created"""

        self.assertIsInstance(self.weconnect, WeConnect,
                              msg="Object must be an instance of WeConnect!")

    def test_user_registration(self):
        """Test user registration"""

        user = self.weconnect.register(self.user)

        self.assertIsInstance(user, User, msg="User was not created!")

    def test_user_already_exists(self):
        """Test if username already exists"""

        self.weconnect.register(self.user)
        a_user = self.weconnect.register(self.a_user)

        self.assertEqual(a_user, "User already exists!", msg="Username not yet taken!")

    def test_user_login(self):
        """Test user login"""

        self.weconnect.register(self.user)

        user_instance = self.weconnect.login("johndoe", "password to hash one")
        wrong_password = self.weconnect.login("johndoe", "wrong password")
        wrong_username = self.weconnect.login("jack", "password to hash one")

        self.assertEqual(user_instance.username, "johndoe",
                         msg="Login failed!")
        self.assertEqual(
            wrong_password, "Incorrect username and password combination!", msg="Login successful!")
        self.assertEqual(
            wrong_username, "This username does not exist! Please register!",
            msg="Login successful!")
