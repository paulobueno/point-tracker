from django.urls import path

from . import views

urlpatterns = [
    path('track', views.track),
    path('teams', views.teams),
    path('team_register', views.team_register),
    path('team/<int:team_external_id>', views.team_page),
    path('jumps/<int:team_external_id>', views.team_jumps),
    path('jump/<int:jump_external_id>', views.team_jump)
]
