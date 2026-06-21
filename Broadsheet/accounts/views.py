from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import LoginForm



# Create your views here.


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = False
    form_class = LoginForm
    


    def get_success_url(self):

        user = self.request.user

        if user.role == "school_admin":
            return reverse_lazy("school_dashboard")

        if user.role == "teacher":
            return reverse_lazy("teacher_dashboard")

        raise ValueError(f"User '{user.username}' has invalid role '{user.role}'"
)


class UserLogoutView(LogoutView):
    next_page = "login"


