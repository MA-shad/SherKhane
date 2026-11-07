from django.contrib import admin
from .models import Poet, Rhythm, Work, Poem, Verse


class VerseInline(admin.TabularInline):
    model = Verse
    extra = 1
    fields = ('order', 'first_couplet', 'second_couplet')


@admin.register(Poet)
class PoetAdmin(admin.ModelAdmin):
    list_display = ('name', 'century', 'birth_place', 'slug')
    search_fields = ('name', 'bio')
    list_filter = ('century',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Rhythm)
class RhythmAdmin(admin.ModelAdmin):
    list_display = ('name', 'bahr', 'pattern')
    search_fields = ('name', 'bahr')


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'poet', 'work_type')
    list_filter = ('work_type', 'poet')
    search_fields = ('title',)


@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    list_display = ('title', 'poet', 'poem_type', 'rhythm', 'order_in_work')
    list_filter = ('poem_type', 'poet', 'rhythm')
    search_fields = ('title', 'verses__first_couplet', 'verses__second_couplet')
    inlines = [VerseInline]


@admin.register(Verse)
class VerseAdmin(admin.ModelAdmin):
    list_display = ('poem', 'order', 'first_couplet', 'second_couplet')
    search_fields = ('first_couplet', 'second_couplet', 'poem__title')
    list_filter = ('poem__poet', 'poem__poem_type')
