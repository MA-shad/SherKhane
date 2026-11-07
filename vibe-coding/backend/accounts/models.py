from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.username


def get_today():
    return timezone.now().date()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='کاربر')
    display_name = models.CharField(max_length=120, blank=True, verbose_name='نام نمایشی')
    bio = models.TextField(blank=True, verbose_name='معرفی کوتاه')
    avatar = models.CharField(max_length=255, default='default-poet.png', verbose_name='آیکون آواتار')
    xp_points = models.PositiveIntegerField(default=100, verbose_name='امتیاز ادب (XP)')
    current_streak = models.PositiveIntegerField(default=1, verbose_name='روزهای متوالی تمرین')
    last_activity_date = models.DateField(default=get_today, verbose_name='آخرین تاریخ فعالیت')

    class Meta:
        verbose_name = 'پروفایل کاربر'
        verbose_name_plural = 'پروفایل‌های کاربران'

    def __str__(self):
        return f"پروفایل {self.display_name or self.user.username}"

    @property
    def literary_title(self) -> str:
        """Calculate title based on XP points"""
        if self.xp_points >= 5000:
            return 'استاد سخن'
        elif self.xp_points >= 2500:
            return 'ادیب سخن‌سنج'
        elif self.xp_points >= 1000:
            return 'سخن‌دان'
        elif self.xp_points >= 400:
            return 'حافظ‌یار'
        return 'نوآموز ادب'

    def record_activity(self):
        """Update consecutive practice streak"""
        today = timezone.now().date()
        act_date = self.last_activity_date
        if hasattr(act_date, 'date'):
            act_date = act_date.date()

        if act_date == today - timedelta(days=1):
            self.current_streak += 1
        elif act_date < today - timedelta(days=1):
            self.current_streak = 1
        self.last_activity_date = today
        self.save(update_fields=['current_streak', 'last_activity_date'])

    def add_xp(self, points: int):
        self.xp_points += points
        self.record_activity()
        self.save(update_fields=['xp_points'])
