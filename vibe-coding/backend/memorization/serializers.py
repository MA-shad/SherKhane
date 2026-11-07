from rest_framework import serializers
from poetry.serializers import PoemListSerializer
from .models import MemorizationItem, MemorizationLog


class MemorizationItemSerializer(serializers.ModelSerializer):
    poem_details = PoemListSerializer(source='poem', read_only=True)
    is_due = serializers.BooleanField(read_only=True)
    mastery_name = serializers.CharField(source='get_mastery_level_display', read_only=True)

    class Meta:
        model = MemorizationItem
        fields = [
            'id', 'poem', 'poem_details', 'mastery_level', 'mastery_name',
            'repetition_count', 'easiness_factor', 'interval_days',
            'next_review_date', 'last_reviewed_at', 'total_correct',
            'total_attempts', 'is_due'
        ]
        read_only_fields = ['id', 'easiness_factor', 'interval_days', 'next_review_date', 'last_reviewed_at', 'total_correct', 'total_attempts']


class ReviewSubmissionSerializer(serializers.Serializer):
    poem_id = serializers.IntegerField()
    quality_grade = serializers.IntegerField(min_value=0, max_value=5)
