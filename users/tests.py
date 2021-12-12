from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class ListViewTests(TestCase):
    def test_list_of_users(self):
        """
        Checking list of created users.
        """
        create_user('Aleksey', 'Navalniy', 'FBK', 'svoboda')
        create_user('Михаил', 'Светов', 'СВТВ', 'liberty')
        response = self.client.get(reverse('users:list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['users']), ['<User: FBK>', '<User: СВТВ>'])


class RegisterUserViewTests(TestCase):
    def test_register(self):
        """
        Checking user registration.
        """
        url = reverse('users:register_user')
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
        url = reverse('users:register_user')
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
        self.assertQuerysetEqual(User.objects.all(), [])


class LoginUserViewTests(TestCase):
    def setUp(self):
        self.created_user = create_user('Aleksey', 'Navalniy', 'FBK', 'svoboda')

    def test_login(self):
        """
        Checking login.
        """
        url = reverse('login')
        user = {
            'username': self.created_user.username,
            'password': 'svoboda',
        }
        response = self.client.post(url, user, follow=True)
        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        logged_user = auth.get_user(self.client)
        self.assertEqual(logged_user, self.created_user)
        self.assertTrue(logged_user.is_authenticated)
        self.assertContains(response, 'Вы залогинены')

    def test_login_validation(self):
        """
        Checking login validation.
        """
        url = reverse('login')
        user = {
            'username': self.created_user.username,
            'password': 'liberty',
        }
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, 200)
        msg = 'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.'
        logged_user = auth.get_user(self.client)
        self.assertFalse(logged_user.is_authenticated)
        self.assertContains(response, msg)

    def test_logout(self):
        """
        Checking logout.
        """
        user = {
            'username': self.created_user.username,
            'password': 'svoboda',
        }
        response = self.client.post(reverse('login'), user, follow=True)
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        url = reverse('logout')
        response = self.client.post(url, follow=True)
        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        self.assertContains(response, 'Вы разлогинены')


class UpdateUserViewTests(TestCase):
    def setUp(self):
        self.first_user = create_user('Aleksey', 'Navalniy', 'FBK', 'svoboda')
        self.second_user = create_user('Михаил', 'Светов', 'СВТВ', 'liberty')

    def test_update(self):
        """
        Checking update user.
        """
        login_url = reverse('login')
        response = self.client.post(login_url, {'username': self.first_user.username, 'password': 'svoboda'})
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        update_url = reverse('users:update_user', args=(self.first_user.id, ))
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
        self.assertEqual(User.objects.get(pk=self.first_user.id).username, 'Либертарианец')

    def test_update_without_login(self):
        """
        Checking permissions to update.
        """
        update_url = reverse('users:update_user', args=(self.second_user.id, ))
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
        login_url = reverse('login')
        response = self.client.post(login_url, {'username': self.first_user.username, 'password': 'svoboda'})
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        update_url = reverse('users:update_user', args=(self.second_user.id, ))
        response = self.client.post(update_url, updated_user, follow=True)
        self.assertRedirects(
            response, '/users/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertEqual(User.objects.get(pk=self.first_user.id).username, 'FBK')
        self.assertContains(response, 'У вас нет прав для изменения другого пользователя')

    def test_update_not_yourself(self):
        """
        Checking permissions to update.
        """
        update_url = reverse('users:update_user', args=(self.second_user.id, ))
        updated_user = {
            'first_name': 'Мюррей',
            'last_name': 'Ротбарт',
            'username': 'Либертарианец',
            'password1': 'liberty',
            'password2': 'liberty',
        }
        login_url = reverse('login')
        response = self.client.post(login_url, {'username': self.first_user.username, 'password': 'svoboda'})
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        update_url = reverse('users:update_user', args=(self.second_user.id, ))
        response = self.client.post(update_url, updated_user, follow=True)
        self.assertRedirects(
            response, '/users/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertEqual(User.objects.get(pk=self.first_user.id).username, 'FBK')
        self.assertContains(response, 'У вас нет прав для изменения другого пользователя')


class DeleteUserViewTests(TestCase):
    def setUp(self):
        self.first_user = create_user('Aleksey', 'Navalniy', 'FBK', 'svoboda')
        self.second_user = create_user('Михаил', 'Светов', 'СВТВ', 'liberty')
        self.login_url = reverse('login')

    def test_delete(self):
        """
        Checking delete user.
        """
        response = self.client.post(self.login_url, {'username': self.first_user.username, 'password': 'svoboda'})
        delete_url = reverse('users:delete_user', args=(self.first_user.id, ))
        response = self.client.post(delete_url, follow=True)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=self.first_user.id)
        self.assertRedirects(
            response, '/users/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Пользователь успешно удалён')

    def test_delete_without_login(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        delete_url = reverse('users:delete_user', args=(self.second_user.id, ))
        response = self.client.post(delete_url, follow=True)
        self.assertEqual(User.objects.get(pk=self.second_user.id).username, 'СВТВ')
        # self.assertQuerysetEqual(list(User.objects.all()), ['<User: СВТВ>', '<User: FBK>'])
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertEqual(User.objects.get(pk=self.first_user.id).username, 'FBK')
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_delete_not_yourself(self):
        """
        Checking permissions to delete.
        """
        response = self.client.post(self.login_url, {'username': self.first_user.username, 'password': 'svoboda'})
        delete_url = reverse('users:delete_user', args=(self.second_user.id, ))
        response = self.client.post(delete_url, follow=True)
        self.assertEqual(User.objects.get(pk=self.second_user.id), self.second_user)
        self.assertRedirects(
            response, '/users/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'У вас нет прав для изменения другого пользователя')


def create_user(first_name, last_name, username, password):
    """
    Create user with given first_name, last_name, username and password.
    """
    user = User(first_name=first_name, last_name=last_name, username=username)
    user.set_password(password)
    user.save()
    return User.objects.get(username=username)
