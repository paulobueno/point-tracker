from django.urls import path

from . import views

urlpatterns = [
    path('track', views.track),
    path('teams', views.teams, name='teams'),
    path('team_register', views.team_register),
    path('athlete_register', views.athlete_register),
    path('athletes', views.athletes),
    path('', views.teams, name='index'),
    path('about', views.about),
    path('track/select-team', views.track_select_team),
    path('team/<uuid:team_external_id>', views.team_page),
    path('jumps/<uuid:team_external_id>', views.team_jumps, name='team_jumps'),
    path('jump/<uuid:jump_external_id>', views.team_jump)
]
