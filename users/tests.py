from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


# Create your tests here.


class UserModelTests(TestCase):

    def setUp(self):
        self.created_user = create_user('Aleksey', 'Navalniy', 'FBK', 'svoboda')

    def test_create_user(self):
        """
        Checking of creating user.
        """
        self.assertEquals(self.created_user.first_name, 'Aleksey')
        self.assertEquals(self.created_user.last_name, 'Navalniy')
        self.assertEquals(self.created_user.check_password("svoboda"), True)

    def test_update_user(self):
        """
        Checking of updating user.
        """
        self.created_user.first_name = 'Михаил'
        self.created_user.last_name = 'Светов'
        self.created_user.username = 'СВТВ'
        self.created_user.set_password('liberty')
        self.created_user.save()
        user = User.objects.get(username='СВТВ')
        self.assertEquals(user.first_name, 'Михаил')
        self.assertEquals(user.last_name, 'Светов')
        self.assertEquals(user.check_password("liberty"), True)

    def test_delete_user(self):
        """
        Checking of deletion user.
        """
        user = User.objects.get(username='FBK')
        self.assertEquals(user.first_name, 'Aleksey')
        self.assertEquals(user.last_name, 'Navalniy')
        self.created_user.delete()
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='FBK')


class ListViewTests(TestCase):
    def test_list_of_user(self):
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

    def test_pass_validation(self):
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
        self.assertContains(response, 'Вы успешно вошли')

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
        self.assertContains(response, msg)

    def test_logout(self):
        """
        Checking logout.
        """
        url = reverse('logout')
        response = self.client.post(url, follow=True)
        self.assertRedirects(
            response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Вы разлогинены')


class UpdateUserViewTests(TestCase):
    def test_update(self):
        """
        Checking update user.
        """
        user = create_user('Aleksey', 'Navalniy', 'FBK', 'svoboda')
        login_url = reverse('login')
        response = self.client.post(login_url, {'username': user.username, 'password': 'svoboda'})
        update_url = reverse('users:update_user', args=(user.id, ))
        updated_user = {
            'first_name': 'Михаил',
            'last_name': 'Светов',
            'username': 'СВТВ',
            'password1': 'liberty',
            'password2': 'liberty',
        }
        response = self.client.post(update_url, updated_user, follow=True)
        self.assertRedirects(
            response, '/users/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Пользователь успешно изменён')
        self.assertQuerysetEqual(User.objects.all(), ['<User: СВТВ>'])

    def test_permissions_to_update(self):
        """
        Checking permissions to update.
        """
        first_user = create_user('Aleksey', 'Navalniy', 'FBK', 'svoboda')
        second_user = create_user('Михаил', 'Светов', 'СВТВ', 'liberty')
        login_url = reverse('login')
        response = self.client.post(login_url, {'username': first_user.username, 'password': 'svoboda'})
        update_url = reverse('users:update_user', args=(second_user.id, ))
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
        self.assertContains(response, 'У вас нет прав для изменения другого пользователя')


class DeleteUserViewTests(TestCase):
    def test_delete(self):
        """
        Checking delete user.
        """
        user = create_user('Aleksey', 'Navalniy', 'FBK', 'svoboda')
        login_url = reverse('login')
        response = self.client.post(login_url, {'username': user.username, 'password': 'svoboda'})
        delete_url = reverse('users:delete_user', args=(user.id, ))
        response = self.client.post(delete_url, follow=True)
        self.assertQuerysetEqual(User.objects.all(), [])
        self.assertRedirects(
            response, '/users/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Пользователь успешно удалён')

    def test_permissions_to_delete(self):
        """
        Checking permissions to delete.
        """
        first_user = create_user('Aleksey', 'Navalniy', 'FBK', 'svoboda')
        second_user = create_user('Михаил', 'Светов', 'СВТВ', 'liberty')
        login_url = reverse('login')
        response = self.client.post(login_url, {'username': first_user.username, 'password': 'svoboda'})
        delete_url = reverse('users:delete_user', args=(second_user.id, ))
        response = self.client.post(delete_url, follow=True)
        self.assertQuerysetEqual(list(User.objects.all()), ['<User: СВТВ>', '<User: FBK>'])
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
