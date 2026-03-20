# virtuhire-backend/contracts/views.py

from django.utils import timezone
from rest_framework import status, serializers
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Contract


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Contract
        fields = ['id', 'status', 'language', 'pdf_file', 'agreed_at', 'created_at']


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def sign_contract(request):
    client    = request.user.client_profile
    language  = request.data.get('language', 'en')
    signature = request.FILES.get('signature')

    contract = Contract.objects.create(
        client=client,
        language=language,
        signature=signature,
        status='signed',
        agreed_at=timezone.now(),
    )
    return Response(ContractSerializer(contract).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def my_contracts(request):
    client    = request.user.client_profile
    contracts = Contract.objects.filter(client=client).order_by('-created_at')
    return Response(ContractSerializer(contracts, many=True).data)