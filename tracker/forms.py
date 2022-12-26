from django import forms
from .models import Team


class TeamRegister(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'foundation']
