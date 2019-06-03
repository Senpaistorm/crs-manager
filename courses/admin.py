from django.contrib import admin

from .models import Course, Assessment, Grade, UserCourse

class AssessmentInline(admin.TabularInline):
    model = Assessment
    extra = 3


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_code',
                    'validate_weight')
    fieldsets = [
        (None, {'fields': ['course_name', 'course_code']}),
    ]
    inlines = [AssessmentInline]
    search_fields = ['course_code']

admin.site.register(UserCourse)
admin.site.register(Course, CourseAdmin)
admin.site.register(Grade)

from django.contrib.admin.sites import AdminSite

from django.contrib.auth.forms import AuthenticationForm

class BasicAdminSite(AdminSite):
    login_form = AuthenticationForm

    def has_permission(self, request):

        return True


basic_admin_site = BasicAdminSite(name='basic_admin')