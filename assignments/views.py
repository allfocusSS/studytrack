from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import AssignmentForm
from .models import Assignment


class StudentAssignmentsMixin(LoginRequiredMixin):
    model = Assignment
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class AssignmentListView(StudentAssignmentsMixin, ListView):
    template_name = "assignments/list.html"
    context_object_name = "assignments"
    http_method_names = ["get", "head", "options"]


class AssignmentCreateView(StudentAssignmentsMixin, CreateView):
    template_name = "assignments/form.html"
    form_class = AssignmentForm
    success_url = reverse_lazy("assignments:list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class AssignmentUpdateView(StudentAssignmentsMixin, UpdateView):
    template_name = "assignments/form.html"
    form_class = AssignmentForm
    success_url = reverse_lazy("assignments:list")


class AssignmentDeleteView(StudentAssignmentsMixin, DeleteView):
    template_name = "assignments/confirm_delete.html"
    success_url = reverse_lazy("assignments:list")
