# virtuhire-backend/hiring/serializers.py

from rest_framework import serializers
from .models import HiringRequest, Shortlist, InterviewRequest, Employee


class HiringRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model  = HiringRequest
        fields = ['id', 'category', 'work_type', 'employee_count',
                  'status', 'hiring_fee_paid', 'batches_used', 'created_at']
        read_only_fields = ['status', 'hiring_fee_paid', 'batches_used']

    def create(self, validated_data):
        client = self.context['request'].user.client_profile
        return HiringRequest.objects.create(client=client, **validated_data)


class ShortlistSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Shortlist
        fields = ['id', 'candidate', 'created_at']

    def validate(self, data):
        hiring_request = self.context['hiring_request']
        if hiring_request.shortlists.count() >= 3:
            raise serializers.ValidationError('Maximum 3 candidates can be shortlisted.')
        return data


class InterviewRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model  = InterviewRequest
        fields = ['id', 'candidate', 'status', 'scheduled_at', 'notes', 'created_at']
        read_only_fields = ['status', 'scheduled_at']


class EmployeeSerializer(serializers.ModelSerializer):
    candidate_name  = serializers.CharField(source='candidate.full_name', read_only=True)
    category        = serializers.CharField(source='candidate.category', read_only=True)
    work_preference = serializers.CharField(source='candidate.work_preference', read_only=True)

    class Meta:
        model  = Employee
        fields = ['id', 'candidate', 'candidate_name', 'category', 'work_preference',
                  'status', 'start_date', 'end_date', 'monthly_rate',
                  'supervisor_email', 'created_at']
        read_only_fields = ['monthly_rate']