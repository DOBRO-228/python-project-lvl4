from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from labels.models import Label


class LabelForm(ModelForm):
    name = forms.CharField(required=True, label='Имя', max_length=100)

    class Meta:
        model = Label
        fields = ['name']
