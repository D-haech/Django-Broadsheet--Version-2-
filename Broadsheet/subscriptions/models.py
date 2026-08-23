from django.db import models
from django.utils import timezone
from schools.models import School
from accounts.models import User

# Create your models here.


class SubscriptionPlan(models.Model):
    """
    Subscription plans available for schools.
    Admin can manage these from Django admin.
    """

    name = models.CharField(max_length=50, help_text="e.g., Basic, Standard, Premium")
    description = models.TextField(blank=True, help_text="Plan description")

    # Pricing
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, help_text="Price in Naira"
    )
    duration_days = models.PositiveIntegerField(
        default=90, help_text="Duration in days (e.g., 90 for term)"
    )

    # Limits
    student_limit = models.PositiveIntegerField(
        default=100, help_text="Maximum number of students allowed"
    )
    teacher_limit = models.PositiveIntegerField(
        default=10, help_text="Maximum number of teachers allowed"
    )

    # Features
    has_broadsheet = models.BooleanField(default=True)
    has_report_cards = models.BooleanField(default=True)
    has_analytics = models.BooleanField(default=False)

    # Status
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(
        default=False, help_text="Default plan shown on pricing page"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["price"]

    def __str__(self):
        return f"{self.name} - ₦{self.price} ({self.duration_days} days)"


class SchoolRegistration(models.Model):
    """
    Pending school registration before approval.
    """

    STATUS_CHOICES = (
        ("pending_payment", "Pending Payment"),
        ("payment_submitted", "Payment Submitted"),
        ("payment_verified", "Payment Verified"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("cancelled", "Cancelled"),
    )

    # Registration reference (e.g., REG-2026-000123)
    reference = models.CharField(max_length=20, unique=True, blank=True)

    # School information
    school_name = models.CharField(max_length=255)
    school_email = models.EmailField()
    school_phone = models.CharField(max_length=20)
    school_address = models.TextField()

    # Contact person
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)

    # Plan information (stored at time of registration)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_students = models.PositiveIntegerField(default=0)

    # Status
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending_payment"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Admin actions
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_registrations",
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_registrations",
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reference} - {self.school_name} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if not self.reference:
            # Generate reference: REG-2026-000001
            year = timezone.now().year
            last = SchoolRegistration.objects.filter(
                reference__startswith=f"REG-{year}"
            ).count()
            self.reference = f"REG-{year}-{str(last + 1).zfill(6)}"
        super().save(*args, **kwargs)

    def can_approve(self):
        """Check if registration can be approved."""
        return self.status == "payment_verified"

    def can_verify_payment(self):
        """Check if payment can be verified."""
        return self.status == "payment_submitted"


class Payment(models.Model):
    """
    Payment confirmation submitted by school.
    """

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("verified", "Verified"),
        ("rejected", "Rejected"),
    )

    registration = models.ForeignKey(
        SchoolRegistration, on_delete=models.CASCADE, related_name="payments"
    )

    # Payment reference (e.g., PAY-2026-000456)
    reference = models.CharField(max_length=20, unique=True, blank=True)

    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    bank_name = models.CharField(max_length=100)
    transaction_reference = models.CharField(max_length=100)
    payer_name = models.CharField(max_length=100)

    # Proof of payment
    proof = models.ImageField(upload_to="payment_proofs/", blank=True, null=True)
    additional_note = models.TextField(blank=True)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    # Admin actions
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_payments",
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reference} - {self.registration.school_name} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if not self.reference:
            # Generate reference: PAY-2026-000456
            year = timezone.now().year
            last = Payment.objects.filter(reference__startswith=f"PAY-{year}").count()
            self.reference = f"PAY-{year}-{str(last + 1).zfill(6)}"
        super().save(*args, **kwargs)


class Subscription(models.Model):
    """
    Active subscription for a school.
    """

    STATUS_CHOICES = (
        ("active", "Active"),
        ("expired", "Expired"),
        ("suspended", "Suspended"),
        ("cancelled", "Cancelled"),
    )

    school = models.OneToOneField(
        School, on_delete=models.CASCADE, related_name="subscription"
    )
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    payment = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subscriptions",
    )

    # Dates
    start_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField()

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.school.name} - {self.plan.name} ({self.get_status_display()})"

    def is_active(self):
        """Check if subscription is currently active."""
        if self.status != "active":
            return False
        if timezone.now() > self.expiry_date:
            self.status = "expired"
            self.save()
            return False
        return True

    def days_remaining(self):
        """Get number of days remaining until expiry."""
        delta = self.expiry_date - timezone.now()
        return max(0, delta.days)
