from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import UserForm


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = '/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class IdentificationMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.id != kwargs['pk']:
            messages.error(request, 'У вас нет прав для изменения другого пользователя.')
            return redirect('users:list')
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
    form_class = UserForm
    success_message = 'Пользователь успешно зарегистрирован'


class UpdateUserView(CustomLoginRequiredMixin, IdentificationMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:list')
    success_message = 'Пользователь успешно изменён'


class DeleteUserView(CustomLoginRequiredMixin, IdentificationMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')

    def post(self, request, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        user.delete()
        messages.success(request, 'Пользователь успешно удалён')
        return redirect('users:list')
