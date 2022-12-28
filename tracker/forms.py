from django import forms
from .models import Team, Jump


class TeamRegister(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'foundation', 'instagram', 'website']


class JumpRegister(forms.ModelForm):
    class Meta:
        model = Jump
        fields = ['team', 'pool', 'video', 'date', 'points', 'busts']
