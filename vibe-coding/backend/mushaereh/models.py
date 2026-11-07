from django.db import models
from django.conf import settings
from django.utils import timezone


class MushaerehRoom(models.Model):
    class Mode(models.TextChoices):
        BOT = 'bot', 'مشاعره با هوش سخن‌سنج'
        MULTIPLAYER = 'multiplayer', 'دو نفره نوبتی'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'در جریان'
        FINISHED = 'finished', 'به پایان رسیده'

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mushaereh_rooms',
        verbose_name='ایجادکننده'
    )
    title = models.CharField(max_length=150, default='مسابقه مشاعره', verbose_name='عنوان مسابقه')
    mode = models.CharField(max_length=20, choices=Mode.choices, default=Mode.BOT, verbose_name='نوع مسابقه')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE, verbose_name='وضعیت')
    current_letter = models.CharField(max_length=5, default='م', verbose_name='حرف جاری نوبت')
    current_turn = models.CharField(max_length=30, default='user', verbose_name='نوبت بازیکن (user / bot)')
    turn_timeout_seconds = models.PositiveIntegerField(default=45, verbose_name='مهلت زمانی نوبت (ثانیه)')
    turn_start_time = models.DateTimeField(default=timezone.now, verbose_name='آغاز زمان نوبت')
    score_user = models.PositiveIntegerField(default=0, verbose_name='امتیاز کاربر')
    score_opponent = models.PositiveIntegerField(default=0, verbose_name='امتیاز حریف / ربات')
    rounds_completed = models.PositiveIntegerField(default=0, verbose_name='تعداد دورهای انجام‌شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')

    class Meta:
        verbose_name = 'اتاق مشاعره'
        verbose_name_plural = 'اتاق‌های مشاعره'
        ordering = ['-created_at']

    def __str__(self):
        return f"مسابقه {self.id} - حرف فعلی: {self.current_letter}"


class MushaerehTurn(models.Model):
    room = models.ForeignKey(MushaerehRoom, on_delete=models.CASCADE, related_name='turns', verbose_name='اتاق')
    turn_number = models.PositiveIntegerField(verbose_name='شماره نوبت')
    player_name = models.CharField(max_length=80, verbose_name='نام سراینده')
    verse_text = models.CharField(max_length=350, verbose_name='بیت خوانده‌شده')
    poet_name = models.CharField(max_length=100, blank=True, verbose_name='شاعر')
    starting_letter = models.CharField(max_length=5, verbose_name='حرف آغازین')
    ending_letter = models.CharField(max_length=5, verbose_name='حرف پایانی')
    is_valid = models.BooleanField(default=True, verbose_name='تایید داوری')
    rejection_reason = models.CharField(max_length=255, blank=True, verbose_name='دلیل رد')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت')

    class Meta:
        verbose_name = 'نوبت مشاعره'
        verbose_name_plural = 'نوبت‌های مشاعره'
        ordering = ['turn_number']

    def __str__(self):
        return f"نوبت {self.turn_number}: {self.player_name} ({self.starting_letter} -> {self.ending_letter})"
