# virtuhire-backend/billing/views.py

from rest_framework import status, permissions, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Invoice, Payment


# ─── Serializers ─────────────────────────────────────────────────

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Invoice
        fields = ['id', 'invoice_number', 'amount', 'status',
                  'description', 'pdf_url', 'due_date', 'paid_at', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Payment
        fields = ['id', 'amount', 'payment_type', 'status',
                  'stripe_payment_intent_id', 'created_at']


# ─── Views ───────────────────────────────────────────────────────

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

    if not amount:
        return Response({'error': 'amount is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount) * 100,
            currency='aed',
            automatic_payment_methods={'enabled': True},
            metadata={
                'client_id':    str(request.user.client_profile.id),
                'payment_type': payment_type,
            }
        )

        Payment.objects.create(
            client=request.user.client_profile,
            amount=int(amount),
            payment_type=payment_type,
            status='pending',
            stripe_payment_intent_id=intent.id,
        )

        return Response({
            'client_secret':     intent.client_secret,
            'publishable_key':   settings.STRIPE_PUBLISHABLE_KEY,
            'payment_intent_id': intent.id,
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def save_card(request):
    import stripe
    from django.conf import settings
    stripe.api_key = settings.STRIPE_SECRET_KEY

    client = request.user.client_profile

    try:
        if not client.stripe_customer_id:
            customer = stripe.Customer.create(
                email=request.user.email,
                metadata={'client_id': str(client.id)},
            )
            client.stripe_customer_id = customer.id
            client.save()

        setup_intent = stripe.SetupIntent.create(
            customer=client.stripe_customer_id,
            automatic_payment_methods={'enabled': True},
        )
        return Response({'client_secret': setup_intent.client_secret})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def stripe_webhook(request):
    import stripe
    from django.conf import settings

    payload    = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    if event['type'] == 'payment_intent.succeeded':
        pi = event['data']['object']
        Payment.objects.filter(
            stripe_payment_intent_id=pi['id']
        ).update(status='succeeded')

        try:
            payment = Payment.objects.get(stripe_payment_intent_id=pi['id'])
            if payment.payment_type in ('monthly', 'balance'):
                from accounts.email import send_invoice_generated
                client = payment.client
                name   = client.full_name or client.company_name or client.user.email
                inv_num = f'INV-{payment.id:04d}'
                send_invoice_generated(client.user.email, name, inv_num, payment.amount)
        except Exception:
            pass

    elif event['type'] == 'payment_intent.payment_failed':
        pi = event['data']['object']
        Payment.objects.filter(
            stripe_payment_intent_id=pi['id']
        ).update(status='failed')

    return Response({'status': 'ok'})