from django.urls import path
from . import views

urlpatterns = [
    path('login', views.EmailLoginView.as_view(), name='login')
]
