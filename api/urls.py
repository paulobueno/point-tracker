from django.urls import path
from . import views


urlpatterns = [
    path('v1/heatmap/plain/<uuid:team_external_id>', views.heatmap, name='heatmap'),
    path('v1/heatmap/comparison/<uuid:team_external_id>', views.heatmap_comparison, name='heatmap_comparison'),
    path('v1/block/plain/<uuid:team_external_id>', views.block, name='block'),
    path('v1/block/comparison/<uuid:team_external_id>', views.block_comparison, name='block_comparison'),
    path('v1/transition/data/<uuid:team_eid>/<point1>/<point2>', views.transition_get, name='transition_trend_data'),
    path('v1/transition/plain/<uuid:team_external_id>', views.transition, name='transition'),
    path('v1/training/points/<uuid:team_external_id>', views.training_points, name='training_points'),
]
