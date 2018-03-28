# tests/test_api_business.py

import json

from tests.test_api_base import WeConnectApiTestBase


class WeConnectApiBusinessTestCase(WeConnectApiTestBase):
    """Test business api logic"""

    def test_api_business_creation(self):
        """Test api business creation"""

        response = self.client.post(self.prefix + 'businesses',
                                    headers={
                                        'Authorization': 'Bearer {}'.format(self.access_token)},
                                    content_type='application/json',
                                    data=json.dumps(self.businesses['one']))
        response_data = json.loads(response.data.decode())

        self.assertEqual("Business added", response_data['message'])
        self.assertEqual(response.status_code, 201)

    def test_api_business_creation_fails(self):
        """Test api business creation fails"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json', data=json.dumps(self.businesses['one']))
        response = self.client.post(self.prefix + 'businesses',
                                    headers={
                                        'Authorization': 'Bearer {}'.format(self.access_token)},
                                    content_type='application/json',
                                    data=json.dumps(self.businesses['one']))
        response1 = self.client.post(self.prefix + 'businesses',
                                     headers={
                                         'Authorization': 'Bearer {}'.format(self.access_token)},
                                     content_type='application/json',
                                     data=json.dumps(self.businesses['two']))
        response_data = json.loads(response.data.decode())
        response_data1 = json.loads(response1.data.decode())

        self.assertEqual("Business already exists", response_data['message'])
        self.assertEqual(response.status_code, 409)
        self.assertEqual("name must be a string", response_data1['message'])
        self.assertEqual(response1.status_code, 400)

    def test_api_businesses_view(self):
        """Test api businesses viewing"""

        response = self.client.get(self.prefix + 'businesses',
                                   headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        response_data = json.loads(response.data.decode())

        self.client.post(self.prefix + 'businesses',
                         headers={'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json', data=json.dumps(self.businesses['one']))

        response1 = self.client.get(self.prefix + 'businesses',
                                    headers={
                                        'Authorization': 'Bearer {}'.format(self.access_token)})
        response_data1 = json.loads(response1.data.decode())

        self.assertEqual("No business found", response_data['message'])
        self.assertEqual(response.status_code, 404)
        self.assertEqual(1, len(response_data1['businesses']))
        self.assertEqual(response1.status_code, 200)

    def test_api_businesses_view_by_name_search(self):
        """Test api businesses viewing by searched name"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json', data=json.dumps(self.businesses['one']))
        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json', data=json.dumps(self.businesses['three']))

        response = self.client.get(self.prefix + 'businesses?q=oNd&limit=13',
                                   headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        response_data = json.loads(response.data.decode())

        self.assertEqual(2, len(response_data['businesses']))
        self.assertEqual(response.status_code, 200)

    def test_api_business_view(self):
        """Test api business view a business"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json', data=json.dumps(self.businesses['one']))
        response = self.client.get(self.prefix + 'businesses/1',
                                   headers={'Authorization': 'Bearer {}'.format(self.access_token)})

        self.assertEqual(response.status_code, 200)

    def test_api_business_view_fails(self):
        """Test api fails to view a business"""

        response = self.client.get(self.prefix + 'businesses/1',
                                   headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        response_data = json.loads(response.data.decode())

        self.assertEqual("Business not found", response_data['message'])
        self.assertEqual(response.status_code, 404)

    def test_api_business_edit(self):
        """Test api business update"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json',
                         data=json.dumps(self.businesses['one']))
        response = self.client.put(self.prefix + 'businesses/1',
                                   headers={
                                       'Authorization': 'Bearer {}'.format(self.access_token)},
                                   content_type='application/json',
                                   data=json.dumps(self.businesses['one_edit']))
        response_data = json.loads(response.data.decode())

        self.assertEqual("Business updated", response_data['message'])
        self.assertEqual(response.status_code, 200)

    def test_api_business_edit_fails_for_bad_input(self):
        """Test api business update fails for bad input"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json',
                         data=json.dumps(self.businesses['one']))
        response = self.client.put(self.prefix + 'businesses/1',
                                   headers={
                                       'Authorization': 'Bearer {}'.format(self.access_token)},
                                   content_type='application/json',
                                   data=json.dumps(self.businesses['two']))

        response_data = json.loads(response.data.decode())
        self.assertEqual("name must be a string", response_data['message'])
        self.assertEqual(response.status_code, 400)

    def test_api_business_edit_fails_for_wrong_user(self):
        """Test api business update fails for wrong user"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json',
                         data=json.dumps(self.businesses['one']))

        self.client.post(self.prefix + 'auth/register', content_type='application/json',
                         data=json.dumps(self.users['four']))
        login4 = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                  data=json.dumps(self.user_login['four']))
        login_data4 = json.loads(login4.data.decode())

        response = self.client.put(self.prefix + 'businesses/1',
                                   headers={
                                       'Authorization': 'Bearer ' + login_data4["access_token"]},
                                   content_type='application/json',
                                   data=json.dumps(self.businesses['one_edit1']))

        response_data = json.loads(response.data.decode())

        self.assertEqual("Only the Business owner can update",
                         response_data['message'])
        self.assertEqual(response.status_code, 409)

    def test_api_business_edit_fails_for_missing_business(self):
        """Test api business update fails for missing business"""

        response = self.client.put(self.prefix + 'businesses/4',
                                   headers={
                                       'Authorization': 'Bearer {}'.format(self.access_token)},
                                   content_type='application/json',
                                   data=json.dumps(self.businesses['one_edit']))

        response_data = json.loads(response.data.decode())

        self.assertEqual("Business not found", response_data['message'])
        self.assertEqual(response.status_code, 404)

    def test_api_business_edit_fails_for_new_existent_business_name(self):
        """Test api business update fails if new business name already exists"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json',
                         data=json.dumps(self.businesses['one']))
        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json',
                         data=json.dumps(self.businesses['three']))
        response = self.client.put(self.prefix + 'businesses/1',
                                   headers={
                                       'Authorization': 'Bearer {}'.format(self.access_token)},
                                   content_type='application/json',
                                   data=json.dumps(self.businesses['one_edit1']))

        response_data = json.loads(response.data.decode())

        self.assertEqual("Business by that name already exists",
                         response_data['message'])
        self.assertEqual(response.status_code, 409)

    def test_api_business_delete(self):
        """Test api business deletion"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json',
                         data=json.dumps(self.businesses['one']))
        response = self.client.delete(self.prefix + 'businesses/1',
                                      headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        response_data = json.loads(response.data.decode())

        self.assertEqual("Business deleted", response_data['message'])
        self.assertEqual(response.status_code, 200)

    def test_api_business_delete_fails_for_missing_business(self):
        """Test api business deletion fails for non existent business"""

        response = self.client.delete(self.prefix + 'businesses/7',
                                      headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        response_data = json.loads(response.data.decode())

        self.assertEqual("Business not found", response_data['message'])
        self.assertEqual(response.status_code, 404)

    def test_api_business_delete_fails_for_wrong_user(self):
        """Test api business delete fails for wrong user"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json',
                         data=json.dumps(self.businesses['one']))

        self.client.post(self.prefix + 'auth/register', content_type='application/json',
                         data=json.dumps(self.users['four']))
        login4 = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                  data=json.dumps(self.user_login['four']))
        login_data4 = json.loads(login4.data.decode())

        response = self.client.delete(self.prefix + 'businesses/1',
                                      headers={'Authorization': 'Bearer ' + login_data4["access_token"]})

        response_data = json.loads(response.data.decode())

        self.assertEqual("Only the Business owner can delete",
                         response_data['message'])
        self.assertEqual(response.status_code, 409)

    def test_api_create_business_reviews(self):
        """Test api business post reviews"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json',
                         data=json.dumps(self.businesses['one']))
        response = self.client.post(self.prefix + 'businesses/1/reviews',
                                    headers={
                                        'Authorization': 'Bearer {}'.format(self.access_token)},
                                    content_type='application/json',
                                    data=json.dumps(self.reviews['one']))
        response_data = json.loads(response.data.decode())

        self.assertEqual("Business review added", response_data['message'])
        self.assertEqual(response.status_code, 201)

    def test_api_create_business_reviews_fails_for_missing_business(self):
        """Test api business post reviews fails if business is not found"""

        response = self.client.post(self.prefix + 'businesses/12/reviews',
                                    headers={
                                        'Authorization': 'Bearer {}'.format(self.access_token)},
                                    content_type='application/json',
                                    data=json.dumps(self.reviews['one']))
        response_data = json.loads(response.data.decode())

        self.assertEqual("Business not found", response_data['message'])
        self.assertEqual(response.status_code, 404)

    def test_api_create_business_reviews_fails_for_new_existent_review_name(self):
        """Test api business post reviews fails if new review name already exists"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json',
                         data=json.dumps(self.businesses['one']))
        self.client.post(self.prefix + 'businesses/1/reviews',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json',
                         data=json.dumps(self.reviews['one']))

        response = self.client.post(self.prefix + 'businesses/1/reviews',
                                    headers={
                                        'Authorization': 'Bearer {}'.format(self.access_token)},
                                    content_type='application/json',
                                    data=json.dumps(self.reviews['one']))

        response_data = json.loads(response.data.decode())

        self.assertEqual(
            "Business review by that name already exists", response_data['message'])
        self.assertEqual(response.status_code, 409)

    def test_api_create_business_reviews_fails_for_bad_input(self):
        """Test api business post reviews fails for bad input"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json',
                         data=json.dumps(self.businesses['one']))

        response = self.client.post(self.prefix + 'businesses/1/reviews',
                                    headers={
                                        'Authorization': 'Bearer {}'.format(self.access_token)},
                                    content_type='application/json',
                                    data=json.dumps(self.reviews['two']))

        response_data = json.loads(response.data.decode())

        self.assertEqual("name must be a string", response_data['message'])
        self.assertEqual(response.status_code, 400)

    def test_api_view_business_reviews(self):
        """Test api business get reviews"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json',
                         data=json.dumps(self.businesses['one']))

        response = self.client.get(self.prefix + 'businesses/1/reviews',
                                   headers={'Authorization': 'Bearer {}'.format(self.access_token)})

        self.client.post(self.prefix + 'businesses/1/reviews',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json',
                         data=json.dumps(self.reviews['one']))

        response1 = self.client.get(self.prefix + 'businesses/1/reviews',
                                    headers={'Authorization': 'Bearer {}'.format(self.access_token)})

        response_data = json.loads(response.data.decode())
        response_data1 = json.loads(response1.data.decode())

        self.assertEqual("Business reviews not found",
                         response_data['message'])
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data1, list)
        self.assertEqual(response1.status_code, 200)

        self.assertEqual(response.status_code, 200)

    def test_api_view_business_reviews_fails_for_missing_business(self):
        """Test api business get reviews fails for non existent business"""

        response = self.client.get(self.prefix + 'businesses/2/reviews',
                                   headers={'Authorization': 'Bearer {}'.format(self.access_token)})

        response_data = json.loads(response.data.decode())

        self.assertEqual("Business not found", response_data['message'])
        self.assertEqual(response.status_code, 404)
