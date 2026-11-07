from django.contrib import admin
from .models import DailyHighlight


@admin.register(DailyHighlight)
class DailyHighlightAdmin(admin.ModelAdmin):
    list_display = ('date', 'poet_name', 'proverb')
    search_fields = ('beyt_first', 'beyt_second', 'poet_name', 'proverb')
