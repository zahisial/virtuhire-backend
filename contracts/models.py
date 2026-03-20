# virtuhire-backend/contracts/models.py

from django.db import models
from accounts.models import ClientProfile


class Contract(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Signature'),
        ('signed',  'Signed'),
    ]
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ar', 'Arabic'),
    ]

    client    = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='contracts')
    status    = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    language  = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    signature = models.ImageField(upload_to='contracts/signatures/', null=True, blank=True)
    pdf_file  = models.FileField(upload_to='contracts/pdf/', null=True, blank=True)
    agreed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Contract — {self.client} ({self.status})'