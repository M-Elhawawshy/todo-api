from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from tasks.models import Tasks, TasksUser


class TasksTestCase(APITestCase):
    def setUp(self):
        # Create user
        self.user = TasksUser.objects.create_user(
            username="testuser",
            password="password"
        )

        # Get JWT tokens
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Authenticated client
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_create_task(self):
        response = self.client.post('/api/tasks/', {
            "title": "Test Task",
            "description": "This is a test task"
        }, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], "Test Task")

    def test_retrieve_task(self):
        task = Tasks.objects.create(
            title="Existing Task",
            description="Already here",
            owner=self.user
        )
        response = self.client.get(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], "Existing Task")

    def test_update_task(self):
        task = Tasks.objects.create(
            title="Original Title",
            description="Original Description",
            owner=self.user
        )

        url = f'/api/tasks/{task.id}/'
        response = self.client.patch(url, {
            "title": "Updated Title",
            "is_completed": True
        }, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], "Updated Title")
        self.assertTrue(response.data['is_completed'])

    def test_delete_task(self):
        task = Tasks.objects.create(
            title="Task to be deleted",
            description="Temporary",
            owner=self.user
        )

        url = f'/api/tasks/{task.id}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Tasks.objects.filter(id=task.id).exists())