# tests/test_api_business.py
"""This script tests the business functionality of WeConnect api business"""

import json

from tests.test_api_base import WeConnectApiTestBase


class WeConnectApiBusinessTestCase(WeConnectApiTestBase):
    """Test business api logic"""

    def test_api_business_creation(self):
        """Test api business creation"""

        response = self.client.post(self.prefix + 'businesses',
                                    headers={
                                        'Authorization': 'Bearer ' + self.access_token},
                                    content_type='application/json',
                                    data=json.dumps(self.business1))
        response_data = json.loads(response.data.decode())

        self.assertEqual("Business added", response_data['message'])
        self.assertEqual(response.status_code, 201)

    def test_api_business_creation_fails(self):
        """Test api business creation fails"""

        self.client.post(self.prefix + 'businesses',
                         headers={'Authorization': 'Bearer ' +
                                  self.access_token},
                         content_type='application/json', data=json.dumps(self.business1))
        response = self.client.post(self.prefix + 'businesses',
                                    headers={
                                        'Authorization': 'Bearer ' + self.access_token},
                                    content_type='application/json',
                                    data=json.dumps(self.business1))
        response1 = self.client.post(self.prefix + 'businesses',
                                     headers={
                                         'Authorization': 'Bearer ' + self.access_token},
                                     content_type='application/json',
                                     data=json.dumps(self.business2))
        response_data = json.loads(response.data.decode())
        response_data1 = json.loads(response1.data.decode())

        self.assertEqual("Business already exists", response_data['message'])
        self.assertEqual(response.status_code, 409)
        self.assertEqual("name must be a string", response_data1['message'])
        self.assertEqual(response1.status_code, 400)

    def test_api_businesses_view(self):
        """Test api businesses viewing"""

        response = self.client.get(self.prefix + 'businesses',
                                   headers={'Authorization': 'Bearer ' + self.access_token})
        response_data = json.loads(response.data.decode())

        self.client.post(self.prefix + 'businesses',
                         headers={'Authorization': 'Bearer ' +
                                  self.access_token},
                         content_type='application/json', data=json.dumps(self.business1))

        response1 = self.client.get(self.prefix + 'businesses',
                                    headers={'Authorization': 'Bearer ' + self.access_token})

        self.assertEqual("No business found", response_data['message'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response1.status_code, 200)

    def test_api_business_view(self):
        """Test api business view a business"""

        self.client.post(self.prefix + 'businesses',
                         headers={'Authorization': 'Bearer ' +
                                  self.access_token},
                         content_type='application/json', data=json.dumps(self.business1))
        response = self.client.get(self.prefix + 'businesses/1',
                                   headers={'Authorization': 'Bearer ' + self.access_token})

        self.assertEqual(response.status_code, 200)

    def test_api_business_view_fails(self):
        """Test api fails to view a business"""

        response = self.client.get(self.prefix + 'businesses/1',
                                   headers={'Authorization': 'Bearer ' + self.access_token})
        response_data = json.loads(response.data.decode())

        self.assertEqual("Business not found", response_data['message'])
        self.assertEqual(response.status_code, 404)

    def test_api_business_edit(self):
        """Test api business update"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer ' + self.access_token},
                         content_type='application/json',
                         data=json.dumps(self.business1))
        response = self.client.put(self.prefix + 'businesses/1',
                                   headers={
                                       'Authorization': 'Bearer ' + self.access_token},
                                   content_type='application/json',
                                   data=json.dumps(self.business1_edit))
        response_data = json.loads(response.data.decode())

        self.assertEqual("Business updated", response_data['message'])
        self.assertEqual(response.status_code, 200)

    def test_api_business_edit_fails_for_bad_input(self):
        """Test api business update fails for bad input"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer ' + self.access_token},
                         content_type='application/json',
                         data=json.dumps(self.business1))
        response = self.client.put(self.prefix + 'businesses/1',
                                   headers={
                                       'Authorization': 'Bearer ' + self.access_token},
                                   content_type='application/json',
                                   data=json.dumps(self.business2))

        response_data = json.loads(response.data.decode())
        self.assertEqual("name must be a string", response_data['message'])
        self.assertEqual(response.status_code, 400)

    def test_api_business_edit_fails_for_wrong_user(self):
        """Test api business update fails for wrong user"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer ' + self.access_token},
                         content_type='application/json',
                         data=json.dumps(self.business1))

        self.client.post(self.prefix + 'auth/register', content_type='application/json',
                         data=json.dumps(self.user_four))
        login4 = self.client.post(self.prefix + 'auth/login', content_type='application/json',
                                  data=json.dumps(self.user_four_login_data))
        login_data4 = json.loads(login4.data.decode())
        response = self.client.put(self.prefix + 'businesses/1',
                                   headers={
                                       'Authorization': 'Bearer ' + login_data4["access_token"]},
                                   content_type='application/json',
                                   data=json.dumps(self.business1_edit1))

        response_data = json.loads(response.data.decode())

        self.assertEqual("Only the Business owner can update",
                         response_data['message'])
        self.assertEqual(response.status_code, 409)

    def test_api_business_edit_fails_for_missing_business(self):
        """Test api business update fails for missing business"""

        response = self.client.put(self.prefix + 'businesses/4',
                                   headers={
                                       'Authorization': 'Bearer ' + self.access_token},
                                   content_type='application/json',
                                   data=json.dumps(self.business1_edit))

        response_data = json.loads(response.data.decode())

        self.assertEqual("Business not found", response_data['message'])
        self.assertEqual(response.status_code, 404)

    def test_api_business_edit_fails_for_new_existent_business_name(self):
        """Test api business update fails if new business name already exists"""

        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer ' + self.access_token},
                         content_type='application/json',
                         data=json.dumps(self.business1))
        self.client.post(self.prefix + 'businesses',
                         headers={
                             'Authorization': 'Bearer ' + self.access_token},
                         content_type='application/json',
                         data=json.dumps(self.business3))
        response = self.client.put(self.prefix + 'businesses/1',
                                   headers={
                                       'Authorization': 'Bearer ' + self.access_token},
                                   content_type='application/json',
                                   data=json.dumps(self.business1_edit1))

        response_data = json.loads(response.data.decode())

        self.assertEqual("Business by that name already exists",
                         response_data['message'])
        self.assertEqual(response.status_code, 409)

    # def test_api_business_delete(self):
    #     """Test api business deletion"""

    #     response = self.client.delete(self.prefix + 'businesses/1',
    #                                   headers={'Authorization': 'Bearer ' + self.access_token})
    #     response_data = json.loads(response.data.decode())

    #     self.assertEqual("Business deleted", response_data['message'])
    #     self.assertEqual(response.status_code, 200)

    # def test_api_business_delete(self):
    #     """Test api business deletion"""

    #     response = self.client.delete(self.prefix + 'businesses/1',
    #                                   headers={'Authorization': 'Bearer ' + self.access_token})
    #     response_data = json.loads(response.data.decode())

    #     self.assertEqual("Business deleted", response_data['message'])
    #     self.assertEqual(response.status_code, 200)

    # def test_api_business_delete_fails(self):
    #     """Test api business deletion fails to non existent business"""

    #     response = self.client.delete(self.prefix + 'businesses/7',
    #                                   headers={'Authorization': 'Bearer ' + self.access_token})
    #     response_data = json.loads(response.data.decode())

    #     self.assertEqual("Business not found", response_data['message'])
    #     self.assertEqual(response.status_code, 404)

    # def test_api_create_business_reviews(self):
    #     """Test api business post reviews"""

    #     self.client.post(self.prefix + 'businesses',
    #                      headers={
    #                          'Authorization': 'Bearer ' + self.access_token},
    #                      content_type='application/json',
    #                      data=json.dumps(self.business1))
    #     response = self.client.post(self.prefix + 'businesses/1/reviews',
    #                                 headers={
    #                                     'Authorization': 'Bearer ' + self.access_token},
    #                                 content_type='application/json',
    #                                 data=json.dumps(self.review1))
    #     response_data = json.loads(response.data.decode())

    #     self.assertEqual("Business review added", response_data['message'])
    #     self.assertEqual(response.status_code, 201)

    # def test_api_create_business_reviews_fails(self):
    #     """Test api business post reviews fails"""

    #     self.client.post(self.prefix + 'businesses',
    #                      headers={
    #                          'Authorization': 'Bearer ' + self.access_token},
    #                      content_type='application/json',
    #                      data=json.dumps(self.business1))
    #     self.client.post(self.prefix + 'businesses/1/reviews',
    #                      headers={
    #                          'Authorization': 'Bearer ' + self.access_token},
    #                      content_type='application/json',
    #                      data=json.dumps(self.review1))
    #     response = self.client.post(self.prefix + 'businesses/12/reviews',
    #                                 headers={
    #                                     'Authorization': 'Bearer ' + self.access_token},
    #                                 content_type='application/json',
    #                                 data=json.dumps(self.review1))
    #     response1 = self.client.post(self.prefix + 'businesses/1/reviews',
    #                                  headers={
    #                                      'Authorization': 'Bearer ' + self.access_token},
    #                                  content_type='application/json',
    #                                  data=json.dumps(self.review1))
    #     response2 = self.client.post(self.prefix + 'businesses/1/reviews',
    #                                  headers={
    #                                      'Authorization': 'Bearer ' + self.access_token},
    #                                  content_type='application/json',
    #                                  data=json.dumps(self.review2))
    #     response_data = json.loads(response.data.decode())
    #     response_data1 = json.loads(response1.data.decode())
    #     response_data2 = json.loads(response2.data.decode())

    #     self.assertEqual("Business not found", response_data['message'])
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(
    #         "Business review by that name already exists", response_data1['message'])
    #     self.assertEqual(response1.status_code, 409)
    #     self.assertEqual("name must be a string", response_data2['message'])
    #     self.assertEqual(response2.status_code, 400)

    # def test_api_view_business_reviews(self):
    #     """Test api business get reviews"""

    #     self.client.post(self.prefix + 'businesses',
    #                      headers={
    #                          'Authorization': 'Bearer ' + self.access_token},
    #                      content_type='application/json',
    #                      data=json.dumps(self.business1))
    #     self.client.post(self.prefix + 'businesses/1/reviews',
    #                      headers={
    #                          'Authorization': 'Bearer ' + self.access_token},
    #                      content_type='application/json',
    #                      data=json.dumps(self.review1))
    #     response = self.client.get(self.prefix + 'businesses/1/reviews',
    #                                headers={'Authorization': 'Bearer ' + self.access_token})
    #     response_data = json.loads(response.data.decode())

    #     self.assertIsInstance(response_data, list)
    #     self.assertEqual(response.status_code, 200)

    # def test_api_view_business_reviews_fails(self):
    #     """Test api business get reviews fails"""

    #     self.client.post(self.prefix + 'businesses',
    #                      headers={
    #                          'Authorization': 'Bearer ' + self.access_token},
    #                      content_type='application/json',
    #                      data=json.dumps(self.business1))
    #     self.client.post(self.prefix + 'businesses',
    #                      headers={
    #                          'Authorization': 'Bearer ' + self.access_token},
    #                      content_type='application/json',
    #                      data=json.dumps(self.business2))
    #     self.client.post(self.prefix + 'businesses/1/reviews',
    #                      headers={
    #                          'Authorization': 'Bearer ' + self.access_token},
    #                      content_type='application/json',
    #                      data=json.dumps(self.review1))
    #     response = self.client.get(self.prefix + 'businesses/2/reviews',
    #                                headers={'Authorization': 'Bearer ' + self.access_token})
    #     response1 = self.client.get(self.prefix + 'businesses/8/reviews',
    #                                 headers={'Authorization': 'Bearer ' + self.access_token})
    #     response_data = json.loads(response.data.decode())
    #     response_data1 = json.loads(response1.data.decode())

    #     self.assertEqual("Business reviews not found",
    #                      response_data['message'])
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual("Business not found", response_data1['message'])
    #     self.assertEqual(response1.status_code, 404)
