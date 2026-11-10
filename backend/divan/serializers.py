from rest_framework import serializers
from .models import Poet, Rhythm, Poem, Verse


class PoetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poet
        fields = ['id', 'name', 'bio', 'century']


class RhythmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rhythm
        fields = ['id', 'name', 'bahr']


class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verse
        fields = ['id', 'order', 'first_couplet', 'second_couplet']


class PoemListSerializer(serializers.ModelSerializer):
    poet_name = serializers.CharField(source='poet.name', read_only=True)
    rhythm_name = serializers.CharField(source='rhythm.name', read_only=True, default=None)

    class Meta:
        model = Poem
        fields = [
            'id', 'title', 'poet', 'poet_name',
            'rhythm', 'rhythm_name', 'poem_type',
            'created_at', 'updated_at'
        ]

class PoemDetailSerializer(serializers.ModelSerializer):
    poet_name = serializers.CharField(source='poet.name', read_only=True)
    rhythm_name = serializers.CharField(source='rhythm.name', read_only=True, default=None)
    verses = VerseSerializer(many=True, read_only=True)

    class Meta:
        model = Poem
        fields = [
            'id', 'title', 'poet', 'poet_name',
            'rhythm', 'rhythm_name', 'poem_type',
            'verses', 'created_at', 'updated_at'
        ]