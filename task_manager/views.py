from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import logging


logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = 'task_manager/home.html'


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Вы успешно вошли')
            logger.debug(request.user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.info(request, 'Вы разлогинены')
    return redirect('home')
