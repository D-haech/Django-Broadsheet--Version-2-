from django.contrib import admin
from .models import AssessmentType, Assessment, StudentScore
from .models import AssessmentType, Assessment, StudentScore, GradeSystem, Grade

# Register your models here.


admin.site.register(StudentScore)



class GradeInline(admin.TabularInline):
    model = Grade
    extra = 6  # Show 6 empty grade rows
    fields = ['grade', 'min_score', 'max_score', 'remark', 'points', 'position']
    ordering = ['position']

@admin.register(GradeSystem)
class GradeSystemAdmin(admin.ModelAdmin):
    list_display = ['name', 'school', 'is_active', 'created_at']
    list_filter = ['school', 'is_active']
    search_fields = ['name']
    inlines = [GradeInline]

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['grade_system', 'grade', 'min_score', 'max_score', 'remark', 'points']
    list_filter = ['grade_system__school', 'grade_system']
    search_fields = ['grade', 'remark']