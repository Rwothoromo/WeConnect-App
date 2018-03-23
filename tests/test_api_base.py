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

        self.user_four = {
            "first_name": "elijah",
            "last_name": "rwoth",
            "username": "elijahrwoth",
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

        self.user_four_login_data = {
            "username": "elijahrwoth",
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

        self.business1 = {
            "name": "Bondo",
            "description": "yummy",
            "category": "Eateries",
            "location": "Kabale",
            "photo": "photo"
        }

        self.business1_edit = {
            "name": "Bondo",
            "description": "yummy foods and deliveries",
            "category": "Eateries",
            "location": "Kabale",
            "photo": "photo"
        }

        self.business1_edit1 = {
            "name": "Boondocks",
            "description": "yummy foods and deliveries",
            "category": "Eateries",
            "location": "Kabale",
            "photo": "photo"
        }

        self.business2 = {
            "name": '',
            "description": '',
            "category": '',
            "location": '',
            "photo": ''
        }

        self.business3 = {
            "name": "Boondocks",
            "description": "your favorite movies",
            "category": "Entertainment",
            "location": "Kamwenge",
            "photo": "photo"
        }

        self.review1 = {
            "name": "extra game",
            "description": "i was given meat yo"
        }

        self.review2 = {
            "name": '',
            "description": ''
        }

        with self.app.app_context():
            db.create_all()

        self.client.post(self.prefix + 'auth/register', content_type='application/json',
                         data=json.dumps(self.user_one))
        login = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                 data=json.dumps(self.user_one_login_data))
        login_data = json.loads(login.data.decode())
        self.access_token = login_data["access_token"]

    def test_api_hello(self):
        """Test api hello text"""

        response = self.client.get(self.prefix)
        response_data = json.loads(response.data.decode())

        self.assertEqual(
            'WeConnect brings businesses and users together, and allows users to review businesses',
            response_data['WeConnect'])
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        with self.app.app_context():
            db.session.close()
            db.drop_all()
