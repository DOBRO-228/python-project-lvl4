from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView


class HandleNoPermissionMixin(object):
    """Override handle_no_permission class method."""

    def handle_no_permission(self):
        """handle_no_permission class method with error message and redirect.

        Returns:
            HttpResponseRedirect.
        """
        messages.error(self.request, self.restriction_message)
        return redirect(self.redirect_url_while_restricted)


class CustomLoginRequiredMixin(HandleNoPermissionMixin, LoginRequiredMixin):
    """Custom LoginRequiredMixin."""

    def dispatch(self, request, *args, **kwargs):
        """Dispatch class method with error message and redirect."""
        self.redirect_url_while_restricted = 'login'
        self.restriction_message = _('You are not authorized! Please sign in.')
        return super().dispatch(request, *args, **kwargs)


class DeleteSuccessMessageMixin(object):
    """Custom LoginRequiredMixin."""

    def delete(self, request, *args, **kwargs):
        """Add success message when delete the object."""
        messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)


class DeleteViewWithRestrictions(DeleteSuccessMessageMixin, DeleteView):
    """DeleteView with checking permissions to delete."""

    def delete(self, request, *args, **kwargs):
        """Before deletion of object check permissions to do that."""
        if self.check_permissions_to_delete(request, **kwargs):
            return self.handle_no_permission()
        return super().delete(request, *args, **kwargs)
