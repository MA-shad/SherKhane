from rest_framework import serializers
from .models import Poet, Work, Rhythm, Poem, Verse


class WorkSerializer(serializers.ModelSerializer):
    poet_name = serializers.CharField(source='poet.name', read_only=True)

    class Meta:
        model = Work
        fields = ['id', 'title', 'poet', 'poet_name', 'description']


class PoetSerializer(serializers.ModelSerializer):
    works = WorkSerializer(many=True, read_only=True)

    class Meta:
        model = Poet
        fields = ['id', 'name', 'bio', 'century', 'works']


class RhythmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rhythm
        fields = ['id', 'name', 'bahr']


class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verse
        fields = ['id', 'poem', 'order', 'first_couplet', 'second_couplet']


class PoemListSerializer(serializers.ModelSerializer):
    poet_name = serializers.CharField(source='poet.name', read_only=True)
    work_title = serializers.CharField(source='work.title', read_only=True, default=None)
    rhythm_name = serializers.CharField(source='rhythm.name', read_only=True, default=None)

    class Meta:
        model = Poem
        fields = [
            'id', 'title', 'poet', 'poet_name',
            'work', 'work_title',
            'rhythm', 'rhythm_name', 'poem_type',
            'created_at', 'updated_at'
        ]

class PoemDetailSerializer(serializers.ModelSerializer):
    poet_name = serializers.CharField(source='poet.name', read_only=True)
    work_title = serializers.CharField(source='work.title', read_only=True, default=None)
    rhythm_name = serializers.CharField(source='rhythm.name', read_only=True, default=None)
    verses = VerseSerializer(many=True, read_only=True)

    class Meta:
        model = Poem
        fields = [
            'id', 'title', 'poet', 'poet_name',
            'work', 'work_title',
            'rhythm', 'rhythm_name', 'poem_type',
            'verses', 'created_at', 'updated_at'
        ]