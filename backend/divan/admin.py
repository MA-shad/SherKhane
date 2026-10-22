from django.contrib import admin
from .models import Poet, Poem, Verse

# Register your models here.

@admin.register(Poet)
class PoetAdmin(admin.ModelAdmin):

    list_display = ('name', 'century', 'created_at')
    search_fields = ('name',)


@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):

    list_display = ('title', 'poet', 'poem_type', 'created_at')
    list_filter = ('poem_type', 'poet')
    search_fields = ('title',)


@admin.register(Verse)
class VerseAdmin(admin.ModelAdmin):

    list_display = ('verse', 'order', 'first_couplet', 'second_couplet')
    list_filter = ('verse', 'order')