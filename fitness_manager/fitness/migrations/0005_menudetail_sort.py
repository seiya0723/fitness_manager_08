# Generated by Django 3.2.15 on 2022-09-07 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0004_menudetail_dt'),
    ]

    operations = [
        migrations.AddField(
            model_name='menudetail',
            name='sort',
            field=models.IntegerField(default=1, verbose_name='順番'),
            preserve_default=False,
        ),
    ]