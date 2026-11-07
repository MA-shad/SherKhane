from django.contrib import admin
from .models import MushaerehRoom, MushaerehTurn


class MushaerehTurnInline(admin.TabularInline):
    model = MushaerehTurn
    extra = 0
    readonly_fields = ('turn_number', 'player_name', 'verse_text', 'starting_letter', 'ending_letter', 'is_valid', 'created_at')


@admin.register(MushaerehRoom)
class MushaerehRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'mode', 'status', 'current_letter', 'score_user', 'score_opponent', 'created_at')
    list_filter = ('mode', 'status', 'created_at')
    search_fields = ('title', 'creator__username')
    inlines = [MushaerehTurnInline]


@admin.register(MushaerehTurn)
class MushaerehTurnAdmin(admin.ModelAdmin):
    list_display = ('room', 'turn_number', 'player_name', 'starting_letter', 'ending_letter', 'is_valid')
    list_filter = ('is_valid', 'starting_letter', 'ending_letter')
