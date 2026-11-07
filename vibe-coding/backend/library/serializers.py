from rest_framework import serializers
from poetry.serializers import PoemListSerializer
from .models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    poem_details = PoemListSerializer(source='poem', read_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'poem', 'poem_details', 'category_tag', 'personal_note', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        bookmark, created = Bookmark.objects.update_or_create(
            user=user,
            poem=validated_data['poem'],
            defaults={
                'category_tag': validated_data.get('category_tag', 'برگزیده‌ها'),
                'personal_note': validated_data.get('personal_note', '')
            }
        )
        return bookmark
