# imports
from django.shortcuts import render
from django.utils import timezone

from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from decimal import Decimal
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from.models import Course, Assessment, Grade, UserCourse

@login_required(login_url='/accounts/login/')
def index(request):
    courses = UserCourse.objects.filter(user=request.user)

    context = {
        'course_list' : courses,
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
                g = a.grade_set.get(component=i, user_id=request.user.id)
                g.mark = mark
                g.save()
            except(Grade.DoesNotExist):
                a.grade_set.create(user_id=request.user.id, mark=mark, component=i)
    # go back to course detail page
    return HttpResponseRedirect(reverse('courses:detail', args=(course.id,)))

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def add_course_view(request):
    # get a list of courses that the user is taking
    cur_courses = UserCourse.objects.filter(user__pk=request.user.id).values('course')
    # exclude the list of courses
    courses = Course.objects.exclude(pk__in=cur_courses)
    
    context = {
        'course_list' : courses,
    }
    return render(request, 'courses/add_course.html', context=context)

@login_required(login_url='/accounts/login/')
def add_course(request, course_id):
    crs = Course.objects.get(pk=course_id)
    newUC = UserCourse(user=request.user, course=crs)
    newUC.save()
    return redirect('/courses/add_course')

def drop_course_view(request):
    # get a list of courses that the user is taking
    cur_courses = UserCourse.objects.filter(user__pk=request.user.id, is_current=True).values('course')
    # exclude the list of courses
    courses = Course.objects.filter(pk__in=cur_courses)
    
    context = {
        'course_list' : courses,
    }
    return render(request, 'courses/drop_course.html', context=context)

@login_required(login_url='/accounts/login/')
def drop_course(request, course_id):
    crs = Course.objects.get(pk=course_id)
    newUC = UserCourse.objects.get(user=request.user, course=crs)
    newUC.delete()
    return redirect('/courses/drop_course')

@login_required(login_url='/accounts/login/')
def complete_course_req(request, course_id):
    crs = Course.objects.get(pk=course_id)
    userCrs = UserCourse.objects.get(user=request.user, course=crs)
    userCrs.is_current = False
    userCrs.save()
    return redirect('/courses/')