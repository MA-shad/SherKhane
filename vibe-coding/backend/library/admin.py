from django.contrib import admin
from .models import Bookmark


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'poem', 'category_tag', 'created_at')
    list_filter = ('category_tag', 'created_at')
    search_fields = ('user__username', 'poem__title', 'personal_note')
