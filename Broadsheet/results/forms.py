from django import forms

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
