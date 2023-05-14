from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _

from users.models import User


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


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)
