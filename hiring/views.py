# virtuhire-backend/hiring/views.py

from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import HiringRequest, Shortlist, InterviewRequest, Employee
from .serializers import (
    HiringRequestSerializer, ShortlistSerializer,
    InterviewRequestSerializer, EmployeeSerializer,
)


@api_view(['POST', 'GET'])
def hiring_requests(request):
    client = request.user.client_profile

    if request.method == 'GET':
        qs = HiringRequest.objects.filter(client=client).order_by('-created_at')
        return Response(HiringRequestSerializer(qs, many=True).data)

    serializer = HiringRequestSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        hr = serializer.save()
        return Response(HiringRequestSerializer(hr).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def shortlist(request, hiring_request_id):
    try:
        hr = HiringRequest.objects.get(pk=hiring_request_id, client=request.user.client_profile)
    except HiringRequest.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ShortlistSerializer(data=request.data, context={'hiring_request': hr})
    if serializer.is_valid():
        serializer.save(hiring_request=hr)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def remove_shortlist(request, hiring_request_id, candidate_id):
    Shortlist.objects.filter(
        hiring_request_id=hiring_request_id,
        candidate_id=candidate_id,
        hiring_request__client=request.user.client_profile
    ).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def request_interview(request, hiring_request_id):
    try:
        hr = HiringRequest.objects.get(pk=hiring_request_id, client=request.user.client_profile)
    except HiringRequest.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = InterviewRequestSerializer(data=request.data)
    if serializer.is_valid():
        interview = serializer.save(hiring_request=hr)
        return Response(InterviewRequestSerializer(interview).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def my_employees(request):
    client    = request.user.client_profile
    employees = Employee.objects.filter(client=client, status='active').select_related('candidate')
    return Response(EmployeeSerializer(employees, many=True).data)


@api_view(['POST'])
def confirm_hire(request, hiring_request_id):
    try:
        hr = HiringRequest.objects.get(pk=hiring_request_id, client=request.user.client_profile)
    except HiringRequest.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    candidate_id = request.data.get('candidate_id')
    from candidates.models import CandidateProfile
    from django.utils import timezone

    try:
        candidate = CandidateProfile.objects.get(pk=candidate_id, status='approved')
    except CandidateProfile.DoesNotExist:
        return Response({'error': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)

    employee = Employee.objects.create(
        client=hr.client,
        candidate=candidate,
        hiring_request=hr,
        start_date=timezone.now().date(),
        monthly_rate=candidate.monthly_rate,
    )
    hr.status = 'completed'
    hr.save()

    return Response(EmployeeSerializer(employee).data, status=status.HTTP_201_CREATED)