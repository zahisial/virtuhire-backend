# virtuhire-backend/support/views.py

from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Ticket, TicketReply


class TicketReplySerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model  = TicketReply
        fields = ['id', 'user_email', 'message', 'created_at']


class TicketSerializer(serializers.ModelSerializer):
    replies = TicketReplySerializer(many=True, read_only=True)

    class Meta:
        model  = Ticket
        fields = ['id', 'category', 'subject', 'message',
                  'status', 'replies', 'created_at', 'updated_at']
        read_only_fields = ['status']


@api_view(['GET', 'POST'])
def tickets(request):
    if request.method == 'GET':
        qs = Ticket.objects.filter(user=request.user).order_by('-created_at')
        return Response(TicketSerializer(qs, many=True).data)

    serializer = TicketSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def ticket_detail(request, pk):
    try:
        ticket = Ticket.objects.get(pk=pk, user=request.user)
    except Ticket.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(TicketSerializer(ticket).data)

    reply = TicketReply.objects.create(
        ticket=ticket,
        user=request.user,
        message=request.data.get('message', ''),
    )
    return Response(TicketReplySerializer(reply).data, status=status.HTTP_201_CREATED)