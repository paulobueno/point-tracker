from django.urls import path

from . import views

urlpatterns = [
    path('track', views.track),
    path('teams', views.teams),
    path('team_register', views.team_register),
    path('team/<int:team_id>', views.team_page),
    path('team/<int:team_id>/jumps', views.team_jumps),
    path('team/<int:team_id>/jump/<int:jump_id>', views.team_jump)
]
