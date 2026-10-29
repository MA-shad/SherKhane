from django.contrib import admin
from .models import Poet, Rhythm, Poem, Verse


# ۱. ساخت فرم خطی برای ابیات (تا زیر صفحه شعر نمایش داده شود)
class VerseInline(admin.TabularInline):
    model = Verse
    extra = 3  # به صورت پیش‌فرض ۳ رالی خالی برای وارد کردن سریع ۳ بیت اول نشان می‌دهد
    fields = ['order', 'first_couplet', 'second_couplet']


@admin.register(Poet)
class PoetAdmin(admin.ModelAdmin):
    list_display = ('name', 'century')
    search_fields = ('name',)


@admin.register(Rhythm)
class RhythmAdmin(admin.ModelAdmin):
    list_display = ('name', 'bahr')
    search_fields = ('name', 'bahr')


@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    list_display = ('title', 'poet', 'poem_type', 'rhythm')
    list_filter = ('poem_type', 'rhythm', 'poet')
    search_fields = ('title',)

    # ۲. متصل کردن ابیات به صفحه مدیریت شعر
    inlines = [VerseInline]


# ۳. اگر خواستیم ابیات را به صورت مستقل هم در ادمین ببینیم
@admin.register(Verse)
class VerseAdmin(admin.ModelAdmin):
    list_display = ('poem', 'order', 'first_couplet', 'second_couplet')
    list_filter = ('poem',)
    search_fields = ('first_couplet', 'second_couplet')