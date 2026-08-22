from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .forms import TeacherUpdateForm
from django.views.generic import UpdateView
from .models import Teacher, TeachingAssignment
from accounts.models import User
from .forms import TeacherCreateForm, TeacherClassForm
from django.views.generic import DeleteView
from .forms import TeachingAssignmentForm
from accounts.mixin import SchoolAdminRequiredMixin

from django.views.generic import UpdateView, TemplateView

from django.urls import reverse_lazy
from django.core.files.storage import default_storage
from .models import School
from .decorators import SchoolAdminRequiredMixin

# Create your views here.


class TeacherListView(LoginRequiredMixin, SchoolAdminRequiredMixin, ListView):

    model = Teacher

    template_name = "schools/teacher_list.html"

    context_object_name = "teachers"

    def get_queryset(self):

        return Teacher.objects.filter(user__school=self.request.user.school)


class TeacherCreateView(LoginRequiredMixin, SchoolAdminRequiredMixin, FormView):

    template_name = "schools/teacher_form.html"

    form_class = TeacherCreateForm

    success_url = reverse_lazy("teacher_list")

    def form_valid(self, form):

        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            email=form.cleaned_data["email"],
            role="teacher",
            school=self.request.user.school,
        )

        Teacher.objects.create(
            user=user,
            phone=form.cleaned_data["phone"],
            address=form.cleaned_data["address"],
            date_employed=form.cleaned_data["date_employed"],
        )

        return super().form_valid(form)


class TeacherUpdateView(LoginRequiredMixin, SchoolAdminRequiredMixin, UpdateView):

    model = Teacher

    form_class = TeacherUpdateForm

    template_name = "schools/teacher_form.html"

    success_url = reverse_lazy("teacher_list")

    def get_queryset(self):

        return Teacher.objects.filter(user__school=self.request.user.school)


class TeacherDeleteView(LoginRequiredMixin, SchoolAdminRequiredMixin, DeleteView):

    model = Teacher

    template_name = "schools/teacher_confirm_delete.html"

    success_url = reverse_lazy("teacher_list")

    def get_queryset(self):

        return Teacher.objects.filter(user__school=self.request.user.school)

    def form_valid(self, form):

        user = self.object.user

        user.delete()

        return redirect(self.success_url)


class TeacherClassAssignView(LoginRequiredMixin, SchoolAdminRequiredMixin, UpdateView):

    model = Teacher

    form_class = TeacherClassForm

    template_name = "schools/teacher_class_assign.html"

    success_url = reverse_lazy("teacher_list")

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()

        kwargs["school"] = self.request.user.school

        return kwargs

    def get_queryset(self):

        return Teacher.objects.filter(user__school=self.request.user.school)


class TeacherAssignmentListView(LoginRequiredMixin, SchoolAdminRequiredMixin, ListView):

    model = TeachingAssignment

    template_name = "schools/teacher_assignment_list.html"

    context_object_name = "assignments"

    def get_queryset(self):

        self.teacher = get_object_or_404(Teacher, pk=self.kwargs["pk"])

        return TeachingAssignment.objects.filter(teacher=self.teacher)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["teacher"] = self.teacher

        return context


class TeacherAssignmentCreateView(LoginRequiredMixin, SchoolAdminRequiredMixin, CreateView):

    model = TeachingAssignment

    form_class = TeachingAssignmentForm

    template_name = "schools/teacher_assignment_form.html"

    def dispatch(self, request, *args, **kwargs):

        self.teacher = get_object_or_404(
            Teacher.objects.filter(user__school=self.request.user.school),
            pk=self.kwargs["pk"],
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["teacher"] = self.teacher

        return context

    def form_valid(self, form):

        form.instance.teacher = self.teacher

        return super().form_valid(form)

    def get_success_url(self):

        return reverse_lazy("teacher_assignments", kwargs={"pk": self.teacher.pk})
    
    def get_form(self, form_class=None):

        form = super().get_form(form_class)

        form.teacher = self.teacher

        return form

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()

        kwargs["school"] = self.request.user.school

        return kwargs


class TeacherAssignmentDeleteView(LoginRequiredMixin, SchoolAdminRequiredMixin, DeleteView):

    model = TeachingAssignment

    template_name = "schools/assignment_confirm_delete.html"

    def get_success_url(self):

        return reverse_lazy(
            "teacher_assignments", kwargs={"pk": self.object.teacher.pk}
        )


# schools Logo Uploads


class SchoolSettingsView(LoginRequiredMixin, SchoolAdminRequiredMixin, TemplateView):
    """View for school settings page with logo upload"""

    template_name = "schools/school_settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["school"] = self.request.user.school
        return context


class UploadLogoView(LoginRequiredMixin, SchoolAdminRequiredMixin, UpdateView):
    """Class-based view for uploading school logo"""

    model = School
    fields = ["logo"]  # Only allow updating the logo
    template_name = "schools/upload_logo.html"
    success_url = reverse_lazy("school_settings")

    def get_object(self, queryset=None):
        # Get the school associated with the current user
        return self.request.user.school

    def form_valid(self, form):
        # Additional validation if needed
        return super().form_valid(form)

    def form_invalid(self, form):
        # Handle errors gracefully
        return super().form_invalid(form)
