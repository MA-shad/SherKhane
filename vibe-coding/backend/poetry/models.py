from django.db import models
from core.normalizer import normalize_persian_text


class Poet(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="نام شاعر")
    slug = models.SlugField(max_length=150, unique=True, allow_unicode=True, verbose_name="شناسه یکتا")
    bio = models.TextField(blank=True, verbose_name="شرح احوال و سبک")
    century = models.IntegerField(blank=True, null=True, verbose_name="سده زندگی (قمری)")
    birth_place = models.CharField(max_length=100, blank=True, verbose_name="زادگاه")
    avatar = models.CharField(max_length=255, blank=True, default='poet-default.jpg', verbose_name="نگاره شاعر")

    class Meta:
        verbose_name = "شاعر"
        verbose_name_plural = "شاعران"
        ordering = ['century', 'name']

    def __str__(self):
        return self.name


class Rhythm(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name="وزن عروضی (افاعیل)")
    bahr = models.CharField(max_length=100, blank=True, verbose_name="بحر عروضی")
    pattern = models.CharField(max_length=100, blank=True, verbose_name="الگوی هجایی")

    class Meta:
        verbose_name = "وزن عروضی"
        verbose_name_plural = "اوزان عروضی"

    def __str__(self):
        return f"{self.name} ({self.bahr})" if self.bahr else self.name


class Work(models.Model):
    poet = models.ForeignKey(Poet, on_delete=models.CASCADE, related_name='works', verbose_name="شاعر")
    title = models.CharField(max_length=200, verbose_name="عنوان اثر / کتاب")
    slug = models.SlugField(max_length=200, allow_unicode=True, verbose_name="شناسه اثر")
    work_type = models.CharField(max_length=50, default='دیوان', verbose_name="نوع اثر")
    description = models.TextField(blank=True, verbose_name="توضیحات و ابواب")

    class Meta:
        verbose_name = "اثر / کتاب"
        verbose_name_plural = "آثار و کتب"
        unique_together = ('poet', 'slug')

    def __str__(self):
        return f"{self.title} - {self.poet.name}"


class Poem(models.Model):
    class PoemType(models.TextChoices):
        GHAZAL = 'غزل', 'غزل'
        QASIDA = 'قصیده', 'قصیده'
        MASNAVI = 'مثنوی', 'مثنوی'
        ROBAEI = 'رباعی', 'رباعی'
        DOBEYTI = 'دوبیتی', 'دوبیتی'
        QATE = 'قطعه', 'قطعه'

    poet = models.ForeignKey(Poet, on_delete=models.CASCADE, related_name='poems', verbose_name="شاعر")
    work = models.ForeignKey(Work, on_delete=models.SET_NULL, null=True, blank=True, related_name='poems', verbose_name="اثر")
    rhythm = models.ForeignKey(Rhythm, on_delete=models.SET_NULL, null=True, blank=True, related_name='poems', verbose_name="وزن شعر")
    title = models.CharField(max_length=255, verbose_name="مطلع یا عنوان شعر")
    slug = models.SlugField(max_length=255, allow_unicode=True, blank=True, verbose_name="شناسه")
    poem_type = models.CharField(max_length=25, choices=PoemType.choices, default=PoemType.GHAZAL, verbose_name="قالب شعری")
    order_in_work = models.PositiveIntegerField(default=1, verbose_name="شماره در دیوان")
    edition_source = models.CharField(max_length=150, blank=True, default='نسخه مرجع تصحیح‌شده', verbose_name="نسخه / تصحیح مبنا")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        verbose_name = "شعر"
        verbose_name_plural = "اشعار"
        ordering = ['poet', 'order_in_work']

    def __str__(self):
        return f"{self.title} ({self.poet.name})"


class Verse(models.Model):
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='verses', verbose_name="شعر")
    order = models.PositiveIntegerField(default=1, verbose_name="شماره بیت")
    first_couplet = models.CharField(max_length=300, verbose_name="مصراع نخست")
    second_couplet = models.CharField(max_length=300, verbose_name="مصراع دوم")
    normalized_text = models.TextField(blank=True, verbose_name="متن پالایش‌شده جهت جست‌وجو")

    class Meta:
        verbose_name = "بیت"
        verbose_name_plural = "ابیات"
        ordering = ['order']
        unique_together = ('poem', 'order')

    def save(self, *args, **kwargs):
        # Automatically update search text
        full_text = f"{self.first_couplet} {self.second_couplet}"
        self.normalized_text = normalize_persian_text(full_text)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"بیت {self.order} از {self.poem.title}"
