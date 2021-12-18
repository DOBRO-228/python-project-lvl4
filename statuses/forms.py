from django import forms
from django.forms import ModelForm
from statuses.models import Status
from django.utils.translation import gettext_lazy as _


class StatusForm(ModelForm):
    name = forms.CharField(required=True, label='Имя')

    class Meta:
        model = Status
        fields = ['name']
