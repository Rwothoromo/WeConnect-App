# tests/test_api_auth.py

import json

from api.v2.tests.test_api_base import WeConnectApiTestBase
from api.v2.models.user import User
from api.v2.models.log import Log
from api.v2.models.blacklist import Blacklist


class WeConnectApiAuthTestCase(WeConnectApiTestBase):
    """Test user api logic"""

    def test_user_registration(self):
        """Test api user registration"""

        response = self.client.post(self.prefix + 'auth/register', content_type='application/json',
                                    data=json.dumps(self.users['two']))

        self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        """Test api user login"""

        self.client.post(self.prefix + 'auth/register', content_type='application/json',
                         data=json.dumps(self.users['two']))
        response = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                    data=json.dumps(self.user_login['two']))

        self.assertEqual(response.status_code, 200)

    def test_user_logout(self):
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

    def test_user_password_reset(self):
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

    def test_user_duplication_fails(self):
        """Test api user registration fails for existent user"""

        self.client.post(self.prefix + 'auth/register', content_type='application/json',
                         data=json.dumps(self.users['two']))
        response = self.client.post(self.prefix + 'auth/register', content_type='application/json',
                                    data=json.dumps(self.users['two']))

        self.assertEqual(response.status_code, 409)

    def test_user_creation_fails(self):
        """Test api user registration fails for bad input"""

        response = self.client.post(self.prefix + 'auth/register', content_type='application/json',
                                    data=json.dumps(self.users['bad']))

        self.assertEqual(response.status_code, 400)

    def test_invalid_input_login_fails(self):
        """Test api user login fails for bad input"""

        response = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                    data=json.dumps(self.user_login['bad']))

        self.assertEqual(response.status_code, 400)

    def test_wrong_password_login_fails(self):
        """Test api user login fails for bad password"""

        self.client.post(self.prefix + 'auth/register',
                         content_type='application/json', data=json.dumps(self.users['three']))
        response = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                    data=json.dumps(self.user_login['bad1']))

        self.assertEqual(response.status_code, 401)

    def test_wrong_username_login_fails(self):
        """Test api user login fails for bad username"""

        self.client.post(self.prefix + 'auth/register',
                         content_type='application/json', data=json.dumps(self.users['three']))
        response = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                    data=json.dumps(self.user_login['bad2']))

        self.assertEqual(response.status_code, 401)

    def test_user_representation(self):
        """Test that the user model can be queried and represented"""

        self.assertEqual(
            repr(
                User(
                    first_name=self.users['two']['first_name'],
                    last_name=self.users['two']['last_name'],
                    username=self.users['two']['username'],
                    password=self.users['two']['password']
                )
            ), "<User: {}>".format(self.users['two']['username']))

    def test_user_as_dict(self):
        """Test that the user model is represented as a dictionary"""

        user = User(
            first_name=self.users['two']['first_name'],
            last_name=self.users['two']['last_name'],
            username=self.users['two']['username'],
            password=self.users['two']['password']
        )

        self.assertIsInstance(user.user_as_dict(), dict)

    def test_log_representation(self):
        """Test that the log model can be queried and represented"""

        self.assertEqual(
            repr(
                Log(
                    action='Login',
                    message='Logged in user: {}'.format(
                        self.users['one']['username']),
                    table='users',
                    user_id=1
                )
            ), "<Log: {}>".format('Logged in user: {}'.format(self.users['one']['username'])))

    def test_blacklist_representation(self):
        """Test that the blacklist model can be queried and represented"""

        self.assertEqual(repr(Blacklist(token=self.access_token)),
                         "<Token: {}>".format(self.access_token))

    def test_blacklist_as_dict(self):
        """Test that the blacklist model is represented as a dictionary"""

        blacklist = Blacklist(token=self.access_token)

        self.assertIsInstance(blacklist.token_as_dict(), dict)
