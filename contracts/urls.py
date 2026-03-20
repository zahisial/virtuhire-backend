# virtuhire-backend/contracts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('sign/', views.sign_contract, name='sign-contract'),
    path('mine/', views.my_contracts,  name='my-contracts'),
]