from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView, UpdateView
from tasks.forms import TaskForm
from users.views import CustomLoginRequiredMixin

from .models import Task


class IdentificationMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.id != Task.objects.get(pk=kwargs['pk']).author:
            messages.error(request, 'Задачу может удалить только её автор')
            return redirect('tasks:list')
        return super().dispatch(request, *args, **kwargs)


class TasksListView(CustomLoginRequiredMixin, generic.ListView):
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    model = Task


class CreateTaskView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:list')
    success_message = 'Задача успешно создана'


class UpdateTaskView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:list')
    success_message = 'Задача успешно изменена'


class DeleteTaskView(CustomLoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:list')

    def post(self, request, **kwargs):
        user = Task.objects.get(pk=kwargs['pk'])
        user.delete()
        messages.success(request, 'Статус успешно удалён')
        return redirect('tasks:list')
