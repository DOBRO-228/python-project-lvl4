# from django.http import HttpResponseRedirect
# from django.shortcuts import get_object_or_404, render
# from django.urls import reverse
from django.views import generic
# from django.utils import timezone

from django.contrib.auth.models import User


class IndexView(generic.ListView):
    template_name = 'users/index.html'
    context_object_name = 'users'

    def get_queryset(self):
        """
        Return the list of users.
        """
        return User.objects.all()
