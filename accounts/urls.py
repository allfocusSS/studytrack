from django.contrib.auth.views import LoginView
from django.urls import path

from .views import RegisterView, StudentLogoutView

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", StudentLogoutView.as_view(), name="logout"),
]
