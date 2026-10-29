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


class PoemSerializer(serializers.ModelSerializer):
    # قرار دادن ابیات به صورت تودرتو زیر مجموعه شعر
    verses = VerseSerializer(many=True, read_only=True)

    class Meta:
        model = Poem
        fields = ['id', 'poet', 'title', 'rhythm', 'poem_type', 'verses', 'created_at']