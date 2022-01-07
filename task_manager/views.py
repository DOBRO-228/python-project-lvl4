from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Home page view."""

    template_name = 'task_manager/home.html'
