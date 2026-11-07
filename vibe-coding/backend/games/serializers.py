from rest_framework import serializers
from .models import GameSession


class GameSessionSerializer(serializers.ModelSerializer):
    game_name = serializers.CharField(source='get_game_type_display', read_only=True)

    class Meta:
        model = GameSession
        fields = ['id', 'game_type', 'game_name', 'score', 'is_completed', 'created_at']
        read_only_fields = ['id', 'created_at']
