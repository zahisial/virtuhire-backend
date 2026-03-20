# virtuhire-backend/billing/views.py

from rest_framework import status, permissions, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Invoice, Payment

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Invoice
        fields = ['id', 'invoice_number', 'amount', 'status',
                  'description', 'pdf_url', 'due_date', 'paid_at', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Payment
        fields = ['id', 'amount', 'payment_type', 'status', 'created_at']


@api_view(['GET'])
def invoices(request):
    client = request.user.client_profile
    qs     = Invoice.objects.filter(client=client).order_by('-created_at')
    return Response(InvoiceSerializer(qs, many=True).data)


@api_view(['GET'])
def payments(request):
    client = request.user.client_profile
    qs     = Payment.objects.filter(client=client).order_by('-created_at')
    return Response(PaymentSerializer(qs, many=True).data)


@api_view(['POST'])
def create_payment_intent(request):
    import stripe
    from django.conf import settings
    stripe.api_key = settings.STRIPE_SECRET_KEY

    amount       = request.data.get('amount')
    payment_type = request.data.get('payment_type', 'hiring_fee')

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount) * 100,
            currency='aed',
            metadata={
                'client_id':    str(request.user.client_profile.id),
                'payment_type': payment_type,
            }
        )
        return Response({'client_secret': intent.client_secret})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def stripe_webhook(request):
    import stripe
    from django.conf import settings
    from django.utils import timezone

    payload    = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

    if event['type'] == 'payment_intent.succeeded':
        pi = event['data']['object']
        Payment.objects.filter(
            stripe_payment_intent_id=pi['id']
        ).update(status='succeeded')

    return Response({'status': 'ok'})