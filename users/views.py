from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView, UpdateView
from mixins import (
    ChecksPermissions,
    CustomLoginRequiredMixin,
    DeleteSuccessMessage,
    PostWithRestrictionsMixin,
    UserIdentificationMixin,
)
from users.forms import UserRegistrationForm


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
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'


class UpdateUserView(
    ChecksPermissions, CustomLoginRequiredMixin, UserIdentificationMixin, SuccessMessageMixin, UpdateView
):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:list')
    success_message = 'Пользователь успешно изменён'


class DeleteUserView(
    ChecksPermissions,
    CustomLoginRequiredMixin,
    UserIdentificationMixin,
    PostWithRestrictionsMixin,
    DeleteSuccessMessage,
    DeleteView,
):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')
    success_message = 'Пользователь успешно удалён'

    def check_delete_restrictions(self, request, **kwargs):
        self.restriction_message = 'Невозможно удалить пользователя, потому что он используется'
        self.redirect_url_while_restricted = self.success_url
        return bool(request.user.created_task.all() or request.user.assigned_task.all())
