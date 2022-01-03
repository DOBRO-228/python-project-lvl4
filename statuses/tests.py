from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from statuses.models import Status
from tasks.models import Task


class StatusesTests(TestCase):
    fixtures = ['statuses.json', 'tasks.json', 'users.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.status_completed = Status.objects.get(pk=1)
        self.status_in_progress = Status.objects.get(pk=2)

    def test_list_of_statuses(self):
        """
        Checking of list of statuses.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('statuses:list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['statuses']), [self.status_completed, self.status_in_progress])

    def test_list_of_statuses_without_login(self):
        """
        Checking of list of statuses without login.
        """
        response = self.client.get(reverse('statuses:list'))
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    def test_status_creating(self):
        """
        Checking of status creating.
        """
        self.client.force_login(self.user)
        status = {'name': 'In progress'}
        response = self.client.post(reverse('statuses:create'), status, follow=True)
        self.assertRedirects(
            response, '/statuses/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Статус успешно создан')
        created_status = Status.objects.get(name=status['name'])
        self.assertEquals(created_status.name, 'In progress')

    def test_status_creating_without_login(self):
        """
        Checking of status creating without login.
        """
        status = {'name': 'In progress'}
        response = self.client.post(reverse('statuses:create'), status, follow=True)
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    def test_status_updating(self):
        """
        Checking of status updating.
        """
        self.client.force_login(self.user)
        update_url = reverse('statuses:update', args=(self.status_completed.id, ))
        updated_status = {'name': 'In progress'}
        response = self.client.post(update_url, updated_status, follow=True)
        self.assertRedirects(
            response, '/statuses/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Статус успешно изменён')
        self.assertEqual(Status.objects.get(pk=self.status_completed.id), self.status_completed)

    def test_status_updating_without_login(self):
        """
        Checking of permissions to update.
        """
        update_url = reverse('statuses:update', args=(self.status_completed.id, ))
        updated_status = {'name': 'In progress'}
        response = self.client.post(update_url, updated_status, follow=True)
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        self.assertEqual(Status.objects.get(pk=self.status_completed.id), self.status_completed)

    def test_status_deletion(self):
        """
        Checking of status deletion.
        """
        self.task = Task.objects.get(pk=1)
        self.task.status = self.status_in_progress
        self.task.save()
        self.client.force_login(self.user)
        delete_url = reverse('statuses:delete', args=(self.status_completed.id, ))
        response = self.client.post(delete_url, follow=True)
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(pk=self.status_completed.id)
        self.assertRedirects(
            response, '/statuses/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Статус успешно удалён')

    def test_status_deletion_without_login(self):
        """
        Checking of status deletion without login.
        """
        delete_url = reverse('statuses:delete', args=(self.status_completed.id, ))
        response = self.client.post(delete_url, follow=True)
        self.assertEqual(Status.objects.get(pk=self.status_completed.id), self.status_completed)
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_restrictions_to_delete(self):
        """
        Checking of deletion while task references on status.
        """
        self.client.force_login(self.user)
        delete_url = reverse('statuses:delete', args=(self.status_completed.id, ))
        response = self.client.post(delete_url, follow=True)
        self.assertTrue(Status.objects.filter(pk=self.status_completed.id).exists())
        self.assertRedirects(
            response, '/statuses/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Невозможно удалить статус, потому что он используется')
