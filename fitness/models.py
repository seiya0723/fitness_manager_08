from django.db import models

from django.core.validators import MinValueValidator,MaxValueValidator
from django.utils import timezone
from django.db.models import Sum

from django.conf import settings

import uuid
import datetime


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

    #TODO:これも文字数制限を加える現状では6文字、CSSを修正して8文字に仕立てる←一旦6文字で
    name    = models.CharField(verbose_name="フィットネスカテゴリ名",max_length=6)
    kcal    = models.IntegerField(verbose_name="1分あたりの消費カロリー",validators=[MinValueValidator(0)])

    user    = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="投稿者",on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class FitnessMemory(models.Model):

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt          = models.DateTimeField(verbose_name='登録日時', default=timezone.now)
    exe_dt      = models.DateTimeField(verbose_name='実施日時')

    #TODO:ここでnullを消す
    category    = models.ForeignKey(FitnessCategory, verbose_name='カテゴリー', on_delete=models.PROTECT)

    #フィットネス時間0秒での投稿は許さない
    time        = models.DurationField(verbose_name="運動時間",validators=[MinValueValidator(datetime.timedelta(seconds=1))])
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="投稿者",on_delete=models.CASCADE)


    def time_format(self):
        return duration_format( int(self.time.total_seconds()) )

    def __str__(self):
        return str(self.id)


#間食、朝食などで仕分けることで後に検索に利用する←グラフ化
class FoodCategory(models.Model):
    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt      = models.DateTimeField(verbose_name='登録日時', default=timezone.now)

    #TODO:これも文字数制限を加える？10rem以内なので太字ありの場合8文字に収める必要がある。
    name    = models.CharField(verbose_name="食事の種類",max_length=8)

    #TODO:開発最終段階でDBとマイグレーションファイルを消す時、このnull=Trueとblank=Trueを消す
    user    = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="投稿者",on_delete=models.CASCADE)


class FoodMemory(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt          = models.DateTimeField(verbose_name='登録日時', default=timezone.now)


    img         = models.ImageField(verbose_name='食事画像', upload_to='fitness/food/',null=True,blank=True)

    #TODO:MaxValueValidatorをセットする( 成人男性の1日のカロリーは多くとも3000kcalなので、体重増加が目的だったとしても、1食10000kcalを上限で良いのでは？←力士は一日で8000kcal摂取する)
    kcal        = models.IntegerField(verbose_name='摂取したカロリー', validators=[MinValueValidator(0),MaxValueValidator(10000)])

    #TODO:ここに文字数制限を加える？このフィールド撤廃する？何を記入するのか？←撤廃されました
    #description = models.CharField(verbose_name="自由記入欄",max_length=500,null=True,blank=True)

    exe_dt      = models.DateTimeField(verbose_name='実施日時')

    #TODO:カテゴリの指定は必須に
    category    = models.ForeignKey(FoodCategory,verbose_name="カテゴリ",on_delete=models.PROTECT)
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

    #TODO:ここでSET_NULLにしてしまうと、Menuを消した時、DBにMenuDetailが残存してしまう。CASCADEを使って対処
    menu        = models.ForeignKey(Menu, verbose_name='メニュー', on_delete=models.CASCADE)


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

    #TODO:トロフィーの名前も8文字に合わせるべきでは？しかし、8文字だとなんのトロフィーかわからないので、widthとfont-sizeを調整することで12文字ぐらいに仕立てる？←とりあえず8文字にして後で拡張しようと思う
    name        = models.CharField(verbose_name='トロフィーの名前', max_length=8)
    img         = models.ImageField(verbose_name='トロフィー画像', upload_to='fitness/trophy/')

    #ユーザーモデルの多対多のフィールド
    user        = models.ManyToManyField(settings.AUTH_USER_MODEL,through='TrophyUser')

    #このトロフィーを取得する条件のフィールドをここに追加する
    total_time = models.DurationField(verbose_name="総合運動時間")
    today_time = models.DurationField(verbose_name="一日の運動時間")
    serial     = models.IntegerField(verbose_name="連続フィットネス日数", default=0)

    """
    トロフィー取得の流れ

    FitnessMemoryのsaveメソッドをオーバーライド、
    ↑書いた条件を元にトロフィーの取得を判定(filterメソッドで条件を満たしたトロフィーのモデルを取り出し、一括で取得処理をする)
    
    トロフィーの追加処理
    https://noauto-nolife.com/post/django-m2m-search-and-add/
    """

    def __str__(self):
        return self.name

#トロフィーモデルとユーザーモデルの中間テーブルに値するモデルを作る(明示的に作る)
class TrophyUser(models.Model):

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trophy      = models.ForeignKey(Trophy,on_delete=models.CASCADE)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="登録者",on_delete=models.CASCADE)
    dt          = models.DateTimeField(verbose_name='登録日時', default=timezone.now)


#TODO:体重と身長を記録するモデルを作る。
class Health(models.Model):

    class Meta:
        unique_together = ("date","user")

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt          = models.DateTimeField(verbose_name='登録日時', default=timezone.now)

    #TODO:ここはunique_togetherで同じ日に登録できないようにするべきでは？
    date        = models.DateField(verbose_name='記録日')
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="登録者",on_delete=models.CASCADE)

    #TODO:DecimalFieldを使って小数第一位まで記録する
    #この2つは入力が面倒にならないよう、最新の値を最初からinputタグのvalueに入れておく
    """
    weight      = models.IntegerField(verbose_name="体重(kg)")
    height      = models.IntegerField(verbose_name="身長(cm)")
    """
    # 123.4 -123.4
    weight      = models.DecimalField(verbose_name="体重(kg)",max_digits=4,decimal_places=1)
    height      = models.DecimalField(verbose_name="身長(cm)",max_digits=4,decimal_places=1)

    #weight      = models.DecimalField(verbose_name="体重(kg)",max_digits=4,decimal_places=1,validators=[MinValueValidator(0))
    #height      = models.DecimalField(verbose_name="身長(cm)",max_digits=4,decimal_places=1,validators=[MinValueValidator(0))


#今月の目標を記録するモデルを作る
class Target(models.Model):

    #TODO:ここはunique_togetherで？同じ月に複数登録できないようにするべきでは？←別途バリデーションを用意するという方法もあるかと？
    class Meta:
        #uniqueはDB上に2つ存在してはいけないという制約であって、既存のレコードの編集はOK
        unique_together = ("date","user")

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt          = models.DateTimeField(verbose_name='登録日時', default=timezone.now)

    # dtだと来月の目標を立てて記録したい場合、今月のデータになってしまう。 
    #とりあえずdtではなく年月日で記録するべきでは？日は1日で固定 2022-11-01 でOK
    #hiddenにselected_dateを入れれば入力の手間は省けると思われる。
    date        = models.DateField(verbose_name="目標年月")

    user        = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="登録者",on_delete=models.CASCADE)

    #目標は15文字に絞る
    title       = models.CharField(verbose_name="目標",max_length=15)

    #目標達成できたら達成済みをチェックする(ここはあくまでも自己評価で)
    done        = models.BooleanField(verbose_name="達成済み",default=False)

