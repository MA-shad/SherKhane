from django.db import models
from django.conf import settings
from poetry.models import Poem


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks', verbose_name='کاربر')
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='bookmarked_by', verbose_name='شعر نشانه‌گذاری شده')
    category_tag = models.CharField(max_length=60, default='برگزیده‌ها', verbose_name='برچسب دسته‌بندی')
    personal_note = models.TextField(blank=True, verbose_name='یادداشت شخصی')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ذخیره')

    class Meta:
        verbose_name = 'نشان شعر'
        verbose_name_plural = 'دفترچه شخصی و نشان‌ها'
        unique_together = ('user', 'poem')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.poem.title}"
