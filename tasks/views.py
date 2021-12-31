from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DeleteView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from mixins import AuthorIdentificationMixin, ChecksPermissions, CustomLoginRequiredMixin, DeleteSuccessMessage
from tasks.forms import TaskForm
from tasks.models import Task


class TasksListView(ChecksPermissions, CustomLoginRequiredMixin, generic.ListView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'


class DetailTaskView(ChecksPermissions, CustomLoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'object'


class CreateTaskView(ChecksPermissions, CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:list')
    success_message = 'Задача успешно создана'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTaskView(ChecksPermissions, CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:list')
    success_message = 'Задача успешно изменена'


class DeleteTaskView(
    ChecksPermissions, AuthorIdentificationMixin, CustomLoginRequiredMixin, DeleteSuccessMessage, DeleteView
):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:list')
    success_message = 'Задача успешно удалена'
