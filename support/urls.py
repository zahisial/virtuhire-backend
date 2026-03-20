# virtuhire-backend/support/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('tickets/',          views.tickets,       name='tickets'),
    path('tickets/<int:pk>/', views.ticket_detail, name='ticket-detail'),
]