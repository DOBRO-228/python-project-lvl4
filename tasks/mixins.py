from django.contrib.auth.mixins import UserPassesTestMixin
from tasks.models import Task


class AuthorIdentificationMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.id == Task.objects.get(pk=self.kwargs['pk']).author.id

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            self.redirect_url_while_restricted = 'tasks:list'
            self.restriction_message = 'Задачу может удалить только её автор'
        return super().dispatch(request, *args, **kwargs)
