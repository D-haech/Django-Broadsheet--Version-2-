from django import forms
from .models import GradeSystem, Grade
from .models import AssessmentType, Assessment
from django import forms


class AssessmentTypeForm(forms.ModelForm):

    class Meta:

        model = AssessmentType

        fields = [
            "name",
            "maximum_score",
        ]


class AssessmentForm(forms.ModelForm):

    class Meta:

        model = Assessment

        fields = [
            "assessment_type",
            "name",
            "maximum_score",
        ]

    def __init__(self, *args, **kwargs):

        school = kwargs.pop("school")

        super().__init__(*args, **kwargs)

        self.fields["assessment_type"].queryset = self.fields[
            "assessment_type"
        ].queryset.filter(school=school)


class BulkScoreEntryForm(forms.Form):

    subject = forms.IntegerField(widget=forms.HiddenInput)

    term = forms.IntegerField(widget=forms.HiddenInput)

    assessment = forms.IntegerField(widget=forms.HiddenInput)



class GradeSystemForm(forms.ModelForm):
    class Meta:
        model = GradeSystem
        fields = ["name", "is_active"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g., Primary Grading"}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        self.school = kwargs.pop("school", None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if (
            self.school
            and GradeSystem.objects.filter(school=self.school, name=name)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError(
                "A grading system with this name already exists for your school."
            )
        return name


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ["grade", "min_score", "max_score", "remark", "points", "position"]
        widgets = {
            "grade": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "A"}
            ),
            "min_score": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "max_score": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "remark": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Excellent"}
            ),
            "points": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
            "position": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.system_pk = kwargs.pop("system_pk", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        min_score = cleaned_data.get("min_score")
        max_score = cleaned_data.get("max_score")

        if min_score is not None and max_score is not None:
            if min_score >= max_score:
                raise forms.ValidationError(
                    "Minimum score must be less than maximum score."
                )

        # Check for overlapping grade ranges
        if self.system_pk:
            grade_system = GradeSystem.objects.get(id=self.system_pk)
            existing_grades = Grade.objects.filter(grade_system=grade_system).exclude(
                pk=self.instance.pk
            )

            for existing in existing_grades:
                if min_score <= existing.max_score and max_score >= existing.min_score:
                    raise forms.ValidationError(
                        f"This score range overlaps with existing grade '{existing.grade}' "
                        f"({existing.min_score} - {existing.max_score})"
                    )

        return cleaned_data
