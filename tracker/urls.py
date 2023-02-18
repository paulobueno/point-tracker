from django.urls import path

from . import views

urlpatterns = [
    path('track', views.track),
    path('teams', views.teams),
    path('team_register', views.team_register),
    path('athlete_register', views.athlete_register),
    path('athletes', views.athletes),
    path('', views.login_view, name='index'),
    path('login', views.login_view, name='login'),
    path('team/heatmap_transition/<uuid:team_external_id>',
         views.heatmap_transitions_data,
         name='heatmap_transition'),
    path('team/heatmap_transition_comparison/<uuid:team_external_id>',
         views.heatmap_transitions_comparison_data,
         name='heatmap_transition_comparison'),
    path('team/<uuid:team_external_id>', views.team_page),
    path('jumps/<uuid:team_external_id>', views.team_jumps, name='team_jumps'),
    path('jump/<uuid:jump_external_id>', views.team_jump)
]
