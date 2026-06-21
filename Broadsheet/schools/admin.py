from django.contrib import admin
from .models import School, Teacher, TeachingAssignment

# Register your models here.



admin.site.register(Teacher)
admin.site.register(TeachingAssignment)

class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "expiry_date")
    search_fields = ("name", "email")
    list_filter = ("created_at", "created_at")
admin.site.register(School, SchoolAdmin)
