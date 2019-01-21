import logging
from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views import generic

from.models import Course, Assessment, Grade
logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    template_name = 'courses/index.html'
    context_object_name = 'latest_course_list'

    def get_queryset(self):
        return Course.objects.filter(
            start_date__lte=timezone.now()
        ).order_by('-start_date')[:5]

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['past_course_list'] = Course.objects.filter(
            start_date__lte=timezone.now()).order_by('-start_date')[5:]
        return data


class DetailView(generic.DetailView):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'polls/detail.html', {'question': question})
    model = Course
    template_name = 'courses/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Course.objects.filter(start_date__lte=timezone.now())


def set_grade(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    assessments = Assessment.objects.filter(course=course)
    for assessment in assessments:
        print(assessment.id)
        for i in range(1, assessment.components+1):
            mark = request.POST[(str)(assessment.id) + "_" + (str)(i)]
            a = Assessment.objects.get(pk=assessment.id)
            print(mark)
            try:
                g = a.grade_set.get(component=i)
                g.mark = mark
                g.save()
            except(Grade.DoesNotExist):
                a.grade_set.create(mark=mark, component=i)
    # go back to course detail page
    return HttpResponseRedirect(reverse('courses:detail', args=(course.id,)))
