"""StudyTrack home and account routes."""

from django.shortcuts import render
from django.urls import include, path
from django.views.decorators.http import require_GET


@require_GET
def home(request):
    return render(request, "home.html")


urlpatterns = [
    path("", home, name="home"),
    path("accounts/", include("accounts.urls")),
    path("assignments/", include("assignments.urls")),
]
