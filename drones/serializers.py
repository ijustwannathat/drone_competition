from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Competition, Drone, DroneCategory, Pilot


class UserDroneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Drone
        fields = ["url", "name"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    drones = UserDroneSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["url", "pk", "drones", "username"]


class DroneCategorySerializer(serializers.HyperlinkedModelSerializer):
    drones = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="drone-detail"
    )

    class Meta:
        model = DroneCategory
        fields = ["url", "pk", "name", "drones"]


class DroneSerializer(serializers.HyperlinkedModelSerializer):
    drone_category = serializers.SlugRelatedField(
        queryset=DroneCategory.objects.all(), slug_field="name"
    )
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Drone
        fields = [
            "url",
            "name",
            "author",
            "drone_category",
            "is_participant",
            "timestamp",
            "manufacturing_date",
        ]


class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
    drone = DroneSerializer()

    class Meta:
        model = Competition
        fields = ["url", "pk", "distance_in_meters", "achieved_distance_date", "drone"]


class PilotSerializer(serializers.HyperlinkedModelSerializer):
    competitions = CompetitionSerializer(many=True, read_only=True)
    gender = serializers.ChoiceField(choices=Pilot.genders)
    gender_description = serializers.CharField(
        source="get_gender_desciption", read_only=True
    )

    class Meta:
        model = Pilot
        fields = [
            "url",
            "name",
            "gender",
            "gender_description",
            "races_amount",
            "pilot_joined",
            "competitions",
        ]


class PilotCompetitionSerializer(serializers.ModelSerializer):
    pilot = serializers.SlugRelatedField(
        queryset=Pilot.objects.all(), slug_field="name"
    )
    drone = serializers.SlugRelatedField(
        queryset=Drone.objects.all(), slug_field="name"
    )

    class Meta:
        model = Competition
        fields = [
            "url",
            "pk",
            "distance_in_meters",
            "achieved_distance_date",
            "pilot",
            "drone",
        ]
