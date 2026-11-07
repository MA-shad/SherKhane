from django.contrib import admin
from .models import GameSession


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'game_type', 'score', 'is_completed', 'created_at')
    list_filter = ('game_type', 'is_completed', 'created_at')
    search_fields = ('user__username',)
