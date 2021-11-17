from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'task_manager/home.html'


class LoginView(TemplateView):
    template_name = 'registration/login.html'
