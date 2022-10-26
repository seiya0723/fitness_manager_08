from django import forms

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Sum
from django.utils import timezone

from .models import FitnessCategory,FitnessMemory,Menu,MenuDetail,Trophy,FoodCategory,FoodMemory


import datetime



# 年月検索用バリデーションフォーム
class YearMonthForm(forms.Form):
    year    = forms.IntegerField()
    month   = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])



class FoodCategoryForm(forms.ModelForm):

    class Meta:
        model   = FoodCategory
        fields  = ["name","user"]

class FoodMemoryForm(forms.ModelForm):

    class Meta:
        model   = FoodMemory
        fields  = ["img","kcal","description","exe_dt","category","user",]




class FitnessCategoryForm(forms.ModelForm):
    class Meta:
        model   = FitnessCategory
        fields  = ["name","kcal","user",]

class FitnessMemoryForm(forms.ModelForm):

    class Meta:
        model   = FitnessMemory
        fields  = ["category","time","user","exe_dt"]


    #https://noauto-nolife.com/post/django-models-save-delete-override/
    def save(self, *args, **kwargs):
        fitness_memory = super().save(*args, **kwargs)

        #現時点でのフィットネス記録をチェック、トロフィーの取得条件を見たしているかfilterでチェックして一括保存


        print(fitness_memory.user.id)

        #総合運動時間
        total_time      = FitnessMemory.objects.filter(user=fitness_memory.user.id).aggregate(Sum('time'))

        #今日の運動時間
        now = timezone.now()

        today_time      = FitnessMemory.objects.filter(user=fitness_memory.user.id, exe_dt__year=now.year, exe_dt__month=now.month, exe_dt__day=now.day ).aggregate(Sum('time'))

        #TODO:連続運動日数
        #一日ごとにマイナスしていくループを作る、fitness_memoryがなくなった時、連続のカウントをやめる


        serial      = 0

        while True:
            #指定日付のデータが存在するかチェック
            serial_flag = FitnessMemory.objects.filter(user=fitness_memory.user.id, exe_dt__year=now.year, exe_dt__month=now.month, exe_dt__day=now.day ).exists()

            if not serial_flag:
                break 

            #1日前に戻る
            now -= datetime.timedelta(days=1)

            #連続日数を1増やす
            serial += 1


        #自分が取得していないトロフィーであり、なおかつ条件を見たしているトロフィーを絞り込む
        trophies = Trophy.objects.filter(total_time__lte=total_time["time__sum"],today_time__lte=today_time["time__sum"], serial__lte=serial ).exclude(user=fitness_memory.user.id)

        #トロフィーをループして取得処理を
        for trophy in trophies:
            trophy.user.add(fitness_memory.user)
            print("追加")



class MenuForm(forms.ModelForm):
    class Meta:
        model   = Menu
        fields  = ["name","user"]

class MenuDetailForm(forms.ModelForm):
    class Meta:
        model   = MenuDetail
        fields  = ["category","menu","time","user","sort"]


class UUIDForm(forms.Form):
    id  = forms.UUIDField()

