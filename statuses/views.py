from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView, UpdateView
from statuses.forms import StatusForm
from users.views import CustomLoginRequiredMixin, ChecksPermissions

from statuses.models import Status


class StatusListView(ChecksPermissions, CustomLoginRequiredMixin, generic.ListView):
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'
    model = Status


class CreateStatusView(ChecksPermissions, CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:list')
    success_message = 'Статус успешно создан'


class UpdateStatusView(ChecksPermissions, CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:list')
    success_message = 'Статус успешно изменён'


class DeleteStatusView(ChecksPermissions, CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:list')
    success_message = 'Статус успешно удалён'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Статус успешно удалён')
        return super().post(request, *args, **kwargs)
