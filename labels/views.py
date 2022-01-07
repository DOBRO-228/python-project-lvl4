from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from labels.models import Label
from mixins import CustomLoginRequiredMixin, DeleteViewWithRestrictions


class LabelListView(CustomLoginRequiredMixin, ListView):
    """ListView of Labels."""

    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'


class CreateLabelView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    """CreateView of Label."""

    model = Label
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels:list')
    success_message = 'Метка успешно создана'
    fields = ['name']


class UpdateLabelView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """UpdateView of Label."""

    model = Label
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels:list')
    success_message = 'Метка успешно изменена'
    fields = ['name']


class DeleteLabelView(CustomLoginRequiredMixin, DeleteViewWithRestrictions):
    """DeleteView of Label."""

    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels:list')
    success_message = 'Метка успешно удалена'

    def check_delete_restrictions(self, request, **kwargs):
        """Check that user can delete the Label.

        Args:
            request: HTTP request.
            **kwargs: kwargs.

        Returns:
            True if restricted, False otherwise.

        """
        self.restriction_message = 'Невозможно удалить метку, потому что она используется'
        self.redirect_url_while_restricted = self.success_url
        return bool(Label.objects.get(pk=kwargs['pk']).tasks.all())
