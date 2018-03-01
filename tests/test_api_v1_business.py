# tests/test_api_v1_business.py
"""This script tests the functionality of WeConnect api v1"""

# third party imports
from unittest import TestCase

import os
import sys
import inspect
import json

# solution to python 3 relative import errors
# use the inspect module because for os.path.abspath(__file__),
# the __file__ attribute is not always given
test_api_v1_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
tests_dir = os.path.dirname(test_api_v1_dir)
sys.path.insert(0, tests_dir)
# sys.path.append(os.path.dirname)
from app.api.api_run import app


class WeConnectApiTestCase(TestCase):
    """Test user and business api logic"""

    def setUp(self):
        self.client = app.test_client()

        self.user_two_login_data = {
            "username": "jimdan",
            "password_hash": "password_hash"
        }

        self.user_two = {
            "first_name": "jim",
            "last_name": "dan",
            "username": "jimdan",
            "password_hash": "password_hash"
        }

        self.prefix = '/api/v1/'

        # self.business_data = {
        #     "name": "Buyondo", "description": "One stop center",
        #     "category": "Construction", "location": "Kabale", "photo": "photo"
        # }

    # def test_api_get_businesses(self):
    #     """Test api get businesses"""

    #     self.client.post(self.prefix+'auth/register', content_type='application/json',
    #                      data=json.dumps(self.user_two))

    #     login = self.client.post(self.prefix+'auth/login', content_type='application/json',
    #                              data=json.dumps(self.user_two_login_data))
    #     login_data = json.loads(login.get_data())
    #     access_token = login_data["access_token"]

    #     response = self.client.get(
    #         self.prefix+'businesses', headers={'Authorization': 'Bearer ' + access_token})

    #     self.assertEqual(response.status_code, 200)

    # def test_api_post_business(self):
    #     """Test api post business"""

    #     self.client.post(self.prefix+'auth/register', content_type='application/json',
    #                      data=json.dumps(self.user_two))

    #     login = self.client.post(self.prefix+'auth/login', content_type='application/json',
    #                              data=json.dumps(self.user_two_login_data))
    #     login_data = json.loads(login.get_data())
    #     access_token = login_data["access_token"]

    #     response = self.client.post(
    #         self.prefix+'businesses', headers={'Authorization': 'Bearer ' + access_token},
    #         data=json.dumps(self.business_data))
    #     response_data = json.loads(response.data.decode())

    #     self.assertEqual('Business added', response_data['message'])
    #     self.assertEqual(response.status_code, 201)