# # tests/test_api_v2_business.py
# """This script tests the business functionality of WeConnect api v1"""

# # third party imports
# from unittest import TestCase

# import os
# import sys
# import inspect
# import json

# # solution to python 3 relative import errors
# # use the inspect module because for os.path.abspath(__file__),
# # the __file__ attribute is not always given
# test_api_v2_dir = os.path.dirname(os.path.abspath(
#     inspect.getfile(inspect.currentframe())))
# tests_dir = os.path.dirname(test_api_v2_dir)
# sys.path.insert(0, tests_dir)
# # sys.path.append(os.path.dirname)
# from app.api.api_run import app


# class WeConnectApiBusinessTestCase(TestCase):
#     """Test business api logic"""

#     def setUp(self):
#         self.client = app.test_client()
#         self.prefix = '/api/v2/'

#         self.user_one = {
#             "first_name": "jack",
#             "last_name": "dan",
#             "username": "jackdan",
#             "password": "password"
#         }

#         self.user_one_login_data = {
#             "username": "jackdan",
#             "password": "password"
#         }

#         self.business1 = {
#             "name": "Bondo",
#             "description": "yummy",
#             "category": "Eateries",
#             "location": "Kabale",
#             "photo": "photo"
#         }

#         self.business1_edit = {
#             "name": "Bondo",
#             "description": "yummy foods and deliveries",
#             "category": "Eateries",
#             "location": "Kabale",
#             "photo": "photo"
#         }

#         self.business1_edit1 = {
#             "name": "Boondocks",
#             "description": "yummy foods and deliveries",
#             "category": "Eateries",
#             "location": "Kabale",
#             "photo": "photo"
#         }

#         self.business2 = {
#             "name": '',
#             "description": '',
#             "category": '',
#             "location": '',
#             "photo": ''
#         }

#         self.business3 = {
#             "name": "Boondocks",
#             "description": "your favorite movies",
#             "category": "Entertainment",
#             "location": "Kabale",
#             "photo": "photo"
#         }

#         self.review1 = {
#             "business": "Bondo",
#             "description": "i was given meat yo",
#             "name": "extra game"
#         }

#         self.review2 = {
#             "business": "Bondo",
#             "description": '',
#             "name": ''
#         }

#         self.client.post(self.prefix + 'auth/register', content_type='application/json',
#                          data=json.dumps(self.user_one))
#         login = self.client.post(self.prefix + 'auth/login', content_type='application/json',
#                                  data=json.dumps(self.user_one_login_data))
#         login_data = json.loads(login.data.decode())
#         self.access_token = login_data["access_token"]

#     def test_api_business_creation(self):
#         """Test api business creation"""

#         response = self.client.post(self.prefix + 'businesses',
#                                     headers={
#                                         'Authorization': 'Bearer ' + self.access_token},
#                                     content_type='application/json',
#                                     data=json.dumps(self.business1))
#         response_data = json.loads(response.data.decode())

#         self.assertEqual("Business added", response_data['message'])
#         self.assertEqual(response.status_code, 201)

#     def test_api_business_creation_fails(self):
#         """Test api business creation fails"""

#         self.client.post(self.prefix + 'businesses',
#                          headers={'Authorization': 'Bearer ' + self.access_token},
#                          content_type='application/json', data=json.dumps(self.business1))
#         response = self.client.post(self.prefix + 'businesses',
#                                     headers={
#                                         'Authorization': 'Bearer ' + self.access_token},
#                                     content_type='application/json',
#                                     data=json.dumps(self.business1))
#         response1 = self.client.post(self.prefix + 'businesses',
#                                      headers={
#                                          'Authorization': 'Bearer ' + self.access_token},
#                                      content_type='application/json',
#                                      data=json.dumps(self.business2))
#         response_data = json.loads(response.data.decode())
#         response_data1 = json.loads(response1.data.decode())

#         self.assertEqual("Business already exists", response_data['message'])
#         self.assertEqual(response.status_code, 409)
#         self.assertEqual("name must be a string", response_data1['message'])
#         self.assertEqual(response1.status_code, 400)

#     def test_api_businesses_view(self):
#         """Test api businesses viewing"""

#         response = self.client.get(self.prefix + 'businesses',
#                                    headers={'Authorization': 'Bearer ' + self.access_token})

#         self.assertEqual(response.status_code, 200)

#     def test_api_business_view(self):
#         """Test api business view a business"""

#         response = self.client.get(self.prefix + 'businesses/1',
#                                    headers={'Authorization': 'Bearer ' + self.access_token})

#         self.assertEqual(response.status_code, 200)

#     def test_api_business_view_fails(self):
#         """Test api fails to view a business"""

#         response = self.client.get(self.prefix + 'businesses/9',
#                                    headers={'Authorization': 'Bearer ' + self.access_token})
#         response_data = json.loads(response.data.decode())

#         self.assertEqual("Business not found", response_data['message'])
#         self.assertEqual(response.status_code, 404)

#     def test_api_business_edit(self):
#         """Test api business update"""

#         self.client.post(self.prefix + 'businesses',
#                          headers={
#                              'Authorization': 'Bearer ' + self.access_token},
#                          content_type='application/json',
#                          data=json.dumps(self.business1))
#         response = self.client.put(self.prefix + 'businesses/1',
#                                    headers={
#                                        'Authorization': 'Bearer ' + self.access_token},
#                                    content_type='application/json',
#                                    data=json.dumps(self.business1_edit))
#         response_data = json.loads(response.data.decode())

#         self.assertEqual("Business updated", response_data['message'])
#         self.assertEqual(response.status_code, 200)

#     def test_api_business_edit_fails(self):
#         """Test api business update fails"""

#         self.client.post(self.prefix + 'businesses',
#                          headers={
#                              'Authorization': 'Bearer ' + self.access_token},
#                          content_type='application/json',
#                          data=json.dumps(self.business1))
#         self.client.post(self.prefix + 'businesses',
#                          headers={
#                              'Authorization': 'Bearer ' + self.access_token},
#                          content_type='application/json',
#                          data=json.dumps(self.business3))
#         response = self.client.put(self.prefix + 'businesses/1',
#                                    headers={
#                                        'Authorization': 'Bearer ' + self.access_token},
#                                    content_type='application/json',
#                                    data=json.dumps(self.business1_edit1))
#         response1 = self.client.put(self.prefix + 'businesses/4',
#                                     headers={
#                                         'Authorization': 'Bearer ' + self.access_token},
#                                     content_type='application/json',
#                                     data=json.dumps(self.business1_edit))
#         response2 = self.client.put(self.prefix + 'businesses/1',
#                                     headers={
#                                         'Authorization': 'Bearer ' + self.access_token},
#                                     content_type='application/json',
#                                     data=json.dumps(self.business2))
#         response_data = json.loads(response.data.decode())
#         response_data1 = json.loads(response1.data.decode())
#         response_data2 = json.loads(response2.data.decode())

#         self.assertEqual("Business by that name already exists",
#                          response_data['message'])
#         self.assertEqual(response.status_code, 409)
#         self.assertEqual("Business not found", response_data1['message'])
#         self.assertEqual(response1.status_code, 404)
#         self.assertEqual("name must be a string", response_data2['message'])
#         self.assertEqual(response2.status_code, 400)

#     def test_api_business_delete(self):
#         """Test api business deletion"""

#         response = self.client.delete(self.prefix + 'businesses/1',
#                                       headers={'Authorization': 'Bearer ' + self.access_token})
#         response_data = json.loads(response.data.decode())

#         self.assertEqual("Business deleted", response_data['message'])
#         self.assertEqual(response.status_code, 200)

#     def test_api_business_delete_fails(self):
#         """Test api business deletion fails to non existent business"""

#         response = self.client.delete(self.prefix + 'businesses/7',
#                                       headers={'Authorization': 'Bearer ' + self.access_token})
#         response_data = json.loads(response.data.decode())

#         self.assertEqual("Business not found", response_data['message'])
#         self.assertEqual(response.status_code, 404)

#     def test_api_create_business_reviews(self):
#         """Test api business post reviews"""

#         self.client.post(self.prefix + 'businesses',
#                          headers={
#                              'Authorization': 'Bearer ' + self.access_token},
#                          content_type='application/json',
#                          data=json.dumps(self.business1))
#         response = self.client.post(self.prefix + 'businesses/1/reviews',
#                                     headers={
#                                         'Authorization': 'Bearer ' + self.access_token},
#                                     content_type='application/json',
#                                     data=json.dumps(self.review1))
#         response_data = json.loads(response.data.decode())

#         self.assertEqual("Business review added", response_data['message'])
#         self.assertEqual(response.status_code, 201)

#     def test_api_create_business_reviews_fails(self):
#         """Test api business post reviews fails"""

#         self.client.post(self.prefix + 'businesses',
#                          headers={
#                              'Authorization': 'Bearer ' + self.access_token},
#                          content_type='application/json',
#                          data=json.dumps(self.business1))
#         self.client.post(self.prefix + 'businesses/1/reviews',
#                          headers={
#                              'Authorization': 'Bearer ' + self.access_token},
#                          content_type='application/json',
#                          data=json.dumps(self.review1))
#         response = self.client.post(self.prefix + 'businesses/12/reviews',
#                                     headers={
#                                         'Authorization': 'Bearer ' + self.access_token},
#                                     content_type='application/json',
#                                     data=json.dumps(self.review1))
#         response1 = self.client.post(self.prefix + 'businesses/1/reviews',
#                                      headers={
#                                          'Authorization': 'Bearer ' + self.access_token},
#                                      content_type='application/json',
#                                      data=json.dumps(self.review1))
#         response2 = self.client.post(self.prefix + 'businesses/1/reviews',
#                                      headers={
#                                          'Authorization': 'Bearer ' + self.access_token},
#                                      content_type='application/json',
#                                      data=json.dumps(self.review2))
#         response_data = json.loads(response.data.decode())
#         response_data1 = json.loads(response1.data.decode())
#         response_data2 = json.loads(response2.data.decode())

#         self.assertEqual("Business not found", response_data['message'])
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(
#             "Business review by that name already exists", response_data1['message'])
#         self.assertEqual(response1.status_code, 409)
#         self.assertEqual("name must be a string", response_data2['message'])
#         self.assertEqual(response2.status_code, 400)

#     def test_api_view_business_reviews(self):
#         """Test api business get reviews"""

#         self.client.post(self.prefix + 'businesses',
#                          headers={
#                              'Authorization': 'Bearer ' + self.access_token},
#                          content_type='application/json',
#                          data=json.dumps(self.business1))
#         self.client.post(self.prefix + 'businesses/1/reviews',
#                          headers={
#                              'Authorization': 'Bearer ' + self.access_token},
#                          content_type='application/json',
#                          data=json.dumps(self.review1))
#         response = self.client.get(self.prefix + 'businesses/1/reviews',
#                                    headers={'Authorization': 'Bearer ' + self.access_token})
#         response_data = json.loads(response.data.decode())

#         self.assertIsInstance(response_data, list)
#         self.assertEqual(response.status_code, 200)

#     def test_api_view_business_reviews_fails(self):
#         """Test api business get reviews fails"""

#         self.client.post(self.prefix + 'businesses',
#                          headers={
#                              'Authorization': 'Bearer ' + self.access_token},
#                          content_type='application/json',
#                          data=json.dumps(self.business1))
#         self.client.post(self.prefix + 'businesses',
#                          headers={
#                              'Authorization': 'Bearer ' + self.access_token},
#                          content_type='application/json',
#                          data=json.dumps(self.business2))
#         self.client.post(self.prefix + 'businesses/1/reviews',
#                          headers={
#                              'Authorization': 'Bearer ' + self.access_token},
#                          content_type='application/json',
#                          data=json.dumps(self.review1))
#         response = self.client.get(self.prefix + 'businesses/2/reviews',
#                                    headers={'Authorization': 'Bearer ' + self.access_token})
#         response1 = self.client.get(self.prefix + 'businesses/8/reviews',
#                                     headers={'Authorization': 'Bearer ' + self.access_token})
#         response_data = json.loads(response.data.decode())
#         response_data1 = json.loads(response1.data.decode())

#         self.assertEqual("Business reviews not found",
#                          response_data['message'])
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual("Business not found", response_data1['message'])
#         self.assertEqual(response1.status_code, 404)
