# virtuhire-backend/candidates/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('apply/',          views.apply,            name='candidate-apply'),
    path('browse/',         views.browse,           name='candidate-browse'),
    path('<int:pk>/',       views.candidate_detail, name='candidate-detail'),
    path('my-application/', views.my_application,   name='my-application'),
]