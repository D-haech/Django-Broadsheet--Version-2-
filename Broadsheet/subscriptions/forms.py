from django import forms
from .models import SubscriptionPlan


class SchoolRegistrationForm(forms.Form):
    """
    Form for school registration.
    """

    # School Information
    school_name = forms.CharField(
        max_length=255,
        label="School Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g., Silver and Bronze Educational Centre",
            }
        ),
    )
    school_email = forms.EmailField(
        label="School Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "school@example.com"}
        ),
    )
    school_phone = forms.CharField(
        max_length=20,
        label="School Phone",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "08012345678"}
        ),
    )
    school_address = forms.CharField(
        label="School Address",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Enter full school address",
            }
        ),
    )

    # Contact Person
    contact_name = forms.CharField(
        max_length=100,
        label="Contact Person Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Full name of contact person",
            }
        ),
    )
    contact_email = forms.EmailField(
        label="Contact Person Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "contact@example.com"}
        ),
    )
    contact_phone = forms.CharField(
        max_length=20,
        label="Contact Person Phone",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "08012345678"}
        ),
    )

    # Plan Selection
    plan = forms.ModelChoiceField(
        queryset=SubscriptionPlan.objects.filter(is_active=True),
        label="Select Plan",
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        empty_label=None,
    )

    estimated_students = forms.IntegerField(
        label="Estimated Number of Students",
        min_value=1,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "e.g., 100"}
        ),
    )

    # Password
    password = forms.CharField(
        label="Create Admin Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Choose a strong password"}
        ),
        help_text="This will be used to login as your school's administrator",
        min_length=8,
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Re-enter your password"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class PaymentConfirmationForm(forms.Form):
    """
    Form for submitting payment confirmation.
    """

    amount = forms.DecimalField(
        label="Amount Paid",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "e.g., 5000.00"}
        ),
    )
    payment_date = forms.DateField(
        label="Payment Date",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    bank_name = forms.CharField(
        max_length=100,
        label="Bank Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "e.g., Zenith Bank"}
        ),
    )
    transaction_reference = forms.CharField(
        max_length=100,
        label="Transaction Reference",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "e.g., T123456789"}
        ),
    )
    payer_name = forms.CharField(
        max_length=100,
        label="Payer Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Name on the payment"}
        ),
    )
    proof = forms.ImageField(
        label="Payment Screenshot/Evidence",
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control", "accept": "image/*"}),
    )
    additional_note = forms.CharField(
        label="Additional Note (Optional)",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Any additional information...",
            }
        ),
    )
