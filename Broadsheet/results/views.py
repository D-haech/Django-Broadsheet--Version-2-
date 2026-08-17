from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .services import calculate_student_subject_result

from accounts.mixin import SchoolAdminRequiredMixin
from academics.models import Student, Subject, Term, Session, SchoolClass
from schools.models import TeachingAssignment, Teacher

from .models import AssessmentType, Assessment, StudentScore
from .forms import AssessmentTypeForm, AssessmentForm

# =========================================================
# ASSESSMENT TYPE
# =========================================================


class AssessmentTypeListView(LoginRequiredMixin, SchoolAdminRequiredMixin, ListView):

    model = AssessmentType

    template_name = "results/assessmenttype_list.html"

    context_object_name = "assessment_types"

    def get_queryset(self):

        return AssessmentType.objects.filter(school=self.request.user.school)


class AssessmentTypeCreateView(
    LoginRequiredMixin, SchoolAdminRequiredMixin, CreateView
):

    model = AssessmentType

    form_class = AssessmentTypeForm

    template_name = "results/assessmenttype_form.html"

    success_url = reverse_lazy("assessment_type_list")

    def form_valid(self, form):

        form.instance.school = self.request.user.school

        return super().form_valid(form)


class AssessmentTypeUpdateView(
    LoginRequiredMixin, SchoolAdminRequiredMixin, UpdateView
):

    model = AssessmentType

    form_class = AssessmentTypeForm

    template_name = "results/assessmenttype_form.html"

    success_url = reverse_lazy("assessment_type_list")

    def get_queryset(self):

        return AssessmentType.objects.filter(school=self.request.user.school)


class AssessmentTypeDeleteView(
    LoginRequiredMixin, SchoolAdminRequiredMixin, DeleteView
):

    model = AssessmentType

    template_name = "results/assessmenttype_confirm_delete.html"

    success_url = reverse_lazy("assessment_type_list")

    def get_queryset(self):

        return AssessmentType.objects.filter(school=self.request.user.school)


# =========================================================
# ASSESSMENT
# =========================================================


class AssessmentListView(LoginRequiredMixin, SchoolAdminRequiredMixin, ListView):

    model = Assessment

    template_name = "results/assessment_list.html"

    context_object_name = "assessments"

    def get_queryset(self):

        return Assessment.objects.filter(school=self.request.user.school)


class AssessmentCreateView(LoginRequiredMixin, SchoolAdminRequiredMixin, CreateView):

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


class AssessmentUpdateView(LoginRequiredMixin, SchoolAdminRequiredMixin, UpdateView):

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


class AssessmentDeleteView(LoginRequiredMixin, SchoolAdminRequiredMixin, DeleteView):

    model = Assessment

    template_name = "results/assessment_confirm_delete.html"

    success_url = reverse_lazy("assessment_list")

    def get_queryset(self):

        return Assessment.objects.filter(school=self.request.user.school)


# =========================================================
# TEACHER SCORE ENTRY
# =========================================================


class TeacherSubjectListView(LoginRequiredMixin, View):

    template_name = "results/teacher_subjects.html"

    def get(self, request):

        teacher = get_object_or_404(Teacher, user=request.user)

        assignments = TeachingAssignment.objects.filter(teacher=teacher).select_related(
            "school_class", "subject"
        )

        current_session = Session.objects.filter(
            school=request.user.school, is_current=True
        ).first()

        current_term = Term.objects.filter(
            school=request.user.school, is_current=True
        ).first()

        return render(
            request,
            self.template_name,
            {
                "assignments": assignments,
                "current_session": current_session,
                "current_term": current_term,
            },
        )


class BulkScoreEntryView(LoginRequiredMixin, View):

    template_name = "results/bulk_score_entry.html"

    def get_teacher(self, request):

        return get_object_or_404(
        Teacher,
        user=request.user
    )

    def get_current_session(self, request):

        return Session.objects.filter(
        school=request.user.school,
        is_current=True
    ).first()

    def get_current_term(self, request, session):

        return Term.objects.filter(
        school=request.user.school,
        session=session,
        is_current=True
    ).first()

    def get(self, request, assignment_id):

        teacher = self.get_teacher(request)

        assignment = get_object_or_404(
            TeachingAssignment.objects.select_related("school_class", "subject"),
            id=assignment_id,
            teacher=teacher,
        )

        session = self.get_current_session(request)

        if not session:
            return render(
                request,
                "results/no_current_session.html",
            )

        term = self.get_current_term(request, session)

        if not term:
            return render(
                request,
                "results/no_current_term.html",
                {
                    "session": session,
                },
            )    

        assessments = Assessment.objects.filter(
            school=request.user.school
        ).select_related("assessment_type")

        assessment_id = request.GET.get("assessment")

        students = Student.objects.filter(
            school=request.user.school,
            student_class=assignment.school_class,
            is_active=True,
        ).order_by("surname", "first_name")

        existing_scores = {}

        if assessment_id:

            assessment = get_object_or_404(
                Assessment, id=assessment_id, school=request.user.school
            )

            scores = StudentScore.objects.filter(
                student__in=students,
                subject=assignment.subject,
                session=session,
                term=term,
                assessment=assessment,
            )

            existing_scores = {score.student_id: score.score for score in scores}

        else:

            assessment = None

        return render(
            request,
            self.template_name,
            {
                "assignment": assignment,
                "session": session,
                "term": term,
                "assessments": assessments,
                "assessment": assessment,
                "students": students,
                "existing_scores": existing_scores,
            },
        )

    def post(self, request, assignment_id):

        teacher = self.get_teacher(request)

        assignment = get_object_or_404(
            TeachingAssignment.objects.select_related("school_class", "subject"),
            id=assignment_id,
            teacher=teacher,
        )

        session = self.get_current_session(request)

        if not session:
            return render(
                request,
                "results/no_current_session.html",
            )

        term = self.get_current_term(request, session)

        if not term:
            return render(
                request,
                "results/no_current_term.html",
                {
                    "session": session,
                },
            )
        # ------------------------------------------------#

        assessment_id = request.POST.get("assessment")

        if not assessment_id:

            return redirect("bulk_score_entry", assignment_id=assignment.id)

        assessment = get_object_or_404(
            Assessment, id=assessment_id, school=request.user.school
        )

        students = Student.objects.filter(
            school=request.user.school,
            student_class=assignment.school_class,
            is_active=True,
        )

        for student in students:

            score = request.POST.get(f"score_{student.id}")

            if score in (None, ""):
                continue

            try:

                score_value = float(score)

            except ValueError:

                continue

            if score_value < 0:
                continue

            if score_value > assessment.maximum_score:
                continue

            StudentScore.objects.update_or_create(
                student=student,
                subject=assignment.subject,
                session=session,
                term=term,
                assessment=assessment,
                defaults={"score": score_value},
            )

        return redirect(
            f"/results/score-entry/{assignment.id}/" f"?assessment={assessment.id}"
        )


class AdminScoreEntryView(
    LoginRequiredMixin,
    SchoolAdminRequiredMixin,
    View,
):

    template_name = "results/admin_score_entry.html"

    def get_current_session(self, request):

        return Session.objects.filter(
            school=request.user.school, is_current=True
        ).first()

    def get_current_term(self, request, session):

        return Term.objects.filter(
            school=request.user.school, session=session, is_current=True
        ).first()

    def get(self, request):

        session = self.get_current_session(request)

        if not session:
            return render(
                request,
                "results/no_current_session.html",
            )

        term = self.get_current_term(request, session)

        if not term:
            return render(
                request,
                "results/no_current_term.html",
                {
                    "session": session,
                },
            )

        school_classes = SchoolClass.objects.filter(
            school=request.user.school
        ).order_by("name")

        subjects = Subject.objects.filter(school=request.user.school).order_by("name")

        assessments = (
            Assessment.objects.filter(school=request.user.school)
            .select_related("assessment_type")
            .order_by(
                "assessment_type__name",
                "name",
            )
        )

        class_id = request.GET.get("class")
        subject_id = request.GET.get("subject")
        assessment_id = request.GET.get("assessment")

        students = Student.objects.none()
        assessment = None

        if class_id and subject_id and assessment_id:

            school_class = get_object_or_404(
                SchoolClass,
                id=class_id,
                school=request.user.school,
            )

            subject = get_object_or_404(
                Subject,
                id=subject_id,
                school=request.user.school,
            )

            assessment = get_object_or_404(
                Assessment,
                id=assessment_id,
                school=request.user.school,
            )

            students = Student.objects.filter(
                school=request.user.school,
                student_class=school_class,
                is_active=True,
            ).order_by(
                "surname",
                "first_name",
            )

        return render(
            request,
            self.template_name,
            {
                "session": session,
                "term": term,
                "school_classes": school_classes,
                "subjects": subjects,
                "assessments": assessments,
                "students": students,
                "assessment": assessment,
                "selected_class": class_id,
                "selected_subject": subject_id,
                "selected_assessment": assessment_id,
            },
        )

    def post(self, request):

        session = self.get_current_session(request)

        if not session:
            return render(
                request,
                "results/no_current_session.html",
            )

        term = self.get_current_term(request, session)

        if not term:
            return render(
                request,
                "results/no_current_term.html",
                {
                    "session": session,
                },
            )

        class_id = request.POST.get("school_class")
        subject_id = request.POST.get("subject")
        assessment_id = request.POST.get("assessment")

        if not all(
            [
                class_id,
                subject_id,
                assessment_id,
            ]
        ):

            return redirect("admin_score_entry")

        school_class = get_object_or_404(
            SchoolClass,
            id=class_id,
            school=request.user.school,
        )

        subject = get_object_or_404(
            Subject,
            id=subject_id,
            school=request.user.school,
        )

        assessment = get_object_or_404(
            Assessment,
            id=assessment_id,
            school=request.user.school,
        )

        students = Student.objects.filter(
            school=request.user.school,
            student_class=school_class,
            is_active=True,
        )

        for student in students:

            score = request.POST.get(f"score_{student.id}")

            if score in (None, ""):
                continue

            try:

                score_value = float(score)

            except ValueError:

                continue

            if score_value < 0:
                continue

            if score_value > assessment.maximum_score:
                continue

            StudentScore.objects.update_or_create(
                student=student,
                subject=subject,
                session=session,
                term=term,
                assessment=assessment,
                defaults={"score": score_value},
            )

        return redirect(
            f"/results/admin-score-entry/"
            f"?class={school_class.id}"
            f"&subject={subject.id}"
            f"&assessment={assessment.id}"
        )


class SummaryBroadsheetView(
    LoginRequiredMixin,
    SchoolAdminRequiredMixin,
    View,
):

    template_name = "results/summary_broadsheet.html"

    def get_current_session(self, request):

        return get_object_or_404(
            Session,
            school=request.user.school,
            is_current=True,
        )

    def get_current_term(self, request, session):

        return get_object_or_404(
            Term,
            school=request.user.school,
            session=session,
            is_current=True,
        )

    def get(self, request):

        session = self.get_current_session(request)

        term = self.get_current_term(
            request,
            session,
        )

        school_classes = SchoolClass.objects.filter(
            school=request.user.school
        ).order_by("name")

        class_id = request.GET.get("class")

        selected_class = None
        students = []
        subjects = []

        if class_id:

            selected_class = get_object_or_404(
                SchoolClass,
                id=class_id,
                school=request.user.school,
            )

            students = Student.objects.filter(
                school=request.user.school,
                student_class=selected_class,
                is_active=True,
            ).order_by(
                "surname",
                "first_name",
            )

            subjects = Subject.objects.filter(school=request.user.school).order_by(
                "name"
            )

        rows = []

        for student in students:

            student_results = []

            grand_total = 0

            for subject in subjects:

                result = calculate_student_subject_result(
                student=student,
                subject=subject,
                session=session,
                term=term,
            )

                student_results.append(
                    {
                        "subject": subject,
                        "result": result,
                    }
                )
                grand_total += result["total"]

            rows.append(
        {
            "student": student,
            "results": student_results,
            "grand_total": round(
                grand_total,
                2,
            ),
        }
    )

        return render(
            request,
            self.template_name,
            {
                "session": session,
                "term": term,
                "school_classes": school_classes,
                "selected_class": selected_class,
                "subjects": subjects,
                "rows": rows,
            },
        )


class CompleteBroadsheetView(
    LoginRequiredMixin,
    SchoolAdminRequiredMixin,
    View,
):

    template_name = "results/complete_broadsheet.html"

    def get_current_session(self, request):

        return get_object_or_404(
            Session,
            school=request.user.school,
            is_current=True,
        )

    def get_current_term(self, request, session):

        return get_object_or_404(
            Term,
            school=request.user.school,
            session=session,
            is_current=True,
        )

    def get(self, request):

        session = self.get_current_session(request)

        term = self.get_current_term(
            request,
            session,
        )

        school_classes = SchoolClass.objects.filter(
            school=request.user.school
        ).order_by("name")

        class_id = request.GET.get("class")

        selected_class = None
        students = []
        subjects = []

        if class_id:

            selected_class = get_object_or_404(
                SchoolClass,
                id=class_id,
                school=request.user.school,
            )

            students = Student.objects.filter(
                school=request.user.school,
                student_class=selected_class,
                is_active=True,
            ).order_by(
                "surname",
                "first_name",
            )

            subjects = Subject.objects.filter(school=request.user.school).order_by(
                "name"
            )

        rows = []

        for student in students:

            student_results = []

            for subject in subjects:

                result = calculate_student_subject_result(
                    student=student,
                    subject=subject,
                    session=session,
                    term=term,
                )

                student_results.append(
                    {
                        "subject": subject,
                        "result": result,
                    }
                )

            rows.append(
                {
                    "student": student,
                    "results": student_results,
                }
            )

        return render(
            request,
            self.template_name,
            {
                "session": session,
                "term": term,
                "school_classes": school_classes,
                "selected_class": selected_class,
                "subjects": subjects,
                "rows": rows,
            },
        )
