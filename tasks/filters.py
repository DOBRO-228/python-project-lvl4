from django import forms
from django.utils.translation import gettext_lazy as _
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter
from labels.models import Label
from tasks.models import Task


class TaskFilter(FilterSet):
    """FilterSet for tasks."""

    labels = ModelChoiceFilter(label=_('Label'), queryset=Label.objects.all())
    self_tasks = BooleanFilter(label=_('Self tasks'), method='self_tasks_filter', widget=forms.CheckboxInput)

    class Meta(object):  # Noqa: D106
        model = Task
        fields = ['status', 'performer', 'labels', 'self_tasks']

    def self_tasks_filter(self, queryset, name, value):  # Noqa: WPS110
        """If filter is selected return queryset of tasks which are created by user.

        Args:
            queryset: Queryset which was created by other filters before.
            name(str): Filter's name.
            value(bool): Filter's value.

        Returns:
            Queryset.
        """
        if value:
            return queryset & self.request.user.created_tasks.all()
        return queryset
