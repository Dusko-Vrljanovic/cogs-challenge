from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from account.factory import UserFactory


class RegistrationViewTest(APITestCase):

    def setUp(self):
        self.data = {
            'username': 'test',
            'email': 'john.doe@test.com',
            'password': 'P@s$w0rD',
            'password2': 'P@s$w0rD',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        self.url = reverse('api:users:register')

    def test_create_user(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertEqual(response_data['username'], self.data['username'])
        self.assertEqual(response_data['email'], self.data['email'])
        self.assertEqual(response_data['first_name'], self.data['first_name'])
        self.assertEqual(response_data['last_name'], self.data['last_name'])
        self.assertNotIn('password', response_data)

    def test_create_user_missing_data(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertIn('email', response_data)
        self.assertIn('username', response_data)
        self.assertIn('password', response_data)
        self.assertIn('password2', response_data)
        self.assertIn('first_name', response_data)
        self.assertIn('last_name', response_data)

    def test_wrong_password(self):
        data = {
            **self.data,
            'password2': 'NotCorrectPassword'
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertEqual(
            response_data['password'], ["Password fields didn't match."]
        )


class UserDetailsView(APITestCase):
    def setUp(self):
        self.url = reverse('api:users:me')

    def test_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_details(self):
        user = UserFactory(screen_name='test')
        self.client.force_authenticate(user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(user.username, response_data['username'])
        self.assertEqual(user.email, response_data['email'])
        self.assertEqual(user.first_name, response_data['first_name'])
        self.assertEqual(user.last_name, response_data['last_name'])
        self.assertEqual(user.screen_name, response_data['screen_name'])
