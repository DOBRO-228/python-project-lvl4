from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class ListViewTests(TestCase):
    fixtures = ['users.json']

    def test_list_of_users(self):
        """
        Checking list of created users.
        """
        first_user = User.objects.get(pk=1)
        second_user = User.objects.get(pk=2)
        response = self.client.get(reverse('users:list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['users']), [str(first_user), str(second_user)])


class RegisterUserViewTests(TestCase):

    def test_register(self):
        """
        Checking user registration.
        """
        url = reverse('users:register')
        user = {
            'first_name': 'Aleksey',
            'last_name': 'Navalniy',
            'username': 'FBK',
            'password1': 'svoboda',
            'password2': 'svoboda',
        }
        response = self.client.post(url, user, follow=True)
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Пользователь успешно зарегистрирован')
        created_user = User.objects.get(username=user['username'])
        self.assertEquals(created_user.first_name, 'Aleksey')
        self.assertEquals(created_user.last_name, 'Navalniy')
        self.assertEquals(created_user.check_password("svoboda"), True)

    def test_password_validation(self):
        """
        Checking password validation.
        """
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
        self.assertEqual(0, User.objects.count())


class LoginUserViewTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.first_user = User.objects.get(pk=1)
        self.url = reverse('login')

    def test_login(self):
        """
        Checking login.
        """
        user = {
            'username': self.first_user.username,
            'password': 'svoboda',
        }
        response = self.client.post(self.url, user, follow=True)
        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        logged_user = auth.get_user(self.client)
        self.assertEqual(logged_user, self.first_user)
        self.assertTrue(logged_user.is_authenticated)
        self.assertContains(response, 'Вы залогинены')

    def test_login_validation(self):
        """
        Checking login validation.
        """
        user = {
            'username': self.first_user.username,
            'password': 'liberty',
        }
        response = self.client.post(self.url, user)
        self.assertEqual(response.status_code, 200)
        logged_user = auth.get_user(self.client)
        self.assertFalse(logged_user.is_authenticated)
        msg = 'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.'
        self.assertContains(response, msg)

    def test_logout(self):
        """
        Checking logout.
        """
        self.client.login(username=self.first_user.username, password='svoboda')
        response = self.client.post(reverse('logout'), follow=True)
        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        self.assertContains(response, 'Вы разлогинены')


class UpdateUserViewTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.first_user = User.objects.get(pk=1)
        self.second_user = User.objects.get(pk=2)

    def test_update(self):
        """
        Checking update user.
        """
        self.client.login(username=self.first_user.username, password='svoboda')
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
            response, '/users/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Пользователь успешно изменён')
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        self.assertEqual(self.first_user.username, 'Либертарианец')
        self.assertEqual(self.first_user.first_name, 'Мюррей')
        self.assertEqual(self.first_user.last_name, 'Ротбарт')

    def test_update_without_login(self):
        """
        Checking permissions to update.
        """
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
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertEqual(User.objects.get(pk=self.first_user.id).username, 'FBK')
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_update_not_yourself(self):
        """
        Checking permissions to update.
        """
        update_url = reverse('users:update', args=(self.second_user.id, ))
        updated_user = {
            'first_name': 'Мюррей',
            'last_name': 'Ротбарт',
            'username': 'Либертарианец',
            'password1': 'liberty',
            'password2': 'liberty',
        }
        self.client.login(username=self.first_user.username, password='svoboda')
        update_url = reverse('users:update', args=(self.second_user.id, ))
        response = self.client.post(update_url, updated_user, follow=True)
        self.assertRedirects(
            response, '/users/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertEqual(User.objects.get(pk=self.first_user.id).username, 'FBK')
        self.assertContains(response, 'У вас нет прав для изменения другого пользователя')


class DeleteUserViewTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.first_user = User.objects.get(pk=1)
        self.second_user = User.objects.get(pk=2)
        self.login_url = reverse('login')

    def test_delete(self):
        """
        Checking delete user.
        """
        self.client.login(username=self.first_user.username, password='svoboda')
        delete_url = reverse('users:delete', args=(self.first_user.id, ))
        response = self.client.post(delete_url, follow=True)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=self.first_user.id)
        self.assertRedirects(
            response, '/users/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Пользователь успешно удалён')

    def test_delete_without_login(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        delete_url = reverse('users:delete', args=(self.second_user.id, ))
        response = self.client.post(delete_url, follow=True)
        self.assertTrue(User.objects.filter(pk=self.second_user.id).exists())
        self.assertTrue(User.objects.filter(pk=self.first_user.id).exists())
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_delete_not_yourself(self):
        """
        Checking permissions to delete.
        """
        self.client.login(username=self.first_user.username, password='svoboda')
        delete_url = reverse('users:delete', args=(self.second_user.id, ))
        response = self.client.post(delete_url, follow=True)
        self.assertEqual(User.objects.get(pk=self.second_user.id), self.second_user)
        self.assertRedirects(
            response, '/users/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'У вас нет прав для изменения другого пользователя')
