from django.contrib import admin

from .models import Course, Assessment, Grade


class AssessmentInline(admin.TabularInline):
    model = Assessment
    extra = 3


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_code',
                    'start_date', 'validate_weight')
    fieldsets = [
        (None, {'fields': ['course_name', 'course_code']}),
        ('Date information', {'fields': ['start_date']}),
    ]
    inlines = [AssessmentInline]
    list_filter = ['start_date']
    search_fields = ['course_code']


admin.site.register(Course, CourseAdmin)
