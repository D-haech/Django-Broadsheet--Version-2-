from django.urls import path
from .views import (SubjectListView, SubjectCreateView, SubjectUpdateView, SubjectDeleteView, SchoolClassListView,
    SchoolClassCreateView,
    SchoolClassUpdateView,
    SchoolClassDeleteView, 
    StudentDeleteView, 
    StudentListView, 
    StudentUpdateView, 
    StudentCreateView,
    SessionCreateView, 
    SessionListView, 
    SessionUpdateView, 
    SessionDeleteView, 
    TermCreateView, 
    TermDeleteView, 
    TermUpdateView, 
    TermListView)

urlpatterns = [
    path("classes/", SchoolClassListView.as_view(), name="class_list"),
    path("classes/create/", SchoolClassCreateView.as_view(), name="class_create"),
    path(
        "classes/<int:pk>/update/", SchoolClassUpdateView.as_view(), name="class_update"
    ),
    path(
        "classes/<int:pk>/delete/", SchoolClassDeleteView.as_view(), name="class_delete"
    ),
    path("subjects/", SubjectListView.as_view(), name="subject_list"),
    path("subjects/create/", SubjectCreateView.as_view(), name="subject_create"),
    path(
        "subjects/<int:pk>/update/", SubjectUpdateView.as_view(), name="subject_update"
    ),
    path(
        "subjects/<int:pk>/delete/", SubjectDeleteView.as_view(), name="subject_delete"
    ),
    path("students/", StudentListView.as_view(), name="student_list"),
    path("students/create/", StudentCreateView.as_view(), name="student_create"),
    path(
        "students/<int:pk>/update/", StudentUpdateView.as_view(), name="student_update"
    ),
    path(
        "students/<int:pk>/delete/", StudentDeleteView.as_view(), name="student_delete"
    ),
    path("sessions/", SessionListView.as_view(), name="session_list"),
    path("sessions/create/", SessionCreateView.as_view(), name="session_create"),
    path(
        "sessions/<int:pk>/update/", SessionUpdateView.as_view(), name="session_update"
    ),
    path(
        "sessions/<int:pk>/delete/", SessionDeleteView.as_view(), name="session_delete"
    ),
    path("terms/", TermListView.as_view(), name="term_list"),
    path("terms/create/", TermCreateView.as_view(), name="term_create"),
    path("terms/<int:pk>/update/", TermUpdateView.as_view(), name="term_update"),
    path("terms/<int:pk>/delete/", TermDeleteView.as_view(), name="term_delete"),
]
