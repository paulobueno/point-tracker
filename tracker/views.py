from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from tracker.models import Team, Jump


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


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
