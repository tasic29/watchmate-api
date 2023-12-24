# from django.contrib.auth.models import User
# from django.urls import reverse

# from rest_framework import status
# from rest_framework.test import APITestCase, APIClient
# from rest_framework.authtoken.models import Token


# class RegisterTestCase(APITestCase):

#     def test_register(self):
#         data = {
#             'username': 'testcase',
#             'email': 'test@email.com',
#             'password': 'newpassword',
#             'password2': 'newpassword'
#         }
#         response = self.client.post(reverse('register'), data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# class LoginLogoutTestCase(APITestCase):

#     def setUp(self):
#         self.user = User.objects.create(username='example',
#                                         password='newpassword')

#     def test_login(self):
#         data = {
#             'username': 'example',
#             'password': 'newpassword'
#         }
#         response = self.client.post(reverse('login'), data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_logout(self):
#         self.token = Token.objects.get(user__username='example')
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
#         response = self.client.post(reverse('logout'))
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
