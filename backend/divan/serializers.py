from rest_framework import serializers
from .models import Poet, Poem, Verse

class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verse
        fields = ['id', 'order', 'first_couplet', 'second_couplet']

class PoemSerializer(serializers.ModelSerializer):
    verses = VerseSerializer(many=True, read_only=True)

    class Meta:
        model = Poem
        fields = ['id', 'title', 'poem_type', 'rhythm', 'verses', 'created_at']

class PoetSerializer(serializers.ModelSerializer):
    poems_count = serializers.IntegerField(source='poems.count', read_only=True)

    class Meta:
        model = Poet
        fields = ['id', 'name', 'bio', 'century', 'poems_count', 'created_at']