from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from mixins import CustomLoginRequiredMixin, DeleteViewWithRestrictions
from users.forms import UserRegistrationForm
from users.mixins import UserIdentificationMixin


class ListUserView(ListView):
    """List View of Users."""

    template_name = 'users/list.html'
    context_object_name = 'users'
    model = User


class LoginUserView(SuccessMessageMixin, LoginView):
    """Login View."""

    success_message = 'Вы залогинены'


class LogoutUserView(LogoutView):
    """Logout View."""

    def dispatch(self, request, *args, **kwargs):
        """Check that user can delete the Label.

        Args:
            request: HTTP request.
            *args: args.
            **kwargs: kwargs.

        Returns:
            Inherited method but with message.

        """
        messages.add_message(request, messages.INFO, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)


class RegisterUserView(SuccessMessageMixin, CreateView):
    """Create User View."""

    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'


class UpdateUserView(  # Noqa: WPS215
    CustomLoginRequiredMixin, UserIdentificationMixin, SuccessMessageMixin, UpdateView,
):
    """Update User View."""

    model = User
    form_class = UserRegistrationForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:list')
    success_message = 'Пользователь успешно изменён'


class DeleteUserView(CustomLoginRequiredMixin, UserIdentificationMixin, DeleteViewWithRestrictions):
    """Delete User View."""

    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')
    success_message = 'Пользователь успешно удалён'

    def check_delete_restrictions(self, request, **kwargs):
        """Check that user can delete User object.

        Args:
            request: HTTP request.
            **kwargs: kwargs.

        Returns:
            True if restricted, False otherwise.

        """
        self.restriction_message = 'Невозможно удалить пользователя, потому что он используется'
        self.redirect_url_while_restricted = self.success_url
        return bool(request.user.created_tasks.all() or request.user.assigned_tasks.all())
