from django import forms
from .models import Team


class TeamRegister(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'foundation', 'instagram', 'website']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control"
            }),
            'website': forms.TextInput(attrs={
                'class': "form-control"
            }),
            'foundation': forms.DateInput(attrs={
                'class': "form-control",
                'type': 'date'
            }),
            'instagram': forms.DateInput(attrs={
                'class': "form-control",
                'placeholder': 'username'
            })
        }
