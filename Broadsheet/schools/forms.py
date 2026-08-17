from django import forms
from .models import Teacher, TeachingAssignment
from academics.models import SchoolClass, Subject
from accounts.models import User

class TeacherCreateForm(forms.Form):

    username = forms.CharField()

    password = forms.CharField(widget=forms.PasswordInput)

    first_name = forms.CharField()

    last_name = forms.CharField()

    email = forms.EmailField()

    phone = forms.CharField(required=False)

    address = forms.CharField(widget=forms.Textarea, required=False)

    date_employed = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )

    def clean_username(self):

        username = self.cleaned_data["username"]

        if User.objects.filter(
            username=username
        ).exists():

            raise forms.ValidationError(
                "Username already exists."
            )

        return username
    def clean_email(self):

        email = self.cleaned_data["email"]

        if User.objects.filter(
            email=email
        ).exists():

            raise forms.ValidationError(
                "Email already exists."
            )

        return email

class TeacherForm(forms.ModelForm):

    class Meta:

        model = Teacher

        fields = [
            "phone",
            "address",
            "date_employed",
        ]


class TeacherUpdateForm(forms.ModelForm):

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:

        model = Teacher

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "date_employed",
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["first_name"].initial = self.instance.user.first_name
        self.fields["last_name"].initial = self.instance.user.last_name
        self.fields["email"].initial = self.instance.user.email

    def save(self, commit=True):

        teacher = super().save(commit=False)

        user = teacher.user

        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        user.save()

        if commit:
            teacher.save()

        return teacher


class TeacherClassForm(forms.ModelForm):

    classes = forms.ModelMultipleChoiceField(
        queryset=SchoolClass.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:

        model = Teacher

        fields = ["classes"]

    def __init__(self, *args, **kwargs):

        school = kwargs.pop("school")

        super().__init__(*args, **kwargs)

        self.fields["classes"].queryset = SchoolClass.objects.filter(school=school)


class TeachingAssignmentForm(forms.ModelForm):

    class Meta:

        model = TeachingAssignment

        fields = [
            "school_class",
            "subject",
        ]

    
    def __init__(self, *args, **kwargs):

        self.school = kwargs.pop("school")

        super().__init__(*args, **kwargs)

        self.fields["school_class"].queryset = (
            SchoolClass.objects.filter(
                school=self.school
            )
        )

        self.fields["subject"].queryset = (
            Subject.objects.filter(
                school=self.school
            )
        )

    def clean(self):

        cleaned_data = super().clean()

        school_class = cleaned_data.get("school_class")

        subject = cleaned_data.get("subject")

        teacher = getattr(self, "teacher", None)

        if (
            teacher
            and school_class
            and subject
        ):

            if TeachingAssignment.objects.filter(
                teacher=teacher,
                school_class=school_class,
                subject=subject,
            ).exists():

                raise forms.ValidationError(
                    "This assignment already exists."
                )

        return cleaned_data
