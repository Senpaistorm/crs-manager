from django.urls import path, include

from . import views


app_name = "courses"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('login/', views.login_view, name='login'),
    path('<int:course_id>/set_grade/', views.set_grade, name='set_grade'),
    path('accounts/', include('django.contrib.auth.urls')),
]
