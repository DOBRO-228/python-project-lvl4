from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView, UpdateView
from mixins import ChecksPermissions, CustomLoginRequiredMixin, DeleteSuccessMessage
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
    success_message = 'Статус успешно создан'


class UpdateLabelView(ChecksPermissions, CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels:list')
    success_message = 'Метка успешно изменена'


class DeleteLabelView(ChecksPermissions, CustomLoginRequiredMixin, DeleteSuccessMessage, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels:list')
    success_message = 'Метка успешно удалена'

    def post(self, request, *args, **kwargs):
        if request.user.created_task.all() or request.user.assigned_task.all():
            self.redirect_url = 'labels:list'
            self.message = 'Невозможно удалить метку, потому что она используется'
            return self.handle_no_permission()
        return super().post(request, *args, **kwargs)
