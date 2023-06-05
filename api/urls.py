from django.urls import path
from . import views


urlpatterns = [
    path('heatmap/plain/<uuid:team_external_id>', views.heatmap, name='heatmap'),
    path('heatmap/comparison/<uuid:team_external_id>', views.heatmap_comparison, name='heatmap_comparison'),
    path('block/plain/<uuid:team_external_id>', views.block, name='block'),
    path('block/comparison/<uuid:team_external_id>', views.block_comparison, name='block_comparison'),
    path('transition/data/<uuid:team_eid>/<point1>/<point2>', views.transition_get, name='transition_trend_data'),
    path('transition/plain/<uuid:team_external_id>', views.transition, name='transition'),
]
