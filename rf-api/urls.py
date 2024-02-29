from django.urls import path
from . import views

urlpatterns = [
    path('get-teams', views.get_teams),
    path('get-points', views.get_points),
    path('get-transitions/<uuid:team_eid>', views.get_transitions)
]
