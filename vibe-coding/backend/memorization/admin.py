from django.contrib import admin
from .models import MemorizationItem, MemorizationLog


class MemorizationLogInline(admin.TabularInline):
    model = MemorizationLog
    extra = 0
    readonly_fields = ('quality_grade', 'exercise_type', 'created_at')


@admin.register(MemorizationItem)
class MemorizationItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'poem', 'mastery_level', 'interval_days', 'next_review_date', 'repetition_count')
    list_filter = ('mastery_level', 'next_review_date')
    search_fields = ('user__username', 'poem__title')
    inlines = [MemorizationLogInline]
