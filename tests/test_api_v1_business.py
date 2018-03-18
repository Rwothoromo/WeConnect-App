# tests/test_api_v1_business.py
"""This script tests the business functionality of WeConnect api v1"""

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


class WeConnectApiBusinessTestCase(TestCase):
    """Test business api logic"""

    def setUp(self):
        self.client = app.test_client()
        self.prefix = '/api/v1/'

        self.user_one = {
            "first_name": "jack",
            "last_name": "dan",
            "username": "jackdan",
            "password": "password"
        }

        self.user_one_login_data = {
            "username": "jackdan",
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
            "location": "Kabale",
            "photo": "photo"
        }

        self.review1 = {
            "business": "Bondo",
            "description": "i was given meat yo",
            "name": "extra game"
        }

        self.client.post(self.prefix + 'auth/register', content_type='application/json',
                         data=json.dumps(self.user_one))
        login = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                 data=json.dumps(self.user_one_login_data))
        login_data = json.loads(login.data.decode())
        self.access_token = login_data["access_token"]


    def test_api_business_creation(self):
        """Test api business creation"""

        response = self.client.post(self.prefix + 'businesses',
                                    headers={'Authorization': 'Bearer ' + self.access_token},
                                    content_type='application/json',
                                    data=json.dumps(self.business1))
        response_data = json.loads(response.data.decode())

        self.assertEqual("Business added", response_data['message'])
        self.assertEqual(response.status_code, 201)
    
    def test_api_businesses_view(self):
        """Test api businesses viewing"""

        response = self.client.get(self.prefix + 'businesses',
                                    headers={'Authorization': 'Bearer ' + self.access_token})
        
        self.assertEqual(response.status_code, 200)
    
    def test_api_business_edit(self):
        """Test api business update"""

        response = self.client.put(self.prefix + 'businesses/1',
                                    headers={'Authorization': 'Bearer ' + self.access_token},
                                    content_type='application/json',
                                    data=json.dumps(self.business1_edit))
        response_data = json.loads(response.data.decode())

        self.assertEqual("Business updated", response_data['message'])
        self.assertEqual(response.status_code, 200)

    def test_api_business_creation_fails(self):
        """Test api business creation fails"""

        self.client.post(self.prefix + 'businesses',
                        headers={'Authorization': 'Bearer ' + self.access_token},
                        content_type='application/json', data=json.dumps(self.business1))
        response = self.client.post(self.prefix + 'businesses',
                                    headers={'Authorization': 'Bearer ' + self.access_token},
                                    content_type='application/json',
                                    data=json.dumps(self.business1))
        response1 = self.client.post(self.prefix + 'businesses',
                                    headers={'Authorization': 'Bearer ' + self.access_token},
                                    content_type='application/json',
                                    data=json.dumps(self.business2))
        response_data = json.loads(response.data.decode())
        response_data1 = json.loads(response1.data.decode())

        self.assertEqual("Business already exists", response_data['message'])
        self.assertEqual(response.status_code, 409)
        self.assertEqual("name must be a string", response_data1['message'])
        self.assertEqual(response1.status_code, 400)

    def test_api_business_edit_fails(self):
        """Test api business update fails"""

        self.client.post(self.prefix + 'businesses',
                                    headers={'Authorization': 'Bearer ' + self.access_token},
                                    content_type='application/json',
                                    data=json.dumps(self.business1))
        self.client.post(self.prefix + 'businesses',
                                    headers={'Authorization': 'Bearer ' + self.access_token},
                                    content_type='application/json',
                                    data=json.dumps(self.business3))
        response = self.client.put(self.prefix + 'businesses/1',
                                    headers={'Authorization': 'Bearer ' + self.access_token},
                                    content_type='application/json',
                                    data=json.dumps(self.business1_edit1))
        response1 = self.client.put(self.prefix + 'businesses/4',
                                    headers={'Authorization': 'Bearer ' + self.access_token},
                                    content_type='application/json',
                                    data=json.dumps(self.business1_edit))
        response_data = json.loads(response.data.decode())
        response_data1 = json.loads(response1.data.decode())

        self.assertEqual("Business by that name already exists", response_data['message'])
        self.assertEqual(response.status_code, 409)
        self.assertEqual("Business not found", response_data1['message'])
        self.assertEqual(response1.status_code, 404)
