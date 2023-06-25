from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User
from apps.application.models import Application


class ClientApplicationCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('client-application-create')
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_application(self):
        data = {
            'type': 'Some type',
            'comment': 'Some comment',
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_application_unauthenticated(self):
        data = {
            'type': 'Some type',
            'comment': 'Some comment',
        }

        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        
class ApplicationListAPIViewTest(APITestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(email='client@example.com', password='password', user_type='CLIENT')
        self.operator_user = User.objects.create_user(email='operator@example.com', password='password', user_type='OPERATOR')
        self.brigade_user = User.objects.create_user(email='brigade@example.com', password='password', user_type='BRIGADE')

        self.client_application = Application.objects.create(type='CLIENT', client=self.client_user)
        self.operator_application = Application.objects.create(type='OPERATOR', operator=self.operator_user)
        self.brigade_application = Application.objects.create(type='BRIGADE', brigade=self.brigade_user)

    def test_client_application_list(self):
        self.client.force_authenticate(user=self.client_user)
        url = reverse('application-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'CLIENT')
        self.assertNotContains(response, 'OPERATOR')
        self.assertNotContains(response, 'BRIGADE')

    def test_operator_application_list(self):
        self.client.force_authenticate(user=self.operator_user)
        url = reverse('application-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotContains(response, 'CLIENT')
        self.assertContains(response, 'OPERATOR')
        self.assertNotContains(response, 'BRIGADE')

    def test_brigade_application_list(self):
        self.client.force_authenticate(user=self.brigade_user)
        url = reverse('application-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotContains(response, 'CLIENT')
        self.assertNotContains(response, 'OPERATOR')
        self.assertContains(response, 'BRIGADE')


class BrigadeApplicationStatusUpdateAPIViewTest(APITestCase):
    def setUp(self):
        self.application = Application.objects.create(type='Some type')

    def test_update_application_status(self):
        url = reverse('application-in_progressing-status', kwargs={'pk': self.application.pk})
        response = self.client.put(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'success'})

        self.application.refresh_from_db()
        self.assertEqual(self.application.status, 'В процессе')
