from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from statuses.models import Status
from tasks.models import Task


class TasksTests(TestCase):
    fixtures = ['tasks.json', 'statuses.json', 'users.json']

    def setUp(self):
        self.first_user = User.objects.get(pk=1)
        self.second_user = User.objects.get(pk=2)
        self.first_task = Task.objects.get(pk=1)
        self.second_task = Task.objects.get(pk=2)
        self.status_completed = Status.objects.get(pk=1)
        self.status_in_progress = Status.objects.get(pk=2)
        self.new_task = {
            'name': 'Salam',
            'description': '228',
            'status': self.status_in_progress.id,
            'performer': self.first_user.id,
        }

    def test_list_of_tasks(self):
        """
        Checking of list of tasks.
        """
        self.client.force_login(self.first_user)
        response = self.client.get(reverse('tasks:list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['tasks']), [self.first_task, self.second_task])

    def test_list_of_tasks_without_login(self):
        """
        Checking of list of tasks without login.
        """
        response = self.client.get(reverse('tasks:list'))
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    def test_task_creating(self):
        """
        Checking of task creating.
        """
        self.client.force_login(self.first_user)
        response = self.client.post(reverse('tasks:create'), self.new_task, follow=True)
        self.assertRedirects(
            response, '/tasks/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Задача успешно создана')
        created_task = Task.objects.get(name=self.new_task['name'])
        self.assertEquals(created_task.name, 'Salam')

    def test_task_creating_without_login(self):
        """
        Checking of task creating without login.
        """
        response = self.client.post(reverse('statuses:create'), self.new_task, follow=True)
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    def test_task_updating(self):
        """
        Checking of task updating.
        """
        self.client.force_login(self.second_user)
        update_url = reverse('tasks:update', args=(self.first_task.id, ))
        response = self.client.post(update_url, self.new_task, follow=True)
        self.assertRedirects(
            response, '/tasks/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Задача успешно изменена')
        self.first_task.refresh_from_db()
        self.assertEqual(self.first_task.name, 'Salam')
        self.assertEqual(self.first_task.description, '228')
        self.assertEqual(self.first_task.author, self.first_user)
        self.assertEqual(self.first_task.status, self.status_in_progress)
        self.assertEqual(self.first_task.performer, self.first_user)

    def test_task_updating_without_login(self):
        """
        Checking of permissions to update.
        """
        update_url = reverse('tasks:update', args=(self.first_task.id, ))
        response = self.client.post(update_url, self.new_task, follow=True)
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        self.first_task.refresh_from_db()
        self.assertEqual(self.first_task.name, 'Имя')
        self.assertEqual(self.first_task.description, 'Описание')
        self.assertEqual(self.first_task.author, self.first_user)
        self.assertEqual(self.first_task.status, self.status_completed)
        self.assertEqual(self.first_task.performer, self.second_user)

    def test_task_deletion(self):
        """
        Checking of task deletion.
        """
        self.client.force_login(self.first_user)
        delete_url = reverse('tasks:delete', args=(self.first_task.id, ))
        response = self.client.post(delete_url, follow=True)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=self.first_task.id)
        self.assertRedirects(
            response, '/tasks/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Задача успешно удалена')

    def test_task_deletion_without_login(self):
        """
        Checking of task deletion without login.
        """
        delete_url = reverse('tasks:delete', args=(self.first_task.id, ))
        response = self.client.post(delete_url, follow=True)
        self.assertTrue(Task.objects.filter(pk=self.first_task.id).exists())
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_restrictions_to_delete(self):
        """
        Checking of deletion while user isn't an author.
        """
        self.client.force_login(self.second_user)
        delete_url = reverse('tasks:delete', args=(self.first_task.id, ))
        response = self.client.post(delete_url, follow=True)
        self.assertTrue(Task.objects.filter(pk=self.first_task.id).exists())
        self.assertRedirects(
            response, '/tasks/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Задачу может удалить только её автор')
