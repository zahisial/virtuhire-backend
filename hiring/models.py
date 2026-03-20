# virtuhire-backend/hiring/models.py

from django.db import models
from accounts.models import ClientProfile
from candidates.models import CandidateProfile


class HiringRequest(models.Model):
    CATEGORY_CHOICES = [
        ('admin-sales', 'Admin & Sales'),
        ('2d-design',   '2D Design'),
    ]
    WORK_TYPE_CHOICES = [
        ('home',   'Home-Based'),
        ('office', 'Office-Based'),
    ]
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('active',    'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    client          = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='hiring_requests')
    category        = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    work_type       = models.CharField(max_length=10, choices=WORK_TYPE_CHOICES)
    employee_count  = models.PositiveIntegerField(default=1)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    hiring_fee_paid = models.BooleanField(default=False)
    batches_used    = models.PositiveIntegerField(default=1)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.client} — {self.category} x{self.employee_count}'


class Shortlist(models.Model):
    hiring_request = models.ForeignKey(HiringRequest, on_delete=models.CASCADE, related_name='shortlists')
    candidate      = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('hiring_request', 'candidate')

    def __str__(self):
        return f'{self.hiring_request} → {self.candidate}'


class InterviewRequest(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    hiring_request = models.ForeignKey(HiringRequest, on_delete=models.CASCADE, related_name='interviews')
    candidate      = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    scheduled_at   = models.DateTimeField(null=True, blank=True)
    notes          = models.TextField(blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Interview: {self.candidate} for {self.hiring_request}'


class Employee(models.Model):
    STATUS_CHOICES = [
        ('active',      'Active'),
        ('replacement', 'Replacement Requested'),
        ('terminated',  'Terminated'),
    ]

    client           = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='employees')
    candidate        = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    hiring_request   = models.ForeignKey(HiringRequest, on_delete=models.CASCADE)
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date       = models.DateField()
    end_date         = models.DateField(null=True, blank=True)
    monthly_rate     = models.PositiveIntegerField()
    supervisor_email = models.EmailField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.candidate} → {self.client} ({self.status})'