# tests/test_api_business.py

import json

from tests.test_api_base import WeConnectApiTestBase


class WeConnectApiBusinessTestCase(WeConnectApiTestBase):
    """Test business api logic"""

    def test_business_creation(self):
        """Test api business creation"""

        response = self.client.post(self.prefix + 'businesses',
                                    headers={
                                        'Authorization': 'Bearer {}'.format(self.access_token)},
                                    content_type='application/json',
                                    data=json.dumps(self.businesses['one']))

        self.assertEqual(response.status_code, 201)

    def test_business_duplication_fails(self):
        """Test api business creation fails for existent business"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json', data=json.dumps(self.businesses['one']))
        response = self.client.post(self.prefix + 'businesses',
                                    headers={
                                        'Authorization': 'Bearer {}'.format(self.access_token)},
                                    content_type='application/json',
                                    data=json.dumps(self.businesses['one']))

        self.assertEqual(response.status_code, 409)

    def test_business_creation_fails(self):
        """Test api business creation fails for bad input"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json', data=json.dumps(self.businesses['one']))
        response = self.client.post(self.prefix + 'businesses',
                                    headers={
                                        'Authorization': 'Bearer {}'.format(self.access_token)},
                                    content_type='application/json',
                                    data=json.dumps(self.businesses['two']))

        self.assertEqual(response.status_code, 400)

    def test_no_businesses_to_view(self):
        """Test api businesses viewing when no businesses were registered"""

        response = self.client.get(self.prefix + 'businesses',
                                   headers={'Authorization': 'Bearer {}'.format(self.access_token)})

        self.assertEqual(response.status_code, 404)

    def test_businesses_view(self):
        """Test api businesses viewing"""

        self.client.post(self.prefix + 'businesses',
                         headers={'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json', data=json.dumps(self.businesses['one']))

        response = self.client.get(self.prefix + 'businesses',
                                   headers={
                                       'Authorization': 'Bearer {}'.format(self.access_token)})

        self.assertEqual(response.status_code, 200)

    def test_businesses_search(self):
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

        self.assertEqual(response.status_code, 200)

    def test_business_view(self):
        """Test api business view a business"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json', data=json.dumps(self.businesses['one']))
        response = self.client.get(self.prefix + 'businesses/1',
                                   headers={'Authorization': 'Bearer {}'.format(self.access_token)})

        self.assertEqual(response.status_code, 200)

    def test_missing_business_view_fails(self):
        """Test api fails to view a non existent business"""

        response = self.client.get(self.prefix + 'businesses/1',
                                   headers={'Authorization': 'Bearer {}'.format(self.access_token)})

        self.assertEqual(response.status_code, 404)

    def test_business_edit(self):
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

        self.assertEqual(response.status_code, 200)

    def test_business_edit_fails_for_invalid_input(self):
        """Test api business update fails for invalid input"""

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

        self.assertEqual(response.status_code, 400)

    def test_business_edit_fails_for_wrong_user(self):
        """Test api business update fails for wrong user"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json',
                         data=json.dumps(self.businesses['one']))

        self.client.post(self.prefix + 'auth/register', content_type='application/json',
                         data=json.dumps(self.users['four']))
        login = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                  data=json.dumps(self.user_login['four']))
        login_data = json.loads(login.data.decode())

        response = self.client.put(self.prefix + 'businesses/1',
                                   headers={
                                       'Authorization': 'Bearer ' + login_data["access_token"]},
                                   content_type='application/json',
                                   data=json.dumps(self.businesses['one_edit1']))

        self.assertEqual(response.status_code, 409)

    def test_business_edit_fails_for_missing_business(self):
        """Test api business update fails for missing business"""

        response = self.client.put(self.prefix + 'businesses/4',
                                   headers={
                                       'Authorization': 'Bearer {}'.format(self.access_token)},
                                   content_type='application/json',
                                   data=json.dumps(self.businesses['one_edit']))

        self.assertEqual(response.status_code, 404)

    def test_business_edit_fails_for_new_existent_business_name(self):
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

        self.assertEqual(response.status_code, 409)

    def test_business_delete(self):
        """Test api business deletion"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json',
                         data=json.dumps(self.businesses['one']))
        response = self.client.delete(self.prefix + 'businesses/1',
                                      headers={
                                          'Authorization': 'Bearer {}'.format(self.access_token)})

        self.assertEqual(response.status_code, 200)

    def test_business_delete_fails_for_missing_business(self):
        """Test api business deletion fails for non existent business"""

        response = self.client.delete(self.prefix + 'businesses/7',
                                      headers={
                                          'Authorization': 'Bearer {}'.format(self.access_token)})

        self.assertEqual(response.status_code, 404)

    def test_business_delete_fails_for_wrong_user(self):
        """Test api business delete fails for wrong user"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json',
                         data=json.dumps(self.businesses['one']))

        self.client.post(self.prefix + 'auth/register', content_type='application/json',
                         data=json.dumps(self.users['four']))
        login = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                  data=json.dumps(self.user_login['four']))
        login_data = json.loads(login.data.decode())

        response = self.client.delete(self.prefix + 'businesses/1',
                                      headers={
                                          'Authorization': 'Bearer ' + login_data["access_token"]})

        self.assertEqual(response.status_code, 409)

    def test_create_business_reviews(self):
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

        self.assertEqual(response.status_code, 201)

    def test_create_business_reviews_fails_for_missing_business(self):
        """Test api business post reviews fails if business is not found"""

        response = self.client.post(self.prefix + 'businesses/12/reviews',
                                    headers={
                                        'Authorization': 'Bearer {}'.format(self.access_token)},
                                    content_type='application/json',
                                    data=json.dumps(self.reviews['one']))

        self.assertEqual(response.status_code, 404)

    def test_create_business_reviews_fails_for_new_existent_review_name(self):
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

        self.assertEqual(response.status_code, 409)

    def test_create_business_reviews_fails_for_bad_input(self):
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

        self.assertEqual(response.status_code, 400)

    def test_no_business_reviews(self):
        """Test api business get reviews if none were created for that business"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer {}'.format(self.access_token)},
                         content_type='application/json',
                         data=json.dumps(self.businesses['one']))

        response = self.client.get(self.prefix + 'businesses/1/reviews',
                                   headers={'Authorization': 'Bearer {}'.format(self.access_token)})

        self.assertEqual(response.status_code, 404)

    def test_view_business_reviews(self):
        """Test api business get reviews"""

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

        response = self.client.get(self.prefix + 'businesses/1/reviews',
                                   headers={
                                       'Authorization': 'Bearer {}'.format(self.access_token)})

        self.assertEqual(response.status_code, 200)

    def test_view_business_reviews_fails_for_missing_business(self):
        """Test api business get reviews fails for non existent business"""

        response = self.client.get(self.prefix + 'businesses/2/reviews',
                                   headers={'Authorization': 'Bearer {}'.format(self.access_token)})

        self.assertEqual(response.status_code, 404)
