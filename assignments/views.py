from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views import View

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

    def get(self, request, *args, **kwargs):
        self.status_filter = request.GET.get("status") or "all"
        self.subject_filter = request.GET.get("subject") or ""
        owned = super().get_queryset()
        self.subjects = list(owned.order_by("subject").values_list("subject", flat=True).distinct())
        if self.status_filter not in ("all", "pending", "completed"):
            return render(request, self.template_name, {
                "subjects": self.subjects, "status_filter": "all", "subject_filter": self.subject_filter,
                "filter_error": "Choose a valid status: All, Not completed, or Completed.",
            }, status=400)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.status_filter != "all":
            queryset = queryset.filter(is_completed=self.status_filter == "completed")
        if self.subject_filter:
            queryset = queryset.filter(subject=self.subject_filter)
        return queryset.order_by(F("deadline").asc(nulls_last=True), "created_at", "pk")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(subjects=self.subjects, status_filter=self.status_filter, subject_filter=self.subject_filter,
                       has_filters=self.status_filter != "all" or bool(self.subject_filter))
        return context


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


class AssignmentStatusView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, pk):
        assignment = get_object_or_404(Assignment.objects.filter(owner=request.user), pk=pk)
        desired_state = request.POST.get("is_completed")
        if desired_state not in ("1", "0"):
            return HttpResponseBadRequest("Choose a completion status: is_completed must be 1 or 0.")
        assignment.is_completed = desired_state == "1"
        assignment.save(update_fields=["is_completed"])
        return redirect("assignments:list")
