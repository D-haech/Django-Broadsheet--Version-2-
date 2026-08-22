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
from .services import calculate_student_subject_result, get_grade_and_remark

from accounts.mixin import SchoolAdminRequiredMixin
from academics.models import Student, Subject, Term, Session, SchoolClass
from schools.models import TeachingAssignment, Teacher



from django.contrib.auth.mixins import LoginRequiredMixin 
from academics.models import Student, Subject, Session, Term, SchoolClass

from .models import AssessmentType, Assessment, StudentScore
from .forms import AssessmentTypeForm, AssessmentForm


from django.urls import reverse_lazy
from django.contrib import messages
from .models import GradeSystem, Grade
from .forms import GradeSystemForm, GradeForm

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

    # results/views.py - Update CompleteBroadsheetView




    def get(self, request):
        session = self.get_current_session(request)
        term = self.get_current_term(request, session)

        school_classes = SchoolClass.objects.filter(
            school=request.user.school
        ).order_by("name")

        class_id = request.GET.get("class")

        selected_class = None
        students = []
        subjects = []
        rows = []
        column_groups = []

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
            ).order_by("surname", "first_name")

            subjects = Subject.objects.filter(school=request.user.school).order_by(
                "name"
            )

            # Build column structure
            if students.exists():
                first_student = students.first()
                for subject in subjects:
                    result = calculate_student_subject_result(
                        student=first_student,
                        subject=subject,
                        session=session,
                        term=term,
                    )

                    type_groups = []
                    for type_name, type_data in result["assessment_types"].items():
                        type_groups.append(
                            {
                                "name": type_name,
                                "assessments": type_data["assessments"],
                                "column_count": (len(type_data["assessments"]) + 1),
                            }
                        )

                    column_groups.append(
                        {
                            "subject": subject,
                            "types": type_groups,
                            "column_count": sum(
                                group["column_count"] for group in type_groups
                            ),
                        }
                    )

            # Calculate results for each student
            from .services import get_grade_and_remark

            for student in students:
                student_results = []

                for subject in subjects:
                    result = calculate_student_subject_result(
                        student=student,
                        subject=subject,
                        session=session,
                        term=term,
                    )

                    # Get grade and remark for this subject
                    total_score = result["total"]
                    grade, remark = get_grade_and_remark(
                        total_score, request.user.school
                    )

                    student_results.append(
                        {
                            "subject": subject,
                            "result": result,
                            "grade": grade,
                            "remark": remark,
                        }
                    )

                rows.append(
                    {
                        "student": student,
                        "results": student_results,
                    }
                )

            # Calculate totals, averages, and positions
            for row in rows:
                row["grand_total"] = sum(
                    item["result"]["total"] for item in row["results"]
                )
                row["average"] = (
                    round(row["grand_total"] / len(subjects), 2) if subjects else 0
                )

                # Get overall grade and remark
                overall_grade, overall_remark = get_grade_and_remark(
                    row["average"], request.user.school
                )
                row["overall_grade"] = overall_grade
                row["overall_remark"] = overall_remark

            # Sort by grand_total descending and assign positions
            rows.sort(key=lambda x: x["grand_total"], reverse=True)
            for position, row in enumerate(rows, 1):
                row["position"] = position

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
                "column_groups": column_groups,
            },
        )


class StudentResultView(LoginRequiredMixin, View):
    template_name = "results/student_result.html"

    def get(self, request, student_id):
        student = get_object_or_404(Student, id=student_id, school=request.user.school)

        session = self.get_current_session(request)
        term = self.get_current_term(request, session)

        # Get all subjects for this class
        subjects = Subject.objects.filter(school=request.user.school).order_by("name")

        # Calculate results for each subject
        subject_results = []
        total_score = 0

        for subject in subjects:
            result = calculate_student_subject_result(
                student=student, subject=subject, session=session, term=term
            )
            subject_results.append({"subject": subject, "result": result})
            total_score += result.get("total", 0)

        # Calculate average and position
        average = round(total_score / len(subjects), 2) if subjects else 0

        return render(
            request,
            self.template_name,
            {
                "student": student,
                "session": session,
                "term": term,
                "subject_results": subject_results,
                "total_score": total_score,
                "average": average,
                "school": request.user.school,
            },
        )


# =========================================================
# GRADE SYSTEM MANAGEMENT
# =========================================================


class GradeSystemListView(LoginRequiredMixin, SchoolAdminRequiredMixin, ListView):
    model = GradeSystem
    template_name = "results/grade_system_list.html"
    context_object_name = "grade_systems"

    def get_queryset(self):
        return GradeSystem.objects.filter(school=self.request.user.school)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_active"] = GradeSystem.objects.filter(
            school=self.request.user.school, is_active=True
        ).exists()
        return context


class GradeSystemCreateView(LoginRequiredMixin, SchoolAdminRequiredMixin, CreateView):
    model = GradeSystem
    form_class = GradeSystemForm
    template_name = "results/grade_system_form.html"
    success_url = reverse_lazy("grade_system_list")

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        messages.success(
            self.request, f"Grading System '{form.instance.name}' created successfully!"
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["school"] = self.request.user.school
        return kwargs


class GradeSystemUpdateView(LoginRequiredMixin, SchoolAdminRequiredMixin, UpdateView):
    model = GradeSystem
    form_class = GradeSystemForm
    template_name = "results/grade_system_form.html"
    success_url = reverse_lazy("grade_system_list")

    def get_queryset(self):
        return GradeSystem.objects.filter(school=self.request.user.school)

    def form_valid(self, form):
        messages.success(
            self.request, f"Grading System '{form.instance.name}' updated successfully!"
        )
        return super().form_valid(form)


class GradeSystemDeleteView(LoginRequiredMixin, SchoolAdminRequiredMixin, DeleteView):
    model = GradeSystem
    template_name = "results/grade_system_confirm_delete.html"
    success_url = reverse_lazy("grade_system_list")

    def get_queryset(self):
        return GradeSystem.objects.filter(school=self.request.user.school)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f"Grading System '{obj.name}' deleted successfully!")
        return super().delete(request, *args, **kwargs)


class GradeCreateView(LoginRequiredMixin, SchoolAdminRequiredMixin, CreateView):
    model = Grade
    form_class = GradeForm
    template_name = "results/grade_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "grade_system_update", kwargs={"pk": self.kwargs["system_pk"]}
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["system_pk"] = self.kwargs["system_pk"]
        return kwargs

    def form_valid(self, form):
        form.instance.grade_system = get_object_or_404(
            GradeSystem, id=self.kwargs["system_pk"], school=self.request.user.school
        )
        messages.success(
            self.request, f"Grade '{form.instance.grade}' added successfully!"
        )
        return super().form_valid(form)


class GradeUpdateView(LoginRequiredMixin, SchoolAdminRequiredMixin, UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = "results/grade_form.html"

    def get_queryset(self):
        return Grade.objects.filter(grade_system__school=self.request.user.school)

    def get_success_url(self):
        return reverse_lazy(
            "grade_system_update", kwargs={"pk": self.object.grade_system.id}
        )

    def form_valid(self, form):
        messages.success(
            self.request, f"Grade '{form.instance.grade}' updated successfully!"
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["system_pk"] = self.object.grade_system.id
        return kwargs


class GradeDeleteView(LoginRequiredMixin, SchoolAdminRequiredMixin, DeleteView):
    model = Grade
    template_name = "results/grade_confirm_delete.html"

    def get_queryset(self):
        return Grade.objects.filter(grade_system__school=self.request.user.school)

    def get_success_url(self):
        return reverse_lazy(
            "grade_system_update", kwargs={"pk": self.object.grade_system.id}
        )

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f"Grade '{obj.grade}' deleted successfully!")
        return super().delete(request, *args, **kwargs)


class StudentResultView(LoginRequiredMixin, View):
    """
    View for individual student result card.
    """

    template_name = "results/student_result.html"

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

    def get_student_position(self, student, students_scores):
        """
        Get student's position in class based on total score.
        """
        # Sort students by total score descending
        sorted_students = sorted(
            students_scores.items(), key=lambda x: x[1], reverse=True
        )

        # Find position
        for position, (stud, score) in enumerate(sorted_students, 1):
            if stud.id == student.id:
                return position
        return None

    def get(self, request, student_id):
        # Get student
        student = get_object_or_404(
            Student, id=student_id, school=request.user.school, is_active=True
        )

        # Get current session and term
        session = self.get_current_session(request)
        term = self.get_current_term(request, session)

        # Get all subjects for this school
        subjects = Subject.objects.filter(school=request.user.school).order_by("name")

        # Calculate results for each subject
        subject_results = []
        grand_total = 0
        total_possible = 0
        subject_count = 0

        for subject in subjects:
            result = calculate_student_subject_result(
                student=student, subject=subject, session=session, term=term
            )

            total_score = result["total"]
            grade, remark = get_grade_and_remark(total_score, request.user.school)

            subject_results.append(
                {
                    "subject": subject,
                    "result": result,
                    "total": total_score,
                    "grade": grade,
                    "remark": remark,
                }
            )

            grand_total += total_score
            # Assuming each subject has a maximum of 100
            total_possible += 100
            subject_count += 1

        # Calculate averages
        average = round(grand_total / subject_count, 2) if subject_count > 0 else 0
        percentage = (
            round((grand_total / total_possible) * 100, 2) if total_possible > 0 else 0
        )

        # Get overall grade and remark
        overall_grade, overall_remark = get_grade_and_remark(
            percentage, request.user.school
        )

        # Calculate class position (get all students in class and their scores)
        class_students = Student.objects.filter(
            school=request.user.school,
            student_class=student.student_class,
            is_active=True,
        )

        students_scores = {}
        for stud in class_students:
            stud_total = 0
            for subject in subjects:
                result = calculate_student_subject_result(
                    student=stud, subject=subject, session=session, term=term
                )
                stud_total += result["total"]
            students_scores[stud] = stud_total

        # Get student position
        position = self.get_student_position(student, students_scores)
        total_students = len(students_scores)

        # Get school with logo
        school = request.user.school

        return render(
            request,
            self.template_name,
            {
                "student": student,
                "session": session,
                "term": term,
                "subject_results": subject_results,
                "grand_total": grand_total,
                "total_possible": total_possible,
                "average": average,
                "percentage": percentage,
                "overall_grade": overall_grade,
                "overall_remark": overall_remark,
                "position": position,
                "total_students": total_students,
                "school": school,
                "subjects": subjects,
                "subject_count": subject_count,
            },
        )
