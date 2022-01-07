from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
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
        self.restriction_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'
        return super().dispatch(request, *args, **kwargs)


class DeleteSuccessMessageMixin(object):
    """Custom LoginRequiredMixin."""

    def delete(self, request, *args, **kwargs):
        """Add success message of deletion object."""
        messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)


class DeleteViewWithRestrictions(DeleteSuccessMessageMixin, DeleteView):
    """DeleteView with checking permissions to delete."""

    def delete(self, request, *args, **kwargs):
        """Add check for deletion object."""
        if self.check_delete_restrictions(request, **kwargs):
            return self.handle_no_permission()
        return super().delete(request, *args, **kwargs)
