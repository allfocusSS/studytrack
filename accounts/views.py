"""Account views using Django's standard forms and session facilities."""

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import FormView


@method_decorator(sensitive_post_parameters("password1", "password2"), name="dispatch")
@method_decorator(never_cache, name="dispatch")
class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("accounts:login")
    http_method_names = ["get", "post", "head", "options"]

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Account created. You can now log in.")
        return super().form_valid(form)


class StudentLogoutView(LoginRequiredMixin, LogoutView):
    """Require an authenticated session before Django's POST-only logout."""
