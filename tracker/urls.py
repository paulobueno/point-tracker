from django.urls import path

from . import views

urlpatterns = [
    path('track', views.track),
    path('teams', views.teams),
    path('team_register', views.team_register),
    path('jump_register', views.jump_register),
    path('team/<int:team_external_id>', views.team_page),
    path('team/<int:team_external_id>/jumps', views.team_jumps),
    path('team/<int:team_external_id>/jump/<int:jump_external_id>', views.team_jump)
]
