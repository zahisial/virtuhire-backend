# virtuhire-backend/candidates/admin.py
from django.contrib import admin
from .models import CandidateProfile

admin.site.register(CandidateProfile)