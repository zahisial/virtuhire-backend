# virtuhire-backend/accounts/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('client',    'Client'),
        ('candidate', 'Candidate'),
        ('admin',     'Admin'),
    ]

    email      = models.EmailField(unique=True)
    phone      = models.CharField(max_length=20, blank=True)
    role       = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    is_active  = models.BooleanField(default=True)
    is_staff   = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class ClientProfile(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('corporate',  'Corporate'),
    ]

    user             = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    account_type     = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)

    # Individual fields
    full_name        = models.CharField(max_length=200, blank=True)
    emirates_id      = models.FileField(upload_to='documents/emirates_id/', blank=True, null=True)

    # Corporate fields
    company_name     = models.CharField(max_length=200, blank=True)
    trade_license    = models.FileField(upload_to='documents/trade_license/', blank=True, null=True)
    vat_number       = models.CharField(max_length=50, blank=True)
    contact_person   = models.CharField(max_length=200, blank=True)

    # Stripe
    stripe_customer_id = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} ({self.account_type})'


class OTP(models.Model):
    email      = models.EmailField()
    code       = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used    = models.BooleanField(default=False)

    def __str__(self):
        return f'OTP for {self.email}'