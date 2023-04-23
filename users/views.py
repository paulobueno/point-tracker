from django.contrib.auth.views import LoginView
from users.forms import EmailLoginForm


class EmailLoginView(LoginView):
    template_name = 'user_login.html'
    authentication_form = EmailLoginForm
