from django.db import models
from django.utils import timezone


class DailyHighlight(models.Model):
    date = models.DateField(unique=True, default=timezone.now, verbose_name='تاریخ تقویمی')
    beyt_first = models.CharField(max_length=255, verbose_name='مصراع اول بیت روز')
    beyt_second = models.CharField(max_length=255, verbose_name='مصراع دوم بیت روز')
    poet_name = models.CharField(max_length=100, verbose_name='شاعر بیت روز')
    poetic_commentary = models.TextField(blank=True, verbose_name='توضیح و نکته ادبی')
    proverb = models.CharField(max_length=200, verbose_name='ضرب‌المثل روز')
    proverb_meaning = models.TextField(verbose_name='معنا و کاربرد ضرب‌المثل')
    proverb_origin = models.TextField(blank=True, verbose_name='ریشه و حکایت کهن')

    class Meta:
        verbose_name = 'محتوای روزانه'
        verbose_name_plural = 'محتواهای روزانه'
        ordering = ['-date']

    def __str__(self):
        return f"محتوای روز {self.date} - {self.poet_name}"
