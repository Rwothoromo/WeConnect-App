# tests/test_api_auth.py

import json

from tests.test_api_base import WeConnectApiTestBase


class WeConnectApiAuthTestCase(WeConnectApiTestBase):
    """Test user api logic"""

    def test_api_user_registration(self):
        """Test api user registration"""

        response = self.client.post(self.prefix + 'auth/register', content_type='application/json',
                                    data=json.dumps(self.users['two']))
        response_data = json.loads(response.data.decode())

        self.assertEqual('User added', response_data['message'])
        self.assertEqual(response.status_code, 201)

    def test_api_user_login(self):
        """Test api user login"""

        self.client.post(self.prefix + 'auth/register', content_type='application/json',
                         data=json.dumps(self.users['two']))
        response = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                    data=json.dumps(self.user_login['two']))
        response_data = json.loads(response.data.decode())

        self.assertEqual('User logged in', response_data['message'])
        self.assertEqual(response.status_code, 200)

    def test_api_user_logout(self):
        """Test api user logout"""

        self.client.post(self.prefix + 'auth/register', content_type='application/json',
                         data=json.dumps(self.users['two']))
        login = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                 data=json.dumps(self.user_login['two']))
        login_data = json.loads(login.data.decode())
        access_token = login_data["access_token"]

        response = self.client.post(
            self.prefix + 'auth/logout', headers={'Authorization': 'Bearer ' + access_token})
        response_data = json.loads(response.data.decode())

        self.assertEqual('Access token revoked', response_data['message'])
        self.assertEqual(response.status_code, 200)

    def test_api_user_password_reset(self):
        """Test api password reset"""

        self.client.post(self.prefix + 'auth/register', content_type='application/json',
                         data=json.dumps(self.users['three']))
        login = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                 data=json.dumps(self.user_login['three']))
        login_data = json.loads(login.data.decode())
        access_token = login_data["access_token"]

        response = self.client.post(self.prefix + 'auth/reset-password',
                                    headers={'Authorization': 'Bearer ' + access_token})
        response_data = json.loads(response.data.decode())

        self.assertEqual('User password reset', response_data['message'])
        self.assertEqual(response.status_code, 200)

    def test_api_user_registration_fails(self):
        """Test api user registration fails"""

        self.client.post(self.prefix + 'auth/register', content_type='application/json',
                         data=json.dumps(self.users['two']))
        response = self.client.post(self.prefix + 'auth/register', content_type='application/json',
                                    data=json.dumps(self.users['two']))
        response1 = self.client.post(self.prefix + 'auth/register', content_type='application/json',
                                     data=json.dumps(self.users['bad']))
        response_data = json.loads(response.data.decode())
        response_data1 = json.loads(response1.data.decode())

        self.assertEqual("User already exists", response_data['message'])
        self.assertEqual(response.status_code, 409)
        self.assertIn("must be a string", response_data1['message'])
        self.assertEqual(response1.status_code, 400)

    def test_api_user_login_fails_for_bad_input(self):
        """Test api user login fails for bad input"""

        self.client.post(self.prefix + 'auth/register',
                         content_type='application/json', data=json.dumps(self.users['three']))
        response = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                    data=json.dumps(self.user_login['bad']))
        response1 = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                     data=json.dumps(self.user_login['bad1']))
        response2 = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                     data=json.dumps(self.user_login['bad2']))
        response_data = json.loads(response.data.decode())
        response_data1 = json.loads(response1.data.decode())
        response_data2 = json.loads(response2.data.decode())

        self.assertIn("must be a string", response_data['message'])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            "Incorrect username and password combination!", response_data1['message'])
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(
            "Incorrect username and password combination!", response_data2['message'])
        self.assertEqual(response2.status_code, 400)
