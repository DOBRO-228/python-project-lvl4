from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django_filters.views import FilterView
from mixins import ChecksPermissionsMixin, CustomLoginRequiredMixin, DeleteSuccessMessageMixin
from tasks.mixins import AuthorIdentificationMixin
from tasks.filters import TaskFilter
from tasks.models import Task


class TasksListView(ChecksPermissionsMixin, CustomLoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class DetailTaskView(ChecksPermissionsMixin, CustomLoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'


class CreateTaskView(ChecksPermissionsMixin, CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:list')
    success_message = 'Задача успешно создана'
    fields = ['name', 'description', 'status', 'performer', 'labels']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTaskView(ChecksPermissionsMixin, CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:list')
    success_message = 'Задача успешно изменена'
    fields = ['name', 'description', 'status', 'performer', 'labels']


class DeleteTaskView(
    ChecksPermissionsMixin, AuthorIdentificationMixin, CustomLoginRequiredMixin, DeleteSuccessMessageMixin, DeleteView
):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:list')
    success_message = 'Задача успешно удалена'
