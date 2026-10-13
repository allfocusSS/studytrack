from django.urls import path

from .views import AssignmentCreateView, AssignmentDeleteView, AssignmentListView, AssignmentStatusView, AssignmentUpdateView

app_name = "assignments"

urlpatterns = [
    path("", AssignmentListView.as_view(), name="list"),
    path("new/", AssignmentCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", AssignmentUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", AssignmentDeleteView.as_view(), name="delete"),
    path("<int:pk>/status/", AssignmentStatusView.as_view(), name="status"),
]
