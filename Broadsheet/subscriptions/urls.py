from django.urls import path
from . import views



urlpatterns = [
    # Public Pages
    path("pricing/", views.PricingView.as_view(), name="pricing"),
    path(
        "register-school/",
        views.SchoolRegistrationView.as_view(),
        name="register_school",
    ),
    path(
        "registration-success/<str:reference>/",
        views.RegistrationSuccessView.as_view(),
        name="registration_success",
    ),
    path(
        "payment/<str:reference>/",
        views.PaymentInstructionsView.as_view(),
        name="payment_instructions",
    ),
    path(
        "payment-confirmation/<str:reference>/",
        views.PaymentConfirmationView.as_view(),
        name="payment_confirmation",
    ),
    path(
        "payment-pending/<str:reference>/",
        views.PaymentPendingView.as_view(),
        name="payment_pending",
    ),
]
