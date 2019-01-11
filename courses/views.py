from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views import generic

from.models import Course,Assessment

class IndexView(generic.ListView):
    template_name = 'courses/index.html'
    context_object_name = 'latest_course_list'

    def get_queryset(self):
        return Course.objects.filter(
            start_date__lte=timezone.now()
        ).order_by('-start_date')[:5]

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['past_course_list'] = Course.objects.filter(start_date__lte=timezone.now()).order_by('-start_date')[5:]
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