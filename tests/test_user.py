# tests/test_user.py
"""This script tests the functionality of User class"""

from werkzeug.security import check_password_hash

from tests.test_weconnect import WeConnectTestCase
from app.models.user import User


class TestUser(WeConnectTestCase):
    """Test User class functionality."""

    def test_user_edit(self):
        """Test if user is edited"""

        self.weconnect.register(self.user)
        user_object = User('jonathan', 'doyle',
                           self.user.username, 'new password')
        updated_user = self.weconnect.edit_user(user_object)

        self.assertIsInstance(updated_user, User, msg='Not a User instance')
        self.assertTrue(check_password_hash(
            updated_user.password_hash, 'new password'), msg='Password mismatch')
        self.assertListEqual(['jonathan', 'doyle', self.user.username], [
            updated_user.first_name, updated_user.last_name, updated_user.username], msg='User was not edited')

    def test_user_delete(self):
        """Test user delete"""

        self.weconnect.register(self.user)
        user_dict = self.weconnect.delete_user("johndoe")

        self.assertIsInstance(user_dict, dict)

    def test_user_edit_fails_for_bad_input(self):
        """Test user edit fails"""

        user = self.weconnect.edit_user("bad input")
        user1 = User("fake", "user", "fakeuser", "password")
        fake_user = self.weconnect.edit_user(user1)

        self.assertEqual(user, "Not a User instance!")
        self.assertEqual(fake_user, "User does not exist!")

    def test_user_delete_fails_for_non_user(self):
        """Test user delete fails"""

        user = self.weconnect.delete_user("non user")

        self.assertEqual(user, "User does not exist!")
