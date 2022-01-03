from django_filters import FilterSet, BooleanFilter, ModelChoiceFilter
from statuses.models import Status
from labels.models import Label
from tasks.models import Task
from django.contrib.auth.models import User
from django import forms


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(label='Статус', queryset=Status.objects.all())
    performer = ModelChoiceFilter(label='Исполнитель', queryset=User.objects.all())
    label = ModelChoiceFilter(label='Метка', queryset=Label.objects.all())
    self_tasks = BooleanFilter(label='Только свои задачи', method='self_tasks_filter', widget=forms.CheckboxInput)

    class Meta:
        model = Task
        fields = ['status', 'performer', 'label', 'self_tasks']

    def self_tasks_filter(self, queryset, name, value):
        if value:
            return queryset & self.request.user.created_tasks.all()
        return queryset & Task.objects.all()
