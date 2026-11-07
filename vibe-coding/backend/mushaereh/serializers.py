from rest_framework import serializers
from .models import MushaerehRoom, MushaerehTurn


class MushaerehTurnSerializer(serializers.ModelSerializer):
    class Meta:
        model = MushaerehTurn
        fields = ['id', 'turn_number', 'player_name', 'verse_text', 'poet_name', 'starting_letter', 'ending_letter', 'is_valid', 'created_at']


class MushaerehRoomSerializer(serializers.ModelSerializer):
    turns = MushaerehTurnSerializer(many=True, read_only=True)

    class Meta:
        model = MushaerehRoom
        fields = [
            'id', 'title', 'mode', 'status', 'current_letter', 'current_turn',
            'turn_timeout_seconds', 'score_user', 'score_opponent',
            'rounds_completed', 'created_at', 'turns'
        ]
        read_only_fields = ['id', 'status', 'current_letter', 'current_turn', 'score_user', 'score_opponent', 'rounds_completed', 'created_at']


class SubmitVerseSerializer(serializers.Serializer):
    verse_text = serializers.CharField(max_length=350)
