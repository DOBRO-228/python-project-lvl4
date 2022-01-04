from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView, UpdateView
from mixins import ChecksPermissionsMixin, CustomLoginRequiredMixin, DeleteSuccessMessageMixin, DeleteWithRestrictionsMixin
from statuses.models import Status


class StatusListView(ChecksPermissionsMixin, CustomLoginRequiredMixin, generic.ListView):
    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'


class CreateStatusView(ChecksPermissionsMixin, CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:list')
    success_message = 'Статус успешно создан'
    fields = ['name']


class UpdateStatusView(ChecksPermissionsMixin, CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:list')
    success_message = 'Статус успешно изменён'
    fields = ['name']


class DeleteStatusView(
    ChecksPermissionsMixin, DeleteWithRestrictionsMixin, CustomLoginRequiredMixin, DeleteSuccessMessageMixin, DeleteView
):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:list')
    success_message = 'Статус успешно удалён'

    def check_delete_restrictions(self, request, **kwargs):
        self.restriction_message = 'Невозможно удалить статус, потому что он используется'
        self.redirect_url_while_restricted = self.success_url
        return bool(Status.objects.get(pk=kwargs['pk']).tasks.all())
