from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView, UpdateView
from tasks.forms import TaskForm
from tasks.models import Task
from mixins import ChecksPermissions, CustomLoginRequiredMixin, DeleteSuccessMessage, AuthorIdentificationMixin


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
