import uuid
from collections import defaultdict
from django.template.defaultfilters import upper
import numpy as np
from rest_framework.response import Response
from rest_framework.decorators import api_view
from tracker.models import Team, Jump, Transition, Point
from .serializers import TeamSerializer, PointSerializer


@api_view(['GET'])
def get_teams(request):
    teams = Team.objects.all()
    serialized = TeamSerializer(teams, many=True)
    return Response(serialized.data)


@api_view(['GET'])
def get_points(request):
    points = Point.objects.all()
    serialized = PointSerializer(points, many=True)
    return Response(serialized.data)


def get_transition(team_eid, point_1, point_2, filter_tag):
    team = Team.objects.get(external_id=team_eid)
    jumps = Jump.objects.filter(team=team)
    if filter_tag not in ['', None]:
        jumps = jumps.filter(jump_tags__external_id=uuid.UUID(filter_tag))
    transitions = Transition.objects.filter(jump__in=jumps, point_1_id=upper(point_1), point_2_id=upper(point_2))
    data = defaultdict(list)
    output_data = []
    for transition in transitions:
        date = str(transition.jump.date)
        duration = float(transition.duration)
        data[date].append(duration)
    for k, v in data.items():
        output_data.append({'date': k,
                            'mean': round(np.quantile(v, 0.5), 2),
                            'q1': round(np.quantile(v, 0.25), 2),
                            'q3': round(np.quantile(v, 0.75), 2)})
    output_data.sort(key=lambda x: x['date'])
    return output_data


@api_view(['GET'])
def get_transitions(request, team_eid, filter_tag=None):
    blocks = [p[0] for p in Point.blocks]
    print(blocks)
    data = {}
    for block in blocks:
        data[block] = get_transition(team_eid, block, block, filter_tag)
    return Response(data)
