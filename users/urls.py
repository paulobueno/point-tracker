from django.urls import path
from . import views

urlpatterns = [
    path('login', views.EmailLoginView.as_view(), name='login'),
    # path('user_registration', views.user_registration, name='user_registration'),
]
