from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from accounts.mixin import SchoolAdminRequiredMixin, TeacherRequiredMixin
from schools.models import Teacher, TeachingAssignment


# Create your views here.


class SchoolDashboardView(LoginRequiredMixin, SchoolAdminRequiredMixin, TemplateView):
    template_name = "dashboard/school_dashboard.html"


class TeacherDashboardView(LoginRequiredMixin, TeacherRequiredMixin, TemplateView):

    template_name = "dashboard/teacher_dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        teacher = get_object_or_404(Teacher, user=self.request.user)

        context["assignments"] = TeachingAssignment.objects.filter(teacher=teacher)

        return context
