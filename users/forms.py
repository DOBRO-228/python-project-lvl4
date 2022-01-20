from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from users.models import User


class UserRegistrationForm(UserCreationForm):
    """User registration form."""

    first_name = forms.CharField(required=True, label=_('First name'))
    last_name = forms.CharField(required=True, label=_('Last name'))

    class Meta(object):  # Noqa: D106
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
