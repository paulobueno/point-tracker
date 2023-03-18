from django.contrib import admin
from .models import Team, TeamMember, Jump, Pool, Transition, Point, JumpAnalytic, Jump_Tags

admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(Jump)
admin.site.register(Pool)
admin.site.register(Transition)
admin.site.register(Point)
admin.site.register(JumpAnalytic)
admin.site.register(Jump_Tags)
