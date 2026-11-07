from django.db import models
from django.conf import settings


class GameSession(models.Model):
    class GameType(models.TextChoices):
        BAIT_CHIN = 'bait_chin', 'بیت‌چین (مرتب‌سازی ابیات)'
        GUESS_POET = 'guess_poet', 'حدس شاعر'
        NEXT_COUPLET = 'next_couplet', 'تکمیل مصراع'
        WORD_QUIZ = 'word_quiz', 'واژه‌نامه ادب کهن'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='game_sessions', verbose_name='کاربر')
    game_type = models.CharField(max_length=30, choices=GameType.choices, verbose_name='نوع بازی')
    score = models.IntegerField(default=0, verbose_name='امتیاز کسب‌شده')
    is_completed = models.BooleanField(default=False, verbose_name='پایان‌یافته')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان شروع')

    class Meta:
        verbose_name = 'نشست بازی ادبی'
        verbose_name_plural = 'نشست‌های بازی‌های ادبی'
        ordering = ['-created_at']

    def __str__(self):
        user_name = self.user.username if self.user else 'مهمان'
        return f"{self.get_game_type_display()} - {user_name} (امتیاز: {self.score})"
