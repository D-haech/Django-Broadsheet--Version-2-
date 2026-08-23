from django.contrib import admin
from .models import SubscriptionPlan, SchoolRegistration, Payment, Subscription

# Register your models here.


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price",
        "duration_days",
        "student_limit",
        "is_active",
        "is_default",
    ]
    list_filter = ["is_active", "is_default"]
    search_fields = ["name", "description"]
    fieldsets = (
        (
            "Plan Information",
            {"fields": ("name", "description", "is_active", "is_default")},
        ),
        ("Pricing & Duration", {"fields": ("price", "duration_days")}),
        ("Limits", {"fields": ("student_limit", "teacher_limit")}),
        (
            "Features",
            {"fields": ("has_broadsheet", "has_report_cards", "has_analytics")},
        ),
    )


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    fields = ["reference", "amount", "transaction_reference", "status", "created_at"]
    readonly_fields = ["reference", "created_at"]


@admin.register(SchoolRegistration)
class SchoolRegistrationAdmin(admin.ModelAdmin):
    list_display = [
        "reference",
        "school_name",
        "plan",
        "amount_due",
        "status",
        "created_at",
    ]
    list_filter = ["status", "plan", "created_at"]
    search_fields = ["reference", "school_name", "contact_name", "contact_email"]
    readonly_fields = ["reference", "created_at", "updated_at"]
    inlines = [PaymentInline]
    fieldsets = (
        ("Registration Information", {"fields": ("reference", "status", "created_at")}),
        (
            "School Information",
            {
                "fields": (
                    "school_name",
                    "school_email",
                    "school_phone",
                    "school_address",
                )
            },
        ),
        (
            "Contact Person",
            {"fields": ("contact_name", "contact_email", "contact_phone")},
        ),
        ("Plan & Payment", {"fields": ("plan", "amount_due", "estimated_students")}),
        (
            "Admin Actions",
            {
                "fields": (
                    "verified_by",
                    "verified_at",
                    "approved_by",
                    "approved_at",
                    "rejection_reason",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "reference",
        "registration",
        "amount",
        "transaction_reference",
        "status",
        "created_at",
    ]
    list_filter = ["status", "created_at"]
    search_fields = [
        "reference",
        "transaction_reference",
        "payer_name",
        "registration__reference",
    ]
    readonly_fields = ["reference", "created_at"]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        "school",
        "plan",
        "start_date",
        "expiry_date",
        "status",
        "is_active",
    ]
    list_filter = ["status", "plan"]
    search_fields = ["school__name", "school__email"]
    readonly_fields = ["created_at"]
