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

from .forms import UserForm


class ListView(generic.ListView):
    template_name = 'users/list.html'
    context_object_name = 'users'
    model = User


class UserLoginView(SuccessMessageMixin, LoginView):
    success_message = 'Вы залогинены'


class CheckAuthenticationMixin(object):
    def check_authentication(self, request, pk):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('login')
        elif request.user.id != pk:
            messages.error(request, 'У вас нет прав для изменения другого пользователя.')
            return redirect('users:list')
        return True


class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, 'Вы разлогинены')
        return response


class RegistrationView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    form_class = UserForm
    success_message = 'Пользователь успешно зарегистрирован'


class UserUpdateView(CheckAuthenticationMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:list')
    success_message = 'Пользователь успешно изменён'

    def get(self, request, *args, **kwargs):
        response = CheckAuthenticationMixin.check_authentication(self, request, kwargs['pk'])
        if response is True:
            return render(request, self.template_name, {'form': self.form_class(instance=request.user)})
        return response

    def form_valid(self, form):
        request = self.request
        response = CheckAuthenticationMixin.check_authentication(self, request, self.kwargs['pk'])
        if response is True:
            form.save()
            logout(request)
            messages.info(request, 'Пользователь успешно изменён')
            return redirect('users:list')
        return response


class DeleteUserView(CheckAuthenticationMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')

    def get(self, request, *args, **kwargs):
        response = CheckAuthenticationMixin.check_authentication(self, request, kwargs['pk'])
        if response is True:
            return render(request, self.template_name)
        return response

    def post(self, request, *args, **kwargs):
        response = CheckAuthenticationMixin.check_authentication(self, request, kwargs['pk'])
        if response is True:
            user = User.objects.get(pk=kwargs['pk'])
            user.delete()
            logout(request)
            messages.success(request, 'Пользователь успешно удалён')
            return redirect('users:list')
        return response
