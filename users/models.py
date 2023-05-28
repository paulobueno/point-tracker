import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from tracker.models import TeamMember


class User(AbstractUser):
    country = CountryField(null=True, blank=True)
    nickname = models.CharField(max_length=100, null=True)
    associated_team_members = models.ManyToManyField(TeamMember)
    # external_id = models.UUIDField(default=uuid.uuid4, unique=True)
