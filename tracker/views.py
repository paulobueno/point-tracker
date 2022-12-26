from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from tracker.forms import TeamRegister
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


def track(request):
    context = {"teams": Team.objects.all(),
               "points": Point.objects.all()}
    if request.method == "POST":
        print("Entered in POST request")
        print(request.POST)
        pool = Pool(point_1=Point.objects.get(pk=request.POST.get('pool-point1')[0]),
                    point_2=Point.objects.get(pk=request.POST.get('pool-point2')[0]),
                    point_3=Point.objects.get(pk=request.POST.get('pool-point3')[0]),
                    point_4=Point.objects.get(pk=request.POST.get('pool-point4')[0]),
                    point_5=Point.objects.get(pk=request.POST.get('pool-point5')[0]))
        pool.save()
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
