from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class UserCRUDTestCase(TestCase):
    def setUp(self):
        # Создаем пользователя, который будет использоваться для тестов обновления и удаления
        self.user = User.objects.create_user(
            username='testuser1',
            password='testuser1',
            first_name='testuser1',
            last_name='testuser1'
        )
        self.update_url = reverse('update_user', kwargs={'pk': self.user.pk})  # Замените 'user_update' на имя вашего URL
        self.delete_url = reverse('delete_user', kwargs={'pk': self.user.pk})  # Замените 'user_delete' на имя вашего URL

    def test_user_registration(self):
        """Тест регистрации нового пользователя"""
        registration_url = reverse('add_user')  # Замените 'register' на имя вашего URL для регистрации
        response = self.client.post(registration_url, {
            'username': 'testuser1',
            'password1': 'testuser1',
            'password2': 'testuser1',
            'first_name': 'testuser1',
            'last_name': 'testuser1',
        })
        self.assertEqual(response.status_code, 302)  # Проверяем редирект после успешной регистрации
        self.assertTrue(User.objects.filter(username='testuser1').exists())  # Проверяем, что пользователь создан

    def test_user_update(self):
        """Тест обновления данных пользователя"""
        self.client.login(username='testuser1', password='testuser1')  # Логинимся как пользователь
        response = self.client.post(self.update_url, {
            'username': 'updateduser',
            'first_name': 'updateduser',
            'last_name': 'updateduser',
            'password': 'updateduser',
            'password_confirm': 'updateduser',
        })
        self.assertEqual(response.status_code, 302)  # Проверяем редирект после успешного обновления
        self.user.refresh_from_db()  # Обновляем данные пользователя из базы
        self.assertEqual(self.user.username, 'updateduser')  # Проверяем, что имя пользователя обновлено
        self.assertEqual(self.user.first_name, 'updateduser')  # Проверяем, что имя обновлено
        self.assertEqual(self.user.last_name, 'updateduser')  # Проверяем, что фамилия обновлена

    def test_user_delete(self):
        """Тест удаления пользователя"""
        self.client.login(username='testuser1', password='testuser1')  # Логинимся как пользователь
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)  # Проверяем редирект после успешного удаления
        self.assertFalse(User.objects.filter(username='testuser').exists())  # Проверяем, что пользователь удален
