# virtuhire-backend/accounts/admin.py
from django.contrib import admin
from .models import User, ClientProfile, OTP

admin.site.register(User)
admin.site.register(ClientProfile)
admin.site.register(OTP)