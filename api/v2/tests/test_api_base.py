# tests/test_api_auth.py

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
from api.v2 import app
from api.db import db


class WeConnectApiTestBase(TestCase):
    """Test user api logic"""

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.prefix = '/api/v2/'

        self.users = {
            'one': {"first_name": "jack", "last_name": "dan", "username": "jackdan", "password": "password"},
            'two': {"first_name": "jim", "last_name": "dan", "username": "jimdan", "password": "password"},
            'three': {"first_name": "eli", "last_name": "rwt", "username": "eli", "password": "password"},
            'four': {"first_name": "elijah", "last_name": "rwoth", "username": "elijahrwoth", "password": "password"},
            'bad': {"first_name": 'first_namefirst_namefirst_namefirst_namefirst_namefirst_namefirst_name', "last_name": '', "username": '', "password": ''}
        }

        self.user_login = {
            'one': {"username": "jackdan", "password": "password"},
            'two': {"username": "jimdan", "password": "password"},
            'three': {"username": "eli", "password": "password"},
            'four': {"username": "elijahrwoth", "password": "password"},
            'bad': {"username": '', "password": ''},
            'bad1': {"username": "eli", "password": "passrd"},
            'bad2': {"username": "elite", "password": "password"}
        }

        self.businesses = {
            'one': {"name": "Bondo", "description": "yummy", "category": "Eateries", "location": "Kabale", "photo": "photo"},
            'one_edit': {"name": "Bondo", "description": "yummy foods and deliveries", "category": "Eateries", "location": "Kabale", "photo": "photo"},
            'one_edit1': {"name": "Boondocks", "description": "yummy foods and deliveries", "category": "Eateries", "location": "Kabale", "photo": "photo"},
            'two': {"name": "", "description": "", "category": "", "location": "", "photo": ""},
            'three': {"name": "Boondocks", "description": "your favorite movies", "category": "Entertainment", "location": "Kamwenge", "photo": "photo"},
        }

        self.reviews = {
            'one': {"name": "extra game", "description": "i was given meat yo"},
            'two': {"name": "", "description": ""}
        }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

        self.client.post(self.prefix + 'auth/register', content_type='application/json',
                         data=json.dumps(self.users['one']))
        login = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                 data=json.dumps(self.user_login['one']))
        login_data = json.loads(login.data.decode())
        self.access_token = login_data["access_token"]

    def test_api_hello(self):
        """Test api hello text"""

        response = self.client.get(self.prefix)

        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        with self.app.app_context():
            db.session.close()
            db.drop_all()
