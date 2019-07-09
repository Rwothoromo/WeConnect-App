"""This script tests the functionality of WeConnect api v1"""

# third party imports
from unittest import TestCase

import json

# local imports
from api.v1 import app


class WeConnectApiTestCase(TestCase):
    """Test user api logic"""

    def setUp(self):
        self.client = app.test_client()
        self.prefix = '/api/v1/'

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

    def test_api_hello(self):
        """Test api hello text"""

        response = self.client.get(self.prefix, follow_redirects=True)
        response_data = json.loads(response.data.decode())

        self.assertEqual(
            'WeConnect brings businesses and users together, and allows users to review businesses',
            response_data['WeConnect'])
        self.assertEqual(response.status_code, 200)

    def test_api_user_registration(self):
        """Test api user registration"""

        response = self.client.post(self.prefix + 'auth/register', content_type='application/json',
                                    data=json.dumps(self.user_one))
        response_data = json.loads(response.data.decode())

        self.assertEqual('User added', response_data['message'])
        self.assertEqual(response.status_code, 201)

    def test_api_user_login(self):
        """Test api user login"""

        self.client.post(self.prefix + 'auth/register', content_type='application/json',
                         data=json.dumps(self.user_two))
        response = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                    data=json.dumps(self.user_two_login_data))
        response_data = json.loads(response.get_data())

        self.assertEqual('User logged in', response_data['message'])
        self.assertEqual(response.status_code, 200)

    def test_api_user_logout(self):
        """Test api user logout"""

        self.client.post(self.prefix + 'auth/register', content_type='application/json',
                         data=json.dumps(self.user_two))
        login = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                 data=json.dumps(self.user_two_login_data))
        login_data = json.loads(login.get_data())
        access_token = login_data["access_token"]

        response = self.client.post(
            self.prefix + 'auth/logout', headers={'Authorization': 'Bearer ' + access_token})
        response_data = json.loads(response.data.decode())

        self.assertEqual('Access token revoked', response_data['message'])
        self.assertEqual(response.status_code, 200)

    def test_api_user_password_reset(self):
        """Test api password reset"""

        self.client.post(self.prefix + 'auth/register', content_type='application/json',
                         data=json.dumps(self.user_three))
        login = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                 data=json.dumps(self.user_three_login_data))
        login_data = json.loads(login.get_data())
        access_token = login_data["access_token"]

        response = self.client.post(self.prefix + 'auth/reset-password',
                                    headers={'Authorization': 'Bearer ' + access_token})
        response_data = json.loads(response.data.decode())

        self.assertEqual('User password reset', response_data['message'])
        self.assertEqual(response.status_code, 200)

    def test_api_user_registration_fails(self):
        """Test api user registration fails"""

        self.client.post(self.prefix + 'auth/register', content_type='application/json',
                         data=json.dumps(self.user_two))
        response = self.client.post(self.prefix + 'auth/register', content_type='application/json',
                                    data=json.dumps(self.user_two))
        response1 = self.client.post(self.prefix + 'auth/register', content_type='application/json',
                                     data=json.dumps(self.user_bad))
        response_data = json.loads(response.data.decode())
        response_data1 = json.loads(response1.data.decode())

        self.assertEqual("User already exists", response_data['message'])
        self.assertEqual(response.status_code, 409)
        self.assertEqual("first_name must be a string",
                         response_data1['message'])
        self.assertEqual(response1.status_code, 400)

    def test_api_user_login_fails_for_bad_input(self):
        """Test api user login fails for bad input"""

        self.client.post(self.prefix + 'auth/register',
                         content_type='application/json', data=json.dumps(self.user_three))
        response = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                    data=json.dumps(self.user_bad_login_data))
        response1 = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                     data=json.dumps(self.user_bad_login_data1))
        response2 = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                     data=json.dumps(self.user_bad_login_data2))
        response_data = json.loads(response.get_data())
        response_data1 = json.loads(response1.get_data())
        response_data2 = json.loads(response2.get_data())

        self.assertEqual("username must be a string", response_data['message'])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            "Incorrect username and password combination!", response_data1['message'])
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(
            "This username does not exist! Please register!", response_data2['message'])
        self.assertEqual(response2.status_code, 400)
