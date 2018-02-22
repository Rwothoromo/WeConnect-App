# app/tests/test_user.py
"""This script tests the functionality of User class"""

from app.models.user import User
from tests.test_weconnect import WeConnectTestCase

import json


class TestUser(WeConnectTestCase):
    """Test User class functionality."""

    def test_encode_auth_token(self):
        """Test if auth token"""

        user = User(first_name = 'eli', last_name = 'rwt', username = 'elirwt', password_hash = 'password_hash')
        auth_token = user.encode_auth_token(user.username)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        """Test if decode auth token"""
        
        user = User(first_name = 'eli', last_name = 'rwt', username = 'elirwt', password_hash = 'password_hash')
        auth_token = user.encode_auth_token(user.username)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token) == 1)
