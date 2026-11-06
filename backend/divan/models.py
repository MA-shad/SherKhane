from django.db import models


#شاعر
class Poet(models.Model):
    name = models.CharField(max_length=150, verbose_name="نام شاعر")
    bio = models.TextField(blank=True, null=True, verbose_name="زندگی‌نامه")
    century = models.IntegerField(blank=True, null=True, verbose_name="قرن")

    class Meta:
        verbose_name = "شاعر"
        verbose_name_plural = "شاعران"

    def __str__(self):
        return self.name


#وزن عروضی
class Rhythm(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="وزن")
    bahr = models.CharField(max_length=100, blank=True, null=True, verbose_name="بحر عروضی")

    class Meta:
        verbose_name = "وزن"
        verbose_name_plural = "اوزان"

    def __str__(self):
        if self.bahr:
            return f"{self.name} | {self.bahr}"
        return self.name


#شعر
class Poem(models.Model):
    poet = models.ForeignKey(Poet, on_delete=models.CASCADE, related_name='poems', verbose_name="شاعر")
    title = models.CharField(max_length=255, verbose_name="عنوان شعر")

    class PoemType(models.TextChoices):
        GHAZAL = 'غزل', 'غزل'
        QASIDA = 'قصیده', 'قصیده'
        MASNAVI = 'مثنوی', 'مثنوی'
        ROBAEI = 'رباعی', 'رباعی'
        DOBEYTI = 'دوبیتی', 'دوبیتی'
        QATE = 'قطعه', 'قطعه'

    rhythm = models.ForeignKey(
        Rhythm,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='poems',
        verbose_name="وزن شعر"
    )

    poem_type = models.CharField(
        max_length=20,
        choices=PoemType.choices,
        default=PoemType.GHAZAL,
        verbose_name="قالب شعر"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        verbose_name = "شعر"
        verbose_name_plural = "اشعار"

    def __str__(self):
        return f"{self.title} - {self.poet.name}"


#بیت
class Verse(models.Model):
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='verses', verbose_name="شعر")
    order = models.PositiveIntegerField(blank=True, null=True, verbose_name="شماره بیت")
    first_couplet = models.CharField(max_length=255, verbose_name="مصرع اول")
    second_couplet = models.CharField(max_length=255, verbose_name="مصرع دوم")

    class Meta:
        ordering = ['order']
        verbose_name = "بیت"
        verbose_name_plural = "ابیات"

    def __str__(self):
        return f"بیت {self.order} از {self.poem.title}"
