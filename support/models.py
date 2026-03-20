# virtuhire-backend/support/models.py

from django.db import models
from accounts.models import User


class Ticket(models.Model):
    CATEGORY_CHOICES = [
        ('sales',     'Sales'),
        ('billing',   'Billing & Finance'),
        ('technical', 'Technical Support'),
        ('hr',        'HR / Employee Issues'),
    ]
    STATUS_CHOICES = [
        ('open',     'Open'),
        ('progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed',   'Closed'),
    ]

    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    subject     = models.CharField(max_length=255)
    message     = models.TextField()
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.category}] {self.subject} — {self.status}'


class TicketReply(models.Model):
    ticket     = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='replies')
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reply to {self.ticket} by {self.user.email}'