from django.db import models

from django.core.validators import MinValueValidator,MaxValueValidator
from django.utils import timezone
from django.db.models import Sum

from django.conf import settings

import uuid


#DurationFieldの表示用処理
def duration_format(total,input_format=False):

    hours   = str( total // 3600 )
    minutes = str( (total % 3600) // 60)
    seconds = str( (total % 60) )

    if input_format:
        return '{}:{}:{}'.format(hours.zfill(2), minutes.zfill(2), seconds.zfill(2))
    else:
        return '{}時間{}分{}秒'.format(hours, minutes, seconds)



class FitnessCategory(models.Model):
    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt      = models.DateTimeField(verbose_name="登録日時",default=timezone.now)
    name    = models.CharField(verbose_name="フィットネスカテゴリ名",max_length=20)
    kcal    = models.IntegerField(verbose_name="1分あたりの消費カロリー",validators=[MinValueValidator(0)])

    """
    #合計のtimedelta型
    def time_total(self):
        memories    = FitnessMemory.objects.filter(category=self.id).aggregate(Sum("time"))
        return memories["time__sum"]

    #合計の時間
    def time_total_format(self):
        td   = self.time_total()

        if td:
            return duration_format(int(td.total_seconds()))
        else:
            return duration_format(0)
    """

    user        = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="投稿者",on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class FitnessMemory(models.Model):

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt          = models.DateTimeField(verbose_name='登録日時', default=timezone.now)

    exe_dt      = models.DateTimeField(verbose_name='実施日時')

    category    = models.ForeignKey(FitnessCategory, verbose_name='カテゴリー', on_delete=models.SET_NULL, null=True)
    time        = models.DurationField(verbose_name="運動時間")
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="投稿者",on_delete=models.CASCADE)



    def time_format(self):
        return duration_format( int(self.time.total_seconds()) )

    def __str__(self):
        return str(self.id)


#間食、朝食などで仕分けることで後に検索に利用する←グラフ化
class FoodCategory(models.Model):
    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt      = models.DateTimeField(verbose_name='登録日時', default=timezone.now)

    name    = models.CharField(verbose_name="食事の種類",max_length=15)


class FoodMemory(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt          = models.DateTimeField(verbose_name='登録日時', default=timezone.now)
    img         = models.ImageField(verbose_name='食事画像', upload_to='fitness/food/')
    kcal        = models.IntegerField(verbose_name='摂取したカロリー', validators=[MinValueValidator(0)])

    exe_dt      = models.DateTimeField(verbose_name='実施日時')

    category    = models.ForeignKey(FoodCategory,verbose_name="カテゴリ",on_delete=models.CASCADE,null=True,blank=True)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="投稿者",on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class Menu(models.Model):
    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt      = models.DateTimeField(verbose_name='登録日時', default=timezone.now)
    name    = models.CharField(verbose_name='名前', max_length=20)
    user    = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="投稿者",on_delete=models.CASCADE)


    def details(self):
        return MenuDetail.objects.filter(menu=self.id).order_by("sort")

    def __str__(self):
        return self.name

class MenuDetail(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt          = models.DateTimeField(verbose_name='登録日時', default=timezone.now)

    menu        = models.ForeignKey(Menu, verbose_name='メニュー', on_delete=models.SET_NULL, null=True)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="投稿者",on_delete=models.CASCADE)

    time        = models.DurationField(verbose_name="運動時間")
    category    = models.ForeignKey(FitnessCategory, verbose_name='カテゴリー', on_delete=models.SET_NULL, null=True)

    sort        = models.IntegerField(verbose_name="順番")

    def time_format(self):
        return duration_format( int(self.time.total_seconds()) )

    #DurationFieldのtimeを00:00:00のフォーマットで返却するメソッド
    def time_input_format(self):
        return duration_format( int(self.time.total_seconds()), input_format=True )

    def __str__(self):
        return str(self.id)

class Trophy(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt          = models.DateTimeField(verbose_name='登録日時', default=timezone.now)
    name        = models.CharField(verbose_name='名前', max_length=20)
    img         = models.ImageField(verbose_name='トロフィー画像', upload_to='fitness/trophy/')

    #TODO:ユーザーモデルの多対多のフィールド
    user        = models.ManyToManyField(settings.AUTH_USER_MODEL,through='TrophyUser')

    def __str__(self):
        return self.name

#TODO:トロフィーモデルとユーザーモデルの中間テーブルに値するモデルを作る(明示的に作る)
class TrophyUser(models.Model):

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trophy      = models.ForeignKey(Trophy,on_delete=models.CASCADE)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="登録者",on_delete=models.CASCADE)
    dt          = models.DateTimeField(verbose_name='登録日時', default=timezone.now)

