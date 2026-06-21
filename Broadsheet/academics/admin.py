from django.contrib import admin
from .models import SchoolClass, Session,Student,Subject,Term
# Register your models here.

admin.site.register(SchoolClass)
admin.site.register(Session)
admin.site.register(Subject)
admin.site.register(Term)


class StudentAdmin(admin.ModelAdmin):
    list_display = ("surname", "first_name", "date_of_birth", "gender")
    search_fields = ("surname", "firstname")
    

admin.site.register(Student, StudentAdmin)