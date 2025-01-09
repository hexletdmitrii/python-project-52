from django.test import TestCase
from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.status = Status.objects.create(name="New")
        self.task = Task.objects.create(
            name="Test Task",
            description="Test Description",
            status=self.status,
            author=self.user
        )

    def test_task_creation(self):
        self.assertEqual(self.task.name, "Test Task")
        self.assertEqual(self.task.description, "Test Description")
        self.assertEqual(self.task.status, self.status)
        self.assertEqual(self.task.author, self.user)

    def test_task_string_representation(self):
        self.assertEqual(str(self.task), "Test Task")
