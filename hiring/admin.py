# virtuhire-backend/hiring/admin.py
from django.contrib import admin
from .models import HiringRequest, Shortlist, InterviewRequest, Employee

admin.site.register(HiringRequest)
admin.site.register(Shortlist)
admin.site.register(InterviewRequest)
admin.site.register(Employee)