# virtuhire-backend/billing/models.py

from django.db import models
from accounts.models import ClientProfile


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('pending',  'Pending'),
        ('paid',     'Paid'),
        ('overdue',  'Overdue'),
        ('refunded', 'Refunded'),
    ]

    client            = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='invoices')
    invoice_number    = models.CharField(max_length=20, unique=True)
    amount            = models.PositiveIntegerField()
    status            = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description       = models.TextField(blank=True)
    stripe_invoice_id = models.CharField(max_length=100, blank=True)
    pdf_url           = models.URLField(blank=True)
    due_date          = models.DateField()
    paid_at           = models.DateTimeField(null=True, blank=True)
    created_at        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.invoice_number} — {self.client} — {self.amount} AED'


class Payment(models.Model):
    TYPE_CHOICES = [
        ('hiring_fee',  'Hiring Fee'),
        ('monthly',     'Monthly Billing'),
        ('extra_batch', 'Extra Candidate Batch'),
        ('buyout',      'Employee Buyout'),
        ('balance',     'First Month Balance'),
    ]
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('succeeded', 'Succeeded'),
        ('failed',    'Failed'),
        ('refunded',  'Refunded'),
    ]

    client                   = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='payments')
    invoice                  = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)
    amount                   = models.PositiveIntegerField()
    payment_type             = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status                   = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True)
    created_at               = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client} — {self.payment_type} — {self.amount} AED ({self.status})'