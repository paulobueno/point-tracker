from django import forms
from .models import Team, TeamMember
from django_countries.widgets import CountrySelectWidget


class TeamRegister(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'category', 'foundation', 'instagram', 'website', 'country']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control"
            }),
            'category': forms.Select(attrs={
                'class': "form-select"
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
            }),
            'country': CountrySelectWidget(attrs={
                'class': "form-select"
            })
        }


class AthleteRegister(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'nickname', 'position', 'team', 'country']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control"
            }),
            'nickname': forms.TextInput(attrs={
                'class': "form-control"
            }),
            'position': forms.Select(attrs={
                'class': "form-select"
            }),
            'team': forms.Select(attrs={
                'class': "form-select"
            }),
            'country': CountrySelectWidget(attrs={
                'class': "form-select"
            })
        }
