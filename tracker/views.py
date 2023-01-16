import uuid
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from tracker.forms import TeamRegister, AthleteRegister
from tracker.models import Team, Jump, Pool, Point, JumpAnalytic, TeamMember
from django.contrib.auth import authenticate, login


def index(request):
    context = {"teams": Team.objects.all(),
               "points": Pool.point_1.field.choices}
    return render(request, 'index.html', context)


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


def track(request):
    context = {"teams": Team.objects.all(),
               "points": Point.objects.all(),
               "positions": sorted([position[1] for position in TeamMember.position.field.choices]),
               "athletes": TeamMember.objects.all()}
    if request.method == "POST":
        team = request.POST.get('team-select')
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
        jump = Jump(team=Team.objects.get(external_id=uuid.UUID(team)),
                    date=jump_date,
                    video=url,
                    pool=pool,
                    points=total_points,
                    busts=total_busts)
        jump.save()

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
                    time=jump_point[2] * 1,
                    diff=jump_point[3] * 1,
                    status=jump_point[4]).save()

    return render(request, 'track.html', context)


def team_page(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    jumps = Jump.objects.filter(team__pk=team_id)
    return render(request, 'team.html', {'team': team,
                                         'jumps': jumps})


def teams(request):
    teams_insts = Team.objects.all()
    return render(request, 'teams.html', {'teams': teams_insts})


def athletes(request):
    athletes_insts = TeamMember.objects.all()
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


def team_jumps(request, jump_id):
    return None


def team_jump(request, team_id, jump_id):
    return HttpResponse(team_id + jump_id)
