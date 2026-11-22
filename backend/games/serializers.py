from rest_framework import serializers
from .models import MoshaerehSession
from divan.serializers import VerseSerializer

class MoshaerehSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoshaerehSession
        fields = [
            'id',
            'current_letter',
            'score',
            'round_count',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields

class PlayTurnInputSerializer(serializers.Serializer):
    verse_text = serializers.CharField(
        max_length=500,
        required=True,
        error_messages={
            'required': "وارد کردن متن بیت الزامی است",
            'blank': "متن بیت نمی‌تواند خالی باشد",
        }
    )

class PlayTurnResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
    bot_verse = VerseSerializer(allow_null=True)
    session = MoshaerehSessionSerializer()