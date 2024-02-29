from rest_framework import serializers
from tracker.models import Team, Jump, Transition, Point


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = '__all__'
