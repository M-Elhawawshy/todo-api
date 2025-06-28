from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from tasks.models import TasksUser


class AuthFlowTest(APITestCase):
    def setUp(self):
        self.signup_url = '/api/auth_service/signup/'
        self.login_url = '/api/auth_service/login/'
        self.refresh_url = '/api/auth_service/refresh/'
        self.protected_url = '/api/tasks/'  # example route

        self.user_data = {
            "username": "Wa3Wa3",
            "password": "password"
        }

    def test_auth_flow(self):
        # Signup
        res = self.client.post(self.signup_url, self.user_data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(TasksUser.objects.filter(username='Wa3Wa3').exists())

        # Login
        res = self.client.post(self.login_url, self.user_data)
        self.assertEqual(res.status_code, 200)
        self.assertIn('access', res.data)

        access_token = res.data['access']
        refresh_cookie = res.cookies.get('refresh')
        self.assertIsNotNone(refresh_cookie)

        # Access protected route
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        res = self.client.get(self.protected_url)
        self.assertNotEqual(res.status_code, 401)

        # Refresh
        self.client.cookies['refresh'] = refresh_cookie.value
        res = self.client.post(self.refresh_url)
        self.assertEqual(res.status_code, 200)
        self.assertIn('access', res.data)



