from django.urls import path, include

from . import views

urlpatterns = [
    path('track', views.track),
    path('teams', views.teams, name='teams'),
    path('team_register', views.team_register),
    path('athlete_register', views.athlete_register),
    path('athletes', views.athletes),
    path('about', views.about),
    path('sign-up', views.sign_up),
    path('', views.index, name='index'),
    path('track/select-team', views.track_select_team),
    path('team/<uuid:team_external_id>', views.team_page),
    path('jumps/<uuid:team_external_id>', views.team_jumps, name='team_jumps'),
    path('jump/<uuid:jump_external_id>', views.team_jump),
    path('rf-api/', include('rf-api.urls'))
]
