from django.urls import path


from .views import (
    AssessmentTypeListView,
    AssessmentTypeCreateView,
    AssessmentTypeUpdateView,
    AssessmentTypeDeleteView,
    AssessmentListView,
    AssessmentCreateView,
    AssessmentUpdateView,
    AssessmentDeleteView,
    TeacherSubjectListView,
    BulkScoreEntryView,
    AdminScoreEntryView,
    SummaryBroadsheetView,
    SummaryBroadsheetView,
    CompleteBroadsheetView,
)

urlpatterns = [
    # =========================
    # Assessment Types
    # =========================
    path(
        "assessment-types/",
        AssessmentTypeListView.as_view(),
        name="assessment_type_list",
    ),
    path(
        "assessment-types/create/",
        AssessmentTypeCreateView.as_view(),
        name="assessment_type_create",
    ),
    path(
        "assessment-types/<int:pk>/update/",
        AssessmentTypeUpdateView.as_view(),
        name="assessment_type_update",
    ),
    path(
        "assessment-types/<int:pk>/delete/",
        AssessmentTypeDeleteView.as_view(),
        name="assessment_type_delete",
    ),
    # =========================
    # Assessments
    # =========================
    path(
        "assessments/",
        AssessmentListView.as_view(),
        name="assessment_list",
    ),
    path(
        "assessments/create/",
        AssessmentCreateView.as_view(),
        name="assessment_create",
    ),
    path(
        "assessments/<int:pk>/update/",
        AssessmentUpdateView.as_view(),
        name="assessment_update",
    ),
    path(
        "assessments/<int:pk>/delete/",
        AssessmentDeleteView.as_view(),
        name="assessment_delete",
    ),
    # =========================
    # Teacher Score Entry
    # =========================
    path(
        "my-subjects/",
        TeacherSubjectListView.as_view(),
        name="teacher_subjects",
    ),
    path(
        "score-entry/<int:assignment_id>/",
        BulkScoreEntryView.as_view(),
        name="bulk_score_entry",
    ),
    path("admin-score-entry/", AdminScoreEntryView.as_view(), name="admin_score_entry"),
    path(
        "summary-broadsheet/",
        SummaryBroadsheetView.as_view(),
        name="summary_broadsheet",
    ),
    path(
        "complete-broadsheet/",
        CompleteBroadsheetView.as_view(),
        name="complete_broadsheet",
    ),
]
