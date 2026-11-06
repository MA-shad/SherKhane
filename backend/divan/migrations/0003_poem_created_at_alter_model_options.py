# Generated manually — verify with: python manage.py makemigrations --check

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('divan', '0002_alter_verse_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='poem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='تاریخ ثبت'),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='poet',
            options={'verbose_name': 'شاعر', 'verbose_name_plural': 'شاعران'},
        ),
        migrations.AlterModelOptions(
            name='rhythm',
            options={'verbose_name': 'وزن', 'verbose_name_plural': 'اوزان'},
        ),
        migrations.AlterModelOptions(
            name='poem',
            options={'verbose_name': 'شعر', 'verbose_name_plural': 'اشعار'},
        ),
        migrations.AlterModelOptions(
            name='verse',
            options={'ordering': ['order'], 'verbose_name': 'بیت', 'verbose_name_plural': 'ابیات'},
        ),
    ]
