from rest_framework import serializers
from .models import Poet, Rhythm, Work, Poem, Verse


class RhythmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rhythm
        fields = ['id', 'name', 'bahr', 'pattern']


class PoetListSerializer(serializers.ModelSerializer):
    poems_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Poet
        fields = ['id', 'name', 'slug', 'century', 'birth_place', 'avatar', 'poems_count']


class PoetDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poet
        fields = ['id', 'name', 'slug', 'bio', 'century', 'birth_place', 'avatar']


class WorkSerializer(serializers.ModelSerializer):
    poet_name = serializers.CharField(source='poet.name', read_only=True)

    class Meta:
        model = Work
        fields = ['id', 'poet', 'poet_name', 'title', 'slug', 'work_type', 'description']


class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verse
        fields = ['id', 'order', 'first_couplet', 'second_couplet']


class PoemListSerializer(serializers.ModelSerializer):
    poet_name = serializers.CharField(source='poet.name', read_only=True)
    rhythm_name = serializers.CharField(source='rhythm.name', read_only=True)
    verses_count = serializers.IntegerField(read_only=True)
    first_verse = serializers.SerializerMethodField()

    class Meta:
        model = Poem
        fields = ['id', 'title', 'slug', 'poet', 'poet_name', 'poem_type', 'rhythm_name', 'verses_count', 'first_verse']

    def get_first_verse(self, obj):
        first = obj.verses.first()
        if first:
            return f"{first.first_couplet} / {first.second_couplet}"
        return ""


class PoemDetailSerializer(serializers.ModelSerializer):
    poet = PoetDetailSerializer(read_only=True)
    rhythm = RhythmSerializer(read_only=True)
    work = WorkSerializer(read_only=True)
    verses = VerseSerializer(many=True, read_only=True)

    class Meta:
        model = Poem
        fields = ['id', 'title', 'slug', 'poet', 'work', 'rhythm', 'poem_type', 'order_in_work', 'edition_source', 'created_at', 'verses']
