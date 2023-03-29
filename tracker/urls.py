from django.urls import path

from . import views

urlpatterns = [
    path('track', views.track),
    path('teams', views.teams),
    path('team_register', views.team_register),
    path('athlete_register', views.athlete_register),
    path('athletes', views.athletes),
    path('', views.teams, name='index'),
    path('login', views.login_view, name='login'),
    path('track/select-team', views.track_select_team),
    path('team/heatmap_transition/<uuid:team_external_id>',
         views.heatmap_transitions_data,
         name='heatmap_transition'),
    path('team/block_transition/<uuid:team_external_id>',
         views.block_transitions_data,
         name='block_transition'),
    path('team/heatmap_transition_comparison/<uuid:team_external_id>',
         views.heatmap_transitions_comparison_data,
         name='heatmap_transition_comparison'),
    path('team/block_transition_comparison/<uuid:team_external_id>',
         views.block_transitions_comparison_data,
         name='block_transition_comparison'),
    path('foo/heatmap_transition_comparison',
         views.foo_heatmap_transitions_comparison_data,
         name='foo_heatmap_transition_comparison'),
    path('foo/block_transition_comparison',
         views.foo_block_transitions_comparison_data,
         name='foo_block_transition_comparison'),
    path('team/<uuid:team_external_id>', views.team_page),
    path('jumps/<uuid:team_external_id>', views.team_jumps, name='team_jumps'),
    path('fooflyers', views.foo_jumps, name='fooflyers_jumps'),
    path('jump/<uuid:jump_external_id>', views.team_jump)
]
