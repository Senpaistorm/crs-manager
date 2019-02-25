import datetime

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

class Course(models.Model):
    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=200)

    def __str__(self):
        return self.course_code + ' ' + self.course_name

    def validate_weight(self):
        weight = 0.0
        assessments = Assessment.objects.filter(course=self)
        for assessment in assessments:
            weight += float(assessment.weight)
        return (weight == 100.0)

    def getTotalAverage(self):
        """
        Calculate total accumulated average, including incomplete assessments,
        calculated out of 100%.
        """
        if not Course.validate_weight(self):
            return 0.0
        mark = 0.0
        assessments = Assessment.objects.filter(course=self)
        for asm in assessments:
            grades = Grade.objects.filter(assessment=asm)
            weight = asm.weight/asm.components
            for grade in grades:
                mark += float(grade.mark) * float(weight) / 100
        return mark

    def getWeightedAverage(self):
        """
        Calculate weighted average of all completed assessments
        Assumption: completed assessments have a mark greater than 0
        """
        if not Course.validate_weight(self):
            return 0.0
        mark = 0.0
        availableMark = 0.0
        assessments = Assessment.objects.filter(course=self)
        for asm in assessments:
            grades = Grade.objects.filter(assessment=asm)
            weight = asm.weight/asm.components
            for grade in grades:
                if grade.mark > 0:
                    availableMark += float(weight)
                mark += (float(grade.mark)/100) * float(weight)
        if not availableMark: return 0
        return mark/availableMark * 100

class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_current = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username + ' is taking ' + self.course.course_name

class Assessment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    components = models.IntegerField(default=1)
    weight = models.DecimalField(decimal_places=2, max_digits=4)

    def __str__(self):
        return (str)(self.components) + ' ' + self.name + ' worth total of '
        + (str)(self.weight) + '%' + " for " + self.course.course_code


class Grade(models.Model):
    user_id = models.IntegerField(default=1)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    mark = models.FloatField(default=0.0)
    component = models.IntegerField(default=1)

    def __str__(self):
        return self.assessment.__str__() + (str)(self.component)
        + " " + (str)(self.mark) + "%"
