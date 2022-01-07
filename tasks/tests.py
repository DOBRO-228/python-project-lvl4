from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from labels.models import Label
from statuses.models import Status
from tasks.models import Task


class TasksTests(TestCase):
    """Test Tasks app."""

    fixtures = ['tasks.json', 'statuses.json', 'labels.json', 'users.json']

    def setUp(self):
        """Prepare data for tests."""
        self.first_user = User.objects.get(pk=1)
        self.second_user = User.objects.get(pk=2)
        self.first_task = Task.objects.get(pk=1)
        self.second_task = Task.objects.get(pk=2)
        self.status_completed = Status.objects.get(pk=1)
        self.status_in_progress = Status.objects.get(pk=2)
        self.label_bug = Label.objects.get(pk=1)
        self.new_task_data = {
            'name': 'Salam',
            'description': '228',
            'status': self.status_in_progress.id,
            'performer': self.first_user.id,
            'labels': [self.label_bug.id],
        }

    def test_list_of_tasks(self):
        """Checking list of tasks."""
        self.client.force_login(self.first_user)
        response = self.client.get(reverse('tasks:list'))
        self.assertEqual(response.status_code, 200)
        response_tasks = list(response.context['tasks'])
        self.assertQuerysetEqual(response_tasks, [self.first_task, self.second_task])

    def test_list_of_tasks_without_login(self):
        """Checking list of tasks without login."""
        response = self.client.get(reverse('tasks:list'))
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True,
        )

    def test_task_creating(self):
        """Checking of task creating."""
        self.client.force_login(self.first_user)
        response = self.client.post(reverse('tasks:create'), self.new_task_data, follow=True)
        self.assertRedirects(
            response, '/tasks/', status_code=302, target_status_code=200, fetch_redirect_response=True,
        )
        self.assertContains(response, 'Задача успешно создана')
        created_task = Task.objects.get(name=self.new_task_data['name'])
        self.assertEquals(created_task.name, 'Salam')

    def test_task_creating_without_login(self):
        """Checking of task creating without login."""
        response = self.client.post(reverse('statuses:create'), self.new_task_data, follow=True)
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True,
        )

    def test_task_updating(self):
        """Checking of task updating."""
        self.client.force_login(self.second_user)
        update_url = reverse('tasks:update', args=(self.first_task.id, ))
        response = self.client.post(update_url, self.new_task_data, follow=True)
        self.assertRedirects(
            response, '/tasks/', status_code=302, target_status_code=200, fetch_redirect_response=True,
        )
        self.assertContains(response, 'Задача успешно изменена')
        self.first_task.refresh_from_db()
        self.assertEqual(self.first_task.name, 'Salam')
        self.assertEqual(self.first_task.description, '228')
        self.assertEqual(self.first_task.author, self.first_user)
        self.assertEqual(self.first_task.status, self.status_in_progress)
        self.assertEqual(self.first_task.performer, self.first_user)

    def test_task_updating_without_login(self):
        """Checking of permissions to update."""
        update_url = reverse('tasks:update', args=(self.first_task.id, ))
        response = self.client.post(update_url, self.new_task_data, follow=True)
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True,
        )
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        self.first_task.refresh_from_db()
        self.assertEqual(self.first_task.name, 'Имя')
        self.assertEqual(self.first_task.description, 'Описание')
        self.assertEqual(self.first_task.author, self.first_user)
        self.assertEqual(self.first_task.status, self.status_completed)
        self.assertEqual(self.first_task.performer, self.second_user)

    def test_task_deletion(self):
        """Checking of task deletion."""
        self.client.force_login(self.first_user)
        delete_url = reverse('tasks:delete', args=(self.first_task.id, ))
        response = self.client.post(delete_url, follow=True)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=self.first_task.id)
        self.assertRedirects(
            response, '/tasks/', status_code=302, target_status_code=200, fetch_redirect_response=True,
        )
        self.assertContains(response, 'Задача успешно удалена')

    def test_task_deletion_without_login(self):
        """Checking of task deletion without login."""
        delete_url = reverse('tasks:delete', args=(self.first_task.id, ))
        response = self.client.post(delete_url, follow=True)
        self.assertTrue(Task.objects.filter(pk=self.first_task.id).exists())
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True,
        )
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_restrictions_to_delete(self):
        """Checking of deletion while user isn't an author."""
        self.client.force_login(self.second_user)
        delete_url = reverse('tasks:delete', args=(self.first_task.id, ))
        response = self.client.post(delete_url, follow=True)
        self.assertTrue(Task.objects.filter(pk=self.first_task.id).exists())
        self.assertRedirects(
            response, '/tasks/', status_code=302, target_status_code=200, fetch_redirect_response=True,
        )
        self.assertContains(response, 'Задачу может удалить только её автор')

    def test_detail_view(self):
        """Checking of detail view."""
        self.client.force_login(self.second_user)
        self.client.post(reverse('tasks:create'), self.new_task_data, follow=True)
        created_task = Task.objects.get(name=self.new_task_data['name'])
        detail_task_url = reverse('tasks:detail', args=(created_task.id, ))
        response = self.client.get(detail_task_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, created_task)
        self.assertContains(response, self.new_task_data['name'])
        self.assertContains(response, self.new_task_data['description'])
        self.assertContains(response, self.new_task_data['performer'])
        self.assertContains(response, self.second_user)
        self.assertContains(response, self.new_task_data['status'])
        self.assertContains(response, self.label_bug)

    def test_filter_self_tasks(self):
        """Checking of filtered list."""
        self.client.force_login(self.first_user)
        filtered_list = '{0}?self_tasks=on'.format(reverse('tasks:list'))
        response = self.client.get(filtered_list)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['tasks']), [self.first_task])

    def test_filter_by_status(self):
        """Checking of filtered list."""
        self.client.force_login(self.first_user)
        filtered_list = '{0}?status=2'.format(reverse('tasks:list'))
        response = self.client.get(filtered_list)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['tasks']), [self.second_task])

    def test_filter_by_performer(self):
        """Checking of filtered list."""
        self.client.force_login(self.first_user)
        filtered_list = '{0}?performer=2'.format(reverse('tasks:list'))
        response = self.client.get(filtered_list)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['tasks']), [self.first_task])

    def test_filter_by_label(self):
        """Checking of filtered list."""
        self.client.force_login(self.first_user)
        self.client.post(reverse('tasks:create'), self.new_task_data, follow=True)
        created_task = Task.objects.get(name=self.new_task_data['name'])
        filtered_list = '{0}?labels=1'.format(reverse('tasks:list'))
        response = self.client.get(filtered_list)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['tasks']), [created_task])

    def test_filter_by_multiply_fields(self):
        """Checking of filtered list."""
        self.client.force_login(self.second_user)
        self.client.post(reverse('tasks:create'), self.new_task_data, follow=True)
        created_task = Task.objects.get(name=self.new_task_data['name'])
        filtered_list = '{0}?status=2&self_tasks=on'.format(reverse('tasks:list'))
        response = self.client.get(filtered_list)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['tasks']), [self.second_task, created_task])
        filtered_list = '{0}?status=2&labels=1&self_tasks=on'.format(reverse('tasks:list'))
        response = self.client.get(filtered_list)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['tasks']), [created_task])
