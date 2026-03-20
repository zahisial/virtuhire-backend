# virtuhire-backend/candidates/models.py

from django.db import models
from accounts.models import User


class CandidateProfile(models.Model):
    CATEGORY_CHOICES = [
        ('admin-sales', 'Admin & Sales'),
        ('2d-design',   '2D Design'),
    ]
    WORK_PREF_CHOICES = [
        ('home',   'Home-Based'),
        ('office', 'Office-Based'),
    ]
    STATUS_CHOICES = [
        ('pending',  'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('update',   'Update Requested'),
    ]

    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    full_name       = models.CharField(max_length=200)
    phone           = models.CharField(max_length=20, blank=True)
    location        = models.CharField(max_length=200, blank=True)
    category        = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    work_preference = models.CharField(max_length=10, choices=WORK_PREF_CHOICES)
    experience      = models.TextField(blank=True)
    cv              = models.FileField(upload_to='candidates/cv/', blank=True, null=True)
    voice_intro     = models.FileField(upload_to='candidates/voice/', blank=True, null=True)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_featured     = models.BooleanField(default=False)
    is_priority     = models.BooleanField(default=False)
    rating          = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    skills          = models.JSONField(default=list, blank=True)
    admin_notes     = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.full_name} ({self.category})'

    @property
    def monthly_rate(self):
        rates = {
            ('admin-sales', 'home'):   2150,
            ('admin-sales', 'office'): 2700,
            ('2d-design',   'home'):   3200,
            ('2d-design',   'office'): 3600,
        }
        return rates.get((self.category, self.work_preference), 0)