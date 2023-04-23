from django.db import models
from django.contrib.auth.models import AbstractUser

from tracker.models import Team


class User(AbstractUser):
    associated_team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    team_name = models.CharField(max_length=100, default="No Name")
    payment_status = models.BooleanField(default=False)
