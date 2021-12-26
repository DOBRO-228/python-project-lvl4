from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView, UpdateView
from tasks.forms import TaskForm
from users.views import CustomLoginRequiredMixin, ChecksPermissions

from tasks.models import Task


class IdentificationMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.id == Task.objects.get(author=self.kwargs['pk'])

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            self.redirect_url = 'users:list'
            self.message = 'У вас нет прав для изменения другого пользователя.'
        return super().dispatch(request, *args, **kwargs)


class TasksListView(ChecksPermissions, CustomLoginRequiredMixin, generic.ListView):
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    model = Task


class CreateTaskView(ChecksPermissions, CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:list')
    success_message = 'Задача успешно создана'


class UpdateTaskView(ChecksPermissions, CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:list')
    success_message = 'Задача успешно изменена'


class DeleteTaskView(ChecksPermissions, CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:list')
    success_message = 'Задача успешна удалена'
