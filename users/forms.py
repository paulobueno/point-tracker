from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.utils.translation import gettext_lazy as _


class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="E-mail",
        widget=forms.TextInput(
            attrs={'autofocus': True,
                   'class': "form-control"}
        ))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password",
                                          'class': "form-control"}),
    )
