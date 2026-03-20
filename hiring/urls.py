# virtuhire-backend/hiring/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('requests/',                                                      views.hiring_requests,   name='hiring-requests'),
    path('requests/<int:hiring_request_id>/shortlist/',                    views.shortlist,         name='shortlist'),
    path('requests/<int:hiring_request_id>/shortlist/<int:candidate_id>/', views.remove_shortlist,  name='remove-shortlist'),
    path('requests/<int:hiring_request_id>/interview/',                    views.request_interview, name='request-interview'),
    path('requests/<int:hiring_request_id>/confirm/',                      views.confirm_hire,      name='confirm-hire'),
    path('employees/',                                                     views.my_employees,      name='my-employees'),
]