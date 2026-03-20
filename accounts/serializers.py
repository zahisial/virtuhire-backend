# virtuhire-backend/accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, ClientProfile


class RegisterSerializer(serializers.ModelSerializer):
    password     = serializers.CharField(write_only=True, min_length=8)
    account_type = serializers.ChoiceField(choices=['individual', 'corporate'])
    full_name    = serializers.CharField(required=False, allow_blank=True)
    company_name = serializers.CharField(required=False, allow_blank=True)
    vat_number   = serializers.CharField(required=False, allow_blank=True)
    contact_person = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model  = User
        fields = ['email', 'phone', 'password', 'role',
                  'account_type', 'full_name', 'company_name',
                  'vat_number', 'contact_person']

    def create(self, validated_data):
        account_type   = validated_data.pop('account_type')
        full_name      = validated_data.pop('full_name', '')
        company_name   = validated_data.pop('company_name', '')
        vat_number     = validated_data.pop('vat_number', '')
        contact_person = validated_data.pop('contact_person', '')

        validated_data['role'] = 'client'
        user = User.objects.create_user(**validated_data)

        ClientProfile.objects.create(
            user=user,
            account_type=account_type,
            full_name=full_name,
            company_name=company_name,
            vat_number=vat_number,
            contact_person=contact_person,
        )
        return user


class LoginSerializer(serializers.Serializer):
    email    = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_active:
            raise serializers.ValidationError('Account is disabled')
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['id', 'email', 'phone', 'role', 'created_at']


class ClientProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)

    class Meta:
        model  = ClientProfile
        fields = ['id', 'email', 'phone', 'account_type', 'full_name',
                  'company_name', 'vat_number', 'contact_person', 'created_at']


class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code  = serializers.CharField(max_length=6)