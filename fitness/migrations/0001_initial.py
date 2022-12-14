# Generated by Django 4.1.2 on 2022-11-17 23:45

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FitnessCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日時')),
                ('name', models.CharField(max_length=6, verbose_name='フィットネスカテゴリ名')),
                ('kcal', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='1分あたりの消費カロリー')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='投稿者')),
            ],
        ),
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日時')),
                ('name', models.CharField(max_length=8, verbose_name='食事の種類')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='投稿者')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日時')),
                ('name', models.CharField(max_length=20, verbose_name='名前')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='投稿者')),
            ],
        ),
        migrations.CreateModel(
            name='Trophy',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日時')),
                ('name', models.CharField(max_length=8, verbose_name='トロフィーの名前')),
                ('img', models.ImageField(upload_to='fitness/trophy/', verbose_name='トロフィー画像')),
                ('total_time', models.DurationField(verbose_name='総合運動時間')),
                ('today_time', models.DurationField(verbose_name='一日の運動時間')),
                ('serial', models.IntegerField(default=0, verbose_name='連続フィットネス日数')),
            ],
        ),
        migrations.CreateModel(
            name='TrophyUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日時')),
                ('trophy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.trophy')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='登録者')),
            ],
        ),
        migrations.AddField(
            model_name='trophy',
            name='user',
            field=models.ManyToManyField(through='fitness.TrophyUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='MenuDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日時')),
                ('time', models.DurationField(verbose_name='運動時間')),
                ('sort', models.IntegerField(verbose_name='順番')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fitness.fitnesscategory', verbose_name='カテゴリー')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.menu', verbose_name='メニュー')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='投稿者')),
            ],
        ),
        migrations.CreateModel(
            name='FoodMemory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日時')),
                ('img', models.ImageField(blank=True, null=True, upload_to='fitness/food/', verbose_name='食事画像')),
                ('kcal', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10000)], verbose_name='摂取したカロリー')),
                ('exe_dt', models.DateTimeField(verbose_name='実施日時')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fitness.foodcategory', verbose_name='カテゴリ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='投稿者')),
            ],
        ),
        migrations.CreateModel(
            name='FitnessMemory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日時')),
                ('exe_dt', models.DateTimeField(verbose_name='実施日時')),
                ('time', models.DurationField(validators=[django.core.validators.MinValueValidator(datetime.timedelta(seconds=1))], verbose_name='運動時間')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fitness.fitnesscategory', verbose_name='カテゴリー')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='投稿者')),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日時')),
                ('date', models.DateField(verbose_name='目標年月')),
                ('title', models.CharField(max_length=15, verbose_name='目標')),
                ('done', models.BooleanField(default=False, verbose_name='達成済み')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='登録者')),
            ],
            options={
                'unique_together': {('date', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Health',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日時')),
                ('date', models.DateField(verbose_name='記録日')),
                ('weight', models.DecimalField(decimal_places=1, max_digits=4, verbose_name='体重(kg)')),
                ('height', models.DecimalField(decimal_places=1, max_digits=4, verbose_name='身長(cm)')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='登録者')),
            ],
            options={
                'unique_together': {('date', 'user')},
            },
        ),
    ]
