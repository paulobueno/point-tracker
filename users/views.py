from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from users.forms import EmailLoginForm, UserRegistrationForm


class EmailLoginView(LoginView):
    template_name = 'user_login.html'
    authentication_form = EmailLoginForm


def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='users.backends.EmailBackend')
            return redirect('teams')
    else:
        form = UserRegistrationForm()
    return render(request, 'user_registration.html', {'form': form})

