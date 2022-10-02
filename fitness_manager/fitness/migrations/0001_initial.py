# Generated by Django 3.2.10 on 2022-08-17 08:37

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
                ('name', models.CharField(max_length=20, verbose_name='フィットネスカテゴリ名')),
                ('kcal', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='1分あたりの消費カロリー')),
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
                ('name', models.CharField(max_length=20, verbose_name='名前')),
                ('img', models.ImageField(upload_to='fitness/trophy/', verbose_name='トロフィー画像')),
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
                ('time', models.DurationField(verbose_name='運動時間')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fitness.fitnesscategory', verbose_name='カテゴリー')),
                ('menu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fitness.menu', verbose_name='メニュー')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='投稿者')),
            ],
        ),
        migrations.CreateModel(
            name='FoodMemory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日時')),
                ('img', models.ImageField(upload_to='fitness/food/', verbose_name='食事画像')),
                ('kcal', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='摂取したカロリー')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='投稿者')),
            ],
        ),
        migrations.CreateModel(
            name='FitnessMemory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日時')),
                ('time', models.DurationField(verbose_name='運動時間')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fitness.fitnesscategory', verbose_name='カテゴリー')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='投稿者')),
            ],
        ),
    ]
