from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'task_manager/home.html'
