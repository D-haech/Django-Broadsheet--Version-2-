# schools/decorators.py
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from functools import wraps


def school_admin_required(function=None):
    """
    Decorator for views that checks if the user is a school admin.
    Works with both function-based and class-based views.
    """

    def check_user(user):
        return (
            user.is_authenticated
            and hasattr(user, "role")
            and user.role == "school_admin"
        )

    actual_decorator = user_passes_test(
        check_user,
        login_url="login",  # Redirect to login if not authenticated
        redirect_field_name="next",
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


class SchoolAdminRequiredMixin:
    """
    Mixin for class-based views that requires the user to be a school admin.
    Use this instead of the decorator for class-based views.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not hasattr(request.user, "role") or request.user.role != "school_admin":
            raise PermissionDenied(
                "You must be a school administrator to access this page."
            )

        return super().dispatch(request, *args, **kwargs)
