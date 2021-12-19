from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from statuses.models import Status


class StatusForm(ModelForm):
    name = forms.CharField(required=True, label='Имя', max_length=100)

    class Meta:
        model = Status
        fields = ['name']
