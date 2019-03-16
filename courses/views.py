# imports
from django.shortcuts import render
from django.utils import timezone

from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views import generic
from decimal import Decimal
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from.models import Course, Assessment, Grade, UserCourse

@login_required(login_url='/accounts/login/')
def index(request):
    courses = UserCourse.objects.filter(user=request.user)

    context = {
        'course_list' : courses
    }

    return render(request, 'courses/index.html', context=context)

# generic DetailView for detail.html
class DetailView(generic.DetailView):
    model = Course
    template_name = 'courses/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Course.objects

@login_required(login_url='/accounts/login/')
def set_grade(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    assessments = Assessment.objects.filter(course=course)
    # loop through assessments and update changed grades
    for assessment in assessments:
        for i in range(1, assessment.components+1):
            mark = request.POST[(str)(assessment.id) + "_" + (str)(i)]
            mark = Decimal.from_float((float)(mark))
            a = Assessment.objects.get(pk=assessment.id)
            try:
                g = a.grade_set.get(component=i)
                g.mark = mark
                g.save()
            except(Grade.DoesNotExist):
                a.grade_set.create(user_id=request.user.id, mark=mark, component=i)
    # go back to course detail page
    return HttpResponseRedirect(reverse('courses:detail', args=(course.id,)))
