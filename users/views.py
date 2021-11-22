# from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
# from django.urls import reverse
from django.views import generic
# from django.utils import timezone
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
import logging


logger = logging.getLogger(__name__)


class ListView(generic.ListView):
    template_name = 'users/list.html'
    context_object_name = 'users'

    def get_queryset(self):
        """
        Return the list of users.
        """
        return User.objects.all()


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно зарегистрирован')
            return redirect('login')
    else:
        form = RegisterForm()
    context = {'form': form, 'buttons_text': 'Зарегистрировать', 'title': 'Регистрация'}
    return render(request, 'users/register.html', context)


def update_user(request, pk):
    if request.user.id is None:
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('login')
    elif request.user.id != pk:
        messages.error(request, 'У вас нет прав для изменения другого пользователя.')
        return redirect('users:list')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = User.objects.get(pk=pk)
                user.username = form.cleaned_data['username']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.set_password(form.cleaned_data['password2'])
                user.save()
                logout(request)
                messages.info(request, 'Пользователь успешно изменён')
                return redirect('users:list')
        else:
            form = RegisterForm()
    context = {'form': form, 'buttons_text': 'Изменить', 'title': 'Изменение пользователя'}
    return render(request, 'users/register.html', context)


def delete_user(request, pk):
    if request.user.id is None:
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('login')
    elif request.user.id != pk:
        messages.error(request, 'У вас нет прав для изменения другого пользователя.')
        return redirect('users:list')
    else:
        if request.method == 'POST':
            user = User.objects.get(pk=pk)
            user.delete()
            logout(request)
            messages.success(request, 'Пользователь успешно удалён')
            return redirect('users:list')
        return render(request, 'users/delete.html')
