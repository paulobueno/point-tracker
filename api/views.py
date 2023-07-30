from collections import defaultdict
from django.http import JsonResponse
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
