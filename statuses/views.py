from django.contrib import messages
from django.contrib.auth import logout
from .models import Status
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView, UpdateView
from statuses.forms import StatusForm
from users.views import CustomLoginRequiredMixin


class StatusListView(CustomLoginRequiredMixin, generic.ListView):
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'
    model = Status


class CreateStatusView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:list')
    success_message = 'Статус успешно создан'


class UpdateStatusView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:list')
    success_message = 'Статус успешно изменён'


class DeleteStatusView(CustomLoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:list')

    def post(self, request, **kwargs):
        user = Status.objects.get(pk=kwargs['pk'])
        user.delete()
        messages.success(request, 'Статус успешно удалён')
        return redirect('statuses:list')
