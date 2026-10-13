"""Protected access probe used only through test ROOT_URLCONF overrides."""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import include, path


@login_required
def protected_probe(request):
    return HttpResponse("Authenticated access")


urlpatterns = [
    path("__account_test__/", protected_probe),
    path("", include("config.urls")),
]
