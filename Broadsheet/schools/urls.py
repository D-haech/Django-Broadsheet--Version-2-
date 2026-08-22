from django.urls import path


from .views import (TeacherListView,TeacherCreateView, TeacherUpdateView, TeacherDeleteView, TeacherClassAssignView, TeacherAssignmentCreateView, TeacherAssignmentDeleteView, TeacherAssignmentListView, SchoolSettingsView, UploadLogoView)


#app_name = "schools"

urlpatterns = [
    path("teachers/", TeacherListView.as_view(), name="teacher_list"),
    path("teachers/create/", TeacherCreateView.as_view(), name="teacher_create"),
    path(
        "teachers/<int:pk>/update/", TeacherUpdateView.as_view(), name="teacher_update"
    ),
    path(
        "teachers/<int:pk>/delete/", TeacherDeleteView.as_view(), name="teacher_delete"
    ),
    path(
        "teachers/<int:pk>/classes/",
        TeacherClassAssignView.as_view(),
        name="teacher_class_assign",
    ),
    path(
        "teachers/<int:pk>/assignments/",
        TeacherAssignmentListView.as_view(),
        name="teacher_assignments",
    ),
    path(
        "teachers/<int:pk>/assignments/create/",
        TeacherAssignmentCreateView.as_view(),
        name="assignment_create",
    ),
    path(
        "assignments/<int:pk>/delete/",
        TeacherAssignmentDeleteView.as_view(),
        name="assignment_delete",
    ),
    path("settings/", SchoolSettingsView.as_view(), name="school_settings"),
    path("upload-logo/", UploadLogoView.as_view(), name="upload_logo"),
]



