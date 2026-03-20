# virtuhire-backend/candidates/serializers.py

from rest_framework import serializers
from .models import CandidateProfile


class CandidateApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CandidateProfile
        fields = [
            'full_name', 'phone', 'location', 'category',
            'work_preference', 'experience', 'cv', 'voice_intro',
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        return CandidateProfile.objects.create(user=user, **validated_data)


class CandidatePublicSerializer(serializers.ModelSerializer):
    """Shown to clients when browsing talent — no contact info."""
    monthly_rate = serializers.ReadOnlyField()

    class Meta:
        model  = CandidateProfile
        fields = [
            'id', 'full_name', 'category', 'work_preference',
            'experience', 'skills', 'rating', 'voice_intro',
            'is_featured', 'monthly_rate',
        ]


class CandidateAdminSerializer(serializers.ModelSerializer):
    """Full detail for admin panel."""
    monthly_rate = serializers.ReadOnlyField()
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model  = CandidateProfile
        fields = '__all__'