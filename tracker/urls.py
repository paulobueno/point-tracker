from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('teams', views.teams, name='teams'),
    path('team/<int:team_id>', views.team_page, name='team'),
    path('team/<int:team_id>/jumps', views.team_jumps, name='team'),
    path('team/<int:team_id>/jump/<int:jump_id>', views.team_jump, name='team')
]
