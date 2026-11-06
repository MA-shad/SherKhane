from django.contrib import admin
from .models import Poet, Rhythm, Poem, Verse


# فرم خطی ابیات برای نمایش زیر صفحه شعر
class VerseInline(admin.TabularInline):
    model = Verse
    extra = 3
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

    # تزریق ابیات به فرم شعر
    inlines = [VerseInline]

# نکته: مدل Verse را به صورت مستقل از اینجا برداشتیم
# تا منوی تکراری در صفحه اصلی ادمین ایجاد نشود.