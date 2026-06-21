from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

class SchoolAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):

        if request.user.role != "school_admin":
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class TeacherRequiredMixin:

    def dispatch(self, request, *args, **kwargs):

        if request.user.role != "teacher":
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)
