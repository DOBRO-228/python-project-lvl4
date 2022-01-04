from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView, UpdateView
from labels.models import Label
from mixins import ChecksPermissionsMixin, CustomLoginRequiredMixin, DeleteSuccessMessageMixin, DeleteWithRestrictionsMixin


class LabelListView(ChecksPermissionsMixin, CustomLoginRequiredMixin, generic.ListView):
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'


class CreateLabelView(ChecksPermissionsMixin, CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels:list')
    success_message = 'Метка успешно создана'
    fields = ['name']


class UpdateLabelView(ChecksPermissionsMixin, CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels:list')
    success_message = 'Метка успешно изменена'
    fields = ['name']


class DeleteLabelView(
    ChecksPermissionsMixin, DeleteWithRestrictionsMixin, CustomLoginRequiredMixin, DeleteSuccessMessageMixin, DeleteView
):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels:list')
    success_message = 'Метка успешно удалена'

    def check_delete_restrictions(self, request, **kwargs):
        self.restriction_message = 'Невозможно удалить метку, потому что она используется'
        self.redirect_url_while_restricted = self.success_url
        return bool(Label.objects.get(pk=kwargs['pk']).tasks.all())
