from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import SchoolClass, Subject, Student, Session, Term
from .forms import SchoolClassForm, SubjectForm, SessionForm, StudentForm, TermForm
from accounts.mixin import SchoolAdminRequiredMixin


# Create your views here.


class SchoolClassListView(LoginRequiredMixin,SchoolAdminRequiredMixin, ListView):

    model = SchoolClass

    template_name = "academics/class_list.html"

    context_object_name = "classes"

    def get_queryset(self):

        return SchoolClass.objects.filter(school=self.request.user.school)


class SchoolClassCreateView(LoginRequiredMixin, SchoolAdminRequiredMixin, CreateView):

    model = SchoolClass

    form_class = SchoolClassForm

    template_name = "academics/class_form.html"

    success_url = reverse_lazy("class_list")

    def form_valid(self, form):

        form.instance.school = self.request.user.school

        return super().form_valid(form)


class SchoolClassUpdateView(LoginRequiredMixin, SchoolAdminRequiredMixin, UpdateView):

    model = SchoolClass

    form_class = SchoolClassForm

    template_name = "academics/class_form.html"

    success_url = reverse_lazy("class_list")

    def get_queryset(self):

        return SchoolClass.objects.filter(school=self.request.user.school)


class SchoolClassDeleteView(LoginRequiredMixin, SchoolAdminRequiredMixin, DeleteView):

    model = SchoolClass

    template_name = "academics/class_confirm_delete.html"

    success_url = reverse_lazy("class_list")

    def get_queryset(self):

        return SchoolClass.objects.filter(school=self.request.user.school)


# Subject CRUD
class SubjectCreateView(LoginRequiredMixin, SchoolAdminRequiredMixin, CreateView):

    model = Subject

    form_class = SubjectForm

    template_name = "academics/subject_form.html"

    success_url = reverse_lazy("subject_list")

    def form_valid(self, form):

        form.instance.school = self.request.user.school

        return super().form_valid(form)


class SubjectUpdateView(LoginRequiredMixin, SchoolAdminRequiredMixin, UpdateView):

    model = Subject

    form_class = SubjectForm

    template_name = "academics/subject_form.html"

    success_url = reverse_lazy("subject_list")

    def get_queryset(self):

        return Subject.objects.filter(school=self.request.user.school)


class SubjectDeleteView(LoginRequiredMixin, SchoolAdminRequiredMixin, DeleteView):

    model = Subject

    template_name = "academics/subject_confirm_delete.html"

    success_url = reverse_lazy("subject_list")

    def get_queryset(self):

        return Subject.objects.filter(school=self.request.user.school)


class SubjectListView(LoginRequiredMixin, SchoolAdminRequiredMixin, ListView):

    model = Subject

    template_name = "academics/subject_list.html"

    context_object_name = "subjects"

    def get_queryset(self):

        return Subject.objects.filter(school=self.request.user.school)


class StudentListView(LoginRequiredMixin, SchoolAdminRequiredMixin, ListView):

    model = Student

    template_name = "academics/student_list.html"

    context_object_name = "students"

    def get_queryset(self):

        return Student.objects.filter(school=self.request.user.school)


class StudentCreateView(LoginRequiredMixin, SchoolAdminRequiredMixin, CreateView):

    model = Student

    form_class = StudentForm

    template_name = "academics/student_form.html"

    success_url = reverse_lazy("student_list")

    def form_valid(self, form):

        form.instance.school = self.request.user.school

        return super().form_valid(form)

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()

        kwargs["school"] = self.request.user.school

        return kwargs


class StudentUpdateView(LoginRequiredMixin, SchoolAdminRequiredMixin, UpdateView):

    model = Student

    form_class = StudentForm

    template_name = "academics/student_form.html"

    success_url = reverse_lazy("student_list")

    def get_queryset(self):

        return Student.objects.filter(school=self.request.user.school)

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()

        kwargs["school"] = self.request.user.school

        return kwargs


class StudentDeleteView(LoginRequiredMixin, SchoolAdminRequiredMixin, DeleteView):

    model = Student

    template_name = "academics/student_confirm_delete.html"

    success_url = reverse_lazy("student_list")

    def get_queryset(self):

        return Student.objects.filter(school=self.request.user.school)


# Session CRUD


class SessionListView(LoginRequiredMixin, SchoolAdminRequiredMixin, ListView):

    model = Session

    template_name = "academics/session_list.html"

    context_object_name = "sessions"

    def get_queryset(self):

        return Session.objects.filter(school=self.request.user.school)


class SessionCreateView(LoginRequiredMixin, SchoolAdminRequiredMixin, CreateView):

    model = Session

    form_class = SessionForm

    template_name = "academics/session_form.html"

    success_url = reverse_lazy("session_list")

    def form_valid(self, form):

        form.instance.school = self.request.user.school

        if form.cleaned_data["is_current"]:

            Session.objects.filter(school=self.request.user.school).update(
                is_current=False
            )

        return super().form_valid(form)


class SessionUpdateView(LoginRequiredMixin, SchoolAdminRequiredMixin, UpdateView):

    model = Session

    form_class = SessionForm

    template_name = "academics/session_form.html"

    success_url = reverse_lazy("session_list")

    def get_queryset(self):

        return Session.objects.filter(school=self.request.user.school)

    def form_valid(self, form):

        if form.cleaned_data["is_current"]:

            Session.objects.filter(school=self.request.user.school).exclude(
                pk=self.object.pk
            ).update(is_current=False)

        return super().form_valid(form)


class SessionDeleteView(LoginRequiredMixin, SchoolAdminRequiredMixin, DeleteView):

    model = Session

    template_name = "academics/session_confirm_delete.html"

    success_url = reverse_lazy("session_list")

    def get_queryset(self):

        return Session.objects.filter(school=self.request.user.school)


class TermListView(LoginRequiredMixin, SchoolAdminRequiredMixin, ListView):

    model = Term

    template_name = "academics/term_list.html"

    context_object_name = "terms"

    def get_queryset(self):

        return Term.objects.filter(school=self.request.user.school)


class TermCreateView(LoginRequiredMixin, SchoolAdminRequiredMixin, CreateView):

    model = Term

    form_class = TermForm

    template_name = "academics/term_form.html"

    success_url = reverse_lazy("term_list")

    def form_valid(self, form):

        form.instance.school = self.request.user.school

        return super().form_valid(form)

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()

        kwargs["school"] = self.request.user.school

        return kwargs


class TermUpdateView(LoginRequiredMixin, SchoolAdminRequiredMixin, UpdateView):

    model = Term

    form_class = TermForm

    template_name = "academics/term_form.html"

    success_url = reverse_lazy("term_list")

    def get_queryset(self):

        return Term.objects.filter(school=self.request.user.school)

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()

        kwargs["school"] = self.request.user.school

        return kwargs


class TermDeleteView(LoginRequiredMixin, SchoolAdminRequiredMixin, DeleteView):

    model = Term

    template_name = "academics/term_confirm_delete.html"

    success_url = reverse_lazy("term_list")

    def get_queryset(self):

        return Term.objects.filter(school=self.request.user.school)
