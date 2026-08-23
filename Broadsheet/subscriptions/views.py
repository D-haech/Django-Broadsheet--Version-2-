from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string

from .models import SubscriptionPlan, SchoolRegistration, Payment
from schools.models import School
from accounts.models import User
from .forms import SchoolRegistrationForm, PaymentConfirmationForm

# Create your views here.


class PricingView(View):
    """
    Public pricing page showing all available plans.
    """

    template_name = "subscriptions/pricing.html"

    def get(self, request):
        plans = SubscriptionPlan.objects.filter(is_active=True)

        # Get the default plan to highlight
        default_plan = plans.filter(is_default=True).first()

        return render(
            request,
            self.template_name,
            {
                "plans": plans,
                "default_plan": default_plan,
            },
        )


class SchoolRegistrationView(View):
    """
    Public school registration form.
    """

    template_name = "subscriptions/register_school.html"

    def get(self, request):
        form = SchoolRegistrationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SchoolRegistrationForm(request.POST)

        if form.is_valid():
            # Get the selected plan
            plan = form.cleaned_data["plan"]

            # Create registration record
            registration = SchoolRegistration.objects.create(
                school_name=form.cleaned_data["school_name"],
                school_email=form.cleaned_data["school_email"],
                school_phone=form.cleaned_data["school_phone"],
                school_address=form.cleaned_data["school_address"],
                contact_name=form.cleaned_data["contact_name"],
                contact_email=form.cleaned_data["contact_email"],
                contact_phone=form.cleaned_data["contact_phone"],
                plan=plan,
                amount_due=plan.price,
                estimated_students=form.cleaned_data["estimated_students"],
                status="pending_payment",
            )

            # Redirect to payment instructions
            return redirect(
                "payment_instructions", reference=registration.reference
            )

        return render(request, self.template_name, {"form": form})


class RegistrationSuccessView(View):
    """
    Success page after registration.
    """

    template_name = "subscriptions/registration_success.html"

    def get(self, request, reference):
        registration = get_object_or_404(SchoolRegistration, reference=reference)

        return render(
            request,
            self.template_name,
            {
                "registration": registration,
            },
        )


class PaymentInstructionsView(View):
    """
    Show payment instructions with bank details.
    """

    template_name = "subscriptions/payment_instructions.html"

    def get(self, request, reference):
        registration = get_object_or_404(
            SchoolRegistration,
            reference=reference,
            status__in=["pending_payment", "payment_submitted"],
        )

        # Check if payment has already been submitted
        has_payment = Payment.objects.filter(registration=registration).exists()
        payment_status = None

        if has_payment:
            payment = Payment.objects.filter(registration=registration).latest(
                "created_at"
            )
            payment_status = payment.status

        # Get bank details from site configuration
        # For now, we'll use hardcoded values - you can move to a config model later
        bank_details = {
            "bank_name": "Zenith Bank",
            "account_name": "Class Sphere Ltd",
            "account_number": "1234567890",
        }

        return render(
            request,
            self.template_name,
            {
                "registration": registration,
                "bank_details": bank_details,
                "payment_status": payment_status,
            },
        )


class PaymentConfirmationView(View):
    """
    Submit payment evidence after making transfer.
    """

    template_name = "subscriptions/payment_confirmation.html"

    def get(self, request, reference):
        registration = get_object_or_404(
            SchoolRegistration,
            reference=reference,
            status__in=["pending_payment", "payment_submitted"],
        )

        # Check if payment already exists
        payment = Payment.objects.filter(registration=registration).first()

        # If payment exists and is pending, show pending page
        if payment and payment.status == "pending":
            return redirect("payment_pending", reference=reference)

        # If payment was rejected, show form again with rejection reason
        rejection_reason = None
        if payment and payment.status == "rejected":
            rejection_reason = payment.rejection_reason

        form = PaymentConfirmationForm()

        return render(
            request,
            self.template_name,
            {
                "registration": registration,
                "form": form,
                "rejection_reason": rejection_reason,
            },
        )

    def post(self, request, reference):
        registration = get_object_or_404(
            SchoolRegistration,
            reference=reference,
            status__in=["pending_payment", "payment_submitted"],
        )

        # Prevent duplicate submissions
        existing_payment = Payment.objects.filter(
            registration=registration, status="pending"
        ).first()

        if existing_payment:
            messages.warning(
                request, "You already have a payment pending verification."
            )
            return redirect("payment_pending", reference=reference)

        form = PaymentConfirmationForm(request.POST, request.FILES)

        if form.is_valid():
            # Create payment record
            payment = Payment.objects.create(
                registration=registration,
                amount=form.cleaned_data["amount"],
                payment_date=form.cleaned_data["payment_date"],
                bank_name=form.cleaned_data["bank_name"],
                transaction_reference=form.cleaned_data["transaction_reference"],
                payer_name=form.cleaned_data["payer_name"],
                proof=request.FILES.get("proof"),
                additional_note=form.cleaned_data.get("additional_note", ""),
                status="pending",
            )

            # Update registration status
            registration.status = "payment_submitted"
            registration.save()

            # Send email notification to admin
            self.send_admin_notification(registration, payment)

            # Redirect to pending page
            return redirect("payment_pending", reference=reference)

        return render(
            request,
            self.template_name,
            {
                "registration": registration,
                "form": form,
            },
        )

    def send_admin_notification(self, registration, payment):
        """
        Send email notification to platform admin.
        """
        try:
            admin_email = settings.ADMIN_EMAIL or "admin@classsphere.com"

            subject = f"New Payment Confirmation - {registration.school_name}"

            context = {
                "registration": registration,
                "payment": payment,
                "admin_url": settings.SITE_URL
                + reverse(
                    "admin_registration_detail", args=[registration.id]
                ),
            }

            html_message = render_to_string(
                "subscriptions/emails/admin_payment_notification.html", context
            )
            plain_message = f"""
New Payment Confirmation

School: {registration.school_name}
Reference: {registration.reference}
Amount: ₦{payment.amount}
Transaction: {payment.transaction_reference}

View: {settings.SITE_URL}{reverse('subscriptions:admin_registration_detail', args=[registration.id])}
"""

            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [admin_email],
                html_message=html_message,
                fail_silently=True,
            )
        except Exception as e:
            # Don't fail the request if email fails
            print(f"Failed to send admin notification: {e}")


class PaymentPendingView(View):
    """
    Show payment pending status page.
    """

    template_name = "subscriptions/payment_pending.html"

    def get(self, request, reference):
        registration = get_object_or_404(SchoolRegistration, reference=reference)
        payment = Payment.objects.filter(registration=registration).latest("created_at")

        return render(
            request,
            self.template_name,
            {
                "registration": registration,
                "payment": payment,
            },
        )
