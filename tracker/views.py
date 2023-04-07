import operator
import uuid
from collections import defaultdict
import json
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.template.defaultfilters import upper
import numpy as np

from tracker.forms import TeamRegister, AthleteRegister
from tracker.models import Team, Jump, Pool, Point, JumpAnalytic, TeamMember, Transition, Jump_Tags
from django.contrib.auth import authenticate, login


def index(request):
    context = {"teams": Team.objects.all(),
               "points": Pool.point_1.field.choices}
    return render(request, 'index.html', context)


@login_required
def athlete_register(request):
    form_msg = ""
    if request.method == 'POST':
        form = AthleteRegister(request.POST)
        if form.is_valid():
            form.save()
            form_msg = "Athlete Saved"
    else:
        form = AthleteRegister()
    context = {"form": form,
               "form_msg": form_msg}
    return render(request, 'athlete_register.html', context)


@login_required
def team_register(request):
    form_msg = ""
    if request.method == 'POST':
        form = TeamRegister(request.POST)
        if form.is_valid():
            form.save()
            form_msg = "Team Saved"
    else:
        form = TeamRegister()
    context = {"form": form,
               "form_msg": form_msg}
    return render(request, 'team_register.html', context)


@login_required
def track(request):
    selected_team_uuid = request.GET.get('selected_team_uuid')
    try:
        selected_team_uuid = uuid.UUID(str(selected_team_uuid))
    except ValueError:
        selected_team_uuid = None
    context = {"teams": Team.objects.all(),
               "points": Point.objects.all(),
               "tags": Jump_Tags.objects.all(),
               "positions": sorted([position[1] for position in TeamMember.position.field.choices]),
               "athletes": [],
               "selected_team_uuid": selected_team_uuid}
    if selected_team_uuid:
        context.update({"athletes": TeamMember.objects.filter(team__external_id=selected_team_uuid)})
    if request.method == "POST":
        tag = request.POST.get('tag-select')
        jump_date = request.POST.get('jump-date')
        url = request.POST.get('url-input')
        total_points = request.POST.get('total-points')
        total_busts = request.POST.get('total-busts')

        def get_point(number):
            point = request.POST.get('pool-point' + str(number))
            if point != "-":
                point_id = Point.objects.get(external_id=uuid.UUID(point))
            else:
                point_id = None
            return point_id

        pool = Pool(point_1=get_point(1),
                    point_2=get_point(2),
                    point_3=get_point(3),
                    point_4=get_point(4),
                    point_5=get_point(5))
        pool.save()
        jump = Jump(team=Team.objects.get(external_id=selected_team_uuid),
                    date=jump_date,
                    video=url,
                    pool=pool,
                    points=total_points,
                    busts=total_busts)
        jump.save()
        if tag != "-":
            jump.jump_tags.add(Jump_Tags.objects.get(external_id=uuid.UUID(tag)))

        def change_to_bool(value):
            if value == "✔":
                return True
            else:
                return False

        jump_points_analytics = list(zip(request.POST.getlist('point-number'),
                                         request.POST.getlist('point-figure'),
                                         request.POST.getlist('current-time'),
                                         request.POST.getlist('time-diff'),
                                         [change_to_bool(status) for status in request.POST.getlist('point-status')]))
        with transaction.atomic():
            for jump_point in jump_points_analytics:
                JumpAnalytic(
                    jump=jump,
                    point_number=jump_point[0],
                    point=Point.objects.get(external_id=uuid.UUID(jump_point[1])),
                    time=float(jump_point[2]),
                    diff=float(jump_point[3]),
                    status=jump_point[4]).save()

        with transaction.atomic():
            for i, point_2 in enumerate(jump_points_analytics[1:]):
                point_1 = jump_points_analytics[i]
                Transition(
                    jump=jump,
                    point_1=Point.objects.get(external_id=uuid.UUID(point_1[1])),
                    point_2=Point.objects.get(external_id=uuid.UUID(point_2[1])),
                    duration=float(point_2[3])
                ).save()

    return render(request, 'track.html', context)


def team_page(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    jumps = Jump.objects.filter(team__pk=team_id).order_by('date')
    context = {'team': team,
               'jumps': jumps}
    return render(request, 'team.html', context)


def teams(request):
    teams_insts = Team.objects.all().order_by('name')
    return render(request, 'teams.html', {'teams': teams_insts})


def athletes(request):
    athletes_insts = TeamMember.objects.all().order_by('team', 'name')
    return render(request, 'athletes.html', {'athletes': athletes_insts})


def login_view(request):
    if request.method == "POST":
        email = request.POST['email-input']
        password = request.POST['password-input']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(teams)
    return render(request, 'login.html')


def heatmap_transitions_data(request, team_external_id, exclude_team=False):
    tag_filter = request.GET.get('tag_filter')
    randoms = [p[0] for p in Point.randoms]
    all_transitions = dict([((_start, _end), dict((('duration_sum', 0), ('count', 0))))
                            for _start in randoms for _end in randoms])
    team = Team.objects.get(external_id=team_external_id)
    jumps = Jump.objects.filter(team=team)
    if exclude_team:
        jumps = Jump.objects.exclude(team=team)
    if (tag_filter not in ['', None, 'None']) and (not exclude_team):
        jumps = jumps.filter(jump_tags__external_id=uuid.UUID(tag_filter))
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


def block_transitions_data(request, team_external_id, exclude_team=False):
    tag_filter = request.GET.get('tag_filter')
    blocks = [p[0] for p in Point.blocks]
    all_transitions = dict([((block, block), dict((('duration_sum', 0), ('count', 0)))) for block in blocks])
    team = Team.objects.get(external_id=team_external_id)
    jumps = Jump.objects.filter(team=team)
    if exclude_team:
        jumps = Jump.objects.exclude(team=team)
    if (tag_filter not in ['', None, 'None']) and (not exclude_team):
        jumps = jumps.filter(jump_tags__external_id=uuid.UUID(tag_filter))
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


@login_required
def heatmap_transitions_comparison_data(request, team_external_id):
    team_data = json.loads(heatmap_transitions_data(request, team_external_id).content)
    other_teams_data = json.loads(heatmap_transitions_data(request, team_external_id, exclude_team=True).content)
    data = []
    for t in team_data:
        for ot in other_teams_data:
            if t['start'] == ot['start'] and t['end'] == ot['end']:
                duration = round(float(t['duration']) - float(ot['duration']), 2)
                data.append({'start': t['start'],
                             'end': t['end'],
                             'duration': duration})
    return JsonResponse(data, safe=False)


@login_required
def block_transitions_comparison_data(request, team_external_id):
    team_data = json.loads(block_transitions_data(request, team_external_id).content)
    other_teams_data = json.loads(block_transitions_data(request, team_external_id, exclude_team=True).content)
    data = []
    for t in team_data:
        for ot in other_teams_data:
            if t['start'] == ot['start'] and t['end'] == ot['end']:
                duration = round(float(t['duration']) - float(ot['duration']), 2)
                data.append({'start': t['start'],
                             'end': t['end'],
                             'duration': duration})
    return JsonResponse(data, safe=False)


def team_jumps(request, team_external_id, fooflyers=False):
    team = Team.objects.get(external_id=team_external_id)
    jumps = Jump.objects.filter(team=team)
    members = TeamMember.objects.filter(team__pk=team.id)
    available_tags = Jump_Tags.objects.filter(jump__in=jumps).distinct()
    blocks = [p[0] for p in Point.blocks]
    tag_filter = request.GET.get('tag_filter', '')
    block_filter = request.GET.get('block_filter', '1')
    if request.method == "POST":
        block_filter = request.POST.get('block_filter', block_filter)
        tag_filter = request.POST.get('tag_filter', tag_filter)
        if fooflyers:
            url = reverse('fooflyers_jumps')
        else:
            url = reverse('team_jumps', kwargs={'team_external_id': team_external_id})
        url = f'{url}?block_filter={block_filter}&tag_filter={tag_filter}'
        return HttpResponseRedirect(url)
    if tag_filter not in ['', None]:
        jumps = jumps.filter(jump_tags__external_id=uuid.UUID(tag_filter))
    transitions = Transition.objects.filter(jump__in=jumps)
    return render(request, 'team.html', {'team': team,
                                         'blocks': blocks,
                                         'members': members,
                                         'jumps': jumps,
                                         'transitions': transitions,
                                         'available_tags': available_tags,
                                         'tag_filter': tag_filter,
                                         'block_filter': block_filter,
                                         'fooflyers': fooflyers})


def foo_jumps(request):
    team_uuid = uuid.UUID("497c2597-4dbb-4cb7-b92d-27cd641f6c9c")
    return team_jumps(request, team_uuid, fooflyers=True)


def team_jump(request, team_id, jump_id):
    return HttpResponse(team_id + jump_id)


def track_select_team(request):
    selected_team_uuid = None
    if request.method == 'POST':
        selected_team_uuid = request.POST.get('team-select')
    return redirect('/track?selected_team_uuid=' + selected_team_uuid)


@login_required
def transition_trend_data(_, team_eid, point1, point2):
    team = Team.objects.get(external_id=team_eid)
    jumps = Jump.objects.filter(team=team)
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
    return JsonResponse(output_data, safe=False)


def foo_transition_trend_data(_, point1, point2):
    team = Team.objects.get(external_id=uuid.UUID('497c2597-4dbb-4cb7-b92d-27cd641f6c9c'))
    jumps = Jump.objects.filter(team=team)
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


def foo_transition_trend_data_all(_):
    blocks = [p[0] for p in Point.blocks]
    data = {}
    for block in blocks:
        data[block] = json.loads(foo_transition_trend_data(None, block, block).content)
    return JsonResponse(data, safe=False)


def foo_heatmap_transitions_comparison_data(request):
    team_data = json.loads(heatmap_transitions_data(request,
                                                    uuid.UUID('497c2597-4dbb-4cb7-b92d-27cd641f6c9c')).content)
    other_teams_data = json.loads(heatmap_transitions_data(request,
                                                           uuid.UUID('497c2597-4dbb-4cb7-b92d-27cd641f6c9c'),
                                                           exclude_team=True).content)
    data = []
    for t in team_data:
        for ot in other_teams_data:
            if t['start'] == ot['start'] and t['end'] == ot['end']:
                duration = round(float(t['duration']) - float(ot['duration']), 2)
                data.append({'start': t['start'],
                             'end': t['end'],
                             'duration': duration})
    return JsonResponse(data, safe=False)


def foo_block_transitions_comparison_data(request):
    team_data = json.loads(block_transitions_data(request,
                                                  uuid.UUID('497c2597-4dbb-4cb7-b92d-27cd641f6c9c')).content)
    other_teams_data = json.loads(block_transitions_data(request,
                                                         uuid.UUID('497c2597-4dbb-4cb7-b92d-27cd641f6c9c'),
                                                         exclude_team=True).content)
    data = []
    for t in team_data:
        for ot in other_teams_data:
            if t['start'] == ot['start'] and t['end'] == ot['end']:
                duration = round(float(t['duration']) - float(ot['duration']), 2)
                data.append({'start': t['start'],
                             'end': t['end'],
                             'duration': duration})
    return JsonResponse(data, safe=False)
