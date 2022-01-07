from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from tasks.models import Task


class UsersTests(TestCase):
    """Test Users app."""

    fixtures = ['users.json', 'tasks.json', 'statuses.json']

    def setUp(self):
        """Prepare data for tests."""
        self.first_user = User.objects.get(pk=1)
        self.second_user = User.objects.get(pk=2)
        self.first_task = Task.objects.get(pk=1)
        self.second_task = Task.objects.get(pk=2)

    def test_list_of_users(self):
        """Checking of list of created users."""
        response = self.client.get(reverse('users:list'))
        self.assertEqual(response.status_code, 200)
        response_tasks = list(response.context['users'])
        self.assertQuerysetEqual(response_tasks, [self.first_user, self.second_user])

    def test_registration(self):
        """Checking of user registration."""
        url = reverse('users:register')
        user = {
            'first_name': 'Igor',
            'last_name': 'Dobro',
            'username': 'Truth',
            'password1': 'svoboda',
            'password2': 'svoboda',
        }
        response = self.client.post(url, user, follow=True)
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True,
        )
        self.assertContains(response, 'Пользователь успешно зарегистрирован')
        created_user = User.objects.get(username=user['username'])
        self.assertEquals(created_user.first_name, 'Igor')
        self.assertEquals(created_user.last_name, 'Dobro')
        self.assertTrue(created_user.check_password('svoboda'))

    def test_password_validation_in_registration(self):
        """Checking of password validation."""
        url = reverse('users:register')
        user_with_too_small_pas = {
            'first_name': 'Aleksey',
            'last_name': 'Navalniy',
            'username': 'FBK',
            'password1': 'sv',
            'password2': 'sv',
        }
        user_with_diff_pas = {
            'first_name': 'Aleksey',
            'last_name': 'Navalniy',
            'username': 'FBK',
            'password1': 'svo1',
            'password2': 'svo',
        }
        self.client.post(url, user_with_too_small_pas)
        self.client.post(url, user_with_diff_pas)
        self.assertEqual(2, User.objects.count())

    def test_login(self):
        """Checking of login."""
        user = {
            'username': self.first_user.username,
            'password': 'svoboda',
        }
        response = self.client.post(reverse('login'), user, follow=True)
        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True,
        )
        logged_user = auth.get_user(self.client)
        self.assertEqual(logged_user, self.first_user)
        self.assertTrue(logged_user.is_authenticated)
        self.assertContains(response, 'Вы залогинены')

    def test_login_validation(self):
        """Checking of login validation."""
        user = {
            'username': self.first_user.username,
            'password': 'liberty',
        }
        response = self.client.post(reverse('login'), user)
        self.assertEqual(response.status_code, 200)
        logged_user = auth.get_user(self.client)
        self.assertFalse(logged_user.is_authenticated)
        msg = 'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.'
        self.assertContains(response, msg)

    def test_logout(self):
        """Checking of logout."""
        self.client.force_login(self.first_user)
        response = self.client.post(reverse('logout'), follow=True)
        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True,
        )
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        self.assertContains(response, 'Вы разлогинены')

    def test_update(self):
        """Checking of update user."""
        self.client.force_login(self.first_user)
        update_url = reverse('users:update', args=(self.first_user.id, ))
        updated_user = {
            'first_name': 'Мюррей',
            'last_name': 'Ротбарт',
            'username': 'Либертарианец',
            'password1': 'liberty',
            'password2': 'liberty',
        }
        response = self.client.post(update_url, updated_user, follow=True)
        self.assertRedirects(
            response, '/users/', status_code=302, target_status_code=200, fetch_redirect_response=True,
        )
        self.assertContains(response, 'Пользователь успешно изменён')
        self.first_user.refresh_from_db()
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        self.assertEqual(self.first_user.username, 'Либертарианец')
        self.assertEqual(self.first_user.first_name, 'Мюррей')
        self.assertEqual(self.first_user.last_name, 'Ротбарт')

    def test_update_without_login(self):
        """Checking of permissions to update."""
        update_url = reverse('users:update', args=(self.second_user.id, ))
        updated_user = {
            'first_name': 'Мюррей',
            'last_name': 'Ротбарт',
            'username': 'Либертарианец',
            'password1': 'liberty',
            'password2': 'liberty',
        }
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        response = self.client.post(update_url, updated_user, follow=True)
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True,
        )
        self.assertEqual(User.objects.get(pk=self.first_user.id).username, 'FBK')
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_update_not_yourself(self):
        """Checking of permissions to update."""
        update_url = reverse('users:update', args=(self.second_user.id, ))
        updated_user = {
            'first_name': 'Мюррей',
            'last_name': 'Ротбарт',
            'username': 'Либертарианец',
            'password1': 'liberty',
            'password2': 'liberty',
        }
        self.client.force_login(self.first_user)
        update_url = reverse('users:update', args=(self.second_user.id, ))
        response = self.client.post(update_url, updated_user, follow=True)
        self.assertRedirects(
            response, '/users/', status_code=302, target_status_code=200, fetch_redirect_response=True,
        )
        self.assertEqual(User.objects.get(pk=self.first_user.id).username, 'FBK')
        self.assertContains(response, 'У вас нет прав для изменения другого пользователя')

    def test_delete(self):
        """Checking of delete user."""
        self.first_task.delete()
        self.second_task.delete()
        self.client.force_login(self.first_user)
        delete_url = reverse('users:delete', args=(self.first_user.id, ))
        response = self.client.post(delete_url, follow=True)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=self.first_user.id)
        self.assertRedirects(
            response, '/users/', status_code=302, target_status_code=200, fetch_redirect_response=True,
        )
        self.assertContains(response, 'Пользователь успешно удалён')

    def test_delete_without_login(self):
        """Checking of deletion users without login."""
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        delete_url = reverse('users:delete', args=(self.second_user.id, ))
        response = self.client.post(delete_url, follow=True)
        self.assertTrue(User.objects.filter(pk=self.second_user.id).exists())
        self.assertTrue(User.objects.filter(pk=self.first_user.id).exists())
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True,
        )
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_delete_not_yourself(self):
        """Checking of permissions to delete."""
        self.client.force_login(self.first_user)
        delete_url = reverse('users:delete', args=(self.second_user.id, ))
        response = self.client.post(delete_url, follow=True)
        self.assertTrue(User.objects.filter(pk=self.second_user.id).exists())
        self.assertRedirects(
            response, '/users/', status_code=302, target_status_code=200, fetch_redirect_response=True,
        )
        self.assertContains(response, 'У вас нет прав для изменения другого пользователя')

    def test_deletion_while_user_is_author(self):
        """Checking of deletion while task references on user."""
        self.second_task = Task.objects.get(pk=2)
        self.second_task.performer = self.second_user
        self.second_task.save()
        self.client.force_login(self.first_user)
        delete_url = reverse('users:delete', args=(self.first_user.id, ))
        response = self.client.post(delete_url, follow=True)
        self.assertTrue(User.objects.filter(pk=self.first_user.id).exists())
        self.assertRedirects(
            response, '/users/', status_code=302, target_status_code=200, fetch_redirect_response=True,
        )
        self.assertContains(response, 'Невозможно удалить пользователя, потому что он используется')

    def test_deletion_while_user_is_performer(self):
        """Checking of deletion while task references on user."""
        self.first_task.author = self.second_user
        self.first_task.save()
        self.client.force_login(self.first_user)
        delete_url = reverse('users:delete', args=(self.first_user.id, ))
        response = self.client.post(delete_url, follow=True)
        self.assertTrue(User.objects.filter(pk=self.first_user.id).exists())
        self.assertRedirects(
            response, '/users/', status_code=302, target_status_code=200, fetch_redirect_response=True,
        )
        self.assertContains(response, 'Невозможно удалить пользователя, потому что он используется')
