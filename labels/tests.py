from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from labels.models import Label


class LabelsTests(TestCase):
    fixtures = ['labels.json', 'users.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.label_bug = Label.objects.get(pk=1)

    def test_list_of_labels(self):
        """
        Checking of list of labels.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('labels:list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['labels']), [self.label_bug])

    def test_list_of_labels_without_login(self):
        """
        Checking of list of labels without login.
        """
        response = self.client.get(reverse('labels:list'))
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    def test_label_creating(self):
        """
        Checking of label creating.
        """
        self.client.force_login(self.user)
        label = {'name': 'Релиз'}
        response = self.client.post(reverse('labels:create'), label, follow=True)
        self.assertRedirects(
            response, '/labels/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Метка успешно создана')
        created_label = Label.objects.get(name=label['name'])
        self.assertEquals(created_label.name, 'Релиз')

    def test_label_creating_without_login(self):
        """
        Checking of label creating without login.
        """
        label = {'name': 'Релиз'}
        response = self.client.post(reverse('labels:create'), label, follow=True)
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    def test_label_updating(self):
        """
        Checking of label updating.
        """
        self.client.force_login(self.user)
        update_url = reverse('labels:update', args=(self.label_bug.id, ))
        updated_label = {'name': 'Баг'}
        response = self.client.post(update_url, updated_label, follow=True)
        self.assertRedirects(
            response, '/labels/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Метка успешно изменена')
        self.assertEqual(Label.objects.get(pk=self.label_bug.id).name, 'Баг')

    def test_label_updating_without_login(self):
        """
        Checking of permissions to update.
        """
        update_url = reverse('labels:update', args=(self.label_bug.id, ))
        updated_label = {'name': 'Релиз'}
        response = self.client.post(update_url, updated_label, follow=True)
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        self.label_bug.refresh_from_db()
        self.assertEqual(self.label_bug.name, 'Баг')

    def test_label_deletion(self):
        """
        Checking of label deletion.
        """
        self.client.force_login(self.user)
        delete_url = reverse('labels:delete', args=(self.label_bug.id, ))
        response = self.client.post(delete_url, follow=True)
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(pk=self.label_bug.id)
        self.assertRedirects(
            response, '/labels/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Метка успешно удалена')

    def test_label_deletion_without_login(self):
        """
        Checking of label deletion without login.
        """
        delete_url = reverse('labels:delete', args=(self.label_bug.id, ))
        response = self.client.post(delete_url, follow=True)
        self.assertEqual(Label.objects.get(pk=self.label_bug.id), self.label_bug)
        self.assertRedirects(
            response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')
