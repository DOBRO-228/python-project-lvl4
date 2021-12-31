from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic.edit import DeletionMixin
from tasks.models import Task


class ChecksPermissions:
    def handle_no_permission(self):
        messages.error(self.request, self.message)
        return redirect(self.redirect_url)


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        self.redirect_url = 'login'
        self.message = 'Вы не авторизованы! Пожалуйста, выполните вход.'
        return super().dispatch(request, *args, **kwargs)


class UserIdentificationMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.id == self.kwargs['pk']

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            self.redirect_url = 'users:list'
            self.message = 'У вас нет прав для изменения другого пользователя.'
        return super().dispatch(request, *args, **kwargs)


class AuthorIdentificationMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.id == Task.objects.get(pk=self.kwargs['pk']).author.id

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            self.redirect_url = 'tasks:list'
            self.message = 'Задачу может удалить только её автор'
        return super().dispatch(request, *args, **kwargs)


class PermissionToDeleteMixin(DeletionMixin):
    def post(self, request, *args, **kwargs):
        if request.user.created_task.all() or request.user.assigned_task.all():
            self.redirect_url = 'users:list'
            self.message = 'Невозможно удалить пользователя, потому что он используется'
            return self.handle_no_permission()
        return super().post(request, *args, **kwargs)


class DeleteSuccessMessage:
    def post(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().post(request, *args, **kwargs)
