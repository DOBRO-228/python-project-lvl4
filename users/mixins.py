from django.contrib.auth.mixins import UserPassesTestMixin


class UserIdentificationMixin(UserPassesTestMixin):
    """Custom UserPassesTestMixin."""

    def test_func(self):
        """Checking that the user is trying to manipulate self User object."""
        return self.request.user.id == self.kwargs['pk']

    def dispatch(self, request, *args, **kwargs):
        """Add message and redirect url while restricted."""
        user_test_result = self.get_test_func()()
        if not user_test_result:
            self.redirect_url_while_restricted = 'users:list'
            self.restriction_message = 'У вас нет прав для изменения другого пользователя.'
        return super().dispatch(request, *args, **kwargs)
