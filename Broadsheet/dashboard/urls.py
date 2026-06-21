from django.urls import path
from django.urls import path

from .views import (SchoolDashboardView,TeacherDashboardView)

urlpatterns = [
    path("school/", SchoolDashboardView.as_view(), name="school_dashboard"),
    path("teacher/", TeacherDashboardView.as_view(), name="teacher_dashboard"),
]
