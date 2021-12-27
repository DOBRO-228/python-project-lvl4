from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect


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
        return self.request.user.id == self.kwargs['pk']

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            self.redirect_url = 'users:list'
            self.message = 'У вас нет прав для изменения другого пользователя.'
        return super().dispatch(request, *args, **kwargs)


class DeleteSuccessMessage:
    def post(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().post(request, *args, **kwargs)
