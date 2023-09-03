from collections import defaultdict
from django.http import JsonResponse
from django.db.models import Avg, Count
from django.core.serializers import serialize
from django.db.models.functions import TruncDate
from tracker.models import Point, Team, Jump, Transition
from django.template.defaultfilters import upper
import numpy as np
import json
import uuid


def heatmap(request, team_external_id, exclude_team=False):
    randoms = [p[0] for p in Point.randoms]
    all_transitions = dict([((_start, _end), dict((('duration_sum', 0), ('count', 0))))
                            for _start in randoms for _end in randoms])
    team = Team.objects.get(external_id=team_external_id)

    if exclude_team:
        jumps = Jump.objects.exclude(team=team)
        if request.GET.get('teams_category', None):
            jumps = jumps.filter(team__category=request.GET.get('teams_category'))
    else:
        jumps = Jump.objects.filter(team=team)
        if request.GET.get('tag_filter', None):
            jumps = jumps.filter(jump_tags__external_id=uuid.UUID(request.GET.get('tag_filter', None)))

    transitions = Transition.objects.filter(jump__in=jumps)
    data = []
    for row in transitions.values():
        if row.get('point_1_id') in randoms and row.get('point_2_id') in randoms:
            k = (str(row.get('point_1_id')), str(row.get('point_2_id')))
            v = all_transitions.get(k)
            all_transitions.update({k: {'duration_sum': v.get('duration_sum') + row.get('duration'),
                                        'count': v.get('count') + 1}})
    for k in all_transitions.keys():
        if all_transitions.get(k).get('count') > 0:
            duration = all_transitions.get(k).get('duration_sum') / all_transitions.get(k).get('count')
            data.append({'start': k[0],
                         'end': k[1],
                         'duration': round(duration, 2)})
    data = sorted(data, key=lambda d: (d['start'], d['end']), reverse=True)
    return JsonResponse(data, safe=False)


def block(request, team_external_id, exclude_team=False):
    blocks = [p[0] for p in Point.blocks]
    all_transitions = dict([((block, block), dict((('duration_sum', 0), ('count', 0)))) for block in blocks])
    team = Team.objects.get(external_id=team_external_id)

    if exclude_team:
        jumps = Jump.objects.exclude(team=team)
        if request.GET.get('teams_category', None):
            jumps = jumps.filter(team__category=request.GET.get('teams_category'))
    else:
        jumps = Jump.objects.filter(team=team)
        if request.GET.get('tag_filter', None):
            jumps = jumps.filter(jump_tags__external_id=uuid.UUID(request.GET.get('tag_filter', None)))

    transitions = Transition.objects.filter(jump__in=jumps)
    data = []
    for row in transitions.values():
        if row.get('point_1_id') in blocks and row.get('point_1_id') == row.get('point_2_id'):
            k = (str(row.get('point_1_id')), str(row.get('point_2_id')))
            v = all_transitions.get(k)
            all_transitions.update({k: {'duration_sum': v.get('duration_sum') + row.get('duration'),
                                        'count': v.get('count') + 1}})
    for k in all_transitions.keys():
        if all_transitions.get(k).get('count') > 0:
            duration = all_transitions.get(k).get('duration_sum') / all_transitions.get(k).get('count')
            data.append({'start': k[0],
                         'end': k[1],
                         'duration': round(duration, 2)})
    data = sorted(data, key=lambda d: int(d['start']))
    return JsonResponse(data, safe=False)


def heatmap_comparison(request, team_external_id):
    team_data = json.loads(heatmap(request, team_external_id).content)
    other_teams_data = json.loads(heatmap(request, team_external_id, exclude_team=True).content)
    data = []
    for t in team_data:
        for ot in other_teams_data:
            if t['start'] == ot['start'] and t['end'] == ot['end']:
                duration = round(float(t['duration']) - float(ot['duration']), 2)
                data.append({'start': t['start'],
                             'end': t['end'],
                             'duration': duration})
    return JsonResponse(data, safe=False)


def block_comparison(request, team_external_id):
    team_data = json.loads(block(request, team_external_id).content)
    other_teams_data = json.loads(block(request, team_external_id, exclude_team=True).content)
    data = []
    for t in team_data:
        for ot in other_teams_data:
            if t['start'] == ot['start'] and t['end'] == ot['end']:
                duration = round(float(t['duration']) - float(ot['duration']), 2)
                data.append({'start': t['start'],
                             'end': t['end'],
                             'duration': duration})
    return JsonResponse(data, safe=False)


def transition_get(request, team_external_id, point1, point2):
    team = Team.objects.get(external_id=team_external_id)
    jumps = Jump.objects.filter(team=team)
    tag_filter = request.GET.get('tag_filter', '')
    if tag_filter not in ['', None]:
        jumps = jumps.filter(jump_tags__external_id=uuid.UUID(tag_filter))
    transitions = Transition.objects.filter(jump__in=jumps, point_1_id=upper(point1), point_2_id=upper(point2))
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
    return JsonResponse(output_data, safe=False)


def transition(request, team_external_id):
    blocks = [p[0] for p in Point.blocks]
    data = {}
    for block in blocks:
        data[block] = json.loads(transition_get(request, team_external_id, block, block).content)
    return JsonResponse(data, safe=False)


def training_points(request, team_external_id):
    team = Team.objects.get(external_id=team_external_id)
    jumps = Jump.objects.filter(team=team)
    values = (jumps
              .values('date')
              .annotate(avg_points=Avg('points'))
              .annotate(total_jumps=Count('points')))
    formatted_json = {}
    for entry in values:
        values = {'avg_points': entry['avg_points'],
                  'total_jumps': entry['total_jumps']}
        formatted_json[entry['date'].strftime('%Y-%m-%d')] = values
    return JsonResponse({k: formatted_json[k] for k in sorted(formatted_json)})


def training_randoms_time(request, team_external_id):
    team = Team.objects.get(external_id=team_external_id)
    transitions = Transition.objects.filter(jump__team=team)
    for block_name in Point.objects.get_blocks():
        point = Point.objects.get(name=block_name)
        transitions = transitions.exclude(point_1=point, point_2=point)
    data = defaultdict(list)
    for t in transitions.values('jump__date', 'duration'):
        date = t['jump__date'].strftime('%Y-%m-%d')
        duration = float(t['duration'])
        data[date].append(duration)
    output_data = []
    for k, v in data.items():
        output_data.append({'date': k,
                            'mean': round(np.quantile(v, 0.5), 2),
                            'q1': round(np.quantile(v, 0.25), 2),
                            'q3': round(np.quantile(v, 0.75), 2)})
    output_data.sort(key=lambda x: x['date'])
    return JsonResponse(output_data, safe=False)
