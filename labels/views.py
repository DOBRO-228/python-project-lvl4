from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView, UpdateView
from mixins import ChecksPermissions, CustomLoginRequiredMixin, DeleteSuccessMessage, PostWithRestrictionsMixin
from labels.forms import LabelForm
from labels.models import Label


class LabelListView(ChecksPermissions, CustomLoginRequiredMixin, generic.ListView):
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'


class CreateLabelView(ChecksPermissions, CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels:list')
    success_message = 'Метка успешно создана'


class UpdateLabelView(ChecksPermissions, CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels:list')
    success_message = 'Метка успешно изменена'


class DeleteLabelView(
    ChecksPermissions, PostWithRestrictionsMixin, CustomLoginRequiredMixin, DeleteSuccessMessage, DeleteView
):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels:list')
    success_message = 'Метка успешно удалена'

    def check_delete_restrictions(self, request, **kwargs):
        self.restriction_message = 'Невозможно удалить метку, потому что она используется'
        self.redirect_url_while_restricted = self.success_url
        return bool(Label.objects.get(pk=kwargs['pk']).tasks.all())
