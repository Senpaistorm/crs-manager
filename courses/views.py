from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views import generic


class IndexView(generic.ListView):
	template_name = 'courses/index.html'
	context_object_name = 'latest_question_list'
