# Generated by Django 4.1.2 on 2022-10-12 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0005_menudetail_sort'),
    ]

    operations = [
        migrations.AddField(
            model_name='trophy',
            name='serial',
            field=models.IntegerField(default=0, verbose_name='連続フィットネス日数'),
        ),
        migrations.AlterField(
            model_name='trophy',
            name='name',
            field=models.CharField(max_length=20, verbose_name='トロフィーの名前'),
        ),
    ]