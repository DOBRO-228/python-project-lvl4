from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from mixins import CustomLoginRequiredMixin, DeleteViewWithRestrictions
from statuses.models import Status


class StatusListView(CustomLoginRequiredMixin, ListView):
    """List view of Statuses."""

    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'


class CreateStatusView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Create status view."""

    model = Status
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:list')
    success_message = 'Статус успешно создан'
    fields = ['name']


class UpdateStatusView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update status view."""

    model = Status
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:list')
    success_message = 'Статус успешно изменён'
    fields = ['name']


class DeleteStatusView(CustomLoginRequiredMixin, DeleteViewWithRestrictions):
    """Delete status view."""

    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:list')
    success_message = 'Статус успешно удалён'

    def check_delete_restrictions(self, request, **kwargs):
        """Check that user can delete Status object.

        Args:
            request: HTTP request.
            **kwargs: kwargs.

        Returns:
            True if restricted, False otherwise.
        """
        self.restriction_message = 'Невозможно удалить статус, потому что он используется'
        self.redirect_url_while_restricted = self.success_url
        return bool(Status.objects.get(pk=kwargs['pk']).tasks.all())
