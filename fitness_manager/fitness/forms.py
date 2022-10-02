from django import forms

from django.core.validators import MinValueValidator, MaxValueValidator

from .models import FitnessCategory,FitnessMemory,Menu,MenuDetail


# 年月検索用バリデーションフォーム
class YearMonthForm(forms.Form):
    year    = forms.IntegerField()
    month   = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])


class FitnessCategoryForm(forms.ModelForm):
    class Meta:
        model   = FitnessCategory
        fields  = ["name","kcal","user",]

class FitnessMemoryForm(forms.ModelForm):

    class Meta:
        model   = FitnessMemory
        fields  = ["category","time","user","exe_dt"]


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

