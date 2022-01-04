from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.edit import DeletionMixin


class ChecksPermissionsMixin:
    def handle_no_permission(self):
        messages.error(self.request, self.restriction_message)
        return redirect(self.redirect_url_while_restricted)


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        self.redirect_url_while_restricted = 'login'
        self.restriction_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'
        return super().dispatch(request, *args, **kwargs)


class DeleteSuccessMessageMixin:
    def post(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().post(request, *args, **kwargs)


class DeleteWithRestrictionsMixin(DeletionMixin):
    def post(self, request, *args, **kwargs):
        if self.check_delete_restrictions(request, **kwargs):
            return self.handle_no_permission()
        return super().post(request, *args, **kwargs)
