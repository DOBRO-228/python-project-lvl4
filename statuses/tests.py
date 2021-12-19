from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Status


class StatusListViewTests(TestCase):
    fixtures = ['statuses.json', 'users.json']

    def setUp(self):
        self.user = User.objects.get(pk=45)

    def test_list_of_statuses(self):
        """
        Checking list of statuses.
        """
        self.client.login(username=self.user.username, password='svoboda')
        response = self.client.get(reverse('statuses:list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['statuses']), ['<Status: завершён>', '<Status: в работе>'])

    def test_list_of_statuses_without_login(self):
        """
        Checking list of statuses without login.
        """
        response = self.client.get(reverse('statuses:list'))
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )


class CreateStatusViewTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user = User.objects.get(pk=45)

    def test_creating(self):
        """
        Checking status creating.
        """
        self.client.login(username=self.user.username, password='svoboda')
        status = {'name': 'In progress'}
        response = self.client.post(reverse('statuses:create'), status, follow=True)
        self.assertRedirects(
            response, '/statuses/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Статус успешно создан')
        created_status = Status.objects.get(name=status['name'])
        self.assertEquals(created_status.name, 'In progress')

    def test_creating_status_without_login(self):
        """
        Checking status creating without login.
        """
        status = {'name': 'In progress'}
        response = self.client.post(reverse('statuses:create'), status, follow=True)
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )


class UpdateStatusViewTests(TestCase):
    fixtures = ['statuses.json', 'users.json']

    def setUp(self):
        self.user = User.objects.get(pk=45)
        self.status = Status.objects.get(pk=1)

    def test_updating(self):
        """
        Checking status updating.
        """
        self.client.login(username=self.user.username, password='svoboda')
        update_url = reverse('statuses:update', args=(self.status.id, ))
        updated_status = {'name': 'In progress'}
        response = self.client.post(update_url, updated_status, follow=True)
        self.assertRedirects(
            response, '/statuses/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Статус успешно изменён')
        self.assertEqual(Status.objects.get(pk=self.status.id).name, 'In progress')

    def test_update_without_login(self):
        """
        Checking permissions to update.
        """
        update_url = reverse('statuses:update', args=(self.status.id, ))
        updated_status = {'name': 'In progress'}
        response = self.client.post(update_url, updated_status, follow=True)
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        self.assertEqual(Status.objects.get(pk=self.status.id).name, 'завершён')


class DeleteStatusViewTests(TestCase):
    fixtures = ['statuses.json', 'users.json']

    def setUp(self):
        self.user = User.objects.get(pk=45)
        self.status = Status.objects.get(pk=1)

    def test_delete(self):
        """
        Checking status deletion.
        """
        self.client.login(username=self.user.username, password='svoboda')
        delete_url = reverse('statuses:delete', args=(self.status.id, ))
        response = self.client.post(delete_url, follow=True)
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(pk=self.status.id)
        self.assertRedirects(
            response, '/statuses/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Статус успешно удалён')

    def test_delete_without_login(self):
        """
        Checking status deletion without login.
        """
        delete_url = reverse('statuses:delete', args=(self.status.id, ))
        response = self.client.post(delete_url, follow=True)
        self.assertEqual(Status.objects.get(pk=self.status.id).name, 'завершён')
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')
