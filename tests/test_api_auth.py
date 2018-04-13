# tests/test_api_auth.py

import json

from tests.test_api_base import WeConnectApiTestBase


class WeConnectApiAuthTestCase(WeConnectApiTestBase):
    """Test user api logic"""

    def test_api_user_registration(self):
        """Test api user registration"""

        response = self.client.post(self.prefix + 'auth/register', content_type='application/json',
                                    data=json.dumps(self.users['two']))

        self.assertEqual(response.status_code, 201)

    def test_api_user_login(self):
        """Test api user login"""

        self.client.post(self.prefix + 'auth/register', content_type='application/json',
                         data=json.dumps(self.users['two']))
        response = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                    data=json.dumps(self.user_login['two']))

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

        self.assertEqual(response.status_code, 200)

    def test_api_user_duplication_fails(self):
        """Test api user registration fails for existent user"""

        self.client.post(self.prefix + 'auth/register', content_type='application/json',
                         data=json.dumps(self.users['two']))
        response = self.client.post(self.prefix + 'auth/register', content_type='application/json',
                                    data=json.dumps(self.users['two']))

        self.assertEqual(response.status_code, 409)

    def test_api_user_creation_fails(self):
        """Test api user registration fails for bad input"""

        response = self.client.post(self.prefix + 'auth/register', content_type='application/json',
                                    data=json.dumps(self.users['bad']))

        self.assertEqual(response.status_code, 400)

    def test_api_bad_user_login_fails(self):
        """Test api user login fails for bad input"""

        response = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                    data=json.dumps(self.user_login['bad']))

        self.assertEqual(response.status_code, 400)

    def test_api_bad_password_fails(self):
        """Test api user login fails for bad password"""

        self.client.post(self.prefix + 'auth/register',
                         content_type='application/json', data=json.dumps(self.users['three']))
        response = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                    data=json.dumps(self.user_login['bad1']))

        self.assertEqual(response.status_code, 401)

    def test_api_bad_username_fails(self):
        """Test api user login fails for bad username"""

        self.client.post(self.prefix + 'auth/register',
                         content_type='application/json', data=json.dumps(self.users['three']))
        response = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                    data=json.dumps(self.user_login['bad2']))

        self.assertEqual(response.status_code, 401)
