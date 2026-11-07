from django.db import models
from django.conf import settings
from django.utils import timezone
from poetry.models import Poem


class MemorizationItem(models.Model):
    class MasteryLevel(models.IntegerChoices):
        NOVICE = 0, 'نوآموز'
        LEARNING = 1, 'در حال یادگیری'
        REVIEWING = 2, 'تثبیت‌شده'
        MASTERED = 3, 'مسلط'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memorization_items', verbose_name='کاربر')
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='memorized_by', verbose_name='شعر انتخابی')
    mastery_level = models.IntegerField(choices=MasteryLevel.choices, default=MasteryLevel.NOVICE, verbose_name='سطح تسلط')
    repetition_count = models.PositiveIntegerField(default=0, verbose_name='تعداد دفعات مرور موفق')
    easiness_factor = models.FloatField(default=2.5, verbose_name='ضریب سهولت (EF)')
    interval_days = models.PositiveIntegerField(default=1, verbose_name='فاصله تا مرور بعدی (روز)')
    next_review_date = models.DateField(default=timezone.now, verbose_name='تاریخ موعد مرور بعدی')
    last_reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name='آخرین زمان مرور')
    total_correct = models.PositiveIntegerField(default=0, verbose_name='تعداد پاسخ‌های درست')
    total_attempts = models.PositiveIntegerField(default=0, verbose_name='کل تلاش‌ها')

    class Meta:
        verbose_name = 'کارت حفظ شعر'
        verbose_name_plural = 'استودیو حفظ شعر'
        unique_together = ('user', 'poem')
        ordering = ['next_review_date']

    def __str__(self):
        return f"{self.user.username} - حفظ {self.poem.title}"

    @property
    def is_due(self) -> bool:
        return self.next_review_date <= timezone.now().date()


class MemorizationLog(models.Model):
    item = models.ForeignKey(MemorizationItem, on_delete=models.CASCADE, related_name='logs', verbose_name='کارت حفظ')
    quality_grade = models.PositiveSmallIntegerField(verbose_name='کیفیت یادآوری (۰ تا ۵)')
    exercise_type = models.CharField(max_length=50, default='cloze', verbose_name='نوع تمرین')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان آزمون')

    class Meta:
        verbose_name = 'گزارش جلسه مرور'
        verbose_name_plural = 'گزارش‌های جلسات مرور'
        ordering = ['-created_at']
