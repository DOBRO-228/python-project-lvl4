from django import forms
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter
from labels.models import Label
from tasks.models import Task


class TaskFilter(FilterSet):
    labels = ModelChoiceFilter(label='Метка', queryset=Label.objects.all())
    self_tasks = BooleanFilter(label='Только свои задачи', method='self_tasks_filter', widget=forms.CheckboxInput)

    class Meta:
        model = Task
        fields = ['status', 'performer', 'labels', 'self_tasks']

    def self_tasks_filter(self, queryset, name, value):
        if value:
            return queryset & self.request.user.created_tasks.all()
        return queryset
