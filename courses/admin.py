from django.contrib import admin
from .models import Course, Assessment,Grade

admin.site.register(Course)

admin.site.register(Assessment)

admin.site.register(Grade)