from django.urls import path
from .views import  UserLoginView, UserLogoutView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView


urlpatterns = [
    path("", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("change-password/",
        PasswordChangeView.as_view(template_name="accounts/change_password.html"),
        name="change_password",
    ),

    path("change-password/done/",
        PasswordChangeDoneView.as_view(template_name="accounts/change_password_done.html"),
        name="password_change_done",)

]
