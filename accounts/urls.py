# virtuhire-backend/accounts/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/',      views.register,     name='register'),
    path('login/',         views.login,        name='login'),
    path('logout/',        views.logout,       name='logout'),
    path('otp/request/',   views.request_otp,  name='request-otp'),
    path('otp/verify/',    views.verify_otp,   name='verify-otp'),
    path('profile/',       views.profile,      name='profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]