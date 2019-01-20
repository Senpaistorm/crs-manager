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

	def validate_weight(self):
		weight = 0.0
		assessments = Assessment.objects.filter(course=self)
		for assessment in assessments:
			weight += float(assessment.weight)
		return (weight == 100.0)


class Assessment(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	components = models.IntegerField(default=1)
	weight = models.DecimalField(decimal_places=2,max_digits=4)

	def __str__(self):
		return (str)(self.components) + ' ' + self.name + ' worth total of ' + (str)(self.weight) + '%' + " for " + self.course.course_code

class Grade(models.Model):
	assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
	mark = models.DecimalField(decimal_places=2, max_digits=4)
	component = models.IntegerField(default=1)

	def __str__(self):
		return self.assessment.__str__() + (str)(self.component) +  " " + (str)(self.mark) + "%"