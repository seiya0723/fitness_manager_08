from django.contrib import admin

from .models import FitnessCategory,FitnessMemory,FoodMemory,Menu,MenuDetail,Trophy,TrophyUser


class FitnessCategoryAdmin(admin.ModelAdmin):
    list_display    = ["id","dt","name","kcal","user",]

class FitnessMemoryAdmin(admin.ModelAdmin):
    list_display    = ["id","dt","category","time","user",]

class FoodMemoryAdmin(admin.ModelAdmin):
    list_display    = ["id","dt","img","kcal","user",]

class MenuAdmin(admin.ModelAdmin):
    list_display    = ["id","dt","name","user",]

class MenuDetailAdmin(admin.ModelAdmin):
    list_display    = ["id","category","menu","time","user","sort"]

class TrophyAdmin(admin.ModelAdmin):
    list_display    = ["id","dt","name","img",]

class TrophyUserAdmin(admin.ModelAdmin):
    list_display    = ["id","trophy","user","dt",]



admin.site.register(FitnessCategory,FitnessCategoryAdmin)
admin.site.register(FitnessMemory,  FitnessMemoryAdmin  )
admin.site.register(FoodMemory,     FoodMemoryAdmin     )
admin.site.register(Menu,           MenuAdmin           )
admin.site.register(MenuDetail,     MenuDetailAdmin     )
admin.site.register(Trophy,         TrophyAdmin         )
admin.site.register(TrophyUser,     TrophyUserAdmin     )
