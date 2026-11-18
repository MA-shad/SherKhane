from django.db import models
from django.conf import settings
from divan.models import Verse


class MoshaerehSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='moshaereh_sessions',
        verbose_name="کاربر"
    )
    current_letter = models.CharField(max_length=5, verbose_name="حرف جاری")
    score = models.PositiveBigIntegerField(default=0, verbose_name="امتیاز")
    round_count = models.PositiveBigIntegerField(default=0, verbose_name="تعداد دور ها")
    used_verse = models.ManyToManyField(Verse, blank=True, related_name='used_in_sessions', verbose_name="ابیات خوانده شده")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")
    
    class Meta:
        verbose_name = "بازی مشاعره"
        verbose_name_plural = "بازی های مشاعره"
        ordering = ['-created_at']

    def __str__(self):
        user_display = (self.user.get_full_name() or self.user.username) if self.user else "کاربر مهمان"
        return f"مشاعره {user_display} - دور {self.round_count} (حرف {self.current_letter})"
        

    
