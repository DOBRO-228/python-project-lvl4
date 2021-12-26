from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView, UpdateView

from users.forms import UserRegistrationForm


class ChecksPermissions:
    def handle_no_permission(self):
        messages.error(self.request, self.message)
        return redirect(self.redirect_url)


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        self.redirect_url = 'login'
        self.message = 'Вы не авторизованы! Пожалуйста, выполните вход.'
        return super().dispatch(request, *args, **kwargs)


class IdentificationMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.id == self.kwargs['pk']

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            self.redirect_url = 'users:list'
            self.message = 'У вас нет прав для изменения другого пользователя.'
        return super().dispatch(request, *args, **kwargs)


class ListUserView(generic.ListView):
    template_name = 'users/list.html'
    context_object_name = 'users'
    model = User


class LoginUserView(SuccessMessageMixin, LoginView):
    success_message = 'Вы залогинены'


class LogoutUserView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)


class RegisterUserView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegistrationForm
    success_message = 'Пользователь успешно зарегистрирован'


class UpdateUserView(ChecksPermissions, CustomLoginRequiredMixin, IdentificationMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:list')
    success_message = 'Пользователь успешно изменён'


class DeleteUserView(ChecksPermissions, CustomLoginRequiredMixin, IdentificationMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Пользователь успешно удалён')
        return super().post(request, *args, **kwargs)
