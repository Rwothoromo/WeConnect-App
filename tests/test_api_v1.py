# app/tests/test_api_v1.py
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

        self.user_registration_data = {
            "first_name": "jack",
            "last_name": "dan",
            "username": "jackdan",
            "password_hash": "password_hash"
            }

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

    def test_api_hello(self):
        """Test api hello text"""

        response = self.client.get('/api/v1/')
        response_data = json.loads(response.data.decode())

        self.assertEqual('WeConnect brings businesses and users together, and allows users to review businesses.',
                         response_data['WeConnect'])

    def test_api_user_registration(self):
        """Test api user registration"""

        response = self.client.post('/api/v1/auth/register', content_type='application/json',
                                    data=json.dumps(self.user_registration_data))
        response_data = json.loads(response.data.decode())

        self.assertEqual('User added', response_data['message'])
        self.assertEqual(response.status_code, 201)

    def test_api_user_login(self):
        """Test api user login"""

        self.client.post('/api/v1/auth/register', content_type='application/json',
                         data=json.dumps(self.user_two))
        response = self.client.post('/api/v1/auth/login', content_type='application/json',
                                    data=json.dumps(self.user_two_login_data))
        response_data = json.loads(response.get_data())

        self.assertEqual('User logged in', response_data['message'])
        self.assertEqual(response.status_code, 200)

    def test_api_user_password_reset(self):
        """Test api password reset"""

        self.client.post('/api/v1/auth/register', content_type='application/json',
                         data=json.dumps(self.user_two))
        login = self.client.post('/api/v1/auth/login', content_type='application/json',
                            data=json.dumps(self.user_two_login_data))
        login_data = json.loads(login.get_data())
        access_token = login_data["access_token"]

        response = self.client.post('/api/v1/auth/reset-password', headers={'Authorization' : 'Bearer '+access_token})
        response_data = json.loads(response.data.decode())

        self.assertEqual('User password reset', response_data['message'])
        self.assertEqual(response.status_code, 200)

    def test_api_user_logout(self):
        """Test api user logout"""

        self.client.post('/api/v1/auth/register', content_type='application/json',
                         data=json.dumps(self.user_two))
        login = self.client.post('/api/v1/auth/login', content_type='application/json',
                                    data=json.dumps(self.user_two_login_data))
        login_data = json.loads(login.get_data())
        access_token = login_data["access_token"]     

        response = self.client.post('/api/v1/auth/logout', headers={'Authorization' : 'Bearer '+access_token})
        response_data = json.loads(response.data.decode())        

        self.assertEqual('Access token revoked', response_data['message'])
        self.assertEqual(response.status_code, 200)
