# Generated by Django 3.2.6 on 2021-08-11 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_auto_20210811_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Фото профиля'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_manager',
            field=models.BooleanField(default=False, verbose_name='Статус менеджера'),
        ),
    ]