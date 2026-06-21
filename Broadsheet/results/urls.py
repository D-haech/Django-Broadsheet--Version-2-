from django.urls import path

from .views import (
    AssessmentTypeListView,
    AssessmentTypeCreateView,
    AssessmentTypeUpdateView,
    AssessmentTypeDeleteView,
    AssessmentCreateView,
    AssessmentDeleteView,
    AssessmentListView,
    AssessmentUpdateView,
)

urlpatterns = [
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
]
