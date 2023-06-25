from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User


class OperatorRegistrationTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('users:operator-reg')
        self.valid_payload = {
            'email': 'test@example.com',
            'password': 'password',
            'password_confirmation': 'password',
            'user_type': 'OPERATOR',
        }
        self.user = get_user_model().objects.create_user(
            email='test@example.com', password='password')
        self.client.force_authenticate(user=self.user)

    def test_operator_registration(self):
        url = reverse('users:operator-reg')
        data = {
            'email': 'operator1@gmail.com',
            'password': 'password123',
            'full_name': 'AigerimKadyrova',
            'user_type': 'OPERATOR',
        }
        response = self.client.post(url, data, format='json')
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

        user = User.objects.first()
        self.assertEqual(user.email, 'operator1@gmail.com')
        self.assertEqual(user.user_type, 'OPERATOR')

        self.assertIn('id', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertIn('user_type', response.data)


class ClientRegisterViewTest(APITestCase):
    def test_client_registration(self):
        url = reverse('users:client-reg')
        data = {
            'email': 'test@example.com',
            'password': 'password123',
            'full_name': 'John Doe',
            'user_type': 'CLIENT',
            'address': '123 Street',
            'phone': '1234567890',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()
        self.assertEqual(user.email, 'test1@example.com')
        self.assertEqual(user.user_type, 'CLIENT')
        self.assertEqual(user.address, '123 Street')
        self.assertEqual(user.phone, '1234567890')

        self.assertIn('id', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertIn('user_type', response.data)
        self.assertEqual(response.data['email'], 'test1@example.com')
        self.assertEqual(response.data['address'], '123 Street')
        self.assertEqual(response.data['phone'], '1234567890')

    def test_invalid_client_registration(self):
        url = reverse('users:client-reg')
        data = {
            'email': 'test@example.com',
            'password': 'password123',
            'full_name': 'John Doe',
            'user_type': 'CLIENT',
            'address': '123 Street',
            'phone': '1234567890',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 3)


class UserLoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='password',
            user_type='CLIENT',
            is_active=True,
        )

    def test_user_login(self):
        url = reverse('users:login')
        data = {
            'email': 'test@example.com',
            'password': 'password',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user_id', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertIn('user_type', response.data)

    def test_user_login_inactive_account(self):
        self.user.is_active = False
        self.user.save()

        url = reverse('users:login')
        data = {
            'email': 'test3@example.com',
            'password': 'password',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Учетная запись пользователя отключена.')


class ClientRegistrationTest(APITestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(email='client@example.com', password='password', user_type='CLIENT')

    def test_client_registration(self):
        url = 'client-reg'

        registration_data = {
            'email': 'client@example.com',
            'password': 'testpassword',
            'password_confirmation': 'testpassword',
            'company_name': 'Example Company',
            'address': 'Example Address',
            'phone': '1234567890'
        }

        response = self.client.post(url, data=registration_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['email'], registration_data['email'])
        self.assertEqual(response.data['user_type'], 'CLIENT')
        self.assertEqual(response.data['company_name'], registration_data['company_name'])
        self.assertEqual(response.data['address'], registration_data['address'])
        self.assertEqual(response.data['phone'], registration_data['phone'])

        refresh = RefreshToken(response.data['refresh'])
        access_token = response.data['access']
        decoded_token = refresh.access_token.payload

        self.assertEqual(decoded_token['id'], response.data['id'])
        self.assertEqual(decoded_token['user_type'], 'CLIENT')

        self.assertTrue(refresh.access_token.check_blacklist())
        self.assertTrue(refresh.access_token.verify())

        self.assertTrue(refresh.blacklisted)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = self.client.get('client-reg')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], response.data['id'])
        self.assertEqual(response.data['user_type'], 'CLIENT')
        self.assertEqual(response.data['email'], registration_data['email'])
        self.assertEqual(response.data['company_name'], registration_data['company_name'])
        self.assertEqual(response.data['address'], registration_data['address'])
        self.assertEqual(response.data['phone'], registration_data['phone'])
