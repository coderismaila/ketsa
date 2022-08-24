from django import forms
from django.forms import ModelForm

from dispatch.models import LoadReading


class CreateLoadReadingForm(ModelForm):
    class Meta:
        model = LoadReading
        fields = "__all__"
