import datetime

from django.db import models
from django.utils import timezone

class Course(models.Model):
    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=200)
    start_date = models.DateTimeField('course starting date')

    def __str__(self):
    	return self.course_code + ' ' + self.course_name

    def is_recent_course(self):
    	now = timezone.now()
    	return now - datetime.timedelta(days=120) <= self.start_date <= now


class Assessment(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	components = models.IntegerField(default=1)
	weight = models.IntegerField(default=0)

	def __str__(self):
		return (str)(self.components) + ' ' + self.name + ' worth total of ' + (str)(self.weight) + '%' + " for " + self.course.course_code

class Grade(models.Model):
	assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
	mark = models.DecimalField(decimal_places=2, max_digits=4)
