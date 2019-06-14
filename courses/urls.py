from django.urls import path, include

from . import views

app_name = "courses"
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:course_id>/set_grade/', views.set_grade, name='set_grade'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('add_course', views.add_course_view, name='add_course'),
    path('add_course_req/<int:course_id>/', views.add_course, name='add_course_req')
]
