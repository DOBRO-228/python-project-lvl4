from django.contrib.auth.mixins import UserPassesTestMixin
from tasks.models import Task


class AuthorIdentificationMixin(UserPassesTestMixin):
    """Custom UserPassesTestMixin."""

    def test_func(self):
        """Checking that the user is the author of Task."""
        task_author = Task.objects.get(pk=self.kwargs['pk']).author.id
        return self.request.user.id == task_author

    def dispatch(self, request, *args, **kwargs):
        """Add message and redirect url while restricted."""
        user_test_result = self.get_test_func()()
        if not user_test_result:
            self.redirect_url_while_restricted = 'tasks:list'
            self.restriction_message = 'Задачу может удалить только её автор'
        return super().dispatch(request, *args, **kwargs)
