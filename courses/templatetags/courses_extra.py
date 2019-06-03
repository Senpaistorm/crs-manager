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


@register.simple_tag
def getMark(assessment_id, c, user_id):
    a = Assessment.objects.get(pk=assessment_id)
    try:
        return float(a.grade_set.get(component=c, user_id=user_id).mark)
    except(Grade.DoesNotExist):
        return 0.0


@register.filter
def getTotalAverage(course_id, user_id):
    c = Course.objects.get(pk=course_id)
    return c.getTotalAverage(user_id)


@register.filter
def getWeightedAverage(course_id, user_id):
    c = Course.objects.get(pk=course_id)
    return c.getWeightedAverage(user_id)
