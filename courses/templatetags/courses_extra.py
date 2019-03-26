from django import template
from courses.models import Course, Assessment, Grade

register = template.Library()


@register.filter
def filter_range(start, end):
    return range(start, end+1)


@register.filter
def mult(value, arg):
    "Multiplies the arg and the value"
    return int(value) * int(arg)


@register.filter
def sub(value, arg):
    "Subtracts the arg from the value"
    return int(value) - int(arg)


@register.filter
def div(value, arg):
    "Divides the value by the arg"
    return int(value) / int(arg)


@register.filter
def getMark(assessment_id, c):
    a = Assessment.objects.get(pk=assessment_id)
    try:
        return float(a.grade_set.get(component=c).mark)
    except(Grade.DoesNotExist):
        return 0.0


@register.filter
def getTotalAverage(course_id):
    c = Course.objects.get(pk=course_id)
    return c.getTotalAverage()


@register.filter
def getWeightedAverage(course_id):
    c = Course.objects.get(pk=course_id)
    return c.getWeightedAverage()
