from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import ScopedRateThrottle

from .models import Competition, Drone, DroneCategory, Pilot
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CompetitionSerializer,
    DroneCategorySerializer,
    DroneSerializer,
    PilotCompetitionSerializer,
    PilotSerializer,
)


class DroneCategoryView(generics.ListCreateAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    filterset_fields = ("name",)
    search_fields = ("^name",)
    ordering_fields = ("name",)
    name = "drone-category"


class DroneCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = "dronecategory-detail"


class DroneView(generics.ListCreateAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    throttle_classes = (ScopedRateThrottle,)
    filterset_fields = ("name", "drone_category")
    ordering_fields = ("name", "drone_category", "timestamp", "manufacturing_date")
    name = "drone"
    permission_classes = [
        IsAuthorOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class DroneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    throttle_classes = (ScopedRateThrottle,)
    permission_classes = [
        IsAuthorOrReadOnly,
    ]
    name = "drone-detail"


class PilotView(generics.ListCreateAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    throttle_classes = (ScopedRateThrottle,)
    filterset_fields = ("name", "races_amount", "pilot_joined")
    ordering_fields = ("name", "races_amount", "pilot_joined")

    name = "pilot"


class PilotDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    throttle_classes = (ScopedRateThrottle,)
    name = "pilot-detail"


class CompetitionView(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    order = ("distance_in_meters", "pilot", "drone")
    filterset_fields = order
    ordering_fields = order
    name = "competition"


class CompetitionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = "competition-detail"


class ApiRoot(generics.GenericAPIView):
    name = "api-root"

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "drone-categories": reverse(DroneCategoryView.name, request=request),
                "drones": reverse(DroneView.name, request=request),
                "pilots": reverse(PilotView.name, request=request),
                "competitions": reverse(CompetitionView.name, request=request),
            }
        )


class ObtainAuthTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token,
                "user_id": user.pk,
                "email": user.email,
            }
        )
