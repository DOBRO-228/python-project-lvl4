from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic.edit import DeletionMixin
from tasks.models import Task


class ChecksPermissions:
    def handle_no_permission(self):
        messages.error(self.request, self.restriction_message)
        return redirect(self.redirect_url_while_restricted)


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        self.redirect_url_while_restricted = 'login'
        self.restriction_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'
        return super().dispatch(request, *args, **kwargs)


class UserIdentificationMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.id == self.kwargs['pk']

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            self.redirect_url_while_restricted = 'users:list'
            self.restriction_message = 'У вас нет прав для изменения другого пользователя.'
        return super().dispatch(request, *args, **kwargs)


class AuthorIdentificationMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.id == Task.objects.get(pk=self.kwargs['pk']).author.id

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            self.redirect_url_while_restricted = 'tasks:list'
            self.restriction_message = 'Задачу может удалить только её автор'
        return super().dispatch(request, *args, **kwargs)


class DeleteSuccessMessage:
    def post(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().post(request, *args, **kwargs)


class PostWithRestrictionsMixin(DeletionMixin):
    def post(self, request, *args, **kwargs):
        if self.check_delete_restrictions(request, **kwargs):
            return self.handle_no_permission()
        return super().post(request, *args, **kwargs)
