# Generated by Django 3.2.10 on 2022-08-29 05:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0003_auto_20220824_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='menudetail',
            name='dt',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日時'),
        ),
    ]