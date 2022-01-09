from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
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
    success_message = _('Status created successfully')
    fields = ['name']


class UpdateStatusView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update status view."""

    model = Status
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:list')
    success_message = _('Status changed successfully')
    fields = ['name']


class DeleteStatusView(CustomLoginRequiredMixin, DeleteViewWithRestrictions):
    """Delete status view."""

    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:list')
    success_message = _('Status deleted successfully')

    def check_permissions_to_delete(self, request, **kwargs):
        """Check that user can delete Status object.

        Args:
            request: HTTP request.
            **kwargs: kwargs.

        Returns:
            True if restricted, False otherwise.
        """
        self.restriction_message = _('Impossible to delete a status because it is in use')
        self.redirect_url_while_restricted = self.success_url
        return bool(Status.objects.get(pk=kwargs['pk']).tasks.all())
