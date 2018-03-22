# tests/test_api_auth.py
"""This script holds the configurations for the WeConnect api tests"""

# third party imports
from unittest import TestCase

import os
import sys
import inspect
import json

# solution to python 3 relative import errors
# use the inspect module because for os.path.abspath(__file__),
# the __file__ attribute is not always given
test_api_v2_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
tests_dir = os.path.dirname(test_api_v2_dir)
sys.path.insert(0, tests_dir)
# sys.path.append(os.path.dirname)

# local imports
from app import app
from app.db import db


class WeConnectApiTestBase(TestCase):
    """Test user api logic"""

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.prefix = '/api/v2/'

        self.user_one = {
            "first_name": "jack",
            "last_name": "dan",
            "username": "jackdan",
            "password": "password"
        }

        self.user_two = {
            "first_name": "jim",
            "last_name": "dan",
            "username": "jimdan",
            "password": "password"
        }

        self.user_three = {
            "first_name": "eli",
            "last_name": "rwt",
            "username": "eli",
            "password": "password"
        }

        self.user_bad = {
            "first_name": '',
            "last_name": '',
            "username": '',
            "password": ''
        }

        self.user_one_login_data = {
            "username": "jackdan",
            "password": "password"
        }

        self.user_two_login_data = {
            "username": "jimdan",
            "password": "password"
        }

        self.user_three_login_data = {
            "username": "eli",
            "password": "password"
        }

        self.user_bad_login_data = {
            "username": '',
            "password": ''
        }

        self.user_bad_login_data1 = {
            "username": "eli",
            "password": "passrd"
        }

        self.user_bad_login_data2 = {
            "username": "elite",
            "password": "password"
        }

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.close()
            db.drop_all()
