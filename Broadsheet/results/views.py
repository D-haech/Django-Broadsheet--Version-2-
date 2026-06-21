from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView)
from accounts.mixin import SchoolAdminRequiredMixin
from .models import AssessmentType, Assessment
from .forms import AssessmentTypeForm
from django.urls import reverse_lazy

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from accounts.mixin import SchoolAdminRequiredMixin


from .forms import AssessmentForm

# Create your views here.


class AssessmentTypeListView(LoginRequiredMixin, SchoolAdminRequiredMixin, ListView):

    model = AssessmentType

    template_name = "results/assessmenttype_list.html"

    context_object_name = "assessment_types"

    def get_queryset(self):

        return AssessmentType.objects.filter(school=self.request.user.school)


class AssessmentTypeCreateView(LoginRequiredMixin, SchoolAdminRequiredMixin, CreateView):

    model = AssessmentType

    form_class = AssessmentTypeForm

    template_name = "results/assessmenttype_form.html"

    success_url = reverse_lazy("assessment_type_list")

    def form_valid(self, form):

        form.instance.school = self.request.user.school

        return super().form_valid(form)


class AssessmentTypeUpdateView(
    LoginRequiredMixin,
    SchoolAdminRequiredMixin,
    UpdateView,
):

    model = AssessmentType

    form_class = AssessmentTypeForm

    template_name = "results/assessmenttype_form.html"

    success_url = reverse_lazy("assessment_type_list")

    def get_queryset(self):

        return AssessmentType.objects.filter(school=self.request.user.school)


class AssessmentTypeDeleteView(
    LoginRequiredMixin,
    SchoolAdminRequiredMixin,
    DeleteView,
):

    model = AssessmentType

    template_name = "results/assessmenttype_confirm_delete.html"

    success_url = reverse_lazy("assessment_type_list")

    def get_queryset(self):

        return AssessmentType.objects.filter(school=self.request.user.school)


class AssessmentListView(LoginRequiredMixin, SchoolAdminRequiredMixin, ListView):

    model = Assessment

    template_name = "results/assessment_list.html"

    context_object_name = "assessments"

    def get_queryset(self):

        return Assessment.objects.filter(school=self.request.user.school)


class AssessmentCreateView(
    LoginRequiredMixin,
    SchoolAdminRequiredMixin,
    CreateView,
):

    model = Assessment

    form_class = AssessmentForm

    template_name = "results/assessment_form.html"

    success_url = reverse_lazy("assessment_list")

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()

        kwargs["school"] = self.request.user.school

        return kwargs

    def form_valid(self, form):

        form.instance.school = self.request.user.school

        return super().form_valid(form)


class AssessmentUpdateView(
    LoginRequiredMixin,
    SchoolAdminRequiredMixin,
    UpdateView,
):

    model = Assessment

    form_class = AssessmentForm

    template_name = "results/assessment_form.html"

    success_url = reverse_lazy("assessment_list")

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()

        kwargs["school"] = self.request.user.school

        return kwargs

    def get_queryset(self):

        return Assessment.objects.filter(school=self.request.user.school)


class AssessmentDeleteView(
    LoginRequiredMixin,
    SchoolAdminRequiredMixin,
    DeleteView,
):

    model = Assessment

    template_name = "results/assessment_confirm_delete.html"

    success_url = reverse_lazy("assessment_list")

    def get_queryset(self):

        return Assessment.objects.filter(school=self.request.user.school)



