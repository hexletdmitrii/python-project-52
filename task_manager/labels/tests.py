from django.test import TestCase
from task_manager.labels.models import Label


class LabelModelTest(TestCase):
    def setUp(self):
        self.label = Label.objects.create(name="Bug")

    def test_label_creation(self):
        """Проверяем, что метка создается корректно"""
        self.assertEqual(self.label.name, "Bug")
        self.assertIsNotNone(self.label.created_at)

    def test_label_string_representation(self):
        """Проверяем строковое представление метки"""
        self.assertEqual(str(self.label), "Bug")

    def test_label_name_unique(self):
        """Проверяем уникальность имени метки"""
        with self.assertRaises(Exception):
            Label.objects.create(name="Bug")
