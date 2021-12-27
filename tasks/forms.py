from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from statuses.models import Status


class TaskForm(ModelForm):
    name = forms.CharField(required=True, label='Имя', max_length=150)
    description = forms.CharField(label='Описание')
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=True, label='Статус', widget=forms.Select())
    performer = forms.ModelChoiceField(queryset=User.objects.all(), label='Исполнитель', widget=forms.Select())

    class Meta:
        model = Status
        fields = ['name', 'description', 'status', 'performer']
