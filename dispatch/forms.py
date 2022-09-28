from django import forms
from django.forms import ModelForm

from dispatch.models import Grid, LoadReading


class CreateLoadReadingForm(ModelForm):
    date = forms.DateTimeField(disabled=True)

    class Meta:
        model = LoadReading
        fields = "__all__"


class GridForm(ModelForm):
    date = forms.DateTimeField(disabled=True)

    class Meta:
        model = Grid
        fields = "__all__"
