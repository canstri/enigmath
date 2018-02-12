from django import forms

from .models import Problem
from django.forms import CharField


class CheckProblemForm(forms.ModelForm):
    exp1 = forms.CharField(label='', widget=forms.Textarea, required=True)
    exp2 = forms.CharField(label='', widget=forms.Textarea, required=False)
    class Meta:
        model = Problem
        fields = [
            "exp1",
            "exp2", 
        ]