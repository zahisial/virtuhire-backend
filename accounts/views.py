# virtuhire-backend/accounts/views.py

import random
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, ClientProfile, OTP
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    ClientProfileSerializer, OTPRequestSerializer, OTPVerifySerializer
)


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access':  str(refresh.access_token),
        'role':    user.role,
        'user_id': user.id,
    }


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'tokens': get_tokens(user),
            'user': UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        return Response({
            'tokens': get_tokens(user),
            'user': UserSerializer(user).data,
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def request_otp(request):
    serializer = OTPRequestSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        code  = str(random.randint(100000, 999999))
        OTP.objects.create(email=email, code=code)
        # TODO: send via email/SMS in production
        print(f'OTP for {email}: {code}')
        return Response({'message': 'OTP sent'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verify_otp(request):
    serializer = OTPVerifySerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        code  = serializer.validated_data['code']
        otp   = OTP.objects.filter(email=email, code=code, is_used=False).last()
        if not otp:
            return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
        otp.is_used = True
        otp.save()
        return Response({'message': 'OTP verified'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
def profile(request):
    try:
        client_profile = request.user.client_profile
    except ClientProfile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(ClientProfileSerializer(client_profile).data)

    serializer = ClientProfileSerializer(client_profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout(request):
    try:
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
    except Exception:
        pass
    return Response({'message': 'Logged out'})