from django.test import TestCase
from task_manager.statuses.models import Status


class StatusModelTest(TestCase):
    def setUp(self):
        self.status = Status.objects.create(name="New")

    def test_status_creation(self):
        """Проверяем, что статус создается корректно"""
        self.assertEqual(self.status.name, "New")
        self.assertIsNotNone(self.status.created_at)

    def test_status_string_representation(self):
        """Проверяем строковое представление статуса"""
        self.assertEqual(str(self.status), "New")

    def test_status_name_unique(self):
        """Проверяем уникальность имени статуса"""
        with self.assertRaises(Exception):
            Status.objects.create(name="New")
