from django.urls import path

from . import views

urlpatterns = [
    path(
        "drone-categories/",
        views.DroneCategoryView.as_view(),
        name=views.DroneCategoryView.name,
    ),
    path(
        "drone-categories/<int:pk>/",
        views.DroneCategoryDetailView.as_view(),
        name=views.DroneCategoryDetailView.name,
    ),
    path("drones/", views.DroneView.as_view(), name=views.DroneView.name),
    path(
        "drones/<int:pk>/",
        views.DroneDetailView.as_view(),
        name=views.DroneDetailView.name,
    ),
    path("pilots/", views.PilotView.as_view(), name=views.PilotView.name),
    path(
        "pilots/<int:pk>/",
        views.PilotDetailView.as_view(),
        name=views.PilotDetailView.name,
    ),
    path(
        "competitions/",
        views.CompetitionView.as_view(),
        name=views.CompetitionView.name,
    ),
    path(
        "competitions/<int:pk>/",
        views.CompetitionDetailView.as_view(),
        name=views.CompetitionDetailView.name,
    ),
    path("", views.ApiRoot.as_view(), name=views.ApiRoot.name),
]
urlpatterns += [
    path("api-token-auth/", views.ObtainAuthToken.as_view()),
]
