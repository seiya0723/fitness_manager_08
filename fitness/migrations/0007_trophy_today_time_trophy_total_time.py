# Generated by Django 4.1.2 on 2022-10-12 09:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0006_trophy_serial_alter_trophy_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='trophy',
            name='today_time',
            field=models.DurationField(default=datetime.timedelta(0), verbose_name='一日の運動時間'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trophy',
            name='total_time',
            field=models.DurationField(default=datetime.timedelta(0), verbose_name='総合運動時間'),
            preserve_default=False,
        ),
    ]
