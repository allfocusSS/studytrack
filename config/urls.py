"""Public bootstrap route for StudyTrack."""

from django.http import HttpResponse
from django.urls import path
from django.views.decorators.http import require_GET


@require_GET
def home(request):
    return HttpResponse("StudyTrack\n", content_type="text/plain; charset=utf-8")


urlpatterns = [path("", home, name="home")]
