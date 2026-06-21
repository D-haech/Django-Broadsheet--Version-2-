from django import forms
from .models import SchoolClass, Student, Subject, Session, Term


class SchoolClassForm(forms.ModelForm):

    class Meta:
        model = SchoolClass
        fields = ["name"]


class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = ["name"]


class StudentForm(forms.ModelForm):

    class Meta:

        model = Student

        fields = [
            "surname",
            "first_name",
            "mid_name",
            "admission_no",
            "gender",
            "date_of_birth",
            "student_class",
            "passport",
            "is_active",
        ]

        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):

        school = kwargs.pop("school")

        super().__init__(*args, **kwargs)

        self.fields["student_class"].queryset = SchoolClass.objects.filter(
            school=school
        )


# Sessions form


class SessionForm(forms.ModelForm):

    class Meta:

        model = Session

        fields = [
            "name",
            "is_current",
        ]


# Term Form

class TermForm(forms.ModelForm):

    class Meta:

        model = Term

        fields = [
            "session",
            "name",
            "is_current",
        ]

    def __init__(self, *args, **kwargs):

        school = kwargs.pop("school")

        super().__init__(*args, **kwargs)

        self.fields["session"].queryset = Session.objects.filter(school=school)
