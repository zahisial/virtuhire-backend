# virtuhire-backend/candidates/views.py

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import CandidateProfile
from .serializers import (
    CandidateApplicationSerializer,
    CandidatePublicSerializer,
    CandidateAdminSerializer,
)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@parser_classes([MultiPartParser, FormParser])
def apply(request):
    """Candidate submits application."""
    serializer = CandidateApplicationSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Application submitted. Status: Under Review.',
            'status': 'pending',
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])   # ← added this line
def browse(request):
    """
    Clients browse approved candidates.
    Filters: category, work_preference
    Pagination: 20 per page
    """
    qs = CandidateProfile.objects.filter(status='approved')

    category  = request.query_params.get('category')
    work_pref = request.query_params.get('work_preference')

    if category:
        qs = qs.filter(category=category)
    if work_pref:
        qs = qs.filter(work_preference=work_pref)

    qs = qs.order_by('-is_featured', '-is_priority', '-rating')

    paginator = PageNumberPagination()
    paginator.page_size = 20
    page = paginator.paginate_queryset(qs, request)
    serializer = CandidatePublicSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def candidate_detail(request, pk):
    """Single candidate detail for clients."""
    try:
        candidate = CandidateProfile.objects.get(pk=pk, status='approved')
    except CandidateProfile.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(CandidatePublicSerializer(candidate).data)


@api_view(['GET'])
def my_application(request):
    """Candidate checks their own application status."""
    try:
        profile = request.user.candidate_profile
    except CandidateProfile.DoesNotExist:
        return Response({'error': 'No application found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({
        'status': profile.status,
        'submitted_at': profile.created_at,
    })