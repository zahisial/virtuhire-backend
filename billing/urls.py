# virtuhire-backend/billing/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('invoices/',              views.invoices,              name='invoices'),
    path('payments/',              views.payments,              name='payments'),
    path('create-payment-intent/', views.create_payment_intent, name='create-payment-intent'),
    path('webhook/',               views.stripe_webhook,        name='stripe-webhook'),
]