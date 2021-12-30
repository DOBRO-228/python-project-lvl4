from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from statuses.models import Status
from tasks.models import Task


class TaskForm(ModelForm):
    name = forms.CharField(required=True, label='Имя', max_length=150)
    description = forms.CharField(label='Описание', required=False)
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label='Статус', required=True, widget=forms.Select())
    performer = forms.ModelChoiceField(
        queryset=User.objects.all(), label='Исполнитель', required=False, widget=forms.Select()
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'performer']
