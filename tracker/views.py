from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from tracker.forms import TeamRegister, JumpRegister
from tracker.models import Team, Jump, Pool, Point


def index(request):
    context = {"teams": Team.objects.all(),
               "points": Pool.point_1.field.choices}
    return render(request, 'index.html', context)


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


def jump_register(request):
    form_msg = ""
    if request.method == 'POST':
        form = JumpRegister(request.POST)
        if form.is_valid():
            form.save()
            form_msg = "Team Saved"
    else:
        form = JumpRegister()
    context = {"form": form,
               "form_msg": form_msg}
    return render(request, 'jump_register.html', context)


def track(request):
    context = {"teams": Team.objects.all(),
               "points": Point.objects.all()}
    if request.method == "POST":
        print("Entered in POST request")
        print(request.POST)
        team = request.POST.get('team-select')[0]*1
        jump_date = request.POST.get('jump-date')
        url = request.POST.get('url-input')[0]
        total_points = request.POST.get('total-points')[0] * 1
        total_busts = request.POST.get('total-busts')[0] * 1

        def get_point(number):
            point = request.POST.get('pool-point' + str(number))[0]
            try:
                point_id = Point.objects.get(pk=point)
            except ObjectDoesNotExist:
                point_id = None
            return point_id

        print([get_point(ponto) for ponto in range(1, 6)])
        pool = Pool(point_1=get_point(1),
                    point_2=get_point(2),
                    point_3=get_point(3),
                    point_4=get_point(4),
                    point_5=get_point(5))
        pool.save()
        print("JUMP DATE ---->", jump_date)
        jump = Jump(team=Team.objects.get(pk=team),
                    date=jump_date,
                    video=url,
                    pool=pool,
                    points=total_points,
                    busts=total_busts)
        jump.save()

    return render(request, 'track.html', context)


def team_page(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    jumps = Jump.objects.filter(team__pk=team_id)
    return render(request, 'team.html', {'team': team,
                                         'jumps': jumps})


def teams(request):
    teams = Team.objects.all()
    return HttpResponse(teams)


def team_jumps(request, jump_id):
    return None


def team_jump(request, team_id, jump_id):
    return HttpResponse(team_id + jump_id)
