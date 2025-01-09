from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

User = get_user_model()


class UserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = 'testuser'
        cls.password = 'qwe123qwe1'
        cls.user = User.objects.create_user(
            username=cls.username,
            password=cls.password,
            first_name='Tester',
            last_name='Testoff'
        )

    def test_create_user(self):
        self.assertTrue(User.objects.filter(username=self.username).exists())

    def test_create_unique_user_form(self):
        with self.assertRaises(IntegrityError) as context:
            User.objects.create_user(
                username=self.username,
                password='newpassword',
                first_name='New',
                last_name='User'
            )
        exception_message = str(context.exception).lower()
        self.assertTrue(
            'unique' in exception_message or 'constraint' in exception_message)

    def test_user_update_form(self):
        new_first_name = 'Updated'
        new_last_name = 'Name'
        self.user.first_name = new_first_name
        self.user.last_name = new_last_name
        self.user.save()

        user_from_db = User.objects.get(username=self.username)
        self.assertEqual(user_from_db.first_name, new_first_name)
        self.assertEqual(user_from_db.last_name, new_last_name)

    def test_user_delete_form(self):
        initial_count = User.objects.count()
        self.user.delete()
        self.assertEqual(User.objects.count(), initial_count - 1)
        self.assertFalse(User.objects.filter(username=self.username).exists())
