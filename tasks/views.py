from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django_filters.views import FilterView
from mixins import CustomLoginRequiredMixin, DeleteViewWithRestrictions
from tasks.filters import TaskFilter
from tasks.mixins import AuthorIdentificationMixin
from tasks.models import Task
from users.models import User


class TasksListView(CustomLoginRequiredMixin, FilterView):
    """List view of Tasks."""

    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class DetailTaskView(CustomLoginRequiredMixin, DetailView):
    """Detail task view."""

    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'


class CreateTaskView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Create task view."""

    model = Task
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:list')
    success_message = _('Task created successfully')
    fields = ['name', 'description', 'status', 'executor', 'labels']

    def form_valid(self, form):
        """Task's author is filled by User from request.

        Args:
            form: Task' form.

        Returns:
            Inherited method.

        """
        form.instance.author = User.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)


class UpdateTaskView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update task view."""

    model = Task
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:list')
    success_message = _('Task changed successfully')
    fields = ['name', 'description', 'status', 'executor', 'labels']


class DeleteTaskView(
    CustomLoginRequiredMixin, AuthorIdentificationMixin, DeleteViewWithRestrictions,
):
    """Delete task view."""

    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:list')
    success_message = _('Task deleted successfully')

    def check_permissions_to_delete(self, request, **kwargs):
        """There aren't restrictions to delete.

        Args:
            request: HTTP request.
            **kwargs: kwargs.

        Returns:
            False.
        """
        return False
